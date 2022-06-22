from CsSnCl3 import CsSnCl3
from CsSnI3 import CsSnI3
from Perovskite_With_Temperature import Perovskite_With_Temperature as Perovskite
from Hamiltonian import Hamiltonian 

def main():
    # components of perovskite
    compound_1 = CsSnCl3.CsSnCl3
    compound_2 = CsSnI3.CsSnI3

    # create perovskite with set variables like temperature, mix proportion etc.
    perovskite = Perovskite(compound_1, compound_2, temperature=300, mix_proportion=0.5)
    
    Zadanie5 = Hamiltonian() # initializate Hamiltonian calculations
    # create graph from eigrenvalues for every k on percent range Gamma-R-M with set step
    Zadanie5.spectrum_eigenvalues(perovskite=perovskite,
                                    step=0.1, 
                                    percent_range=15,
                                    tension=0,
                                    name="1")

if __name__ == "__main__":
    main()