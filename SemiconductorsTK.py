import matplotlib.pyplot as plt
import numpy as np
from typing import List, Optional, Mapping, Union, Dict
import os
from regex import A
from sklearn import mixture

from Interpolate import Interpolate as I
from Perovskite import Perovskite as P
from CsSnCl3 import CsSnCl3
from CsSnI3 import CsSnI3
from CsPbI3 import CsPbI3
from CsSiI3 import CsSiI3

from Energetic_profile import Energetic_profile

from Zadanie2 import Zadanie2
from Perovskite_With_Temperature import Perovskite_With_Temperature as Perovskite
from Hamiltonian import Hamiltonian as Ha
from G_R_M import G_R_M
from Zadanie5 import grapgh_for_gif

def update_for_k(E_VB, E_CS, E_CH, E_CL, k, P, gammav, gamma1, gamma2, gamma3):
    H_REDUCED = 6.582119569
    m0 = 1

    P_plus = P * (k[0] + 1j*k[1])
    P_minus = P * (k[0] - 1j*k[1])
    P_z = P * k[2]

    VB = E_VB - H_REDUCED**2 / (2 * m0) * gammav * (k[0]**2 + k[1]**2 + k[2]**2)
    CS = E_CS + H_REDUCED**2 / (2 * m0) * (gamma1*(k[0]**2 + k[1]**2 + k[2]**2))
    CH = E_CH + H_REDUCED**2 / (2 * m0) *((gamma1+gamma2) * (k[0]**2 + k[1]**2) + (gamma1 - 2*gamma2)*k[2]**2)
    CL = E_CL + H_REDUCED**2 / (2 * m0) *((gamma1-gamma2) * (k[0]**2 + k[1]**2) + (gamma1 + 2*gamma2)*k[2]**2)

    S = H_REDUCED**2 / (2*m0) * 2 * np.sqrt(3) * gamma3 * (-k[0]+1j*k[1]) * k[2]
    R = H_REDUCED**2 / (2*m0) * np.sqrt(3) * (gamma2 * (k[0]**2 - k[1]**2) - 2j*gamma3*k[0]*k[1])
    D = H_REDUCED**2 / (2*m0) * np.sqrt(2) * gamma2 * (k[0]**2 + k[1]**2 - 2*k[2]**2)
    return VB, CS, CH, CL, P_plus, P_minus, P_z, S, R, D

def main():
    
    H_REDUCED = 6.582119569
    m0 = 1
    compound_1 = CsSnCl3.CsSnCl3
    compound_2 = CsSnI3.CsSnI3

    #compound_1 = CsPbI3.CsPbI3
    #compound_2 = CsSiI3.CsSiI3
    MIX_PROPORTION = np.arange(start=0, stop=1, step=0.01) 
    TEMPERATURES = np.arange(start=0, stop=500, step=15)
    BOWING = np.arange(start=-0.01, stop=0.01, step=0.0005)
    TENSION = np.arange(start=-6,stop=6, step=0.2)

    perovskite = Perovskite(compound_1, compound_2, temperature=300)
    #print(per.perovskite)
    
    en_prof = Energetic_profile(perovskite)
    Table = en_prof.return_bands(0)
    print(Table)
    gamma1 = perovskite.perovskite["gamma_1"] - 1/3 * perovskite.perovskite["Ep"]/perovskite.Eg_with_temperature
    gamma2 = perovskite.perovskite["gamma_2"] - 1/6 * perovskite.perovskite["Ep"]/perovskite.Eg_with_temperature
    gamma3 = perovskite.perovskite["gamma_3"] - 1/6 * perovskite.perovskite["Ep"]/perovskite.Eg_with_temperature
    gammav = m0 / perovskite.perovskite["mh"] - perovskite.perovskite["Ep"]/3 * (2 / perovskite.Eg_with_temperature + 1 / (perovskite.Eg_with_temperature + perovskite.perovskite["delta"]))
    print(gamma1, gamma2, gamma3, gammav)

    P = np.sqrt(perovskite.perovskite["Ep"] * H_REDUCED**2 / (2*m0))
    #k = [1,1,1]
    #k = np.multiply(k, -np.pi/6.065)
    #k = np.multiply(k, 15/100)
    k = [-0.041116057004616686, -0.041116057004616686, -0.041116057004616686]

    VB, CS, CH, CL, P_plus, P_minus, P_z, S, R, D = update_for_k(E_VB=Table[0],E_CS=Table[1],E_CH=Table[2],E_CL=Table[3],k=k, P=P, gammav=gammav, gamma1=gamma1, gamma2=gamma2, gamma3=gamma3)
    print(VB, CS, CH, CL, P_plus, P_minus, P_z, S, R, D)

    #print(vars(perovskite))
   
    
    dra = G_R_M(compound_1=compound_1, compound_2=compound_2)
    dra.draw(
                compound_1=compound_1,
                compound_2=compound_2,
                mix_proportion=0.5,
                temperature=300,
                bowing=0,
                tension=0,
                resolution=0.01,
                percent_range=15,
                name="example"
            )
    H = Ha()
    k = [-0.041116057004616686, -0.041116057004616686, -0.041116057004616686]
    print(H.eigenvalues(perovskite=perovskite, k=k, tension=0 ))



    mix = False
    bow = False
    tem = False
    ten = False

    gif = grapgh_for_gif()

    if mix:
        gif.gif_with_mix_proportion(
            compound_1=compound_1,
            compound_2=compound_2,
            MIX_proportion=MIX_PROPORTION,
            temperature=300,
            bowing=0,
            tension=0,
            resolution=0.1,
            percent_range=15,
        )

    if tem:
        gif.gif_with_temperature(
            compound_1=compound_1,
            compound_2=compound_2,
            mix_proportion=0.5,
            Temperature=TEMPERATURES,
            bowing=0,
            tension=0,
            resolution=0.1,
            percent_range=15,
        )
    
    if bow:
        gif.gif_with_bowing(
            compound_1=compound_1,
            compound_2=compound_2,
            mix_proportion=0.5,
            temperature=300,
            Bowing=BOWING,
            tension=0,
            resolution=0.1,
            percent_range=15,
        )
    
    if ten:
        gif.gif_with_tensin(
            compound_1=compound_1,
            compound_2=compound_2,
            mix_proportion=0.5,
            temperature=300,
            bowing=0,
            Tension=TENSION,
            resolution=0.1,
            percent_range=15,
        )


    


if __name__ == "__main__":
    main()