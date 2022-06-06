from typing import List, Optional, Mapping, Union, Dict

from Perovskite_With_Temperature import Perovskite_With_Temperature as Perovskite
from Hamiltonian import Hamiltonian

class G_R_M:
    def __init__ (
        self,
        compound_1: Mapping[str, float],
        compound_2: Mapping[str, float],  
        mix_proportion: Optional[float] = 0.5, 
        temperature: Optional[float] = 300,
        bowing: Optional[float] = 0,
        tension: Optional[float] = 0,
        resolution: Optional[float] = 0.1,
        percent_range: Optional[float] =  15,
        name: Optional[str] = "1"
    ):
        self.compound_1=compound_1,
        self.compound_2=compound_2,  
        self.mix_proportion=mix_proportion, 
        self.temperature=temperature,
        self.bowing=bowing,
        self.tension=tension,
        self.resolution=resolution,
        self.percent_range=percent_range,
        self.name = name,
            
    def draw(self, compound_1, compound_2, mix_proportion, temperature, bowing, resolution, percent_range, tension, name):
        perovskite = Perovskite(
            compound_1=compound_1, 
            compound_2=compound_2,  
            mix_proportion=mix_proportion, 
            temperature=temperature,
            bowing=bowing)
        perovskite.perovskite["Ep"] /= 2
        H = Hamiltonian()
        H.spectrum_eigenvalues(perovskite=perovskite, step=resolution, percent_range=percent_range, tension=tension, name=name)