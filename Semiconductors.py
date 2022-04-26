import matplotlib.pyplot as plt
import numpy as np
from typing import List, Optional, Mapping, Union
import os

from regex import A


class Perovskite:
    def __init__(
        self,
        resolution: int,
        compound_1: Mapping[str, float],
        compound_2: Mapping[str, float],
        arg_start: Optional[float] = 0,
        arg_stop: Optional[float] = 1,
    ):
        self.arguments = (
            np.linspace(arg_start, arg_stop, resolution) if resolution > 1 else 0.5
        )
        self.compound_1 = compound_1
        self.compound_2 = compound_2

    def interpolate(
        self,
        parameter_1: float,
        parameter_2: float,
        bowing: Optional[float] = 0,
        constant: Optional[float] = 0,
        arguments: Optional[Union[List[float], bool]] = None,
    ) -> List[float]:

        if arguments is None:
            arguments = self.arguments

        return [
            parameter_1 * x + parameter_2 * (1 - x) + bowing * (1 - x) * x + constant
            for x in arguments
        ]

    def draw_graphs(
        self,
        bowing: Optional[float] = 0,
        save: Optional[bool] = True,
    ):
        for key in self.compound_1:
            values = self.interpolate(
                self.compound_1[key], self.compound_2[key], bowing
            )
            plt.plot(self.arguments, values)
            plt.title(f"{key} in Cs Sn [C_l3x I_3(1-x)], bowing=" + str(bowing))
            plt.ylabel(key)
            plt.xlabel("x")
            if save:
                if not os.path.isdir("graphs"):
                    os.makedirs("graphs")
                plt.savefig(str(f"graphs/bowing_{str(bowing)}_{str(key)}.png"))
            else:
                plt.show()
            plt.clf()

    def draw_Eg(
        self,
        bowing: Optional[float] = 0,
        save: Optional[bool] = False,
    ):

        Eg = self.interpolate(self.compound_1["Eg"], self.compound_2["Eg"], bowing)
        a = self.interpolate(self.compound_1["a"], self.compound_2["a"], bowing)
        plt.plot(a, Eg)
        plt.title("Eg(a) in Cs Sn [C_l3x I_3(1-x)], bowing=" + str(bowing))
        plt.ylabel("Eg")
        plt.xlabel("a")
        if save:
            if not os.path.isdir("graphs"):
                os.makedirs("graphs")
            plt.savefig(str(f"graphs/Eg_a_bowing_{str(bowing)}.png"))
        else:
            plt.show()
        plt.clf()

    def draw_Eg_temp(
        self,
        temp_start: Optional[int] = 250,
        temp_stop: Optional[int] = 350,
    ):

        alpha = self.interpolate(
            self.compound_1["alpha"], self.compound_2["alpha"], arguments=[0.5]
        )[0]
        temperatures = np.linspace(temp_start, temp_stop, 1000)

        Eg_0 = (
            self.interpolate(
                self.compound_1["Eg"], self.compound_2["Eg"], arguments=[0.5]
            )[0]
            + 250 * alpha
        )

        Eg_temp = self.interpolate(
            parameter_1=alpha,
            constant=Eg_0,
            arguments=temperatures,
            parameter_2=0,
            bowing=0,
        )

        plt.plot(temperatures, Eg_temp)
        plt.title("Eg(T), Cs Sn [C_l3x I_3(1-x)] for x=0.5")
        plt.ylabel("Eg [eV]")
        plt.xlabel("T [K]")
        plt.show()
        plt.clf()


def main():

    CsSnCl3 = {
        "Eg": 2.69,
        "delta": 0.45,
        "gamma_1": 6.4,
        "gamma_2": 2.5,
        "gamma_3": 0.8,
        "mh": 0.140,
        "Ep": 34.7,
        "a": 5.560,
        "alpha": 0.7 * 0.001,  # eV/K
    }

    CsSnI3 = {
        "Eg": 1.01,
        "delta": 0.42,
        "gamma_1": 13.0,
        "gamma_2": 5.6,
        "gamma_3": 2.1,
        "mh": 0.069,
        "Ep": 29.9,
        "a": 6.219,
        "alpha": 0.35 * 0.001,  # eV/K
    }

    perovskite = Perovskite(compound_1=CsSnCl3, compound_2=CsSnI3, resolution=1)
    perovskite.draw_Eg_temp()


if __name__ == "__main__":
    main()
