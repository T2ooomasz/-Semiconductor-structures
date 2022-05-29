import matplotlib.pyplot as plt
import numpy as np
from typing import List, Optional, Mapping, Union, Dict
import os
from regex import A

from Interpolate import Interpolate as I
from Perovskite import Perovskite
from CsSnCl3 import CsSnCl3
from CsSnI3 import CsSnI3

from Zadanie2 import Zadanie2
from Perovskite_With_Temperature import Perivskite_With_Temperature as Perovskite_wT


def main():
    compound_1 = CsSnCl3.CsSnCl3
    compound_2 = CsSnI3.CsSnI3
    mix_proportion=0.35
    
    perovskite = Perovskite(compound_1=compound_1, compound_2=compound_2,  mix_proportion=mix_proportion)

    perovskite1 = Perovskite_wT(perovskite=perovskite, temperature=250)
    print(
        perovskite1.Eg_with_temperature,
        perovskite1.E_VB_with_temperature,
        perovskite1.E_CH_with_temperature,
        perovskite1.E_CL_with_temperature,
        perovskite1.E_CS_with_temperature)
        
    perovskite1.draw_bands(temp_start=200, temp_stop=300)
    
    


if __name__ == "__main__":
    main()