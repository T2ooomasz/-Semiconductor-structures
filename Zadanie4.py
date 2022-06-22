from typing import List, Optional, Mapping, Union, Dict
import matplotlib.pyplot as plt

from Perovskite_With_Temperature import Perovskite_With_Temperature as Perovskite
from Syntetic_material import A 
from CsSnCl3 import CsSnCl3
from CsSnI3 import CsSnI3

'''
Energetic profile of material A/B/A, where:
B - perovskite
A - syntetic material (with syntetic necesary values)
'''

'''
Take: self
return: graphs of energetic value for set values and tensions
'''
def draw_graph(perovskite, tensions, b, CS_0, CH_0, CL_0, CS_A, VBO_perovskite):
    print(perovskite.perovskite["a"], type(perovskite.perovskite["a"]))
    for tension in tensions:
        # tenison
        name = str(tension)
        tension = tension/100
        a_A = (1 + tension) * perovskite.perovskite["a"]
        eps_xx = (a_A - perovskite.perovskite["a"]) / perovskite.perovskite["a"]
        # prędkości zmian
        dEC_H = 2 * perovskite.perovskite["a^c"] * (1 - perovskite.perovskite["C_12"] / perovskite.perovskite["C_11"]) * eps_xx
        dEV_H = 2 * perovskite.perovskite["a^v"] * (1 - perovskite.perovskite["C_12"] / perovskite.perovskite["C_11"]) * eps_xx
        dE_S = b * (1 + 2 * perovskite.perovskite["C_12"] / perovskite.perovskite["C_11"]) * eps_xx
        # pasma:
        E_VB_0 = 0
        E_VB = E_VB_0 + dEV_H
        E_CS = CS_0 + dEC_H
        E_CH = CH_0 + dEC_H + dE_S
        E_CL = CL_0 + dEC_H - dE_S
        VBO_A = A.A["VBO"]

        save(VBO_A, CS_A, VBO_perovskite, E_CS, E_CH, E_CL, perovskite.perovskite["a"], name)

'''
Take: values to plot graph
return: graph
'''
def save(E_VB_A, E_CS_A, VBO_B, E_CS, E_CH, E_CL, a_B, name):
    fig, ax = plt.subplots()
    ax.hlines(y=E_VB_A, xmin=0, xmax=50, linewidth=2, color='r', label = "E_VB_A")
    ax.hlines(y=E_VB_A, xmin=100, xmax=150, linewidth=2, color='r')

    ax.hlines(y=E_CS_A, xmin=0, xmax=50, linewidth=2, color='b', label = "E_CS_A")
    ax.hlines(y=E_CS_A, xmin=100, xmax=150, linewidth=2, color='b')

    ax.hlines(y=VBO_B, xmin=50, xmax=100, linewidth=2, label = "VBO_B", color="darkred")
    ax.hlines(y=E_CS, xmin=50, xmax=100, linewidth=2, label = "E_CS",color="darkblue")
    ax.hlines(y=E_CH, xmin=50, xmax=100, linewidth=4, label = "E_CH", color="green", linestyle='dotted')
    ax.hlines(y=E_CL, xmin=50, xmax=100, linewidth=2, label = "E_CL", color="orange")

    ax.vlines(x=50, ymin=E_CS, ymax=E_CS_A, color='blue')
    ax.vlines(x=100, ymin=E_CS, ymax=E_CS_A, color='blue')
    ax.vlines(x=50, ymin=E_VB_A, ymax=VBO_B, color='red')
    ax.vlines(x=100, ymin=E_VB_A, ymax=VBO_B, color='red')

    plt.xlabel('z [nm]')
    plt.ylabel('E [eV]')
    plt.title('')
    plt.legend()
    plt.grid()
    #plt.show()
    plt.savefig(str(f"graphs4/{str(name)}.png"))

def main():

    compound_1 = CsSnCl3.CsSnCl3
    compound_2 = CsSnI3.CsSnI3

    perovskite = Perovskite(compound_1, compound_2, temperature=300, mix_proportion=0.5)

    b = -1.7 #like for GaAs
    tensions = [-3,0,3]
    # Pasma w punkcie R
    VBO_perovskite = 1 
    CS_0 =VBO_perovskite + perovskite.Eg_with_temperature
    CH_0 = VBO_perovskite + perovskite.Eg_with_temperature + perovskite.perovskite["delta"]
    CL_0 = CH_0 
    CS_A = VBO_perovskite + perovskite.Eg_with_temperature + 3
    
    draw_graph(perovskite, tensions, b, CS_0, CH_0, CL_0, CS_A, VBO_perovskite)

if __name__ == "__main__":
    main()