"""Library containing the complementary mathematical functions necessary for the operation of the code.

	Autor: Javier Díez Sierra
	Fechas 06-02-2017
    
    Updated by Salvador Navas Fernández
    Date 01-07-2021
"""



import sys
import matplotlib.pyplot as plt

import pandas as pd
import numpy as np
import datetime
from datetime import timedelta

def allmonths(dataframe):
    """Paso el dataframe a 12 columnas con 12 meses"""
    
    dataframe_meses=pd.DataFrame(index=dataframe.index, columns=np.arange(1,13))
    if len(dataframe.columns)==12:
        dataframe_meses.loc[:,:] = dataframe.values
    else:
        for i,ii in enumerate(dataframe.columns):
            for j in list(map(int, ii[1:-1].split(','))):
                dataframe_meses.loc[:,j] = dataframe.loc[:,ii]

   
    return dataframe_meses


def datetime2matlabdn(dt):
    mdn = dt + timedelta(days = 366)
    frac_seconds = (dt-datetime.datetime(dt.year,dt.month,dt.day,0,0,0)).seconds\
    /(24.0 * 60.0 * 60.0)
    frac_microseconds = dt.microsecond / (24.0 * 60.0 * 60.0 * 1000000.0)
    return mdn.toordinal() + frac_seconds + frac_microseconds



def datetime2matlabdnJavi(pdt, dt):
    '''
    Funcion que passa de un vectors de pandas a una lista de tiempo en formato ordinal
    pdt=pd.date_range
    dt = resolución days/hours/minutes/seconds
    '''
    
    if dt=='days':
        dt_ordinal=1
    elif dt=='hours':
        dt_ordinal=1/24
    elif dt=='minutes':
        dt_ordinal=1/(24*60)
    elif dt=='seconds':
        dt_ordinal=1/(24*60*60)
        
    d1 = datetime.datetime(pdt.year[0], pdt.month[0], pdt.day[0])# start date
    tt_ordinal_aux=list()
    
    dtt=0
    for i in range(len(pdt)):
        if i ==0:
            #tt_ordinal_origen=(d1).toordinal()
            tt_ordinal_origen=datetime2matlabdn(d1)
            tt_ordinal_aux.append(tt_ordinal_origen)
        else:
            tt_ordinal_aux.append(tt_ordinal_origen+dtt)
            
        dtt=dtt+dt_ordinal
        
    return tt_ordinal_aux

def func(x, a, b, c):
    """Funcion a la que voy a ajustar los valores de correlación espacial"""

    return a * np.exp(-b * x) + c

def distancia_f(x1, y1, x2, y2):
    dist=((x1-x2)**2 + (y1-y2)**2)**0.5
    return dist
def haversine(lon1, lat1, lon2, lat2):
    from math import radians, cos, sin, asin, sqrt
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    km = 6367 * c
    return km

    model.params
    model.plot_summary()
    RETURN_PERIODS.return_periods=model.return_periods
    RETURN_PERIODS.return_values=model.return_values
    plt.show()

def IDW_f(xx, yy, zz, x, y, betha):
    ##xx, yy --> Coordenadas de las estaciones
    ##zz --> variable que quieres interpolar
    ##x, y --> punto donde quieres obtener el resultado
    ## betha--> exponente de peso. Cuanto mayor, más peso se le asigna a los puntos cercanos
    dist=list()
    for i in range(len(xx)):
        dist.append(haversine(xx[i], yy[i], x, y))
    dist=np.array(dist)
    weights=(dist**(-betha))/np.sum(dist**(-betha))
    
    return np.sum(zz*weights)

def compare_statistics(CAL, SIM):
    
    stats_obs=allmonths(CAL.statististics_Real)
    stats_fit=allmonths(CAL.statististics_Fit)
    stats_sim=allmonths(SIM.statististics_Simulated)
    
    RK=int(np.ceil(np.sqrt(len(stats_obs.index)))); 
    if len(stats_obs.index) % RK == 0:
        CK = int(len(stats_obs.index)/RK)
    else:
        CK = int(np.ceil(np.sqrt(len(stats_obs.index))))
    fig, axes = plt.subplots(RK, CK, figsize=(15, 15))
    for i, ii in enumerate(stats_obs.index):
        Data_sta=pd.DataFrame(index=np.arange(1, 13))
        Obs=list(); Fit=list(); Sim=list();
        for m in np.arange(1, 13):
            Obs.append(stats_obs[m].loc[ii])
            Fit.append(stats_fit[m][ii])
            Sim.append(stats_sim[m].loc[ii])

        Data_sta['Obs']=Obs
        Data_sta['Fit']=Fit
        Data_sta['Sim']=Sim
        #Ploteo
        row = i // CK
        col = i % CK
        ax=axes[row,col]
        ax.set_title(ii)
        ax.grid(True)
        #Data_sta.plot(ax=axes[row,col])
        legnd=['Obs', 'Fit', 'Sim']
        pp=Data_sta['Obs'].plot(style='k--', lw=2,  ax=axes[row,col])
        Data_sta['Fit'].plot(style='bs', ax=axes[row,col])
        Data_sta['Sim'].plot(style='r^', ax=axes[row,col])
        pp.legend(legnd, loc='best', fontsize=15)
        if ii[0:2]==('fi' or 'au'):
            ax.set_ylim(0, 1)

def exceedence_probability(Serie_Observed, Serie_Simulated, temporal_resolution):
    # Observed
    aux=Serie_Observed.values; aux=aux[aux>=0]
    s_obs = np.sort(aux, axis=None)[::-1]
    exc_obs = np.arange(1.,len(s_obs)+1) / len(s_obs)

    # Simulated
    if temporal_resolution == 'd':
        units = 'mm/day'
    elif temporal_resolution == 'h':
        units = 'mm/hour'

    aux = Serie_Simulated.values; aux=aux[aux>=0]
    s_sim = np.sort(aux, axis=None)[::-1]
    exc_sim = np.arange(1.,len(s_sim)+1) / len(s_sim)
    
    fig, ax = plt.subplots(figsize=(10, 5))

    ax.plot(exc_obs*100, s_obs, '.k', markersize=8,  label='Obs')
    ax.plot(exc_sim*100, s_sim, 'r',  label='Sim')
    ax.set_xlabel("Exceedence Probability", fontsize=13)
    ax.set_ylabel(units, fontsize=13)
    ax.set_xscale('log')
    ax.grid(True)
    ax.tick_params(labelsize=13)
    ax.legend(fontsize = 15)
 

	

