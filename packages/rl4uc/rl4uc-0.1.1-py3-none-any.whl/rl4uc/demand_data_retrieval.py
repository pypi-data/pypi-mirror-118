#!/usr/bin/env python

import pandas as pd
import os
import requests
import io
import dotenv

if __name__=="__main__":

	dotenv.load_dotenv('../.env')
	API_KEY = os.getenv('BMRS_KEY')

	RESULTS_DIR = 'data/demand_data'
	os.makedirs(RESULTS_DIR, exist_ok=True)

	UNIT_ID = 'WHILW-1' # specify the BM Unit ID to retrieve for

	COLUMNS = ['date', 'period', 'demand_mw']

	def get_demand_data(start_date, end_date, save_fn):
		date_range = pd.date_range(start_date, end_date).tolist()
		date_range = [f.strftime('%Y-%m-%d') for f in date_range]

		all_df = pd.DataFrame(columns=COLUMNS)

		for date in date_range:

			print(date)

			url = 'https://api.bmreports.com/BMRS/SYSDEM/v1?APIKey={}&FromDate={}&ToDate={}&ServiceType=csv'.format(API_KEY, start_date, end_date)
			response = requests.get(url, allow_redirects=True)
			df = pd.read_csv(io.StringIO(response.content.decode('utf-8'))).reset_index()

			# Rename columns
			df = df.rename(columns={'level_0': 'type', 'level_1': 'date', 'HDR': 'period', 'SYSTEM DEMAND': 'demand_mw'})

			# Get just ITSDO standing for Initial Transmission System Demand Outturn
			df = df[df.type=='ITSDO']

			# Reformat dates and periods
			df.date = pd.to_datetime(df.date, format='%Y%m%d')
			df.period = df.period.astype('int')

			df = df.filter(COLUMNS)

			all_df = all_df.append(df)

		all_df.to_csv(os.path.join(RESULTS_DIR, save_fn), index=False)

	get_demand_data('2019-01-01', '2019-12-31', 'demand_test.csv')
	get_demand_data('2015-01-01', '2018-12-31', 'demand_train.csv')
	
