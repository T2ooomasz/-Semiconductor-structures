import numpy as np
import matplotlib.pyplot as plt
from typing import List, Optional, Mapping, Union, Dict
from Perovskite_With_Temperature import Perovskite_With_Temperature as Perovskite
from Energetic_profile import Energetic_profile

class Hamiltonian:
    def __init__(self):
        self.H_REDUCED = 6.582119569  # [eV]
        self.m0 = 1 # idk how much it should be

    def Ham(self, VB, CH, CL, CS, P_plus, P_minus, P_z, S, R, D):
        s2 = np.sqrt(2)
        Is2 = 1/s2
        s3 = np.sqrt(3)
        Is3 = 1/s3
        s6 = np.sqrt(6)
        Is6 = 1/s6
        Sc = np.conj(S)
        Rc = np.conj(R)

        H = np.array([[VB,          0,              Is2*P_plus,     -s2/s3*P_z,     -Is6*P_minus,   0,              -Is3*P_z,       -Is3*P_minus],
                      [0,           VB,             0,              Is6*P_plus,     -s2/s3*P_z,     -Is2*P_minus,   -Is3*P_plus,    Is3*P_z     ],
                      [Is2*P_minus, 0,              CH,             S,              -R,             0,              Is2*S,          -s2*R       ],
                      [-s2/s3*P_z,  Is6*P_minus,   Sc,             CL,             0,              -R,             -D,             -s3/s2*S     ],
                      [-Is6*P_plus, -s2/s3*P_z,     -Rc,            0,              CL,             -S,             -s3/s2*Sc,      D           ],
                      [0,           -Is2*P_plus,    0,              -Rc,            -Sc,            CH,             s2*Rc,          Is2*Sc      ],
                      [-Is3*P_z,    -Is3*P_minus,   Is2*Sc,         -D,             -s3/s2*S,       s2*R,           CS,             0           ],
                      [-Is3*P_plus, Is3*P_z,        -s2*Rc,         -s3/s2*Sc,       D,              Is2*S,          0,              CS          ]])

        w,v =  np.linalg.eig(H)
        idx = w.argsort() #small to large
        w = w[idx] # wartości własne
        #v = v[:,idx] # wektory własne
        #diagonal = np.diag(w)

        return w

    def update_for_k(self, E_VB, E_CS, E_CH, E_CL, k, P, gammav, gamma1, gamma2, gamma3):
        P_plus = P * (k[0] + 1j*k[2])
        P_minus = P * (k[0] - 1j*k[2])
        P_z = P * k[2]

        VB = E_VB - self.H_REDUCED**2 / (2 * self.m0) * gammav * (k[0]**2 + k[1]**2 + k[2]**2)
        CS = E_CS + self.H_REDUCED**2 / (2 * self.m0) * (gamma1*(k[0]**2 + k[1]**2 + k[2]**2))
        CH = E_CH + self.H_REDUCED**2 / (2 * self.m0) *((gamma1+gamma2) * (k[0]**2 + k[1]**2) + (gamma1 - 2*gamma2)*k[2]**2)
        CL = E_CL + self.H_REDUCED**2 / (2 * self.m0) *((gamma1-gamma2) * (k[0]**2 + k[1]**2) + (gamma1 + 2*gamma2)*k[2]**2)

        S = self.H_REDUCED**2 / (2*self.m0) * 2 * np.sqrt(3) * gamma3 * (-k[0]+1j*k[1]) * k[2]
        R = self.H_REDUCED**2 / (2*self.m0) * np.sqrt(3) * (gamma2 * (k[0]**2 - k[1]**2) - 2*1j*gamma3*k[0]*k[1])
        D = self.H_REDUCED**2 / (2*self.m0) * np.sqrt(2) * gamma2 * (k[0]**2 + k[1]**2 - 2*k[2]**2)
        return VB, CS, CH, CL, P_plus, P_minus, P_z, S, R, D

    def eigenvalues(self, perovskite: Perovskite, k, tension):
        Energetic_p = Energetic_profile(perovskite=perovskite)
        Table = Energetic_p.return_bands(tension=tension)
        
        gamma1 = perovskite.perovskite["gamma_1"] - 1/3 * perovskite.perovskite["Ep"]/perovskite.Eg_with_temperature
        gamma2 = perovskite.perovskite["gamma_2"] - 1/6 * perovskite.perovskite["Ep"]/perovskite.Eg_with_temperature
        gamma3 = perovskite.perovskite["gamma_3"] - 1/6 * perovskite.perovskite["Ep"]/perovskite.Eg_with_temperature
        gammav = 1 / perovskite.perovskite["mh"] - perovskite.perovskite["Ep"]/3 * (2 / perovskite.Eg_with_temperature + 1 / (perovskite.Eg_with_temperature + perovskite.perovskite["delta"]))

        P = np.sqrt(perovskite.perovskite["Ep"] * self.H_REDUCED**2 / (2*self.m0))
        VB, CS, CH, CL, P_plus, P_minus, P_z, S, R, D = self.update_for_k(E_VB=Table[0],E_CS=Table[1],E_CH=Table[2],E_CL=Table[3],k=k, P=P, gammav=gammav, gamma1=gamma1, gamma2=gamma2, gamma3=gamma3)
        #eigenvalues from hamiltonian
        eigenvalues = self.Ham(VB=VB, CH=CH, CL=CL, CS=CS, P_plus=P_plus, P_minus=P_minus, P_z=P_z, S=S, R=R, D=D)
        return eigenvalues.real

    def spectrum_eigenvalues(self, perovskite: Perovskite, step, percent_range, tension, name):
        A = []
        R = np.array([0,0,0])
        Gamma = np.array([1,1,1])
        M = np.array([0,0,1])
        k_values = np.arange(step, percent_range+step, step)
        R_Gamma = [(x/100*Gamma) for x in k_values]
        R_Gamma = np.multiply(R_Gamma, -np.pi/perovskite.perovskite["a"])
        R_M = [(x/100*M) for x in k_values]
        R_M = np.multiply(R_M, -np.pi/perovskite.perovskite["a"])

        for k in reversed(R_Gamma):
            A.append(self.eigenvalues(perovskite=perovskite, k=k, tension=tension))

        A.append(self.eigenvalues(perovskite=perovskite, k=R, tension=tension))

        for k in R_M:
            A.append(self.eigenvalues(perovskite=perovskite, k=k, tension=tension))

        for j in range(8):
            Y = []
            for i in range(len(A)):
                Y.append(A[i][j])

            X = -k_values
            X = np.append(X, 0)
            X = np.append(X, k_values)
            X.sort()

            name_series = 'eigenvalue ' + str(j)
            plt.plot(X, Y, label=name_series)

        plt.xlabel('Gamma - R - M [% of range from R]')
        plt.ylabel('E [eV]')
        plt.title('')
        #plt.legend()
        plt.grid()
        plt.savefig(str(f"graphsforGIF/{str(name)}.png"))
        plt.clf()

        