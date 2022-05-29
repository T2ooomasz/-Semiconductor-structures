from typing import List, Optional, Mapping, Union, Dict
import numpy as np
import matplotlib.pyplot as plt
import os

from Perovskite import Perovskite 
from Interpolate import Interpolate as I

# want to make it child of Perovskite class - can be initializated separatly
class Perivskite_With_Temperature:
    '''
    Zadanie 3 - dependency on Temperature
    contain variables of bonds in wanted temperature

    WHAT IS WRONG:
        when calculated from list of temperatures results are different for the same temperature if list range is different
        (Ex: temperatures=[150-300] Eg[temp=250]=1.78 || temperatures=[249-251] Eg[temp250]=1.83)
        calculation for list with lenght=1 crash (espetially for CL band)
    '''
    def __init__(
        self,
        perovskite: Perovskite,
        resolution: Optional[int] = 1000,
        temperature: Optional[float] = 0,
        bowing: Optional[Union[float, bool]] = None,
    ):
        self.perovskite = perovskite
        self.resolution = resolution
        self.temperature = temperature
        if bowing == None:
            self.bowing = self.perovskite.bowing
        else:
            self.bowing = bowing
        self.arguments = np.linspace(0,1,num=resolution)
        self.H_REDUCED = perovskite.H_REDUCED  # [eV]
        self.Eg_with_temperature = self.calculate_Eg_temp([self.temperature], self.perovskite.perovskite)[0]
        self.E_VB_with_temperature = self.bands_calculate_VB([self.Eg_with_temperature], self.perovskite.perovskite)[0]
        self.E_CH_with_temperature = self.bands_calculate_CH([self.Eg_with_temperature], self.perovskite.perovskite)[0]
        self.E_CL_with_temperature = self.bands_calculate_CL([self.Eg_with_temperature], self.perovskite.perovskite)[0]
        self.E_CS_with_temperature = self.bands_calculate_CS([self.Eg_with_temperature], self.perovskite.perovskite)[0]
    
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

    '''
    calculate Eg for perovskite in set temperature (or list of temperatures)
    take: list of temperaturs, mixed_parameters of perovskite (perovskite.perovskite)
    return: Eg for every temperature
    '''
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
    Plot values of bands in range of temperaturs
    take: temperature for start and stop, resolution, save
    return: plots of:
            Eg dependend on temperatur
            bands VB, CH, CL, CS dependend on temerature
    '''
    def draw_bands(
        self,
        temp_start: Optional[int] = 250,
        temp_stop: Optional[int] = 350,
        resolution: Optional[int] = 1000,
        save: Optional[bool] = True,
    ) -> None:

        #mix_parameter = self.perovskite.mix_proportion
        mixed_params = self.perovskite.perovskite
        #temperatures = np.linspace(temp_start, temp_stop, resolution, mix_parameter)
        temperatures = np.linspace(temp_start, temp_stop, resolution)
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

    '''
    calculate value of band VB
    take: list of Eg (to calculate VB for every Eg), mixed parameters (perovskite)
    return: values of band VB for every Eg
    '''
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

    '''
    calculate value of band CH
    take: list of Eg (to calculate CH for every Eg), mixed parameters (perovskite)
    return: values of band CH for every Eg
    '''
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

    '''
    calculate value of band CL
    take: list of Eg (to calculate CL for every Eg), mixed parameters (perovskite)
    return: values of band CL for every Eg
    '''
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

    '''
    calculate value of band CS
    take: list of Eg (to calculate CS for every Eg), mixed parameters (perovskite)
    return: values of band CS for every Eg
    '''
    def bands_calculate_CS(
        self, Eg_temp: List[float], param: Dict[str, float]
    ) -> List[float]:

        return [
            self.H_REDUCED
            / (2 * param["mh"])
            * ((param["gamma_1"] - 1 / 3 * (param["Ep"] / Eg)) * 2 - param["delta"])
            for Eg in Eg_temp
        ]

