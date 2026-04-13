"""
Three-layer evapotranspiration and saturation-excess runoff model
Python implementation based on Xinanjiang model principles
Functions:
    R_cal(): Calculate runoff using tension water capacity curve
    run_model(): Main function (evapotranspiration + runoff generation + flow separation)
Reference: Xinanjiang model (Zhao Renjun et al.)
"""
import numpy as np


def R_cal(b, WM, W, PE):
    WMM = (1 + b) * WM
    a = WMM * (1 - (1 - W / WM) ** (1 / (1 + b)))
    if a + PE <= WMM:
        R = PE - WM * (1 - a / WMM) ** (1 + b) + WM * (1 - (a + PE) / WMM) ** (1 + b)
    else:
        R = PE + W - WM
    return R


def run_model(data, params):
    # Read parameters
    WUM = params["WUM"]
    WLM = params["WLM"]
    WDM = params["WDM"]
    C = params["C"]
    b = params["b"]
    Fc = params["Fc"]
    WM = WUM + WLM + WDM

    # Data cleaning
    data["P"] = data["P"].fillna(0)
    data["Ep"] = data["Ep"].fillna(0)

    # Data format conversion
    P = data['P'].values
    Ep = data['Ep'].values
    date = data['date'].values
    n = len(P)

    # Initialize variables
    WU = np.zeros(n + 1)
    WL = np.zeros(n + 1)
    WD = np.zeros(n + 1)
    W = np.zeros(n + 1)

    EU = np.zeros(n)
    EL = np.zeros(n)
    ED = np
    zeros(n)
    E = np.zeros(n)
    PE = np.zeros(n)

    R = np.zeros(n)
    RG = np.zeros(n)
    RS = np.zeros(n)

    # Initial values
    WU[0] = params["WU_0"]
    WL[0] = params["WL_0"]
    WD[0] = params["WD_0"]
    W[0] = WU[0] + WL[0] + WD[0]

    for i in range(len(date)):
        if P[i] - Ep[i] > 0:
            PE[i] = P[i] - Ep[i]
            E[i] = EU[i] = Ep[i]
            ED[i] = 0
            EL[i] = 0
            R[i] = R_cal(b, WM, W[i], PE[i])
            if PE[i] + W[i] - R[i] >= WM:
                WU[i + 1] = WUM
                WL[i + 1] = WLM
                WD[i + 1] = WDM
            elif PE[i] + WU[i] - R[i] <= WUM:
                WU[i + 1] = PE[i] - R[i] + WU[i]
                WL[i + 1] = WL[i]
                WD[i + 1] = WD[i]
            elif PE[i] - R[i] + WU[i] > WUM and PE[i] - R[i] - (WUM - WU[i]) + WL[i] <= WLM:
                WU[i + 1] = WUM
                WL[i + 1] = PE[i] - R[i] - (WUM - WU[i]) + WL[i]
                WD[i + 1] = WD[i]
            else:
                WU[i + 1] = WUM
                WL[i + 1] = WLM
                WD[i + 1] = PE[i] - R[i] - (WUM - WU[i]) - (WLM - WL[i]) + WL[i]
        else:
            R[i] = 0
            if WU[i] + P[i] >= Ep[i]:
                EU[i] = Ep[i]
                EL[i] = 0
                ED[i] = 0
                WU[i + 1] = WU[i] - EU[i] + P[i]
                WD[i + 1] = WD[i]
                WL[i + 1] = WL[i]
            elif WU[i] + P[i] < Ep[i] and WL[i] >= C * WLM:
                EU[i] = WU[i] + P[i]
                EL[i] = (Ep[i] - EU[i]) * WL[i] / WLM
                ED[i] = 0
                WU[i + 1] = 0
                WL[i + 1] = WL[i] - EL[i]
                WD[i + 1] = WD[i]
            elif WU[i] + P[i] < Ep[i] and C * (Ep[i] - P[i] - WU[i]) <= WL[i] < C * WLM:
                EU[i] = WU[i] + P[i]
                WU[i + 1] = 0
                EL[i] = (Ep[i] - EU[i]) * C
                WL[i + 1] = WL[i] - EL[i]
                ED[i] = 0
                WD[i + 1] = WD[i]
            else:
                EU[i] = WU[i] + P[i]
                WU[i + 1] = 0
                EL[i] = WL[i]
                WL[i + 1] = 0
                ED[i] = C * (Ep[i] - EU[i]) - EL[i]
                WD[i + 1] = WD[i] - ED[i]
            E[i] = EU[i] + ED[i] + EL[i]
            PE[i] = P[i] - E[i]
        W[i + 1] = WU[i + 1] + WL[i + 1] + WD[i + 1]

    WU = WU[:-1];
    WL = WL[:-1];
    WD = WD[:-1];
    W = W[:-1]

    # Two water sources division
    for i in range(len(date)):
        if PE[i] <= Fc:
            RG[i] = R[i]
            RS[i] = 0
        else:
            RG[i] = Fc * (R[i] / PE[i])  # R/PE is the runoff area ratio, also known as runoff coefficient
            RS[i] = R[i] - RG[i]

    # Organize data into a table
    results = {'date': date, 'P': P, 'Ep': Ep, 'EU': EU, 'EL': EL, 'ED': ED, 'E': E,
               "PE": PE, "WU": WU, "WL": WL, "WD": WD, "W": W, "R": R, "RG": RG, "RS": RS}

    return results