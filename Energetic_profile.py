from typing import List, Optional, Mapping, Union, Dict
import matplotlib.pyplot as plt

from Perovskite_With_Temperature import Perovskite_With_Temperature as Perovskite
from Syntetic_material import A 
'''
Energetic profile of material A/B/A, where:
B - perovskite
A - syntetic material (with syntetic necesary values)
'''
class Energetic_profile:
    def __init__(
        self,
        perovskite: Perovskite,
        b: Optional[float] = -1.7, #like for GaAs
        tensions: Optional[float] = [0],

    ):
        self.perovskite = perovskite
        self.b = b
        self.tensions = tensions
        # Pasma w punkcie (poki co R)
        self.VBO_perovskite = 0 # normalization before: 1
        self.CS_0 = self.VBO_perovskite + self.perovskite.Eg_with_temperature
        self.CH_0 = self.VBO_perovskite + self.perovskite.Eg_with_temperature + self.perovskite.perovskite["delta"]
        self.CL_0 = self.CH_0 
        self.CS_A = self.VBO_perovskite + self.perovskite.Eg_with_temperature + 3 # CS band for syntetic material

    '''
    Take: self
    return: graphs of energetic value for set values and tensions
    '''
    def return_bands(self, tension):
            # tenison
            tension = tension/100
            a_A = (1 + tension) * self.perovskite.perovskite["a"]
            eps_xx = (a_A - self.perovskite.perovskite["a"]) / self.perovskite.perovskite["a"]
            # prędkości zmian
            dEC_H = 2 * self.perovskite.perovskite["a^c"] * (1 - self.perovskite.perovskite["C_12"] / self.perovskite.perovskite["C_11"]) * eps_xx
            dEV_H = 2 * self.perovskite.perovskite["a^v"] * (1 - self.perovskite.perovskite["C_12"] / self.perovskite.perovskite["C_11"]) * eps_xx
            dE_S = self.b * (1 + 2 * self.perovskite.perovskite["C_12"] / self.perovskite.perovskite["C_11"]) * eps_xx
            # pasma:
            E_VB_0 = 0
            E_VB = E_VB_0 + dEV_H
            E_CS = self.CS_0 + dEC_H
            E_CH = self.CH_0 + dEC_H + dE_S
            E_CL = self.CL_0 + dEC_H - dE_S
            VBO_A = A.A["VBO"]
            #print(self.perovskite.perovskite["a"])

            return [E_VB, E_CS, E_CH, E_CL, self.perovskite.perovskite["a"], tension*100]


    '''
    Take: self
    return: graphs of energetic value for set values and tensions
    '''
    def draw_graph(self):
        for tension in self.tensions:
            # tenison
            name = str(tension)
            tension = tension/100
            a_A = (1 + tension) * self.perovskite.perovskite["a"]
            eps_xx = (a_A - self.perovskite.perovskite["a"]) / self.perovskite.perovskite["a"]
            # prędkości zmian
            dEC_H = 2 * self.perovskite.perovskite["a^c"] * (1 - self.perovskite.perovskite["C_12"] / self.perovskite.perovskite["C_11"]) * eps_xx
            dEV_H = 2 * self.perovskite.perovskite["a^v"] * (1 - self.perovskite.perovskite["C_12"] / self.perovskite.perovskite["C_11"]) * eps_xx
            dE_S = self.b * (1 + 2 * self.perovskite.perovskite["C_12"] / self.perovskite.perovskite["C_11"]) * eps_xx
            # pasma:
            E_VB_0 = 0
            E_VB = E_VB_0 + dEV_H
            E_CS = self.CS_0 + dEC_H
            E_CH = self.CH_0 + dEC_H + dE_S
            E_CL = self.CL_0 + dEC_H - dE_S
            VBO_A = A.A["VBO"]
            print(self.perovskite.perovskite["a"])

            self.save(VBO_A, self.CS_A, self.VBO_perovskite, E_CS, E_CH, E_CL, self.perovskite.perovskite["a"], name)

    '''
    Take: values to plot graph
    return: graph
    '''
    def save(self, E_VB_A, E_CS_A, VBO_B, E_CS, E_CH, E_CL, a_B, name):
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