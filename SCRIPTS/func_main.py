import numpy as np
from SCRIPTS.constants import *


def _dG_I_calc(SF, BOX):
    Zcat=2 * SF
    Zace=-1 * SF
    Zcl=-1 * SF
    V=BOX[0]*BOX[1]*BOX[2] * 10**(-24) #L

    C = 1/(V * Na) #M
    I = 1/2 * C * (Zcat**2 + Zace**2 + Zcl**2)

    loggamma_cat = -A * Zcat**2 * np.sqrt(I)
    loggamma_ace = -A * Zace**2 * np.sqrt(I)
    loggamma_catace = -A * (Zcat+Zace)**2 * np.sqrt(I)
    
    dG_I = kBT * (loggamma_cat+loggamma_ace-loggamma_catace)
    
    return dG_I

def dG_calc(L, PMF, 
            SYSTEM #'AS/MG_0.8'
            ):
    
    SF = float(SYSTEM.split('_')[1])
    SYS = SYSTEM.split('/')[0] 
    
    is_bulk=np.int_((L>L_BULK_MIN) & (L<L_BULK_MAX))    
    is_bond=np.int_(L<L_BOND_MAX)
    dx = L[2]-L[1]
    L_u = L_BULK_MAX-L_BULK_MIN
    S_u = np.pi*R_CYL[SYS]**2 + 2*np.pi*R_CYL[SYS]*np.sqrt(np.pi*kBT/(2*K_RES)) + 2*np.pi*kBT/K_RES
    
    dG_PMF = kBT * np.log((np.nansum(np.exp(-PMF/kBT)*is_bulk)*dx) / np.nansum(np.exp(-PMF/kBT)*is_bond*dx))
    dG_R = -kBT * np.log(L_u * S_u / V0)
    
    dG_I = _dG_I_calc(SF, BOX[SYS])
    
    dG0 = dG_PMF + dG_R + dG_I
    
    return (dG_PMF, dG_R, dG_I, dG0)

