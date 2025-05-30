"""
.. module:: pymeteo.thermo
   :platform: Unix, Windows
   :synopsis: Thermodynamic routines

.. moduleauthor:: Casey Webster <casey.webster@gmail.com>

"""
#todo
# complete constants and function library

#constants
import numpy as np
from sounding.constants import p00, kappa_d, epsilon, T00, gravity

def T(theta,p):
    """Convert Potential Temperature :math:`\\theta` to Temperature
    
    :parameter theta: Potential temperature (K)
    :parameter p: Pressure (Pa)
    :returns: Temperature (K) 
    """
    return theta * (p00/p)**-kappa_d


def theta(T,p):
    return T * (p00/p)**kappa_d


def es(T):
    es = 6.122 * np.exp(17.67 * (T - 273.15) / (243.5 + (T - 273.15)))
    es[T==273.15] = 6.122
    return es # ----------> modificado   (05/05/2017)


def w_vs(T,pd):
    return epsilon * (es(T)/pd)


def theta_v(th, qv):
    return th * (1. + 0.61*qv)

def DewPoint(e):
    """ Use Bolton's (1980, MWR, p1047) formulae to find tdew.
    INPUTS:
    e (Pa) Water Vapor Pressure
    OUTPUTS:
    Td (C) 
      """

    ln_ratio=np.log(e/611.2)
    Td=((17.67-ln_ratio)*T00+243.5*ln_ratio)/(17.67-ln_ratio)
    return Td-T00

def MixR2VaporPress(qv,p):
    """Return Vapor Pressure given Mixing Ratio and Pressure
    INPUTS
    qv (kg kg^-1) Water vapor mixing ratio`
    p (Pa) Ambient pressure
          
    RETURNS
    e (Pa) Water vapor pressure
    """
    return qv*p/(epsilon+qv)

def TTK(TA, PA, TD):
    #Calculando indice K
    #T e TD[C]
    
    # Encontrando os indices
    ind1 = (PA-500.)**2
    ind500 = np.nonzero(ind1 == min(ind1))
    
    ind2 = (PA-700.)**2
    ind700 = np.nonzero(ind2 == min(ind2))

    ind3 = (PA-850.)**2
    ind850 = np.nonzero(ind3 == min(ind3))

    T500,P500,TD500 = TA[ind500], PA[ind500], TD[ind500]
    T700,P700,TD700 = TA[ind700], PA[ind700], TD[ind700]
    T850,P850,TD850 = TA[ind850], PA[ind850], TD[ind850]
    K = (T850 - T500) + TD850 - (T700 - TD700)
    tt= (T850 + TD850) - 2*T500
    return K, tt

def wh2o(PA,TA,TD):
    Pr = PA
    Ta = TA
    Td = TD

    # Calculando IWV [Kg m-2]
    tam = len(Ta)
    t1  = tam-1
    dp  = np.zeros(t1)
    dr  = np.zeros(t1)
    rdp = np.zeros(t1)
    ea  = 6.122*np.exp(17.67*Td/(243.5+Td))   # Pressao Parcial de Vapor
    r   = epsilon*ea/(Pr-ea)

    for j in range(t1):
        dp[j]  = (Pr[j] - Pr[j+1])*100
        dr[j]  = (r[j+1]+r[j])/2
        rdp[j] = dp[j]*dr[j]

    WH2O = np.sum(rdp)/gravity
    return WH2O

# ----------------------->>>>>>>>>>>>>>>>>>> MODIFICADO (05/05/2017)
def thetaes(p, T):
    cl = 4190.  # 'J K-1 kg-1', 'Spec heat liquid water'
    p0 = 1000.
    # compute saturation equivalent potential temperature thes [K]
    # given temperature T [K] and pressure p [mb]
    # Use Bohren+Albrecht (6.123), p.293
    esat = es(T)
    ws = epsilon * esat / (p - esat)

    """
    Latent heat of evaporation/condensation of water (vapor - liquid)
    valid from -40 to +40 C.
    Cubic fit to Table 2.1,p.16, Textbook: R.R.Rogers & M.K. Yau,
    A Short Course in Cloud Physics, 3e,(1989), Pergamon press
    http://en.wikipedia.org/wiki/Latent_heat  (2009-11-09)
    V 2009-11-09, (p) dietmar.thaler@gmx.at
    | T .. Temperature in C
    | l_evw .. Latent heat in J/kg as function of Temperature
    """
    lv = (
         -0.0000614342 * (T - 273.15) ** 3 + 0.00158927 * (T - 273.15) ** 2 - 2.36418 * (T - 273.15) + 2500.79) * 1000.0
    cp = cpd + ws * cl
    thes = T * ((p - esat) / p0) ** (-Rd / cp) * np.exp(lv * ws / cp / T)
    return thes

# ------------------------>>>>>>>>>>>>>>> MODIFICADO  (05/05/2017)
