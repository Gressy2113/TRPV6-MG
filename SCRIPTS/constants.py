kBT = 310*8.314462618/1000 # 2.577 kJ/mol 
V0 = 1.661 # nm^3
BIASF = 5 

# dG calculation parameterss
L_BULK_MIN = 2
L_BULK_MAX = 2.5
L_BOND_MAX = 0.4
K_RES = 100000 # kJ/mol/nm2
R_CYL = {
    'AS': 0.7, # nm
    'PS': 0.9,  # nm
    'PS-apo': 0.9  # nm

    }
BOX = {
    'AS': [5, 6, 5], # nm^3
    'PS': [5, 8, 5], # nm^3
    'PS-apo': [5, 8, 5] # nm^3

}

# Ionic strength constants
A=0.519 # M^(-1/2)
B=0.331*10**(-8) # cm^(-1) * M*(-1/2)
Na = 6 * 10**23 # mol^(-1)


#################
SYSTEMS = {
    'AS':       ['MG_0.8', 'CA_0.8', 'CA_0.85'],
    'PS':       ['MG_0.8', 'CA_0.85'],
    'PS-apo':   ['MG_0.8', 'CA_0.85'],
}

# T_minmax = {
#     'AS': [1, 3], #us
#     'PS': [0.5, 2]
# }

colors = {
    'MG_0.8':'magenta',
    'CA_0.8': 'green',
    'CA_0.85': 'blue',
}

# CV = {
#     'AS': ['dp', 'cn'], 
#     'PS': ['d_489', 'd_580', 'cn']
# }