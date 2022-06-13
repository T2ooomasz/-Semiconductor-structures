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

    for temp in range(100):
        perovskite = Perovskite(compound_1=compound_1, compound_2=compound_2, temperature=temp)
        print(perovskite.Eg_with_temperature, perovskite.perovskite["Eg"])



if __name__ == "__main__":
    main()