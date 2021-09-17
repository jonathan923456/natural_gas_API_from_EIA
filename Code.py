#import librarires

import pandas as pd 
import requests
import numpy as np
import matplotlib.pyplot as plt 
from datetime import date
import matplotlib.ticker as ticker
import xlsxwriter

#Getting data from EIA

api_key = 'Get your API key from https://www.eia.gov/opendata/' #just need to register

#column names
column_names = ['Dry Gas Production','Gas Consumption','Net Import','Gas Net Withdrawal from Storage','Henry Hub Futures']

# Enter all your Series IDs here
gas_key = ['NG.N9070US1.M','NG.N9140US1.M','NG.N9180US1.M','NG.N9220US1.M','NG.RNGC1.M']

final_data = [] #to store all the data

#choose the start and end date in format yyyy-mm-dd
start_date = '2001-01-01'
end_date = '2021-12-01'

for i in range(len(gas_key)):
    r = requests.get('http://api.eia.gov/series/?api_key=' + api_key + '&series_id=' + gas_key[i])
    gas_json = r.json()
        df = pd.DataFrame(gas_json.get('series')[0].get('data'), columns = ['Date', column_names[i]])
    df.set_index('Date', drop=True, inplace=True)
    final_data.append(df)
    
# Combine all the data into one dataframe and create date as datatype
natural_gas_bcf = pd.concat(final_data, axis=1)
natural_gas_bcf['Year'] = natural_gas_bcf.index.astype(str).str[:4]
natural_gas_bcf['Month'] = natural_gas_bcf.index.astype(str).str[4:]
natural_gas_bcf['Day'] = 1
natural_gas_bcf['Date'] = pd.to_datetime(natural_gas_bcf[['Year','Month','Day']])
natural_gas_bcf.set_index('Date',drop=True,inplace=True)
natural_gas_bcf.sort_index(inplace=True)
natural_gas_bcf = natural_gas_bcf[start_date:end_date]
natural_gas_bcf = natural_gas_bcf.iloc[:,:5]
natural_gas_bcf

# Export data to excel
outpath = 'Location/US_Natural_Gas_EIA.xlsx'
writer = pd.ExcelWriter(outpath, engine= 'xlsxwriter')
natural_gas_bcf.to_excel(writer, sheet_name = 'Summary', index = True)
writer.save()
