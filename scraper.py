# -*- coding: utf-8 -*-

import scraperwiki
import urllib2
from datetime import datetime
from bs4 import BeautifulSoup

# Set up variables
entity_id = "E5032_BLBC_gov"
url = "http://www.bexley.gov.uk/index.aspx?articleid=10819"

# Set up functions
def convert_mth_strings ( mth_string ):
	month_numbers = {'JAN': '01', 'FEB': '02', 'MAR':'03', 'APR':'04', 'MAY':'05', 'JUN':'06', 'JUL':'07', 'AUG':'08', 'SEP':'09','OCT':'10','NOV':'11','DEC':'12' }
	#loop through the months in our dictionary
	for k, v in month_numbers.items():
		#then replace the word with the number
		mth_string = mth_string.replace(k, v)
	return mth_string

# pull down the content from the webpage
html = urllib2.urlopen(url)
soup = BeautifulSoup(html)

# find all entries with the required class
blocks = soup.findAll('div', {'class':'even'})

for block in blocks:

	fileUrl = block.a['href']
	title = block.a.contents[0]
	
	# create the right strings for the new filename
	title = title.upper().strip()
	csvYr = title.split(' ')[2]
	csvMth = title.split(' ')[1][:3]
	csvMth = convert_mth_strings(csvMth);
		
	filename = entity_id + "_" + csvYr + "_" + csvMth
		
	todays_date = str(datetime.now())
		
	scraperwiki.sqlite.save(unique_keys=['l'], data={"l": fileUrl, "f": filename, "d": todays_date })
			
	print filename
