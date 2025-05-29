from numpy import array,logspace,log,zeros,exp,trapz,\
        where,concatenate,nan,isnan,argsort,log10

from sounding.indices import theta as Theta
from sounding.indices import MixR2VaporPress, DewPoint
from sounding.constants import epsilon, Rd,  cpd, T00

# Local thermodynamics stuff, see thermodynamics.py
#from thermodynamics import VirtualTemp,Latentc,VaporPressure,MixRatio,GammaW,\
#    VirtualTempFromMixR,MixR2VaporPress,DewPoint,Theta,TempK,Density,DensHumid,\
#    ThetaE,ThetaV,barometric_equation_inv
#from thermodynamics import Rd, cpd, Epsilon,T00

#-----------------------------------------------------------------------
# Here we go. A set of functions that I use from time to time to calculate 
# the basic stuff that I'm sick of doing over and over! I'm going to 
# endeavour to include references and global constants to make it all nice 
# and legible.
#-----------------------------------------------------------------------


def get_cape(HG, PA, TA, TD ,startp,startt,startdp,totalcape):
    """Wrapper for the numerics of calculating CAPE.
                                                                       
    INPUTS:                                                            
    startp,startt,startdp: Definition of the parcel that we will base
                           the calculations on. This can be the output
                           of Sounding.get_parcel() or it can be a user-
                           defined parcel. 
    totalcape [=False]   : Flag defining method of identifying the so-
                           called "Equilibrium Level" (Reference).
                           If False  (default), use the first stable 
                           layer above the LFC, and ignore any CAPE in 
                           unstable layers above this. If True, use all
                           CAPE up to the highest equilibrium level.
                                                                      
    OUTPUTS:                                                           
    P_lcl                : The lifted condensation level (LCL)
    P_lfc                : The level of free convection (LFC). Can be
                           the same as the LCL, or can be NaN if there
                           are no unstable layers.
    P_el                 : The Equilibrium Level, used to determine the
                           CAPE. If totalcape=True, use the highest 
                           equilibrium level, otherwise use the first 
                           stable equilibrium level above the LFC.
    CAPE                 : CAPE calculated from virtual temperature
    CIN                  : CIN calculated from virtual temperature
                              
    HINT:                     
    parcel=S.get_parcel('mu') 
    lcl,lfc,el,cape,cin=get_cape(*parcel)
    """
    from numpy import interp
    #assert startt>=startdp,"Not a valid parcel. Check Td<Tc"

    # fundamental environmental variables
    pres=PA #self.soundingdata['pres']        # DPE
    temp=TA #self.soundingdata['temp']        # DPE

    # Get Sub-LCL traces
    presdry,tempdry,tempiso=dry_ascent(startp,startt,startdp,nsteps=101)

    # make lcl variables explicit
    P_lcl=presdry[-1]
    T_lcl=tempdry[-1]

    # Now lift a wet parcel from the intersection point
    # preswet=linspace(P_lcl,100,101)
    preswet,tempwet=moist_ascent(P_lcl,T_lcl,nsteps=101)

    # tparcel is the concatenation of tempdry and 
    # tempwet, and so on.
    tparcel=concatenate((tempdry,tempwet[1:]))
    pparcel=concatenate((presdry,preswet[1:]))
    dpparcel=concatenate((tempiso,tempwet[1:]))

    # Interpolating the environmental profile onto the 
    # parcel pressure coordinate
    # tempenv=interp(preswet,pres[::-1],temp[::-1])
    ## NEW, for total column:
    tempenv=interp(pparcel,pres[::-1],temp[::-1])

    # now soLe for the equlibrium levels above LCL
    # (all of them, including unstable ones)
    # eqlev,stab=soLe_eq(preswet[::-1],(tempwet-tempenv)[::-1])
    # NEW, for total column:
    # On second thought, we don't really want/need
    # any equilibrium levels below LCL
    # eqlev,stab=soLe_eq(pparcel[::-1],(tparcel-tempenv)[::-1])
    # This is equivalent to the old statement :
    indice,eqlev,stab=soLe_eq(pparcel[pparcel<=P_lcl][::-1],\
            (tparcel-tempenv)[pparcel<=P_lcl][::-1])

    if (indice == False):
      P_lcl = []
      P_lfc = []
      P_el  = []
      CAPE  = []
      CIN   = []
      result= 0 
      return P_lcl,P_lfc,P_el,CAPE,CIN,result
    else:

      # Sorting index by decreasing pressure
      I=argsort(eqlev)[::-1]
      eqlev=eqlev[I]; stab=stab[I]


      # temperatures at the equilibrium level
      # tempeq=interp(eqlev,preswet[::-1],tempenv[::-1])
      ## NEW, for total column:
      tempeq=interp(eqlev,pparcel[::-1],tparcel[::-1])

      # This helps with debugging
      # for ii,eq in enumerate(eqlev):
          # print "%5.2f  %5.2f  %2d"%(eq,tempeq[ii],stab[ii])

      # need environmental temperature at LCL
      tenv_lcl=interp(P_lcl,pparcel[::-1],tempenv[::-1])

      isstab=where(stab==1.,True,False)
      unstab=where(stab==1.,False,True)

      if eqlev.shape[0]==0:
          # no unstable layers in entire profile
          # because the parcel never crosses the tenv
          P_lfc=nan
          P_el=nan
      elif T_lcl>tenv_lcl:
          # check LCL to see if this is unstable
          P_lfc=P_lcl
          if totalcape is True:
              P_el=eqlev[isstab][-1]
          else:
              P_el=eqlev[isstab][0]
      elif eqlev.shape[0]>1:
          # Parcel is stable at LCL so LFC is the 
          # first unstable equilibrium level and 
          # "EQ" level is the first stable equilibrium 
          # level
          P_lfc=eqlev[unstab][0]
          if totalcape is True:
              P_el=eqlev[isstab][-1]
          else:
              P_el=eqlev[isstab][0]
      else:
          # catch a problem... if there is only
          # one eqlev and it's unstable (this is 
          # unphysical), then it could be a vertical
          # resolution thing. This is a kind of 
          # "null" option
          if isstab[0]:
              P_el=eqlev[isstab][0]
              P_lfc=nan
          else:
              P_lfc=nan
              P_el=nan

      if isnan(P_lfc):
          return P_lcl,P_lfc,P_el,0,0

      # need to handle case where dwpt is not available 
      # above a certain level for any reason. Most simplest 
      # thing to do is set it to a reasonably low value; 
      # this should be a conservative approach!
      dwpt=TD #self.soundingdata['dwpt'].copy().soften_mask()    #DPE
      # raise ValueError
      ###if dwpt[(pres>=P_el).data*(pres<P_lfc).data].mask.any():                               #DPE
      ###    print "WARNING: substituting -200C for masked values of DWPT in this sounding"     #DPE
      ###dwpt[dwpt.mask]=-200                                                                   #DPE
      # dwptenv=interp(preswet,pres[::-1],dwpt[::-1])                                           #DPE
      # NEW:
      dwptenv=interp(pparcel,pres[::-1],dwpt[::-1])

      hght=HG #self.soundingdata['hght']                         #DPE
      ###if hght[(pres>=P_el).data].mask.any():                                                #DPE
      ###    raise NotImplementedError,\                                                       #DPE
      ###            "TODO: Implement standard atmosphere to substitute missing heights"       #DPE
      # hghtenv=interp(preswet,pres[::-1],self.soundingdata['hght'][::-1])
      # NEW:
      hghtenv=interp(pparcel,pres[::-1],HG[::-1]) #self.soundingdata['hght'][::-1])            #DPE

      # Areas of POSITIVE Bouyancy
      cond1=(tparcel>=tempenv)*(pparcel<=P_lfc)*(pparcel>P_el)
      # Areas of NEGATIVE Bouyancy
      if totalcape is True:
#          cond2=(tparcel<tempenv)*(pparcel>P_el)     #DPE
          cond2=(tparcel<tempenv)*(pparcel>P_lfc)
      else:
          cond2=(tparcel<tempenv)*(pparcel>P_lfc)

    # Do CAPE calculation
    # 1. Virtual temperature of parcel... remember it's saturated above LCL.
    # e_parcel=VaporPressure(tempwet)
    # Tv_parcel=VirtualTemp(tempwet+T00,preswet*100.,e_parcel)
    # e_env=VaporPressure(dwptenv)
    # Tv_env=VirtualTemp(tempenv+T00,preswet*100.,e_env)
    # TODO: Implement CAPE calculation with virtual temperature
    # (This will affect the significant level calculations as well!!)
    # e_parcel=VaporPressure(dpparcel)
    # Tv_parcel=VirtualTemp(tparcel+T00,pparcel*100.,e_parcel)
    # e_env=VaporPressure(dwptenv)
    # Tv_env=VirtualTemp(tempenv+T00,pparcel*100.,e_env)
    # CAPE=trapz(9.81*(Tv_parcel[cond1]-Tv_env[cond1])/Tv_env[cond1],hghtenv[cond1])
    # CIN=trapz(9.81*(Tv_parcel[cond2]-Tv_env[cond2])/Tv_env[cond2],hghtenv[cond2])

      CAPE=trapz(9.81*(tparcel[cond1]-tempenv[cond1])/(tempenv[cond1] + 273.15),hghtenv[cond1])
      CIN=trapz(9.81*(tparcel[cond2]-tempenv[cond2])/(tempenv[cond2] + 273.15),hghtenv[cond2])
      
      if False:
         print("%3s  %7s  %7s  %7s  %7s  %7s  %7s  %7s  %7s"%\
                 ("IX", "PRES", "TPARCEL", "DPPARCE", "TENV",\
                 "DPENV", "TV PARC", "TV ENV", "HEIGHT"))
         for ix,c2 in enumerate(cond2):
             if c2:
                 print("%3d  %7.3f  %7.3f  %7.3f  %7.3f  %7.3f  %7.3f  %7.3f"+\
                         "  %7.3f"%(ix,pparcel[ix],tparcel[ix],dpparcel[ix],\
                         tempenv[ix],dwptenv[ix],Tv_parcel[ix],Tv_env[ix],hghtenv[ix]))

      result = 1
      return P_lcl,P_lfc,P_el,CAPE,CIN,result

def get_parcel(HG, PA,TA,TD,method):
    """Automatically generate a parcel based on the sounding characteristics
    INPUTS
    method ['mu']   : Parcel type. Choose from the following
                      Mixed Layer  : 'ml'
                      Surface Based: 'sb'
                      Most Unstable: 'mu'
    depth           : Both the mixed layer and the most unstable parcel 
                      require a threshold on the depth of the layer used 
                      to determine the parcel
    OUTPUTS
    (pres,temp,dwpt): The parcel characteristics 
    """

    if method=='most_unstable' or method=='mu':
        return most_unstable_parcel(HG, PA,TA,TD)
    elif method=='surface' or method=='sb':
        return surface_parcel(PA,TA,TD)
    if method=='mixed_layer' or method=='ml':
        return mixed_layer_parcel(PA,TA,TD)
    else:
        raise NotImplementedError

def surface_parcel(PA,TA,TD):
    """Return ACUTAL lowest parcel, handling frequent missing data from lowest levels"""
    pres= PA #self.soundingdata["pres"]                #DPE
    temp= TA #self.soundingdata["temp"]                #DPE
    #assert self.soundingdata.has_key('dwpt'), "Moisture needed for parcel calculation! Add DWPT" #DPE
    dwpt= TD #self.soundingdata["dwpt"]                #DPE

    ii=0                                             
    ###while True:                                      #DPE
    ###    if dwpt.mask[ii] or temp.mask[ii]:           #DPE
    ###        ii+=1                                    #DPE
    ###    else:                                        #DPE
    return pres[ii],temp[ii],dwpt[ii],'sb'

def most_unstable_parcel(HG, PA,TA,TD,depth=300):
    """Return a parcel representing conditions for the most unstable 
    level in the lowest <depth> hPa"""

    hlge=HG                                            #DPE
    pres=PA #self.soundingdata['pres']                 #DPE
    temp=TA #self.soundingdata['temp']                 #DPE
    dwpt=TD #self.soundingdata['dwpt']                 #DPE
#    thta=TH #self.soundingdata['thta']                #DPE

    cape=zeros(pres.shape)
    for ii in range((pres>pres[0]-depth).sum()):
        #if temp.mask[ii]:
        #    continue
        #if dwpt.mask[ii]:
        #    continue
        theparcel=pres[ii], temp[ii], dwpt[ii]
        calc=get_cape(HG, PA, TA, TD, theparcel[0], theparcel[1], theparcel[2],totalcape=True) #DPE
        thecape = calc[-3]

        if calc[-1] == 0:
#        except ValueError:
            # this is raised when get_cape fails to find
            # equilibrium levels, which happens when the 
            # parcel doesn't "completely" intersect the 
            # sounding profile.
            continue
        else:
            cape[ii]=thecape
        # print "%7.2f  %7.2f  %7.2f  %7.2f"%(pres[ii],temp[ii],dwpt[ii],thecape)

    if cape.max()==0.:
        return surface_parcel(PA,TA,TD)
      
    # choose max cape
    I=where(cape==cape.max())[0][0]

    # need to descend along adiabat!
    # convert parcel to equivalent surface parcel
    # thetheta=thta[I]
    # parceltemp=(temp[I]+T00)*(pres[0]/pres[I])**(Rd/cpd)-T00
    # the_e=VaporPressure(dwpt[I])
    # themixr=MixRatio(the_e,pres[I]*100)
    # parcele=MixR2VaporPress(themixr,pres[0]*100)
    # parceldwpt=DewPoint(parcele)
    # return pres[0],parceltemp,parceldwpt,'mu'

    # return conditions at the mu level.
        
    return pres[I],temp[I],dwpt[I],'mu'

def mixed_layer_parcel(PA,TA,TD,depth=100):
    """Returns parameters for a parcel initialised by:
    1. Surface pressure (i.e. pressure of lowest level)
    2. Surface temperature determined from mean(theta) of lowest <depth> mbar
    3. Dew point temperature representative of lowest <depth> mbar

    Inputs:
    depth (mbar): depth to average mixing ratio over
    """

    pres=PA #self.soundingdata["pres"]    #DPE
    temp=TA #self.soundingdata["temp"]    #DPE
    dwpt=TD #self.soundingdata["dwpt"]    #DPE

    pres0,temp0,dwpt0 = PA[0],TA[0],TD[0] #,null=self.surface_parcel() #DPE

    # identify the layers for averaging
    layers=pres>(pres0-depth)
        
    # average theta over mixheight to give
    # parcel temperature
    thta_mix=Theta(temp[layers]+T00,pres[layers]*100.).mean()
    temp_s=TempK(thta_mix,pres0*100)-T00

    # average mixing ratio over mixheight
    vpres=VaporPressure(dwpt)
    mixr=MixRatio(vpres,pres*100)
    mixr_mix=mixr[layers].mean()
    vpres_s=MixR2VaporPress(mixr_mix,pres0*100)

    # surface dew point temp
    dwpt_s=DewPoint(vpres_s)

    # print "----- Mixed Layer Parcel Characteristics -----"
    # print "Mixed layer depth                     : %5d mb "%depth
    # print "Mean mixed layer potential temperature: %5.1f K"%thta_mix
    # print "Mean mixed layer mixing ratio         : %5.2f g/kg"%(mixr_mix*1e3)

    return pres0,temp_s,dwpt_s,'ml'

    raise NotImplementedError

def dry_ascent(startp,startt,startdp,nsteps=101):
    from numpy import interp
    #--------------------------------------------------------------------
    # Lift a parcel dry adiabatically from startp to LCL.
    # Init temp is startt in C, Init dew point is stwrtdp,
    # pressure levels are in hPa    
    #--------------------------------------------------------------------

    #assert startdp<=startt

    if startdp==startt:
        return array([startp]),array([startt]),array([startdp]),

    # Pres=linspace(startp,600,nsteps)
    Pres=logspace(log10(startp),log10(600),nsteps)

    # Lift the dry parcel
    T_dry=(startt+T00)*(Pres/startp)**(Rd/cpd)-T00 

    # Mixing ratio isopleth
    starte=VaporPressure(startdp)
    startw=MixRatio(starte,startp*100)
    e=Pres*startw/(.622+startw)
    T_iso=243.5/(17.67/log(e/6.112)-1)

    # SoLe for the intersection of these lines (LCL).
    # interp requires the x argument (argument 2)
    # to be ascending in order!
    P_lcl=interp(0,T_iso-T_dry,Pres)
    T_lcl=interp(P_lcl,Pres[::-1],T_dry[::-1])

    # presdry=linspace(startp,P_lcl)
    presdry=logspace(log10(startp),log10(P_lcl),nsteps)

    tempdry=interp(presdry,Pres[::-1],T_dry[::-1])
    tempiso=interp(presdry,Pres[::-1],T_iso[::-1])


    return presdry,tempdry,tempiso

def moist_ascent(startp,startt,ptop=10,nsteps=501):
    #--------------------------------------------------------------------
    # Lift a parcel moist adiabatically from startp to endp.
    # Init temp is startt in C, pressure levels are in hPa    
    #--------------------------------------------------------------------
    
    # preswet=linspace(startp,ptop,nsteps)
    preswet=logspace(log10(startp),log10(ptop),nsteps)
    temp=startt
    tempwet=zeros(preswet.shape);tempwet[0]=startt
    for ii in range(preswet.shape[0]-1):
        delp=preswet[ii]-preswet[ii+1]
        temp=temp+100*delp*GammaW(temp+T00,(preswet[ii]-delp/2)*100)
        tempwet[ii+1]=temp

    return preswet,tempwet

def soLe_eq(preswet,func):
    """SoLe the peicewise-linear stability of a parcel

    INPUTS: variables from the most ascent of a parcel
    preswet: pressure
    func   : piecewise linear function to soLe (tw-te)

    OUTPUTS:
    solutions: zeros of the function (tw-te)
    stability: indication of the stability of this solution.

    NOTE ABOUT STABILITY
    Stability is the sign of (d(func)/dP). So if you have used tw-te
    like you were supposed to, d(tw-te)/dP>0 means this is a stbale 
    equilibrium level (flip the sign to envision d(tw-te)/dz).
    """

    from numpy import sign,diff

    # Sorry to be annoying but I'm going to force you to use
    # a monotonically increasing variable
    #assert (sign(diff(preswet))==1).all(), "Use a monotonically increasing abscissa" #DPE
    aaa=(sign(diff(preswet))==1).all()
    if aaa == True:      #DPE
      # Identify changes in sign of function
      dsign=sign(func)
      isdiff=zeros(dsign.shape,dtype=bool)
      isdiff[1:]=abs(diff(dsign)).astype(bool)

      # shift to get the value on the other side
      # of the x-axis
      shift=zeros(dsign.shape,dtype=bool)
      shift[:-1]=isdiff[1:]; shift[-1]=isdiff[0]

      # soLe by linear interpolation between 
      # values points
      sols=zeros((isdiff.sum()))
      stab=zeros((isdiff.sum()))
      for ii in range(isdiff.sum()):
          f0=func[isdiff][ii]
          f1=func[shift][ii]
          p0=preswet[isdiff][ii]
          p1=preswet[shift][ii]
          slope=(f1-f0)/(p1-p0)
          sols[ii]=p0-f0/slope
          stab[ii]=sign(slope)

      ### Debug with plots
      # fig=figure()
      # ax=fig.add_subplot(111)
      # ax.plot(preswet,func)
      # ax.plot(sols,zeros(sols.shape),ls='',marker='o')
      # ax.plot(preswet[isdiff],func[isdiff],ls='',marker='+',mew=2)
      # ax.plot(preswet[shift],func[shift],ls='',marker='x',mew=2)
      # ax.grid(True)
      # show()
      indice = True
      return indice,sols,stab
    else:
      indice = False
      sols   = -1
      stab   = -1
      return indice,sols,stab

def TempK(theta,pres,pref=100000.):
    """Inverts Theta function."""

    try:
        minpres=min(pres)
    except TypeError:
        minpres=pres

    if minpres<2000:
        print("WARNING: P<2000 Pa; did you input a value in hPa?")

    return theta*(pres/pref)**(Rd/cpd)

def VaporPressure(tempc,phase="liquid"):
    """Water vapor pressure over liquid water or ice.

    INPUTS: 
    tempc: (C) OR dwpt (C), if SATURATION vapour pressure is desired.
    phase: ['liquid'],'ice'. If 'liquid', do simple dew point. If 'ice',
    return saturation vapour pressure as follows:

    Tc>=0: es = es_liquid
    Tc <0: es = es_ice

   
    RETURNS: e_sat  (Pa)
    
    SOURCE: http://cires.colorado.edu/~voemel/vp.html (#2:
    CIMO guide (WMO 2008), modified to return values in Pa)
    
    This formulation is chosen because of its appealing simplicity, 
    but it performs very well with respect to the reference forms
    at temperatures above -40 C. At some point I'll implement Goff-Gratch
    (from the same resource).
    """

    over_liquid=6.112*exp(17.67*tempc/(tempc+243.12))*100.
    over_ice=6.112*exp(22.46*tempc/(tempc+272.62))*100.
    # return where(tempc<0,over_ice,over_liquid)

    if phase=="liquid":
        # return 6.112*exp(17.67*tempc/(tempc+243.12))*100.
        return over_liquid
    elif phase=="ice":
        # return 6.112*exp(22.46*tempc/(tempc+272.62))*100.
        return where(tempc<0,over_ice,over_liquid)
    else:
        raise NotImplementedError

def MixRatio(e,p):
    """Mixing ratio of water vapour
    INPUTS
    e (Pa) Water vapor pressure
    p (Pa) Ambient pressure
          
    RETURNS
    qv (kg kg^-1) Water vapor mixing ratio`
    """

    return epsilon*e/(p-e)

def GammaW(tempk,pres):
    """Function to calculate the moist adiabatic lapse rate (deg C/Pa) based
    on the environmental temperature and pressure.

    INPUTS:
    tempk (K)
    pres (Pa)
    RH (%)

    RETURNS:
    GammaW: The moist adiabatic lapse rate (Deg C/Pa)
    REFERENCE: 
    http://glossary.ametsoc.org/wiki/Moist-adiabatic_lapse_rate
    (Note that I multiply by 1/(gravity*rho) to give MALR in deg/Pa)

    """

    tempc=tempk-T00
    es=VaporPressure(tempc)
    ws=MixRatio(es,pres)

    # tempv=VirtualTempFromMixR(tempk,ws)
    tempv=VirtualTemp(tempk,pres,es)
    latent=Latentc(tempc)

    Rho=pres/(Rd*tempv)

    # This is the previous implementation:
    # A=1.0+latent*ws/(Rd*tempk)
    # B=1.0+Epsilon*latent*latent*ws/(cpd*Rd*tempk*tempk)
    # Gamma=(A/B)/(cpd*Rho)

    # This is algebraically identical but a little clearer:
    A=-1.*(1.0+latent*ws/(Rd*tempk))
    B=Rho*(cpd+epsilon*latent*latent*ws/(Rd*tempk*tempk))
    Gamma=A/B

    return Gamma

def VirtualTemp(tempk,pres,e):
    """Virtual Temperature

    INPUTS:
    tempk: Temperature (K)
    e: vapour pressure (Pa)
    p: static pressure (Pa)

    OUTPUTS:
    tempv: Virtual temperature (K)

    SOURCE: hmmmm (Wikipedia)."""
    #rm=0.622*e/pres
    #tempvk = tempk*(1. + 0.61*rm)
    tempvk=tempk/(1-(e/pres)*(1-epsilon))
    return tempvk

def Latentc(tempc):
    """Latent heat of condensation (vapourisation)

    INPUTS:
    tempc (C)

    OUTPUTS:
    L_w (J/kg)

    SOURCE:
    http://en.wikipedia.org/wiki/Latent_heat#Latent_heat_for_condensation_of_water
    """
   
    return 1000*(2500.8 - 2.36*tempc + 0.0016*tempc**2 - 0.00006*tempc**3)
