'''
Library containing classes for keeping the simulation output.

	Authors: 
        + Javier Díez Sierra
	    + Salvador Navas Fernández
        + Manuel del Jesus
    
'''

import pandas as pd

class outputs_simulation (object):
    def __init__(self,Dataframe_simulacion_unido_day_,Dataframe_simulacion_unido_hour_,statististics_simulacion_dataframe,temporal_resolution):
        self.Daily_Simulation        = Dataframe_simulacion_unido_day_
        self.Hourly_Simulation       = Dataframe_simulacion_unido_hour_
        self.statististics_Simulated = statististics_simulacion_dataframe
        self.temporal_resolution = temporal_resolution

    def save_files(self,path_output_files):
        self.Daily_Simulation.to_csv(path_output_files+'Time_serie_daily_simulated.csv')
        self.Hourly_Simulation.to_csv(path_output_files+'Time_serie_hourly_simulated.csv')
        if self.temporal_resolution == 'd':
            self.statististics_Simulated.to_csv(path_output_files+'statistic_daily_simulated.csv')
        elif self.temporal_resolution == 'h':
            self.statististics_Simulated.to_csv(path_output_files+'statistic_hourly_simulated.csv')
