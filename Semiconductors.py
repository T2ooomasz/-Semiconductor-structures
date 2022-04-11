import matplotlib.pyplot as plt
import numpy as np
from typing import List, Optional, Mapping
import os


class Perovskite:
    def __init__(self, arg_start: float, arg_stop: float, steps: int):
        # self.arg_start = arg_start
        # self.arg_stop = arg_stop
        # self.steps = steps
        self.arguments = np.linspace(arg_start, arg_stop, steps)

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
        compound_1: Mapping[str, float],
        compound_2: Mapping[str, float],
        bowing: Optional[float] = 0,
    ):
        for key in compound_1:
            values = self.interpolate(compound_1[key], compound_2[key], bowing)
            plt.plot(self.arguments, values)
            plt.title(f"{key} in Cs Sn [C_l3x I_3(1-x)]")
            plt.ylabel(key)
            plt.xlabel("x")
            if not os.path.isdir("graphs"):
                os.makedirs("graphs")
            plt.savefig(str(f"graphs/bowing_{str(bowing)}_{str(key)}.png"))
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
    }

    perovskite = Perovskite(0, 1, 1000)
    perovskite.draw_graphs(CsSnCl3, CsSnI3, bowing=0)
    perovskite.draw_graphs(CsSnCl3, CsSnI3, bowing=2)


if __name__ == "__main__":
    main()
