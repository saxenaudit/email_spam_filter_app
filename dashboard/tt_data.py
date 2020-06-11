import numpy as np 
import pandas as pd 

def get_data(product):
	df = pd.read_csv('StoreIndia.csv')
	df_ = df[df['Sub-Category']==product][['Profit','Sales','Order Date','Ship Date','City','State','latitude','longitude','Segment']]
	df_['Profit'] = round(df_['Profit'],2)
	df_['Sales']  = round(df_['Sales'],2)
	df_=df_.rename(columns={'Ship Date':'Date'})
	return df_
