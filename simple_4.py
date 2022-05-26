import matplotlib.pyplot as plt

def save(E_VB_A, E_CS_A, VBO_B, E_CS, E_CH, E_CL, a_B, name):
    fig, ax = plt.subplots()
    ax.hlines(y=E_VB_A, xmin=0, xmax=50, linewidth=2, color='r', label = "E_VB_A")
    ax.hlines(y=E_VB_A, xmin=100, xmax=150, linewidth=2, color='r')

    ax.hlines(y=E_CS_A, xmin=0, xmax=50, linewidth=2, color='b', label = "E_CS_A")
    ax.hlines(y=E_CS_A, xmin=100, xmax=150, linewidth=2, color='b')

    ax.hlines(y=VBO_B, xmin=50, xmax=100, linewidth=2, label = "VBO_B", color="darkred")
    ax.hlines(y=E_CS, xmin=50, xmax=100, linewidth=2, label = "E_CS",color="darkblue")
    ax.hlines(y=E_CH, xmin=50, xmax=100, linewidth=4, label = "E_CH", color="green", linestyle='dotted')
    ax.hlines(y=E_CL, xmin=50, xmax=100, linewidth=2, label = "E_CL", color="orange")

    ax.vlines(x=50, ymin=E_CS, ymax=E_CS_A, color='blue')
    ax.vlines(x=100, ymin=E_CS, ymax=E_CS_A, color='blue')
    ax.vlines(x=50, ymin=E_VB_A, ymax=VBO_B, color='red')
    ax.vlines(x=100, ymin=E_VB_A, ymax=VBO_B, color='red')

    plt.xlabel('z [nm]')
    plt.ylabel('E [eV]')
    plt.title('')
    plt.legend()
    plt.grid()
    name += ".png"
    #plt.show()
    plt.savefig(name)

def naprezenia(naprezenie, a_B, ac, av, C_12, C_11, b, E_CS_0, E_CH_0, E_CL_0, E_VB_A, E_CS_A, VBO_B):
    # naprężenie
    name = str(naprezenie)
    naprezenie = naprezenie/100
    a_A = (1 + naprezenie) * a_B
    eps_xx = (a_A - a_B) / a_B
    # prędkości zmian
    dEC_H = 2 * ac * (1 - C_12 / C_11) * eps_xx
    dEV_H = 2 * av * (1 - C_12 / C_11) * eps_xx
    dE_S = b * (1 + 2 * C_12 / C_11) * eps_xx
    # pasma:
    E_VB_0 = 0
    E_VB = E_VB_0 + dEV_H
    E_CS = E_CS_0 + dEC_H
    E_CH = E_CH_0 + dEC_H + dE_S
    E_CL = E_CL_0 + dEC_H - dE_S

    save(E_VB_A, E_CS_A, VBO_B, E_CS, E_CH, E_CL, a_B, name)

def main():
    # stałe:
    CsSnCl3 = {
        "Eg": 2.69,
        "delta": 0.45,
        "gamma_1": 6.4,
        "gamma_2": 2.5,
        "gamma_3": 0.8,
        "mh": 0.140,
        "Ep": 34.7,
        "a": 5.560,
        "alpha": 0.7 * 0.001,  # eV/K
        "a^c" : -0.808,
        "a^v" : -5.752,
        "C_11" : 49.35,
        "C_12" : 8.77,
    }

    CsSnI3 = {
        "Eg": 1.01,
        "delta": 0.42,
        "gamma_1": 13.0,
        "gamma_2": 5.6,
        "gamma_3": 2.1,
        "mh": 0.069,
        "Ep": 29.9,
        "a": 6.219,
        "alpha": 0.35 * 0.001,  # eV/K
        "a^c" : -0.052,
        "a^v" : -3.651,
        "C_11" : 21.34,
        "C_12" : 1.22,
    }
    b = -1.7
    T = 300

    f = open("data_simple_4.txt", "w")
    #materiał A:
    VBO_A = 0
    E_VB_A = VBO_A

    #skład:
    x = 0.65
    bowing = 0.9
    C_12 = x * CsSnCl3["C_12"] + (1 - x) * CsSnI3["C_12"] - bowing * (x * x - x) 
    C_11 = x * CsSnCl3["C_11"] + (1 - x) * CsSnI3["C_11"] - bowing * (x * x - x) 
    f.write(str(C_11) + "\n" + str(C_12) + "\n")

    # przerwa wzbroniona:
    CsSnCl3_Eg = CsSnCl3["Eg"] + CsSnCl3["alpha"] * T
    CsSnI3_Eg = CsSnI3["Eg"] + CsSnI3["alpha"] * T
    f.write(str(CsSnCl3_Eg) + "\n" + str(CsSnI3_Eg) + "\n")

    # stała siatki:
    a_B = x * CsSnCl3["a"] + (1 - x) *CsSnI3["a"] - bowing * (x * x - x)
    f.write(str(a_B) + "\n")

    # przerwa wzbroniona:
    Eg_CsSn = x *CsSnCl3_Eg + (1 - x) * CsSnI3_Eg + bowing * x * (1 - x)
    EB_g = Eg_CsSn
    f.write(str(Eg_CsSn) + "\n")

    # SOC:
    Delta_CsSn = x * CsSnCl3["delta"] + (1 - x) * CsSnI3["delta"] + bowing * (x * x - x)
    f.write(str(Delta_CsSn) + "\n")

    # pasma w punkcie R:
    VBO_B = 1
    E_CS_0 = VBO_B + Eg_CsSn
    E_CH_0 = VBO_B + Eg_CsSn + Delta_CsSn
    E_CL_0 = E_CH_0
    f.write(str(VBO_B) + "\n" + str(E_CS_0) + "\n" + str(E_CH_0) + "\n" + str(E_CL_0) + "\n")

    # potencjały:
    ac = CsSnI3["a^c"] * x + CsSnCl3["a^c"] * (1 - x)
    av = CsSnI3["a^v"] * x + CsSnCl3["a^v"] * (1 - x)
    f.write(str(ac) + "\n" + str(av) + "\n")

    # przerwa wzbroniona materiału A:
    EA_g = VBO_B + EB_g + 3
    E_CS_A = EA_g
    f.write(str(EA_g) + "\n" + str(E_CS_A) + "\n")

    # naprężenie 0%
    naprezenie = 0
    naprezenia(naprezenie, a_B, ac, av, C_12, C_11, b, E_CS_0, E_CH_0, E_CL_0, E_VB_A, E_CS_A, VBO_B)
    

    # naprężenie ściskające -3%
    naprezenie = -3
    naprezenia(naprezenie, a_B, ac, av, C_12, C_11, b, E_CS_0, E_CH_0, E_CL_0, E_VB_A, E_CS_A, VBO_B)


    # naprężenie rozciągające +3%
    naprezenie = 3
    naprezenia(naprezenie, a_B, ac, av, C_12, C_11, b, E_CS_0, E_CH_0, E_CL_0, E_VB_A, E_CS_A, VBO_B)
    f.close()

if __name__ == "__main__":
    main()