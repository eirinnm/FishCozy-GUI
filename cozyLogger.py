
import csv
import time, datetime


class CozyLogger:

    
    def __init__(self,refreshRateSeconds=5):
        self.timeZero = int(time.time())
        self.date = str(datetime.datetime.fromtimestamp(self.timeZero).strftime('%Y%m%d_%H%M'))
        self.refreshRateSeconds = refreshRateSeconds  

    def logWriter (self, chambers): 

        timeOne = int(time.time())
        
        if(timeOne - self.timeZero >= self.refreshRateSeconds):
            temperatures=[round(chamber.temperature,1) for chamber in chambers]
            setpoints=[chamber.setpoint for chamber in chambers]

            with open (self.date+'CozyLog.csv','a') as csv_file:
                writer= csv.writer(csv_file)
                writer.writerow( [int(timeOne)] + temperatures + setpoints )
            
            self.timeZero= int(time.time())

            print('Logging...')


# ########################### EXAMPLE FOR ME ####################
#             import pandas as pd

#             df = pd.read_csv('path/to/csv.csv', delimiter='\t')
#             # this line creates a new column, which is a Pandas series.
#             new_column = df['AUTOWOGEN'] + 1
#             # we then add the series to the dataframe, which holds our parsed CSV file
#             df['NewColumn'] = new_column
#             # save the dataframe to CSV
#             df.to_csv('path/to/file.csv', sep='\t')