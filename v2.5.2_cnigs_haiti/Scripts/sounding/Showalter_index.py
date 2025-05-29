#######################################################################################################
# LICENSE
# Copyright (C) 2020 - INPE - NATIONAL INSTITUTE FOR SPACE RESEARCH - BRAZIL
# This program is free software: you can redistribute it and/or modify it under the terms of the GNU
# General Public License as published by the Free Software Foundation, either version 3 of the License,
# or (at your option) any later version.
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without
# even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General
# Public License for more details.
# You should have received a copy of the GNU General Public License along with this program.
# If not, see http://www.gnu.org/licenses/.
#######################################################################################################
__author__ = 'Diego Enore'
__email__  = 'diego.enore@inpe.br'

import numpy as np
import sys  
Tice = 273.15

def showalter_index_bolton1(t_lower,t_upper,td_lower,p_lower=850.0,p_upper=500.0):
    """
    Showalter index [C] as a function of pressure, temperature and
    dewpoint at the lower level and pressure and temperature at
    the upper level. Calculation is done  according to Bolton(1980):
    "The Computation of Eqivalent Potential Temperature"  (MWR Vol.108).  
    Terminates with an error message when there is no
    convergence within 100 iterations.
 
    | t_lower   ... temperature at p_lower in C
    | t_upper   ... temperature at p_upper in C
    | td_lower  ... dewpoint temperature at p_lower in C
    | p_lower   ... pressure at the lower level in hPa
    | p_upper   ... pressure at the upper level in hPa    
    | showalter_index_bolton1 ... Showalter Index (SWI) in C

    SWI = Temp at the upper level - Showalter temperature for the upper level"""

    t_lift = t_lifting_condensation_level_bolton1(t_lower+Tice,td_lower+Tice)
    ew_lower = e_water(td_lower)
    mw_lower = m_mixingratio(ew_lower, p_lower)
    th_e = e_pot_temp_bolton(t_lower+Tice, t_lift, p_lower, mw_lower)
    t_swi_1guess = t_upper 
    t_swi = showalter_temperature_bolton1(th_e,p_upper,t_swi_1guess)
    return t_upper - t_swi


######################### NAO CHAMA NINGUEM #################################
def e_water(t=0.0):
    """
    Saturation water vapor over a plane liqid water surface
    (according http://cires.colorado.edu/~voemel/vp.html
    or http://cires.colorado.edu/~voemel/vp.html
    Guide to Meteorological Instruments and Methods of Observation,
    CIMO Guide, WMO 2008)

    | t ... temperature t in C
    | e_water ... sat. water vapor in hPa

    """
    E0=6.112 # hPa
    E=E0*np.exp(17.62*t/(243.12+t))
    return E

def m_mixingratio(e,p):
    """
    mixing ratio as function of water-vapor pressure and air pressure

    | e   ... vapor pressur
    | p   ... air pressure
    | m_mixingratio ...   mixing ratio in kg/kg
    """
    m = 0.622 * e/(p-e)  # Bolton (1980)
    return m

def t_lifting_condensation_level_bolton1(Tk,Td):
    """
    Lifting condensation according to Bolton(1980):
    "The Computation of Eqivalent Potential Temperature" (MWR Vol.108)
 
    | Tk ... Temp in the starting level of ascend in K
    | Td ... Dewpoint Temp. in the starting in the starting level of ascend in K
    | p ... pressure in hPa
    | m ... mixing ration in kg/kg (!)
    | t_lifting_condensation_level_bolton1 ... lift. condens.level in K"""

    return (1/(1/(Td-56.0) + np.log(Tk/Td)/800)) + 56.0

def e_pot_temp_bolton(Tk,Tl,p,m):
    """
    Equivalent potential temperature K after Bolton(1980):
    The Computation of Eqivalent Potential Temperature (MWR Vol.108)

    | Tk ... Temp in the starting level of ascend in K
    | Tl ... Temp. in the lifting condensation level in K
    | p ... pressure in hPa
    | m ... mixing ration in kg/kg (!)
    | e_pot_temp_bolton ... equivalent potential temp. in K"""

    mg = m*1000.0
    A = Tk * (1000.0/p)**(0.2854*(1-0.00028*mg))
    B = np.exp((3.376/Tl - 0.00254)*(mg*(1+0.00081*mg)))
    return A*B

def showalter_temperature_bolton1(ThetaE,p,tswi):
    """
    Showalter temperature [C] as a function of the eqivalent-potential
    temperature according to Bolton(1980): "The Computation of Eqivalent 
    Potential Temperature"  (MWR Vol.108) and pressure.  
    Terminates with an error message when there is no
    convergence within 100 iterations.
 
    | ThetaE ... equivalent (pseudo-) potential temp. 
    | p ... pressure in hPa
    | tswi ... start value for the Showalter temperature as 0th-approximation [C]
    | showalter_temperature_bolton1 ... Showalter temperature [C]"""

    THETA_EPSILON = 1e-5
    NMAX_ITER = 100
    n = 0
    while n < NMAX_ITER:
        e = e_water(tswi)
        m = m_mixingratio(e,p)
        th_eb = e_pot_temp_bolton(tswi+Tice, tswi+Tice, p, m)
        dtheta = ThetaE - th_eb
        #print "%6.0f %6.1f %6.1f %7.3f" % (p,ThetaE,th_eb,tswi)
        tswi =  tswi + dtheta/2.0
        if abs(dtheta) < THETA_EPSILON:
            return tswi
        n = n+1
    print("\nERROR in function <showalter_temperature_Bolton1>:")
    print("No convergence after %d iterations." % NMAX_ITER)
    print("Try a better first guess for the SWI-temperature\n")
    sys.exit(1)
