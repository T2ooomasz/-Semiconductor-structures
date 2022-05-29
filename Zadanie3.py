from typing import List, Optional, Mapping, Union, Dict
import numpy as np
import matplotlib.pyplot as plt
import os

from Perovskite import Perovskite 
from Interpolate import Interpolate as I

class Zadanie3:
    '''
    Zadanie 3 - dependency on Temperature
    '''
    def __init__(
        self,
        perovskite: Perovskite,
        resolution: Optional[int] = 1000,
        temperature: Optional[float] = 250,
        bowing: Optional[Union[float, bool]] = None,
    ):
        self.perovskite = perovskite
        self.with_temperature =  self.perovskite.perovskite['Eg'] + temperature * self.perovskite.perovskite["alpha"] 
        self.resolution = resolution
        self.temperature = temperature
        if bowing == None:
            self.bowing = self.perovskite.bowing
        else:
            self.bowing = bowing
        self.arguments = np.linspace(0,1,num=resolution)
        self.H_REDUCED = perovskite.H_REDUCED  # [eV]

    def calculate_Eg_temp(
            self,
            temperatures: List[float],
            mixed_params: Dict[str, float],
        ) -> List[float]:

            Eg_0 = (
                self.perovskite.perovskite['Eg'] + temperatures[0]* mixed_params["alpha"] 
            )

            Eg_T = I.interpolate(
                parameter_1=mixed_params["alpha"],
                constant=Eg_0,
                arguments=temperatures,
                parameter_2=0,
                bowing=0,
            )

            return Eg_T

    '''
    Methods to draw dependency on temperature
    '''
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
            if not os.path.isdir("graphs3"):
                os.makedirs("graphs3")
            plt.savefig(str(f"graphs3/Eg_as_a_function_of_T_x_0,35.png"))
        else:
            plt.show()
        plt.clf()

    
    def draw_bands(
        self,
        temp_start: Optional[int] = 250,
        temp_stop: Optional[int] = 350,
        resolution: Optional[int] = 1000,
        save: Optional[bool] = True,
    ) -> None:

        mix_parameter = self.perovskite.mix_proportion
        mixed_params = self.perovskite.perovskite
        temperatures = np.linspace(temp_start, temp_stop, resolution, mix_parameter)
        Eg_temp = self.calculate_Eg_temp(temperatures, mixed_params)

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
            if not os.path.isdir("graphs3"):
                os.makedirs("graphs3")
            plt.savefig(str(f"graphs3/bands_x_0,35.png"))
            plt.show()
        else:
            plt.show()
        plt.clf()

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

