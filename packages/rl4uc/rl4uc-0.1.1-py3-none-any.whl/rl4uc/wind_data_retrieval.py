#!/usr/bin/env python

import pandas as pd
import os
import requests
import io
import dotenv

if __name__=="__main__":

	dotenv.load_dotenv('../.env')
	API_KEY = os.getenv('BMRS_KEY')

	RESULTS_DIR = 'data/wind_data'
	os.makedirs(RESULTS_DIR, exist_ok=True)

	UNIT_ID = 'WHILW-1' # specify the BM Unit ID to retrieve for

	COLUMNS = ['Settlement Date', 'SP', 'Quantity (MW)']

	def get_wind_data(start_date, end_date, unit_id, save_fn):
		date_range = pd.date_range(start_date, end_date).tolist()
		date_range = [f.strftime('%Y-%m-%d') for f in date_range]
		all_df = pd.DataFrame(columns=COLUMNS)

		for date in date_range: 
		    url = 'https://api.bmreports.com/BMRS/B1610/v2?APIKey={}&SettlementDate={}&Period=*&ServiceType=csv&NGCBMUnitID={}'.format(API_KEY, date, unit_id)
		    response = requests.get(url, allow_redirects=True)
		    print(date, response.status_code)
		    df = pd.read_csv(io.StringIO(response.content.decode('utf-8')), header=1).filter(COLUMNS)
		    all_df = all_df.append(df)

		# Sort and rename cols
		all_df = all_df.sort_values(['Settlement Date', 'SP']).reset_index(drop=True)
		all_df = all_df.rename(columns={'Settlement Date': 'date', 'SP': 'period', 'Quantity (MW)': 'wind_mw'})

		# write to csv
		all_df.to_csv(os.path.join(RESULTS_DIR, save_fn))

	# Test data
	get_wind_data('2019-01-01', '2019-12-31', UNIT_ID, 'wind_test.csv')

	# Training data
	get_wind_data('2015-01-01', '2018-12-31', UNIT_ID, 'wind_train.csv')
