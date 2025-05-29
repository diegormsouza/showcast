"""This module provides constants used in the rest of the package

"""
# some constants

missingval = -99999999.
m2km = 0.001
km2m = 1000.
gravity = 9.81
maxparcels = 99999
L = 2.501e6    # latent heat of vaporization
Rd = 287.04         # gas constant dry air
Rv = 461.5              # gas constant water vapor
epsilon = Rd/Rv
cp = 1005.7              # what about cpd vs cpv
cpd = 1005.7             # what about cpd vs cpv
cpv = 1875.0
cpl = 4190.0
cpi = 2118.636
cv = 718.
g = gravity
p00 = 100000.   # reference pressure
T00 = 273.15
xlv = L
xls = 2836017.0
P_top, P_bot = 1e4, 1e5 # Top/bottom pressure levels, Pa
T_base = 300.0
gamma_d = 9.8 # dry adiabatic lapse rate, C/km
Cv_v=1410.            # Specific heat at constant volume for water vapour
Cp_lw=4218	      # Specific heat at constant pressure for liquid water
rho_w=1000.           # Liquid Water density kg m^{-3}
boltzmann=5.67e-8     # Stefan-Boltzmann constant
mv=18.0153e-3         # Mean molar mass of water vapor(kg/mol)
m_a=28.9644e-3        # Mean molar mass of air(kg/mol)
Rstar_a=8.31432       # Universal gas constant for air (N m /(mol K))
Pb=1013.25
Tb=288.15
Lb=-.0065
M=0.0289644

# Derivced values

lv1 = xlv+(cpl-cpv)*T00
lv2 = cpl - cpv
ls1 = xls+(cpi-cpv)*T00
ls2 = cpi - cpv

kappa = (cp-cv)/cp
kappa_d = Rd/cp
rp00 = 1./p00
reps = Rv/Rd
eps = epsilon
rddcp = kappa_d
cpdrd = cp/Rd
cpdg = cp/g

converge = 0.0002

