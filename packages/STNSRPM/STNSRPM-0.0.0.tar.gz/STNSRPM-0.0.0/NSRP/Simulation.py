'''
Library containing classes for simulating time series from the model.

	Authors: 
        + Javier Díez Sierra
	    + Salvador Navas Fernández
        + Manuel del Jesus
    
'''



from NSRP.MathematicalPropertiesNSRP import *
from NSRP.utils import *
from NSRP.libs_NSRP import *
from NSRP.inputs_simulation import *
from NSRP.outputs_simulation import *
import time

class Simulation(object):
    def __init__(self,hiperparams):
        self.hiperparams = hiperparams
        
    def __call__(self, params_cal):
   
        statististics_simulacion_dataframe=pd.DataFrame(index=self.hiperparams.statistics_name,columns=self.hiperparams.Seasonality_str)
        
        Dataframe_parametros = inputs_simulation(params_cal).params_cal
        
        
        Dataframe_parametros=allmonths(Dataframe_parametros)
        print('')
        print('')
        print('#'*80)
        print('Synthetic simulation')
        print('')
        print('')
		## We start with synthetic simulation and statistical calculations.
        
        if self.hiperparams.process=='normal':
            [Dataframe_simulacion_unido_hour_, Dataframe_simulacion_unido_day_, Intensidad_cellss, Duracion_horas_cellss]=\
            NSRP_simulation1(Dataframe_parametros, self.hiperparams.year_ini, self.hiperparams.year_fin, self.hiperparams.temporal_resolution, self.hiperparams.process, self.hiperparams.Seasonality)
            print('Total cumulative rainfall - Analytical estimation = ' + "{:15.2f}".format(np.sum(Intensidad_cellss*Duracion_horas_cellss)))
            print('Total cumulative rainfall -             Simulated = ' + "{:15.2f}".format(np.sum(Dataframe_simulacion_unido_day_.values)))
            
        elif self.hiperparams.process=='storms':

            Dataframe_parametros1=pd.DataFrame(index=['landa', 'ipsilon', 'eta', 'xi', 'betha'],columns=Dataframe_parametros.columns)
            for i in Dataframe_parametros.columns:
                Dataframe_parametros1.loc[:,i]=Dataframe_parametros.loc[:,i].values[0:5]

            Dataframe_parametros2=pd.DataFrame(index=['landa', 'ipsilon', 'eta', 'xi', 'betha'],columns=Dataframe_parametros.columns)
            for i in Dataframe_parametros.columns:
                Dataframe_parametros2.loc[:,i]=Dataframe_parametros.loc[:,i].values[5:]

            [Dataframe_simulacion_unido_hour_1, Dataframe_simulacion_unido_day_1, Intensidad_cellss1, Duracion_horas_cellss1]=\
            NSRP_simulation1(Dataframe_parametros1, self.hiperparams.year_ini, self.hiperparams.year_fin, self.hiperparams.temporal_resolution, 'normal', self.hiperparams.Seasonality)

            [Dataframe_simulacion_unido_hour_2, Dataframe_simulacion_unido_day_2, Intensidad_cellss2, Duracion_horas_cellss2]=\
            NSRP_simulation1(Dataframe_parametros2, self.hiperparams.year_ini, self.hiperparams.year_fin, self.hiperparams.temporal_resolution, 'normal', self.hiperparams.Seasonality)

			##Combino los dos processos
            Dataframe_simulacion_unido_hour_=pd.DataFrame(index=Dataframe_simulacion_unido_hour_1.index)
            Dataframe_simulacion_unido_hour_['Rain']=Dataframe_simulacion_unido_hour_1.values+Dataframe_simulacion_unido_hour_2.values
            Dataframe_simulacion_unido_day_=pd.DataFrame(index=Dataframe_simulacion_unido_day_2.index)
            Dataframe_simulacion_unido_day_['Rain']=Dataframe_simulacion_unido_day_1.values+Dataframe_simulacion_unido_day_2.values

            print('Total cumulative rainfall - Analytical estimation - Storm 1 = ' + "{:15.2f}".format(np.sum(Intensidad_cellss1*Duracion_horas_cellss1))) 
            print('Total cumulative rainfall - Analytical estimation - Storm 2 = ' + "{:15.2f}".format(np.sum(Intensidad_cellss2*Duracion_horas_cellss2)))  

            print('Total cumulative rainfall - Analytical estimation = ' + \
            "{:15.2f}".format(np.sum(Intensidad_cellss1*Duracion_horas_cellss1)+np.sum(Intensidad_cellss2*Duracion_horas_cellss2)))
            print('Total cumulative rainfall -             Simulated = ' + "{:15.2f}".format(np.sum(Dataframe_simulacion_unido_day_.values)))    


        #statististics_dataframe=allmonths(statististics_dataframe)
        #print('')
        #print('')
        #print('#'*80)
        #print('Results Validation')
        #print('')
        #print('')
        
        ## Real, adjusted and simulated statistical calculations.

        for pri, prii in enumerate(self.hiperparams.Seasonality):
            if self.hiperparams.temporal_resolution == 'd':
                Datos=Dataframe_simulacion_unido_day_.copy()
            elif self.hiperparams.temporal_resolution == 'h':
                Datos=Dataframe_simulacion_unido_hour_.copy()
            Datos[Datos['Rain']<0]=np.nan
            Datos[Datos['Rain']<0]=np.nan

            if len(self.hiperparams.Seasonality)==12:
             
                Datos['Estacionalidad']=Datos['Rain']*np.nan
                pos=np.where(Datos.index.month == prii); pos=pos[0]
                Datos['Estacionalidad'].iloc[pos]=Datos['Rain'].iloc[pos]
                Pluvio_GS = Datos['Estacionalidad'][Datos['Estacionalidad']>=0]
                Pluvio_GS[Pluvio_GS<0.001]=0
                Datos=Pluvio_GS.astype(float)
                
            else:
  
                Datos['Estacionalidad']=Datos['Rain']*np.nan
                for i, ii in enumerate(prii):
                    pos=np.where(Datos.index.month == ii); pos=pos[0]
                    Datos['Estacionalidad'].iloc[pos]=Datos['Rain'].iloc[pos]
                Pluvio_GS = Datos['Estacionalidad'][Datos['Estacionalidad']>=0]
                Pluvio_GS[Pluvio_GS<0.001]=0
                Datos=Pluvio_GS.astype(float)



            statististics_values_sintetico=calculate_statistics(Datos,self.hiperparams.statistics_name,self.hiperparams.temporal_resolution)
            statististics_simulacion_dataframe.loc[:,str(prii)]=statististics_values_sintetico  

        #statististics_simulacion_dataframe=allmonths(statististics_simulacion_dataframe)
        
        results = outputs_simulation(Dataframe_simulacion_unido_day_,Dataframe_simulacion_unido_hour_,statististics_simulacion_dataframe, self.hiperparams.temporal_resolution)

        return results
        
    # def save_files(self,results,path_output_files):
        
    #     results.Hourly_Simulation.to_csv(path_output_files+'Time_serie_hourly_simulated.csv')
    #     results.statististics_Simulated.to_csv(path_output_files+'statistic_hourly_simulated.csv')
    #     results.Daily_Simulation.to_csv(path_output_files+'Time_serie_day_simulated.csv')
