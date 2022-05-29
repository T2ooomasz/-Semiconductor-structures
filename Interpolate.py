from typing import List, Optional, Mapping, Union, Dict

class Interpolate:
    def __init__(
        self,
        parameter_1: float,
        parameter_2: float,
        arguments: Union[List[float], bool] = None,
        bowing: Optional[float] = 0,
        constant: Optional[float] = 0,
    ):
        self.parameter_1 = parameter_1,
        self.parameter_2 = parameter_2,
        self.arguments = arguments,
        self.bowing = bowing,
        self.constant = constant,
        self.interpolated = self.interpolate2()

    '''
    take: param1, param2, arguments, optional: bowing, constant
    return: interpolated param1 with param2 with weight coresponded to arguments 
    EX: param1 = 1, param2 = 2, arguments = [0, 0.3, 0.6. 1]
        return [param1*0+param2*(1-0), param1*0.3+param2*(1-0.3), ...]
    '''
    def interpolate2(self):
        return [
            self.parameter_1 * x + self.parameter_2 * (1 - x) + self.bowing * (1 - x) * x + self.constant
            for x in self.arguments
        ]

    '''
    take: param1, param2, arguments, optional: bowing, constant
    return: interpolated param1 with param2 with weight coresponded to arguments 
    EX: param1 = 1, param2 = 2, arguments = [0, 0.3, 0.6. 1]
        return [param1*0+param2*(1-0), param1*0.3+param2*(1-0.3), ...]
    '''
    def interpolate(
        parameter_1: float,
        parameter_2: float,
        arguments: Optional[Union[List[float], bool]] = None,
        bowing: Optional[float] = 0,
        constant: Optional[float] = 0,
    ) -> List[float]:

        return [
            parameter_1 * x + parameter_2 * (1 - x) + bowing * (1 - x) * x + constant
            for x in arguments
        ]
