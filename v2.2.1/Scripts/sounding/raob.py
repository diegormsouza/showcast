#! /usr/bin/env python
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
__author__ = 'Diego Enore; Aurelienne Jorge'
__email__  = 'diego.enore@inpe.br; aurelienne.jorge@inpe.br'

# Bibliotecas padrao
import os
import sys
import configparser
import time

import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.cbook import get_sample_data

# Importa funcoes termodinamicas e indices
from constants import *
import dynamics as dyn
import Showalter_index as si
import skewt, cape, indices

# Recebe argumentos
pscript = sys.argv[1:]
CONF_FILE = pscript[0]                      # Arquivo de configuração
FILEIN = pscript[1]

# Leitura do arquivo de configurações
config = configparser.ConfigParser()
config.read(CONF_FILE)

# Definição dos diretórios
DIRINP = config.get('PATH', 'DIRINP')    # Define diretorio com arquivos de entrada
DIROUT = config.get('PATH', 'DIROUT')    # Define diretorio de saida
DIRLOG = config.get('PATH', 'DIRLOG')    # Define diretorio local
DIRIMG = config.get('PATH', 'DIRAUX')    # Define diretorio de imagens auxiliares
DIRLOC = os.path.dirname(os.path.abspath(__file__))    # Define diretorio local

class InputFile:

    def __init__(self, FILEIN, DIRINP, DIRLOG, DIRLOC):
        self.filein = FILEIN
        self.dirinp = DIRINP
        self.dirlog = DIRLOG
        self.dirloc = DIRLOC
        self.arq = None
        self.linhas = None
        self.ind = None
        self.station_list = None
        self.invalid_lines = None

    def read_file(self):
        self.arq = np.loadtxt(os.path.join(self.dirinp, self.filein), skiprows=1)
        self.linhas = np.shape(self.arq)[0]+1
        self.remove_invalid_lines()
        self.station_list = self.arq[:, 0]          # Id da estacao
        self.ind = np.unique(self.station_list)    # Lista todas as estacoes presentes no arquivo

    def remove_invalid_lines(self):
        """Remove as linhas que contenham algum valor 9999.99 nas medições (sensor nao fez a medicao).
         Remove também as linhas cuja Temperatura do ar seja menor que o Ponto de Orvalho."""
        remove_list = []
        for i in range(len(self.arq[:, 0])):
            if 9999.99 in self.arq[i, 3:9]:
                remove_list.append(i)
            if self.arq[i,7] < self.arq[i,8]:
                remove_list.append(i)

        self.invalid_lines = self.arq[remove_list,:]
        self.arq = np.delete(self.arq, remove_list, 0)

    def get_lines_by_station(self, id_station):
        """Seleciona conjunto de linhas (níveis) por estação"""
        # Localiza todas as linhas que possuem as estacoes listadas
        loc = np.nonzero(self.station_list == id_station)
        # Colunas do arquivo a ser lido:
        # [id_est - lon - lat - p - gp - d - f - t - td - data - hora]
        station_lines = self.arq[loc, :][0]
        return station_lines

    def update_log_last_file(self):
        """Atualiza informação do último arquivo processado"""
        nout = os.path.join(self.dirloc,'ultimo_raob.txt')
        with open(nout, 'w') as arqsaida:
            arqsaida.write(str(self.filein) + ' ' + str(int(self.linhas)) + ' ' + str(time.strftime("%d/%m/%Y_%H:%M")))


class Station:

    def __init__(self, id_station, station_lines):
        self.id_station = int(id_station)
        self.station_lines = station_lines

        self.niveis = len(self.station_lines)

        self.id_station = station_lines[0, 0]
        self.data = station_lines[0, 9]
        self.hora = station_lines[0, 10]
        self.lat = station_lines[0, 2]
        self.lon = station_lines[0, 1]
        self.pa = station_lines[:, 3]  # Pressao atmosferica [hPa]
        self.hg = station_lines[:, 4]  # Altura Geopotencial [m]
        self.dv = station_lines[:, 5]  # Direcao do vento    [graus]
        self.vv = station_lines[:, 6]  # Velocidade do vento [m/s]
        self.ta = station_lines[:, 7]  # Temperatuda do ar   [C]
        self.td = station_lines[:, 8]  # Temperatura do ponto de orvalho [C]
        self.vv[self.vv == 9999.99] = 0.  # Assina valores invalidos com NaN


class Calc:

    def __init__(self):
        self.ea = None
        self.rh = None
        self.rm = None
        self.u = None
        self.v = None
        self.vh = None
        self.show = None
        self.cap = None
        self.cin = None
        self.indk = None
        self.tt = None
        self.shr500 = None
        self.shr850 = None
        self.h2o = None
        self.thte = None
        self.theta_es = None
        self.thtv = None
        self.dthe_850 = None
        self.dthe_700 = None
        self.dthe_500 = None
        self.dthes_850 = None
        self.dthes_700 = None
        self.dthes_500 = None
        self.srh01 = None
        self.srh03 = None
        self.bulk = None
        self.shr6 = None
        self.ehi01 = None
        self.ehi03 = None
        self.severe = None
        self.dtdz = None

    def verify_default_levels(self):
        """Verifica se os niveis padroes (500, 700, 850 ou proximos) estao presentes nas radiossondagens"""
        flag = indices.ver_flag(station.pa)
        if flag == 0:
            return False
        return True

    def calculate_initial_parameters(self):
        self.ea = 6.122 * np.exp(17.67 * station.td / (243.5 + station.td))     # Pressao parcial de vapor (hPa)
        self.rh = (self.ea / indices.es(station.ta + T00)) * 100                # Umidade Relativa (%)
        self.rm = cape.MixRatio(self.ea * 100, station.pa * 100)                # Razao de Mistura (Kg/Kg)
        self.u, self.v = dyn.wind_deg_to_uv(station.dv, station.vv)             # Vento zonal (m/s)

    def geometric_height(self):
        th = len(station.hg)
        self.vh = np.zeros(th)
        for i in range(th):
            self.vh[i] = station.hg[i] - station.hg[0]


    # --------------------------------- SHOWALTER INDEX -------------------------------------
    def show_alter_index(self):
        # Localiza as posicoes 850 e 500 no vetor de pressao
        aa = (station.pa - 850) ** 2
        bb = np.nonzero(aa == min(aa))
        t_lower = station.ta[bb]
        td_lower = station.td[bb]
        cc = (station.pa - 500) ** 2
        dd = np.nonzero(cc == min(cc))
        t_upper = station.ta[dd]
        td_upper = station.td[dd]

        self.show = si.showalter_index_bolton1(t_lower, t_upper, td_lower, p_lower=850.0, p_upper=500.0)[0]

    def calculate_cape_cine(self):
        """
        Automatically generate a parcel based on the sounding characteristics
            Escolha um dos seguintes tipos de parcela:
            - Mixed Layer  : 'ml'
            - Surface Based: 'sb'
            - Most Unstable: 'mu'
        """
        method = ('ml', 'sb', 'mu')
        # Inicializa as saidas de CAPE e CINE
        self.cap = []
        self.cin = []
        for met in method:
            for i in range(0,len(station.ta)):
                if station.ta[i] < station.td[i]:
                    lf.write("***Parcela invalida! Temperatura menor do que Ponto de Orvalho.\n")
                    return False
            # Obtem informacoes termodinamicas das parcelas para os tres tipos de parcela considerados
            info_parcel = cape.get_parcel(station.hg, station.pa, station.ta, station.td, met)
            startp, startt, startdp = info_parcel[0], info_parcel[1], info_parcel[2]
            if startt < startdp:
                lf.write("***Parcela invalida! Temperatura menor do que Ponto de Orvalho.\n")
                return False
            # Calcula CAPE e CINE (a funcao "get_cape" tambem tem outras saidas que podem ser interessantes)
            val_calc = cape.get_cape(station.hg, station.pa, station.ta, station.td, startp, startt, startdp, totalcape=True)
            self.cap.append(val_calc[3])
            self.cin.append(val_calc[4])
        return True

    # ------------------------------- K INDEX ------------------------------------------
    def kindex(self):
        self.indk = indices.TTK(station.ta, station.pa, station.vv, station.td)[0][0]
        self.tt = indices.TTK(station.ta, station.pa, station.vv, station.td)[-1][0]

    # ------------------------------ SHEAR 500, 850 --------------------------------------
    def shear(self):
        self.shr500 = indices.SHR(station.pa, station.ta, station.td, station.vv)[0]
        self.shr850 = indices.SHR(station.pa, station.ta, station.td, station.vv)[1]

    # ------------------------------- PRECIPITABLE WATER ----------------------------------
    def prec_water(self):
        self.h2o = indices.wh2o(station.pa, station.ta, station.td)

    # ------------------------------- THETAe ----------------------------------------------
    def thetae(self):
        self.thte = np.zeros((len(station.pa)))
        for k in range(len(station.pa)):
            self.thte[k]= indices.th_e(station.pa[k] * 100, station.ta[k] + 273, station.td[k] + 273, self.rm[k])

    # ------------------------------- THETAES ----------------------------------------------
    def thetaes(self):
        self.theta_es = indices.thetaes(station.pa, station.ta + 273.15)  # ----------> modificado (05/05/2017)

    # ------------------------------- THETAv ----------------------------------------------
    def thetav(self):
        self.thtv = indices.theta_v(self.thte, self.rm)

    # ------------------------------- D(Tetae)/dz -----------------------------------------
    def dthetae(self):
        aa, bb, cc = (station.pa-850)**2,(station.pa-700)**2,(station.pa-500)**2
        i850, i700, i500 = np.nonzero(aa == min(aa)), np.nonzero(bb == min(bb)), np.nonzero(cc == min(cc))
        z850, z700, z500 = self.vh[i850], self.vh[i700], self.vh[i500]

        self.dthe_850 = 1000.*((self.thte[i850] - self.thte[0])/(z850 - self.vh[0]))    # 850 - SFC
        self.dthe_700 = 1000.*((self.thte[i700] - self.thte[i850])/(z700 - z850))       # 700 - 850
        self.dthe_500 = 1000.*((self.thte[i500] - self.thte[i700])/(z500 - z700))       # 500 - 700

    # -------------------------------- D(Tetaes)/dz ---------------------------------------
        self.dthes_850 = 1000.*((self.theta_es[i850] - self.theta_es[0]) / (z850 - self.vh[0]))  # 850 - SFC            ----------> modificado (05/05/2017)
        self.dthes_700 = 1000.*((self.theta_es[i700] - self.theta_es[i850]) / (z700 - z850))  # 700 - 850            ----------> modificado (05/05/2017)
        self.dthes_500 = 1000.*((self.theta_es[i500] - self.theta_es[i700]) / (z500 - z700))  # 500 - 700            ----------> modificado (05/05/2017)

    def lapse(self):
        aa, cc = (station.pa-850)**2,(station.pa-500)**2
        i850, i500 = np.nonzero(aa == min(aa)), np.nonzero(cc == min(cc))
        z850, z500 = self.vh[i850], self.vh[i500]
        self.dtdz = 1000. * ((station.ta[i500] - station.ta[i850]) / (z500 - z850))  # 500 - 850

    # ------------------------------- BULK RICHARDSON NUMBER ------------------------------
    def calc_bulk(self):
        self.bulk = []
        for cape in self.cap:
          self.bulk.append(dyn.brn(self.u, self.v, self.vh, cape))

    # ----------------------------------- CISALHAMENTO 0-6km ------------------------------
    def cisalhamento(self):
        uu, vv = dyn.shear(self.u, self.v, station.hg, 0., 6000.)
        self.shr6 = (uu**2+vv**2)**0.5

    # ------------------ Energy-Helicity-Index (Para os niveis de 1 e 3 km) ---------------
    def helicity(self):
        # Considerando o movimento da tempestade
        ucb = dyn.storm_motion_bunkers(self.u, self.v, self.vh)
        self.srh01 = dyn.srh(self.u, self.v, self.vh, 0., 1000., ucb[0], ucb[1])
        self.srh03 = dyn.srh(self.u, self.v, self.vh, 0., 3000., ucb[0], ucb[1])

        self.ehi01, self.ehi03 = [], []
        for cape in self.cap:
            self.ehi01.append(cape*self.srh01/1.6E5)
            self.ehi03.append(cape*self.srh03/1.6E5)

    # --------------------------- SWEAT (SEVERE WEATHER THREAT INDEX) -----------------------
    def severe_index(self):
        self.severe = indices.sweat(station.ta, station.pa, station.vv, station.td, station.dv)


class Output:

    def __init__(self, dirimg, dirout):
        self.out = np.empty((len(file.ind), 24))
        self.dirimg = dirimg
        self.dirout = dirout
        self.sounding = None
        self.figname = None
        self.textfile = None
        self.skew_figname = None
        self.cape_figname = None

    def plot_skewt(self):
        sondagem = np.zeros((len(station.pa), 11))
        sondagem[:, 0] = station.pa
        sondagem[:, 1] = calc.vh
        sondagem[:, 2] = station.ta
        sondagem[:, 3] = station.td
        sondagem[:, 4] = calc.rh
        sondagem[:, 5] = calc.rm*1000.
        sondagem[:, 6] = station.dv
        sondagem[:, 7] = station.vv
        sondagem[:, 8] = indices.theta(station.ta, station.pa)
        sondagem[:, 9] = calc.u
        sondagem[:, 10] = calc.v

        columns = [
            "pressure",     # hPa
            "height",       # meters
            "temperature",  # C
            "dewpoint",     # C
            "rh",           # %
            "mixing_ratio", # g/kg
            "direction",    # degrees
            "sknt",         # knots
            "theta",        # K
            "us",           # m/s
            "vs",           # m/s
        ]
        self.sounding = pd.DataFrame(sondagem, columns=columns)
        self.sounding.misc = {'CAPV': calc.cap, 'CINV': calc.cin, 'BRN': calc.bulk[0], 'KINDEX': calc.indk,
                              'Showalter': calc.show, 'IWV': calc.h2o}  # DPE

        # Define a hora para ser colocada na figura e no nome do arquivo de saida
        horan = file.filein[24:26]
        fig = plt.figure(1, figsize=(14, 8))
        # Skew-T
        #             x   y   tx  ty
        ax = plt.axes([0.08, 0.07, 0.4, 0.85])
        titulo = (
                "Station: " + str("%d" % station.id_station) + "\nDate:     " + str(int(station.data)) + " - "
                + '{:04d}'.format(int(station.hora)) + "Z")
        skewt.plot_skewt(self.sounding, ax=ax, title=titulo,
                         lift_parcel=True, plot_winds=True, diags=["CAPE", ],
                         label_altitudes=True)

        #fig = plt.figure(1, figsize=(14, 8))
        im = plt.imread(get_sample_data(os.path.join(self.dirimg,'inpe_cptec.jpg')))
        ax = fig.add_axes([0.92, 0, 0.07, 0.07], anchor='NE', zorder=-1)
        plt.setp(plt.gca(), frame_on=False, xticks=(), yticks=())
        ax.imshow(im)

        # Plota Hodografo
        ax2 = plt.subplot(222)
        skewt.plot_hodo_axes(ax2)
        skewt.plot_hodograph(ax2, self.sounding)
        return fig

    def plot_tables(self, fig):
        plt.xticks([]), plt.yticks([])
        plt.axes([0.53, 0.73, .2, .4])
        info = ('Sounding at location: ' + str("%.2f" % station.lat) + ', ' + str("%.2f" % station.lon) + ', ' +
                str(int(station.hg[0])) + ' m and ' + str(int(len(station.hg))) + ' vertical levels')
        plt.text(0.02, 0.5, info, ha='left', va='bottom', size=12, color='black')
        plt.setp(plt.gca(), frame_on=False, xticks=(), yticks=())
        ################## MONTA TABELAS NO GRAFICO ################################
        plt.xticks([]), plt.yticks([])
        ax3 = fig.add_subplot(224)
        plt.axis([-1, 1, -1, 1])
        ax3.set_axis_off()
        x = -1.05
        y = 1.3
        line = 'Surface Parcel'
        plt.text(x, y, line, verticalalignment='center', horizontalalignment='center', fontsize=12)
        x = -1.3
        y = 1.15
        line = r'CAPE {1:10.1f} J kg$^-$$^1$'.format(int(calc.cap[1]), calc.cap[1])
        if 1000. <= calc.cap[1] < 2500.:
            plt.text(x, y, line, verticalalignment='center', horizontalalignment='left', fontsize=12, color='g')
        elif 2500. <= calc.cap[1] < 3500.:
            plt.text(x, y, line, verticalalignment='center', horizontalalignment='left', fontsize=12,
                     color='darkorange')
        elif calc.cap[1] >= 3500.:
            plt.text(x, y, line, verticalalignment='center', horizontalalignment='left', fontsize=12, color='r')
        else:
            plt.text(x, y, line, verticalalignment='center', horizontalalignment='left', fontsize=12)
        y = 1.0
        line = r'CINE {1:10.1f} J kg$^-$$^1$'.format(int(calc.cin[1]), calc.cin[1])
        plt.text(x, y, line, verticalalignment='center', horizontalalignment='left', fontsize=12)
        y = 0.85
        line = r'BRN {1:10.1f} adm'.format(int(calc.bulk[1]), calc.bulk[1])
        if 10 <= calc.bulk[1] < 45:
            plt.text(x, y, line, verticalalignment='center', horizontalalignment='left', fontsize=12, color='darkorange')
        elif calc.bulk[1] >= 45:
            plt.text(x, y, line, verticalalignment='center', horizontalalignment='left', fontsize=12,color='r')
        else:
            plt.text(x, y, line, verticalalignment='center', horizontalalignment='left', fontsize=12)
        y = 0.7
        line = r'EHI1km {1:10.1f}'.format(int(calc.ehi01[1]), calc.ehi01[1])
        plt.text(x, y, line, verticalalignment='center', horizontalalignment='left', fontsize=12)
        y = 0.55
        line = r'EHI3km {1:10.1f}'.format(int(calc.ehi03[1]), calc.ehi03[1])
        plt.text(x, y, line, verticalalignment='center', horizontalalignment='left', fontsize=12)

        x = -0.2
        y = 1.3
        line = 'Mixed Layer'
        plt.text(x, y, line, verticalalignment='center', horizontalalignment='center', fontsize=12)
        x = -0.41
        y = 1.15
        line = r'CAPE {1:10.1f} J kg$^-$$^1$'.format(int(calc.cap[0]), calc.cap[0])
        if 1000. <= calc.cap[0] < 2500.:
            plt.text(x, y, line, verticalalignment='center', horizontalalignment='left', fontsize=12, color='g')
        elif 2500. <= calc.cap[0] < 3500.:
            plt.text(x, y, line, verticalalignment='center', horizontalalignment='left', fontsize=12,
                     color='darkorange')
        elif calc.cap[0] >= 3500.:
            plt.text(x, y, line, verticalalignment='center', horizontalalignment='left', fontsize=12, color='r')
        else:
            plt.text(x, y, line, verticalalignment='center', horizontalalignment='left', fontsize=12)
        y = 1.0
        line = r'CINE {1:10.1f} J kg$^-$$^1$'.format(int(calc.cin[0]), calc.cin[0])
        plt.text(x, y, line, verticalalignment='center', horizontalalignment='left', fontsize=12)
        y = 0.85
        line = r'BRN {1:10.1f} adm'.format(int(calc.bulk[0]), calc.bulk[0])
        if 10 <= calc.bulk[0] < 45:
            plt.text(x, y, line, verticalalignment='center', horizontalalignment='left', fontsize=12, color='darkorange')
        elif calc.bulk[0] >= 45:
            plt.text(x, y, line, verticalalignment='center', horizontalalignment='left', fontsize=12,color='r')
        else:
            plt.text(x, y, line, verticalalignment='center', horizontalalignment='left', fontsize=12)
        y = 0.7
        line = r'EHI1km {1:10.1f}'.format(int(calc.ehi01[0]), calc.ehi01[0])
        plt.text(x, y, line, verticalalignment='center', horizontalalignment='left', fontsize=12)
        y = 0.55
        line = r'EHI3km {1:10.1f}'.format(int(calc.ehi03[0]), calc.ehi03[0])
        plt.text(x, y, line, verticalalignment='center', horizontalalignment='left', fontsize=12)

        x = 0.8
        y = 1.3
        line = 'Most Unstable'
        plt.text(x, y, line, verticalalignment='center', horizontalalignment='center', fontsize=12)
        x = 0.55
        y = 1.15
        line = r'CAPE {1:10.1f} J kg$^-$$^1$'.format(int(calc.cap[2]), calc.cap[2])
        if 1000. <= calc.cap[2] < 2500.:
            plt.text(x, y, line, verticalalignment='center', horizontalalignment='left', fontsize=12, color='g')
        elif 2500. <= calc.cap[2] < 3500.:
            plt.text(x, y, line, verticalalignment='center', horizontalalignment='left', fontsize=12,
                     color='darkorange')
        elif calc.cap[2] >= 3500.:
            plt.text(x, y, line, verticalalignment='center', horizontalalignment='left', fontsize=12, color='r')
        else:
            plt.text(x, y, line, verticalalignment='center', horizontalalignment='left', fontsize=12)
        y = 1.0
        line = r'CINE {1:10.1f} J kg$^-$$^1$'.format(int(calc.cin[2]), calc.cin[2])
        plt.text(x, y, line, verticalalignment='center', horizontalalignment='left', fontsize=12)
        y = 0.85
        line = r'BRN {1:10.1f} adm'.format(int(calc.bulk[2]), calc.bulk[2])
        if 10 <= calc.bulk[2] < 45:
            plt.text(x, y, line, verticalalignment='center', horizontalalignment='left', fontsize=12, color='darkorange')
        elif calc.bulk[2] >= 45:
            plt.text(x, y, line, verticalalignment='center', horizontalalignment='left', fontsize=12,color='r')
        else:
            plt.text(x, y, line, verticalalignment='center', horizontalalignment='left', fontsize=12)
        y = 0.7
        line = r'EHI1km {1:10.1f}'.format(int(calc.ehi01[2]), calc.ehi01[2])
        plt.text(x, y, line, verticalalignment='center', horizontalalignment='left', fontsize=12)
        y = 0.55
        line = r'EHI3km {1:10.1f}'.format(int(calc.ehi03[2]), calc.ehi03[2])
        plt.text(x, y, line, verticalalignment='center', horizontalalignment='left', fontsize=12)

        # Outras informacoes
        # Coluna 1
        ax3 = fig.add_subplot(224)
        plt.axis([-1, 1, -1, 1])
        ax3.set_axis_off()
        x = 0
        y = 0.2
        line = 'Other relevant information'
        plt.text(x, y, line, verticalalignment='center', horizontalalignment='center', fontsize=12)
        x = -1.3
        y = 0
        line = 'K  {1:10.1f} adm'.format(int(calc.indk), calc.indk)
        if 20 <= calc.indk < 25:
            plt.text(x, y, line, verticalalignment='center', horizontalalignment='left', fontsize=12, color='g')
        elif 25 <= calc.indk < 30:
            plt.text(x, y, line, verticalalignment='center', horizontalalignment='left', fontsize=12, color='darkorange')
        elif calc.indk >= 30:
            plt.text(x, y, line, verticalalignment='center', horizontalalignment='left', fontsize=12, color='r')
        else:
            plt.text(x, y, line, verticalalignment='center', horizontalalignment='left', fontsize=12)
        y = -0.12
        line = r'IWV {1:6.1f} mm'.format(int(calc.h2o), calc.h2o)
        plt.text(x, y, line, verticalalignment='center', horizontalalignment='left', fontsize=12)
        y = -0.24
        line = 'SHW {1:6.1f} adm'.format(int(calc.show), calc.show)
        if -4 <= calc.show <= 0:
            plt.text(x, y, line, verticalalignment='center', horizontalalignment='left', fontsize=12, color='g')
        elif -7 <= calc.show < -4:
            plt.text(x, y, line, verticalalignment='center', horizontalalignment='left', fontsize=12, color='darkorange')
        elif calc.show < -7:
            plt.text(x, y, line, verticalalignment='center', horizontalalignment='left', fontsize=12, color='r')
        else:
            plt.text(x, y, line, verticalalignment='center', horizontalalignment='left', fontsize=12)
        y = -0.36
        line = r'$\theta_e$ {1:9.1f} K'.format(int(calc.thte[0]), calc.thte[0])
        plt.text(x, y, line, verticalalignment='center', horizontalalignment='left', fontsize=12)
        y = -0.48
        line = r'$\theta_v$ {1:9.1f} K'.format(int(calc.thtv[0]), calc.thtv[0])
        plt.text(x, y, line, verticalalignment='center', horizontalalignment='left', fontsize=12)
        y = -0.72
        line = r'Storm Relative Helicity (0-1km) {1:9.1f} m$^2$/s$^2$'.format(float(calc.srh01), calc.srh01)
        plt.text(x, y, line, verticalalignment='center', horizontalalignment='left', fontsize=12)
        y = -0.84
        line = 'Storm Relative Helicity (0-3km) {1:9.1f} m$^2$/s$^2$'.format(float(calc.srh03), calc.srh03)
        plt.text(x, y, line, verticalalignment='center', horizontalalignment='left', fontsize=12)
        y = -0.96
        line = 'Severe Weather Threat (SWEAT) {0:9.1f} adm'.format(float(calc.severe))
        if 250 <= calc.severe < 400:
            plt.text(x, y, line, verticalalignment='center', horizontalalignment='left', fontsize=12,color='darkorange')
        elif calc.severe >= 400:
            plt.text(x, y, line, verticalalignment='center', horizontalalignment='left', fontsize=12, color='r')
        else:
            plt.text(x, y, line, verticalalignment='center', horizontalalignment='left', fontsize=12)
        y = -1.08
        line = 'Total Totals                                 {0:9.1f} adm'.format(float(calc.tt))
        if 44 < calc.tt <= 50:
            plt.text(x, y, line, verticalalignment='center', horizontalalignment='left', fontsize=12,color='g')
        elif 50 < calc.tt <=52:
            plt.text(x, y, line, verticalalignment='center', horizontalalignment='left', fontsize=12,color='darkorange')
        elif calc.tt > 52:
            plt.text(x, y, line, verticalalignment='center', horizontalalignment='left', fontsize=12,color='r')
        else:
            plt.text(x, y, line, verticalalignment='center', horizontalalignment='left', fontsize=12)
        # Coluna 2
        x = -0.7
        y = 0
        line = 'Shear (500 mb) {1:6.1f} m/s'.format(int(calc.shr500), calc.shr500)
        plt.text(x, y, line, verticalalignment='center', horizontalalignment='left', fontsize=12)
        y = -0.12
        line = 'Shear (850 mb) {1:6.1f} m/s'.format(int(calc.shr850), calc.shr850)
        plt.text(x, y, line, verticalalignment='center', horizontalalignment='left', fontsize=12)
        y = -0.24
        line = r'$d\theta_e/dz$ (850-Sfc) {1:6.2f} K/km'.format(int(calc.dthe_850[0]), calc.dthe_850[0])
        plt.text(x, y, line, verticalalignment='center', horizontalalignment='left', fontsize=12)
        y = -0.36
        line = r'$d\theta_e/dz$ (850-700) {1:6.2f} K/km'.format(int(calc.dthe_700[0]), calc.dthe_700[0])
        plt.text(x, y, line, verticalalignment='center', horizontalalignment='left', fontsize=12)
        y = -0.48
        line = r'$d\theta_e/dz$ (700-500) {1:6.2f} K/km'.format(int(calc.dthe_500[0]), calc.dthe_500[0])
        plt.text(x, y, line, verticalalignment='center', horizontalalignment='left', fontsize=12)
        ############### ----------> modificado (05/05/2017)
        # Coluna 3
        x = 0.4
        y = 0
        line = r'$d\theta es/dz$ (850-Sfc) {1:6.2f} K/km'.format(int(calc.dthes_850[0]), calc.dthes_850[0])
        plt.text(x, y, line, verticalalignment='center', horizontalalignment='left', fontsize=12)
        y = -0.12
        line = r'$d\theta es/dz$ (850-700) {1:6.2f} K/km'.format(int(calc.dthes_700[0]), calc.dthes_700[0])
        plt.text(x, y, line, verticalalignment='center', horizontalalignment='left', fontsize=12)
        y = -0.24
        line = r'$d\theta es/dz$ (700-500) {1:6.2f} K/km'.format(int(calc.dthes_500[0]), calc.dthes_500[0])
        plt.text(x, y, line, verticalalignment='center', horizontalalignment='left', fontsize=12)
        y = -0.36
        line = 'dT/dz (850-500) {1:6.2f} K/km'.format(int(calc.dtdz[0]), calc.dtdz[0])
        plt.text(x, y, line, verticalalignment='center', horizontalalignment='left', fontsize=12)
        ############## ----------> modificado (05/05/2017)

    def save_figure(self):
        """Salva figura com SKEWT por estação"""
        filename = 'SKEW_'+ str(int(station.id_station)) + '_' + str(int(station.data)) + '{:04d}'\
                   .format(int(station.hora)) + '00.png'
        self.skew_figname = os.path.join(DIROUT, filename)
        # plt.show(fig)
        plt.savefig(self.skew_figname)
        plt.close('all')
        if os.path.exists(self.skew_figname):
            return True
        else:
            return False

    def create_output_file(self, nn):
        self.out[nn, 0] = station.id_station     # Station ID
        self.out[nn, 1] = station.lat            # Latitude
        self.out[nn, 2] = station.lon            # Longitude
        self.out[nn, 3] = station.data           # Date
        self.out[nn, 4] = station.hora           # Hour
        self.out[nn, 5] = calc.show           # Showalter Index
        self.out[nn, 6] = calc.indk           # K index
        self.out[nn, 7] = calc.cap[0]         # Convective Available Potential Energy (using virtual temperature)
        self.out[nn, 8] = calc.cap[1]         # Convective Available Potential Energy (using virtual temperature)
        self.out[nn, 9] = calc.cap[2]         # Convective Available Potential Energy (using virtual temperature)
        self.out[nn, 10] = calc.cin[0]        # Convective Inhibition (using virtual temperature)
        self.out[nn, 11] = calc.cin[1]        # Convective Inhibition (using virtual temperature)
        self.out[nn, 12] = calc.cin[2]        # Convective Inhibition (using virtual temperature)
        self.out[nn, 13] = calc.bulk[0]       # Bulk Richardson Number (using CAPV)
        self.out[nn, 14] = calc.h2o           # Precipitable Water [mm] for entire sounding
        self.out[nn, 15] = calc.shr850        # Wind Shear in 850 mb level
        self.out[nn, 16] = calc.shr500        # Wind Shear in 500 mb level
        self.out[nn, 17] = calc.ehi01[0]      # Energy-helicity index
        self.out[nn, 18] = calc.ehi03[0]      # Energy-helicity index
        self.out[nn, 19] = calc.tt            # Totals Totals
        self.out[nn, 20] = calc.shr6          # Shear 0-6 km
        self.out[nn, 21] = calc.severe        # Severe Weather Threat Index
        self.out[nn, 22] = calc.dtdz        # Lapse Rate (850 - 50 hPa)
        indsevero=0
        if calc.cap[0] or calc.cap[1] or calc.cap[2] > 1000:
            indsevero+=1
        if calc.bulk[0] > 10:
            indsevero+=1
        if calc.severe >=250:
            indsevero+=1
        if calc.tt > 44:
            indsevero+=1
        if calc.show < 0:
            indsevero+=1
        if calc.indk>20:
            indsevero+=1

        if indsevero == 0:
            self.out[nn,23] = 1111
        elif indsevero == 1:
            self.out[nn,23] = 2222
        elif indsevero == 2:
            self.out[nn,23] = 3333
        elif indsevero >= 3:
            self.out[nn,23] = 4444

    def save_text_file(self):
        """Salva arquivo texto com índices calculados"""
        cab = 'id lat lon data hora show indk cap1 cap2 cap3 cin1 cin2 cin3 ri wh2o shr850 shr500 ehi01 ehi03 tt shr6 sweat lapse cor'
        filename = 'INDX_10001_'+ str(int(station.data)) + '{:04d}'.format(int(station.hora)) + '00.txt'
        self.textfile = os.path.join(self.dirout, filename)
        np.savetxt(self.textfile, self.out, header=cab,
                   fmt='%-5.0f %-4.2f %-3.2f %-6.0f %-7.0f %-7.1f %-7.1f %-7.2f %-7.2f %-7.2f %-7.2f %-7.2f %-7.2f '
                       '%-7.2f %-7.2f %-7.2f %-7.2f %-7.2f %-7.2f %-7.2f' '%-7.2f' '%-7.2f' '%-7.2f' '%-4.0f')
        if os.path.exists(self.textfile):
            return True
        else:
            return False

    def create_cape_img(self):
        filename = 'CAPE_10000_' + str(int(station.data)) + '{:04d}'.format(int(station.hora)) + '00.png'
        self.cape_figname = os.path.join(self.dirout, filename)

        idstation = [83971, 83827, 83768, 83779, 83746, 83612, 83566, 83362, 83378, 83208, 82705, 82824, 82965, 82397,
                     82599, 82400]
        nastation = ['Porto Alegre/RS', 'Foz do Iguaçu/PR', 'Londrina/PR', 'Campo de Marte/SP', 'Galeão/RJ', 'Campo Grande/MS',
                     'Confins/MG', 'Cuiabá/MT', 'Brasília/DF', 'Vilhena/RO', 'Cruzeiro do Sul/AC', 'Porto Velho/RO',
                     'Alta Floresta/MT', 'Fortaleza/CE', 'Natal/RN', 'Fernando de Noronha/PE']
        mastation = ['black', 'gray', 'firebrick', 'sienna', 'gold', 'chartreuse', 'darkturquoise', 'lightgray', 'blue', 'm', 'orange', 'dodgerblue', 'crimson', 'yellow', 'teal', 'pink']


        plt.figure(1)
        cc = np.arange(0, 5000, 1)
        br = [100, 20, 10, 1]
        y = np.empty((5000, 4))
        ii = 0
        for x in br:
            y[:, ii] = (cc / (0.5 * x)) ** 0.5
            ii += 1

        # Procurando estacoes
        ###rj = np.nonzero(self.out[:, 0] == 83746)
        ###sp = np.nonzero(self.out[:, 0] == 83779)

        # Criando o grafico

        plt.plot(cc, y[:, 0], '-k')
        plt.plot(cc, y[:, 1], '-k')
        plt.plot(cc, y[:, 2], '-k')
        plt.plot(cc, y[:, 3], '-k')

        points=[]
        for i in range(len(idstation)):
            ind=np.nonzero(self.out[:,0] == idstation[i])
            if ind[0]:
                points += plt.plot(self.out[ind,9], self.out[ind,20], 's', markeredgecolor='None', markerfacecolor=mastation[i], label = nastation[i])
        labels = [p.get_label() for p in points]
        plt.legend(points, labels, numpoints=1, fontsize=6, ncol=2)
        x, y = 4970, 8
        line = '100'
        plt.text(x, y, line, verticalalignment='center', horizontalalignment='right', fontsize=12)
        y = 20
        line = '20'
        plt.text(x, y, line, verticalalignment='center', horizontalalignment='right', fontsize=12)
        y = 30
        line = '10'
        plt.text(x, y, line, verticalalignment='center', horizontalalignment='right', fontsize=12)
        x, y = 990, 39
        line = '1'
        plt.text(x, y, line, verticalalignment='center', horizontalalignment='right', fontsize=12)

        plt.axis([0, 5000, 0, 40])
        plt.xlabel(r'CAPE (J kg$^{-1}$)')
        plt.ylabel(r'0-6 km shear (ms$^{-1}$)')
        titulo = 'Date: ' + str(int(station.data)) + ' - ' + '{:04d}'.format(int(station.hora)) + 'Z'
        plt.title(titulo, loc='left', fontsize=15)
        #plt.savefig('teste.png')

        """caprj = self.out[rj, 9]
        shrrj = abs(self.out[rj, 20])
        capsp = self.out[sp, 9]
        shrsp = abs(self.out[sp, 20])

        if rj[0]:
            x5, = plt.plot(caprj, shrrj, 'or')
        else:
            caprj, shrrj = -9999, -9999
            x5, = plt.plot(caprj, shrrj, 'or')

        if sp[0]:
            x6, = plt.plot(capsp, shrsp, 'ob')
        else:
            capsp, shrsp = -9999, -9999
            x6, = plt.plot(capsp, shrsp, 'ob')

        plt.legend((x5, x6), ('83746 - SBGL/RJ', '83779 - SBMT/SP'), framealpha=0.6, numpoints=1)

        x, y = 4970, 8
        line = '100'
        plt.text(x, y, line, verticalalignment='center', horizontalalignment='right', fontsize=12)
        y = 20
        line = '20'
        plt.text(x, y, line, verticalalignment='center', horizontalalignment='right', fontsize=12)
        y = 30
        line = '10'
        plt.text(x, y, line, verticalalignment='center', horizontalalignment='right', fontsize=12)
        x, y = 990, 39
        line = '1'
        plt.text(x, y, line, verticalalignment='center', horizontalalignment='right', fontsize=12)
        plt.axis([0, 5000, 0, 40])
        plt.xlabel(r'CAPE (J kg$^{-1}$)')
        plt.ylabel(r'0-6 km shear (ms$^{-1}$)')
        titulo = 'Date: ' + str(int(station.data)) + ' - ' + '{:04d}'.format(int(station.hora)) + 'Z'
        plt.title(titulo, loc='left', fontsize=15)
        # plt.show(fig1)"""
        plt.savefig(self.cape_figname)
        plt.close('all')

        if os.path.exists(self.cape_figname):
            return True
        else:
            return False


if __name__ == '__main__':
    #Lê arquivo de entrada
    file = InputFile(FILEIN, DIRINP, DIRLOG, DIRLOC)
    file.read_file()

    # Abre/cria arquivo de log
    lf = open(os.path.join(DIRLOG, 'raob_'+time.strftime("%Y%m%d")), 'a')
    lf.write('> Iniciando processamento do arquivo ' + FILEIN + ' (linhas='+str(file.linhas)+') em ' +
             time.strftime("%d/%m/%Y %H:%M") + '\n' + 'Linhas invalidas removidas:' + '\n' + str(file.invalid_lines) + '\n')

    # Cria arquivos para armazenar as estações com erro para exibição no ecFlow
    error_log = os.path.join(DIRLOG, 'raob_ERRO.log')
    if os.path.exists(error_log):
        os.remove(error_log)
    el = open(error_log, 'w')

    # Loop das estacoes
    nn = 0
    output = Output(DIRIMG, DIROUT)
    for i in range(len(file.ind)):
        #Lê dados da estação
        id_station = int(file.ind[i])
        station_lines = file.get_lines_by_station(id_station)
        station = Station(id_station, station_lines)
        lf.write('>> STATION:' + str(id_station) + ' DATA: '+str(int(station.data))+'\n')

        # Verifica se a estação tem no mínimo 10 níveis de medição para prosseguir com os cálculos
        if station.niveis <= 10:
            el.write(str(id_station) + ' ')
            lf.write('*** Estacao descartada! Nao possui mais de 10 niveis!\n')
            continue

        #Calcula os índices
        calc = Calc()
        if calc.verify_default_levels():
            calc.calculate_initial_parameters()
            calc.geometric_height()
            calc.show_alter_index()
            if not calc.calculate_cape_cine():
                continue
            calc.kindex()
            calc.shear()
            calc.prec_water()
            calc.thetae()
            calc.thetaes()
            calc.thetav()
            calc.dthetae()
            calc.calc_bulk()
            calc.cisalhamento()
            calc.helicity()
            calc.severe_index()
            calc.lapse()
        else:
            lf.write('*** Estacao descartada! Nao passou na checagem de niveis padroes!\n')
            el.write(str(id_station) + ' ')
            continue

        #Gera saídas
        fig = output.plot_skewt()
        output.plot_tables(fig)
        if output.save_figure():
            lf.write('>>> Figura SKEW Gerada: '+output.skew_figname+'\n')
        output.create_output_file(nn)
        nn += 1

    output.out = output.out[0:nn, :]
    if output.save_text_file():
        lf.write('>> Arquivo texto gerado: '+output.textfile+'\n')
    else:
        lf.write('** ERRO: Arquivo INDX nao foi gerado!\n')
        print('ERRO: Arquivo INDX nao foi gerado!')
        sys.exit()
    if output.create_cape_img():
        lf.write('>> Figura CAPE Gerada: ' + output.cape_figname+'\n')
    else:
        lf.write('** ERRO: Figura CAPE nao foi gerada!')
        print('ERRO: Figura CAPE nao foi gerada!')
        sys.exit()

    file.update_log_last_file()
    lf.write('> Finalizado processamento do arquivo '+FILEIN+' em '+time.strftime("%d/%m/%Y  %H:%M") + '\n\n')
    lf.close()
    el.close()
