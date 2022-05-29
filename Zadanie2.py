import string
from typing import List, Optional, Mapping, Union, Dict
import numpy as np
import matplotlib.pyplot as plt
import os

from Perovskite import Perovskite 
from Interpolate import Interpolate as I

class Zadanie2:
    '''
    Zadanie 2 - dependency on mix proportion
    plot graphs for different composition of component_1 and component_2
    from 100% of component_1 to 100% of component_2
    take: perovskite, optional resolution (for interpolate) and bowing
    '''
    def __init__(
        self,
        perovskite: Perovskite,
        resolution: Optional[int] = 1000,
        bowing: Optional[Union[float, bool]] = None,
    ):
        self.serolution = resolution
        self.perovskite = perovskite
        if bowing == None:
            self.bowing = self.perovskite.bowing
        else:
            self.bowing = bowing
        self.arguments = np.linspace(0,1,num=resolution)

    '''
    Draw Eg (a) with set bowing
    take: bowing, save
    return plot 

    maybe bowing from perovskite is better?
    '''
    def draw_Eg(
        self,
        #bowing: Optional[float] = 0,
        save: Optional[bool] = False,
    ):

        Eg = I.interpolate(self.perovskite.compound_1["Eg"], self.perovskite.compound_2["Eg"], arguments=self.arguments, bowing=self.bowing)
        a = I.interpolate(self.perovskite.compound_1["a"], self.perovskite.compound_2["a"], arguments=self.arguments, bowing=self.bowing)
        plt.plot(a, Eg)
        plt.title("Eg(a)      CsSn [C_l3x I_3(1-x)], bowing=" + str(self.bowing))
        plt.ylabel("Eg")
        plt.xlabel("a")
        plt.grid()
        if save:
            if not os.path.isdir("graphs"):
                os.makedirs("graphs")
            plt.savefig(str(f"graphs/Eg_a_bowing_{str(self.bowing)}.png"))
        else:
            plt.show()
        plt.clf()

    '''
    Draw all graphs from components in 'związki' with:
    take: bowing, save
    return: plots
    '''
    def draw_all_graphs(
        self,
        #bowing: Optional[float] = 0,
        save: Optional[bool] = True,
    ):
        for key in self.perovskite.compound_1:
            values = I.interpolate(
                self.perovskite.compound_1[key], self.perovskite.compound_2[key], arguments=self.arguments, bowing=self.bowing
            )
            plt.plot(self.arguments, values)
            plt.title(f"{key} in Cs Sn [C_l3x I_3(1-x)], bowing=" + str(self.bowing))
            plt.ylabel(key)
            plt.xlabel("x")
            if save:
                if not os.path.isdir("graphs"):
                    os.makedirs("graphs")
                plt.savefig(str(f"graphs/bowing_{str(self.bowing)}_{str(key)}.png"))
            else:
                plt.show()
            plt.clf()

    '''
    Draw one graph of selected value for compoents in 'związki' with:
    take: of, optional: save
    return: plots
    '''
    def draw_graph(
        self,
        #bowing: Optional[float] = 0,
        of: string,
        save: Optional[bool] = True,
    ):
        key = of
        values = I.interpolate(
                self.perovskite.compound_1[key], self.perovskite.compound_2[key], arguments=self.arguments, bowing=self.bowing
            )
        plt.plot(self.arguments, values)
        plt.title(f"{key} in Cs Sn [C_l3x I_3(1-x)], bowing=" + str(self.bowing))
        plt.ylabel(key)
        plt.xlabel("x")
        if save:
            if not os.path.isdir("graphs"):
                os.makedirs("graphs")
            plt.savefig(str(f"graphs/bowing_{str(self.bowing)}_{str(key)}.png"))
        else:
            plt.show()
        plt.clf()