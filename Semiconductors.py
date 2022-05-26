import matplotlib.pyplot as plt
import numpy as np
from typing import List, Optional, Mapping, Union, Dict
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
        self.H_REDUCED = 6.582119569  # [eV]

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
        plt.title("Eg(a)      CsSn [C_l3x I_3(1-x)], bowing=" + str(bowing))
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

    def draw_Eg_temp(
        self,
        temperatures: List[float],
        Eg_temp: List[float],
        save: Optional[bool] = True,
    ) -> None:

        plt.plot(temperatures, Eg_temp)
        plt.title("Eg(T)      CsSn [C_l3x I_3(1-x)] for x=0.35")
        plt.ylabel("Eg [eV]")
        plt.xlabel("T [K]")
        plt.grid()

        if save:
            if not os.path.isdir("graphs2"):
                os.makedirs("graphs2")
            plt.savefig(str(f"graphs2/Eg_as_a_function_of_T_x_0,35.png"))
        else:
            plt.show()
        plt.clf()

    def calculate_Eg_temp(
        self,
        temperatures: List[float],
        mix_parameter: float,
        mixed_params: Dict[str, float],
    ) -> List[float]:

        Eg_0 = (
            self.interpolate(
                self.compound_1["Eg"], self.compound_2["Eg"], arguments=[mix_parameter]
            )[0]
            + 250 * mixed_params["alpha"]
        )

        Eg_T = self.interpolate(
            parameter_1=mixed_params["alpha"],
            constant=Eg_0,
            arguments=temperatures,
            parameter_2=0,
            bowing=0,
        )

        return Eg_T

    def draw_bands(
        self,
        temp_start: Optional[int] = 250,
        temp_stop: Optional[int] = 350,
        resolution: Optional[int] = 1000,
        mix_parameter: Optional[float] = 0.35,
        save: Optional[bool] = True,
    ) -> None:

        mixed_params = self.calculate_mixed_params(mix_parameter)
        temperatures = np.linspace(temp_start, temp_stop, resolution, mix_parameter)
        Eg_temp = self.calculate_Eg_temp(temperatures, mix_parameter, mixed_params)

        self.draw_Eg_temp(temperatures, Eg_temp)

        VB = self.bands_calculate_VB(Eg_temp, mixed_params)
        plt.plot(temperatures, VB, label="VB", alpha=0.7)
        plt.title("bands(T)        CsSn [C_l3x I_3(1-x)] for x=0.35")
        plt.ylabel("E [eV]")
        plt.xlabel("T [K]")

        CH = self.bands_calculate_CH(Eg_temp, mixed_params)
        plt.plot(temperatures, CH, label="CH", alpha=1, linewidth=2.0, color='purple')

        CL = self.bands_calculate_CH(Eg_temp, mixed_params)
        plt.plot(
            temperatures, CL, label="CL", alpha=1, linewidth=1.5, linestyle="dashed", color='yellow'
        )

        CS = self.bands_calculate_CS(Eg_temp, mixed_params)
        plt.plot(temperatures, CS, label="CS", alpha=1, linewidth=1.5, linestyle="-")

        plt.legend()
        plt.grid()
        if save:
            if not os.path.isdir("graphs2"):
                os.makedirs("graphs2")
            plt.savefig(str(f"graphs2/bands_x_0,35.png"))
            plt.show()
        else:
            plt.show()
        plt.clf()

    def calculate_mixed_params(self, mix_parameter) -> Dict[str, float]:

        mixed_params = {
            parameter: self.interpolate(
                self.compound_1[parameter],
                self.compound_2[parameter],
                arguments=[mix_parameter],
            )[0]
            for parameter in self.compound_1.keys()
        }
        return mixed_params

    def bands_calculate_VB(
        self, Eg_temp: List[float], param: Dict[str, float]
    ) -> List[float]:

        return [
            Eg
            + (
                self.H_REDUCED
                / 2
                * param["mh"]
                * (
                    1 / param["mh"]
                    - param["Ep"] / 3 * (2 / Eg + 1 / (Eg + param["delta"]))
                )
                * 2
            )
            for Eg in Eg_temp
        ]

    def bands_calculate_CH(
        self, Eg_temp: List[float], param: Dict[str, float]
    ) -> List[float]:

        return [
            self.H_REDUCED
            / (2 * param["mh"])
            * (
                (
                    (param["gamma_1"] - 1 / 3 * (param["Ep"] / Eg))
                    + (param["gamma_2"])
                    - 1 / 6 * (param["Ep"] / Eg)
                )
                * 2
            )
            for Eg in Eg_temp
        ]

    def bands_calculate_CL(
        self, Eg_temp: List[float], param: Dict[str, float]
    ) -> List[float]:

        return [
            self.H_REDUCED
            / (2 * param["mh"])
            * (
                (
                    (param["gamma_1"] - 1 / 3 * (param["Ep"] / Eg))
                    - (param["gamma_2"])
                    - 1 / 6 * (param["Ep"] / Eg)
                )
                * 2
            )
            for Eg in Eg_temp
        ]

    def bands_calculate_CS(
        self, Eg_temp: List[float], param: Dict[str, float]
    ) -> List[float]:

        return [
            self.H_REDUCED
            / (2 * param["mh"])
            * ((param["gamma_1"] - 1 / 3 * (param["Ep"] / Eg)) * 2 - param["delta"])
            for Eg in Eg_temp
        ]


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
    perovskite.draw_bands()


if __name__ == "__main__":
    main()
