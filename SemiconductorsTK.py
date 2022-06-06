import matplotlib.pyplot as plt
import numpy as np
from typing import List, Optional, Mapping, Union, Dict
import os
from regex import A

from Interpolate import Interpolate as I
from Perovskite import Perovskite as P
from CsSnCl3 import CsSnCl3
from CsSnI3 import CsSnI3
from Energetic_profile import Energetic_profile

from Zadanie2 import Zadanie2
from Perovskite_With_Temperature import Perovskite_With_Temperature as Perovskite
from Hamiltonian import Hamiltonian as Ha
from G_R_M import G_R_M
from Zadanie5 import grapgh_for_gif

def main():
    compound_1 = CsSnCl3.CsSnCl3
    compound_2 = CsSnI3.CsSnI3
    MIX_PROPORTION = np.arange(start=0, stop=1, step=0.025) 
    TEMPERATURES = np.arange(start=0, stop=100, step=100)
    BOWING = np.arange(start=-0.5, stop=0.5, step=0.01)
    TENSION = np.arange(start=-3,stop=3, step=0.3)

    gif = grapgh_for_gif()
    
    gif.gif_with_mix_proportion(
        compound_1=compound_1,
        compound_2=compound_2,
        MIX_proportion=MIX_PROPORTION,
        temperature=300,
        bowing=0,
        tension=0,
        resolution=0.1,
        percent_range=15,
    )

    gif.gif_with_temperature(
        compound_1=compound_1,
        compound_2=compound_2,
        mix_proportion=0.5,
        Temperature=TEMPERATURES,
        bowing=0,
        tension=0,
        resolution=0.1,
        percent_range=15,
    )

    gif.gif_with_bowing(
        compound_1=compound_1,
        compound_2=compound_2,
        mix_proportion=0.5,
        temperature=300,
        Bowing=BOWING,
        tension=0,
        resolution=0.1,
        percent_range=15,
    )
    gif.gif_with_tensin(
        compound_1=compound_1,
        compound_2=compound_2,
        mix_proportion=0.5,
        temperature=300,
        bowing=0,
        Tension=TENSION,
        resolution=0.1,
        percent_range=15,
    )
    
    


if __name__ == "__main__":
    main()