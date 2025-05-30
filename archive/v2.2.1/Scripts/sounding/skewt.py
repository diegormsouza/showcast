"""
Utilities for reading, analyzing, and visualizing idealized or observed
atmospheric profiles/soundings. 

Adapated from the `pywrfplotutils` package by Geiur Arne Waagbm, 
http://code.google.com/p/pywrfplot

Author: Daniel Rothenberg (darothen@mit.edu)

"""

import math
import numpy as np
import pandas as pd
from scipy.interpolate import interp1d

import matplotlib.pyplot as plt
from sounding.constants import *

## Thermodynamic constants
R = Rd
eps = epsilon
fontscalefactor = 1

def plot_skewt(sounding, ax=None, figsize=(8,8),
    lift_parcel=False, plot_winds=False, diags=[], draw_ytick=True,
    **kwargs):
    """ Plot a Skew-T/Log-P diagram generated from a given sounding, and 
    perform any additional analytical/diagnostic calculations specified.

    This basic routine was adopted from the pywrfplot utility, particularly
    the implementation of skewed axes. Additional diagnostic calculations 
    have been added later.

    Parameters
    ----------
    sounding : pd.DataFrame 
        Environmental sounding data with the following columns:
        - *temperature* : environmental temperature in degrees C
        - *pressure* : environmental pressure in hPa
        - *dewpoint* : environmental dewpoint in degrees C

        **Necessary for ``lift_parcel == True``**
        - *height* : measurement altitude in meters
        - *mixing_ratio* : environmental water vapor mixing ratio in g/kg
        **Necessary for ``plot_winds == True``**
        - *us*, *vs* : zonal and meridional winds, knots *or*
        - *sknt*, *direction* : wind absolute speed, knots, and direction, degrees
    ax : axis
        If present, will draw the plot on the user-given axis
    figsize : tuple
        If present, will force the plot figure size
    lift_parcel : Boolean
        Perform a lifted-parcel calculation from the surface to plot on the
        diagram
    plot_winds : Boolean
        Plot wind barbs with height on the diagram
    diags : list
        Optional diagnostics to calculate for the sounding. Possible values
        include - [, ]

    Returns
    -------
    axis on which the diagram was plotted

    """

    def _choose_kwargs(key, default):
        if key in kwargs:
            return kwargs[key]
        else:
            return default

    skewness = _choose_kwargs("skewness", 37.5)
    P_b = _choose_kwargs("P_b", 105000.)  # Bottom pressure, Pa
    P_t = _choose_kwargs("P_t", 10000.)  # Top pressure, Pa
    dp = _choose_kwargs("dp", 50.)  # Pressure increment, Pa
    T_left = _choose_kwargs("T_left", -40.)
    T_right = _choose_kwargs("T_right", 50.)
    label_altitudes = _choose_kwargs("label_altitudes", False)
    title = _choose_kwargs("title", None)

    plevs = np.arange(P_b, P_t-1, -dp)

    ## Start making figure
    if ax is None:
        fig = plt.figure(figsize=figsize)
        ax = fig.add_subplot(111)
    ax.grid(None, which='both', axis='both', alpha=0.)

    def _skewnessTerm(P):
        return skewness * np.log(P_bot / P)

    def _isotherms():
        for temp in np.arange(-140, 50, 10):
            ax.semilogy(temp + _skewnessTerm(plevs), plevs, basey=math.e, \
                        color=('blue' if temp <= 0 else 'red'), \
                        linestyle=('solid' if temp == 0 else 'dashed'), linewidth=.5)

    def _isobars():
        for n in np.arange(P_bot, P_t - 1, -10 ** 4):
            ax.plot([-40, 50], [n, n], color='black', linewidth=.5)

    def _dry_adiabats():
        for tk in T00 + np.arange(-30, 210, 10):
            dry_adiabat = tk * (plevs / P_bot) ** kappa - T00 + _skewnessTerm(plevs)
            ax.semilogy(dry_adiabat, plevs, basey=math.e, color='brown', \
                        linestyle='dashed', linewidth=.5)

    def _moist_adiabats():
        ps = [p for p in plevs if p <= P_bot]
        for temp in np.concatenate((np.arange(-40., 10.1, 5.), np.arange(12.5, 45.1, 2.5))):
            moist_adiabat = []
            for p in ps:
                temp -= dp * gamma_s(temp, p)
                moist_adiabat.append(temp + _skewnessTerm(p))
            ax.semilogy(moist_adiabat, ps, basey=math.e, color='green', \
                        linestyle='dotted', linewidth=.5)

    def _mix_rats():
        ## Following SkewT (https://github.com/tchubb/SkewT/blob/master/skewt/SkewT.py)
        rs = np.array([0.0001, 0.0004, 0.001, 0.002, 0.004, 0.007, 0.01, 0.016, 0.24, 0.032])
        plevs_trunc = plevs[plevs >= 70000.]

        e = np.array([plevs_trunc * r / (0.622 + r) for r in rs])
        t = 243.5 / (17.67 / np.log(e / 611.2) - 1.)

        for tt, mr in zip(t, rs):
            ax.semilogy(tt + _skewnessTerm(plevs_trunc), plevs_trunc, basey=math.e, \
                        color="green", linestyle="dashed", lw=1.)
            if (tt[0] > T_left) and (tt[-1] < T_right):
                if mr * 1e3 < 1:
                    fmt = "%4.1f"
                else:
                    fmt = "%d"
                ax.text(tt[10] + 2. + _skewnessTerm(plevs_trunc[10]), plevs_trunc[10],
                        fmt % (mr * 1e3),
                        color="green", fontsize=8, ha="center", va="bottom")

    def _temperature(temperature, pressure):
        linestyle = _choose_kwargs("T_style", "-")
        color = _choose_kwargs("T_color", "black")
        s = linestyle + "k"  # note that color will always be overridden
        ax.semilogy(temperature + _skewnessTerm(pressure), pressure, s, basey=math.e, color=color, \
                    linestyle='solid', linewidth=2.)

    def _dewpoint(dewpoints, pressure):
        linestyle = _choose_kwargs("Td_style", "-")
        color = _choose_kwargs("Td_color", "blue")
        s = linestyle + "k"  # note that color will always be overridden
        ax.semilogy(dewpoints + _skewnessTerm(pressure), pressure, s, basey=math.e, color=color, \
                    linestyle='solid', linewidth=2.)

    _isotherms()
    _isobars()
    _dry_adiabats()
    _moist_adiabats()
    _mix_rats()

    pressure = sounding['pressure']*100. # hPa -> Pa  #DPE
    height = sounding['height'] # m                   #DPE
    temperature = sounding['temperature'] # C         #DPE
    dewpoint = sounding['dewpoint']                   #DPE

    _temperature(temperature, pressure)
    _dewpoint(dewpoint, pressure)

    if plot_winds:
        barb_color = _choose_kwargs("barb_color", 'k')
        T_location = _choose_kwargs("barb_loc", 45.)

        #        if (("us" in sounding) and ("vs" in sounding)):            #DPE
        #            us, vs = sounding['us'].values, sounding['vs'].values  #DPE
        #        elif (("sknt" in sounding) and ("direction" in sounding)): #DPE
        ## Calculate zonal/meridional wind vectors
        model_dir = sounding.direction  # DPE
        model_wspd = sounding.sknt  # DPE

        dirs = np.pi * (model_dir + 180.) / 180. # in radians
        us = model_wspd * np.sin(dirs) * 1.9434
        vs = model_wspd * np.cos(dirs) * 1.9434

        wind_ax = ax.twinx()
        wind_ax.grid(None)
        for spine in wind_ax.spines.values():
            spine.set_visible(False)
        wind_ax.xaxis.set_visible(False)
        wind_ax.yaxis.set_visible(False)

        wind_ax.barbs(np.ones_like(us)[::2] * T_location, pressure[::2], us[::2], vs[::2],
                      length=6, barbcolor=barb_color)

        wind_ax.get_shared_y_axes().join(ax, wind_ax)
        wind_ax.semilogy()

    if lift_parcel:
        first_index = _choose_kwargs("first_index", 1)
        parcel_sounding = compute_lifted_parcel(sounding, first_index)
        misc = parcel_sounding.misc
        color = _choose_kwargs("parcel_color", "red")

        p_pressure, p_temperature = parcel_sounding['pressure'] * 100., parcel_sounding['temperature']
        ax.semilogy(p_temperature + _skewnessTerm(p_pressure), p_pressure, basey=math.e, color=color,
                    linestyle='dashed', linewidth=1.5)

        parcel_sounding_iso = parcel_sounding.dropna()
        p_pres_iso, p_temp_iso = parcel_sounding_iso['pressure'] * 100., parcel_sounding_iso['t_rsfc_iso']
        ax.semilogy(p_temp_iso + _skewnessTerm(p_pres_iso), p_pres_iso, basey=math.e, color=color,
                    linestyle='dashed', linewidth=1.5)

        ax.plot(misc['T_lcl'] + _skewnessTerm(misc['P_lcl'] * 100.), misc['P_lcl'] * 100.,
                color=color, marker='o', ms=4, zorder=-1)

        ## Perform additional diagnostics and print output
        #print "sounding diagnostics"                                                 #DPE
        #print "--"*35                                                                #DPE
        #fmt = "    {key:s} {val:6.1f}"                                               #DPE

        misc = parcel_sounding.misc
        #print fmt.format(key="LCLT", val=misc["T_lcl"])                             #DPE
        #print fmt.format(key="LCLP", val=misc["P_lcl"])                             #DPE
        
        #if "CAPE" in diags:                                                         #DPE
            #parcel_sounding = compute_CAPE(sounding, parcel_sounding)               #DPE
        #    print fmt.format(key="CAPV", val=sounding.misc["CAPV"][0])              #DPE
        #    print fmt.format(key="EQTV", val=1000)                                  #DPE
        #    print fmt.format(key="LFCV", val=1000)                                  #DPE


    #axis([40, 50, P_b, P_t])
    ax.set_xlim(T_left, T_right)
    ax.set_ylim(P_b, P_t)

    ax.set_xlabel('Temperature ($^{\circ}$C)', fontsize=10, color='k')
    xtick = np.arange(-40, 51, 5)
    ax.set_xticks(xtick)
    ax.set_xticklabels(['' if tick % 10 != 0 else str(tick) for tick in xtick])

    if draw_ytick:
        ax.set_ylabel('Pressure (hPa)', fontsize=10, color='k')
        ytick = np.arange(P_bot, P_t - 1, -10 ** 4)
        ax.set_yticks(ytick)
        ax.set_yticklabels(["%4d" % tick for tick in ytick / 100.])
    else:
        ax.set_yticklabels([])

    ## Label pressure altitudes
    if label_altitudes:
        p_subset = pressure[::6]
        z_subset = height[::6]
        for p, z in zip(p_subset, z_subset):
            if p < P_t: continue
            ax.text(T_left + 0.5, p,
                    "{:>6.1f} m".format(z), fontsize=8, ha="left", va="center")

    ## Add title
    if title:
        plt.title(title, fontweight='bold', loc="left", fontsize=12)

    if lift_parcel:
        return ax, parcel_sounding
    else:
        return ax


def compute_lifted_parcel(sounding, height_cutoff=10000.0, first_index=1):
    """ Lift a parcel from a surface with respect to a given sounding

    Parameters
    ----------
    sounding : pd.DataFrame
        The environmmental profile, conforming to the requirements in ``plot_skewt``
    height_cutoff : float
        Altitude at which to stop lifting the parcel
    first_index : int
        Index of the level from which valid data begins; the user might need to specify this

    Returns
    -------
    A new pd.DataFrame with the profile of the lifted parcel ascent with respect to
    height, pressure, temperature, and virtual temperature

    """
    height_cutoff = 1e5
    dp = 1.  # hPa

    trunc_sounding = sounding[sounding['height'] < height_cutoff].dropna()
    p_interp = interp1d(trunc_sounding.height, trunc_sounding.pressure, 'slinear')
    first = trunc_sounding.index[first_index]

    ## 1) Compute the surface dry adiabat and lift it all the way to the
    ##    top of the sounding. We'll use it to find the LCL and then replace
    ##    everything above it with the appropriate moist adiabat. 
    #print(dir(trunc_sounding[["temperature", "pressure", "mixing_ratio"]]))
    t0, p0, r0 = trunc_sounding[["temperature", "pressure", "mixing_ratio"]].loc[first]
    # print "Lifting parcel from T=%3.1f C, P=%4d hPa, Qv=%2.1f g/kg" % (t0, p0, r0)           #DPE
    p_all = trunc_sounding.pressure.values
    p_dry = np.arange(p_all[0], p_all[-1], -dp)

    # dry adiabat
    theta0 = (t0 + 273.15) * ((1e3 / p0) ** (Rd / cp))  # Kelvin
    ts_from_theta0 = theta0 * (p_all / 1e3) ** (Rd / cp) - 273.15  # deg C
    ts_theta0_interp = interp1d(p_all[::-1], ts_from_theta0[::-1], 'slinear')
    T_dry_adiabat = ts_theta0_interp(p_dry)

    # sfc mixing ratio isopleth
    r0 *= 1e-3
    e = (p_dry * 100.) * r0 / (0.622 + r0)
    ts_from_r0 = 243.5 / (17.67 / np.log(e / 611.2) - 1.)
    T_r_isopleth = ts_from_r0
    # print r0, ts_from_r0[0], e[0]

    # compute where the two sfc temperature curves intersect
    P_lcl = np.interp(0., T_r_isopleth - T_dry_adiabat, p_dry)
    T_lcl = np.interp(P_lcl, p_dry[::-1], T_dry_adiabat[::-1])

    ## 2) Lift the parcel adiabatically from the LCL pressure level
    p_moist = np.arange(P_lcl, 100., -dp)
    T_moist_adiabat = np.zeros_like(p_moist)
    T_moist_adiabat[0] = T_lcl
    for i in range(1, len(T_moist_adiabat)):
        dp_layer = p_moist[i] - p_moist[i - 1]
        dt_dp = gamma_s(T_moist_adiabat[i - 1], 100. * (p_moist[i - 1] + p_moist[i]) / 2.)
        T_moist_adiabat[i] = T_moist_adiabat[i - 1] + 100. * dt_dp * dp_layer

    ## 3) Setup output

    # shrink down the dry-lifting arrays to only go up to the LCL
    T_dry_adiabat = T_dry_adiabat[p_dry > P_lcl]
    T_r_isopleth = T_r_isopleth[p_dry > P_lcl]
    p_dry = p_dry[p_dry > P_lcl]

    p_combined = np.concatenate((p_dry, p_moist))
    t_combined = np.concatenate((T_dry_adiabat, T_moist_adiabat))
    t_iso = np.empty(t_combined.shape)
    t_iso[p_combined <= P_lcl] = np.nan
    t_iso[p_combined > P_lcl] = T_r_isopleth

    output = pd.DataFrame({'pressure': p_combined, 'temperature': t_combined,
                           't_rsfc_iso': t_iso,})
    output.misc = {'T_lcl': T_lcl, 'P_lcl': P_lcl,}

    return output


def gamma_s(T, p):
    """ Calculates the moist adiabatic lapse rate at a given temperature
    and pressure, using Rogers and Yau, Formula 3.16

    .. note:: although typically given as :math:`\frac{dT}{dz}`, here we have
        used the dry adiabatic lapse rate and the hydrostatic equation to 
        compute instead :math:`\frac{dT}{dP}` 

    Parameters
    ----------
    T : temperature in degrees C
    P : pressure in Pa

    Returns
    -------
    moist adiabatic lapse rate, in deg C / Pa

    """
    a = 2. / 7.
    b = eps * L * L / (R * cp)
    c = a * L / R

    esat = calc_es(T)
    wsat = eps * esat / (p - esat)  # Rogers and Yau 2.18
    numer = a * (T + T00) + c * wsat
    denom = p * (1. + b * wsat / ((T + T00) ** 2))

    return numer / denom  # Rogers and Yau 3.16


def calc_es(T):
    """ Calculate the equilibrium saturation vapor pressure for a parcel of
    air with given temperature, following Rogers and Yau, Formula 2.17

    Parameters
    ----------
    T : temperature in degrees C

    Returns
    -------
    equilibrium saturation vapor pressure in Pa 

    """
    arg = 17.67*T/(T + 243.5)
    return 611.2*np.exp(arg)

