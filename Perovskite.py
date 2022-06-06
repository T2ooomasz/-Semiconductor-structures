from typing import List, Optional, Mapping, Union, Dict
from Interpolate import Interpolate as I

class Perovskite:
    '''
    initialize Perovskite class which contain:
        compount_1 (first compound e.q. CsSnCl_3)
        compount_2 (second compound e.g. CsSnI_3)
    and parameters for creation of Perovskite: 
    [parameter_1 * x + parameter_2 * (1 - x) + bowing * (1 - x) * x + constant]
        mix_proportion (=x)  (proportion betwen compounds)
        bowing  (for non linear combination of compounds)
        constant    (for constant shift of all parameters)
    '''
    def __init__(
        self,
        compound_1: Mapping[str, float],
        compound_2: Mapping[str, float],

        # parameters for calculation perovskite
        mix_proportion: Optional[float] = 0.5,
        bowing: Optional[float] = 0,
        constant: Optional[float] = 0
    ):
        self.compound_1 = compound_1
        self.compound_2 = compound_2

        # parameters for calculation perovskite
        self.mix_proportion = mix_proportion
        self.bowing = bowing
        self.constant = constant
        self.H_REDUCED = 6.582119569  # [eV]
        '''
        perovskite in class Perovskite (perovskite.perovskite) 
        is the mix of all parameters in components of perovskite
        with set mix proportion and bowing (if wanted)
        '''
        self.perovskite = self.calculate_mixed_params(self.mix_proportion)

    '''
    take: proportion of parameters
    return: mixed parameters with proportion taken
    EX: mix_parameter = 0.35
        return component1*0.35+component2*(1-0.35)
    '''
    def calculate_mixed_params(self, mix_parameter) -> Dict[str, float]:

        mixed_params = {
            parameter: I.interpolate(
                parameter_1 = self.compound_1[parameter],
                parameter_2 = self.compound_2[parameter],
                arguments = [mix_parameter],
                bowing = self.bowing,
                constant = self.constant
            )[0]
            for parameter in self.compound_1.keys()
        }
        return mixed_params
