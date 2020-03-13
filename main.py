import requests
import os, sys, glob
import pandas as pd
import numpy as np
import random
import time


import logging
logging.basicConfig(filename='test.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')

states = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DC", "DE", "FL", "GA", 
          "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", 
          "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", 
          "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", 
          "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]


user_agent_list = [
   #Chrome
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (Windows NT 5.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    #Firefox
    'Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1)',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 6.2; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)',
    'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)'
]

from bs4 import BeautifulSoup
from uszipcode import SearchEngine

class_name = "panel__panel___3Q2zW panel__white___19KTz colors__bgWhite___1stjL panel__bordered___1Xe-S panel__rounded___2etNE GenericStationListItem__station___1O4vF GenericStationListItem__clickable___30MZX"


price_name = "text__left___1iOw3 GenericStationListItem__price___3GpKP"
location_name = "GenericStationListItem__address___1VFQ3"
name_name = "header__header3___1b1oq header__header___1zII0 header__evergreen___2DD39 header__snug___lRSNK GenericStationListItem__stationNameHeader___3qxdy"
last_update_name = "ReportedBy__postedTime___J5H9Z"  #time
updated_by_name = "ReportedBy__user___gVNBF"		#who


headers = {'User-Agent': random.choice(user_agent_list)}

search = SearchEngine(simple_zipcode=True)
#res = search.by_state("Florida", returns=0)




for state in states:

	df_list = []

	res = search.by_state(state, returns=0)
	for i, zip_value in enumerate(res):

		print(f"Processing {zip_value.zipcode} in {state} #{i}/{len(res)} zipcodes")


		test = requests.get("https://www.gasbuddy.com/home?search=%d&fuel=1" % (int(zip_value.zipcode)), headers=headers)

		soup = BeautifulSoup(test.content, 'html.parser')


		container = soup.find_all('div', {"class":class_name})

		for gas_station in container:


			try: #make sure program doesnt crash

				location = gas_station.find_all("div", {"class":location_name})[0].contents  #contain address, br, and city,state

				assert len(location) == 3, f"location doesnt equal 3, {location}"

				name = gas_station.find_all("h3", {"class":name_name})[0].a.text
				id_value = gas_station.find_all("h3", {"class":name_name})[0].a["href"]

				try:
					price = gas_station.find_all("span", {"class":price_name})[0].text
					last_update = gas_station.find_all("span", {"class":last_update_name})[0].text
					updated_by = gas_station.find_all("span", {"class":updated_by_name})[0].text
					
					df_list.append([id_value, name, location[0], location[-1], state, zip_value.zipcode, price, last_update, updated_by])
					print(f"{id_value} {name} at {location} price:{price}, updated by: {updated_by} {last_update}")
				except IndexError:
					df_list.append([id_value, name, location[0], location[-1], state, zip_value.zipcode, None, None, None])
					#print(f"no gas price for {name} at {location}")
					#logging.warning(f"no gas price for {name} at {location}")

			except Exception as e:
				logging.warning(f"{gas_station} in {state} ERROR:{e}, skipping....")



		time.sleep(1) #please dont arrest me! i tried!!!


	pd.DataFrame(df_list, columns=["id_value", "name", "address", "city_state", "state", "zip_code", "price", "last_update_time", "updated_by"]).to_csv(f"{state}_gas.csv", index=False)

	