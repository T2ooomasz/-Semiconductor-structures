import matplotlib.pyplot as plt
import numpy as np
from typing import List, Optional, Mapping
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
        self.arguments = np.linspace(arg_start, arg_stop, resolution)
        self.compound_1 = compound_1
        self.compound_2 = compound_2

    def interpolate(
        self,
        parameter_1: float,
        parameter_2: float,
        bowing: Optional[float] = 0,
    ) -> List[float]:

        return [
            parameter_1 * x + parameter_2 * (1 - x) + bowing * (1 - x) * x
            for x in self.arguments
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
            plt.plot(self.arguments, values, color='red')
            plt.title(f"{key} in CsSn [Cl_3x I_3(1-x)]        bowing=" + str(bowing))
            plt.ylabel(key)
            plt.xlabel("x")
            plt.grid()
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
        save: Optional[bool] = True,
    ):

        Eg = self.interpolate(self.compound_1["Eg"], self.compound_2["Eg"], bowing)
        a = self.interpolate(self.compound_1["a"], self.compound_2["a"], bowing)
        plt.plot(a, Eg, color='red')
        plt.title("Eg(a) in CsSn [Cl_3x I_3(1-x)]        bowing=" + str(bowing))
        plt.ylabel("Eg")
        plt.xlabel("a")
        plt.grid()
        if save:
            if not os.path.isdir("graphs"):
                os.makedirs("graphs")
            plt.savefig(str(f"graphs/Eg_a_bowing_{str(bowing)}.png"))
        else:
            plt.show()
        plt.clf()


def main():

    CsSnCl3 = {
        "Eg": 2.69,
        "delta": 0.45,
        "\u03B3_1": 6.4, # gamma
        "\u03B3_2": 2.5,
        "\u03B3_3": 0.8,
        "mh": 0.140,
        "Ep": 34.7,
        "a": 5.560,
    }

    CsSnI3 = {
        "Eg": 1.01,
        "delta": 0.42,
        "\u03B3_1": 13.0, # gamma
        "\u03B3_2": 5.6,
        "\u03B3_3": 2.1,
        "mh": 0.069,
        "Ep": 29.9,
        "a": 6.219,
    }

    perovskite = Perovskite(compound_1=CsSnCl3, compound_2=CsSnI3, resolution=1000)

    perovskite.draw_graphs(bowing=0, save=True)
    perovskite.draw_graphs(bowing=1.5, save=True)
    perovskite.draw_Eg(bowing=0, save=True)
    perovskite.draw_Eg(bowing=1.5, save=True)


if __name__ == "__main__":
    main()