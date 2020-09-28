#!/usr/bin/python
#calulate the number of days until the next crate day

import datetime
import time

def finalHTML(days_to, crate_date):
	print('Content-Type: text/html')
	print()
	print('<title>Days until Crate Day</title>')
	print('<center>')	
	if days_to == 0:
		print('<H1>Crate Day is Today!</H1>')
	else:
		print('<H1>The next Crate Day is on', str(crate_date.day), ' / ', str(crate_date.month), ' / ', str(crate_date.year), '</H1>')
		print('<H1>There are', str(days_to), 'days until the next Crate Day</H1>')
	print('</center>')
#get the date of this year's crate day (the first Saturday of December) as well as next year's
current_year = int(time.time()) // (365 * 24 * 60 * 60) + 1970
crate_date = datetime.date(current_year, 12, 1)
crate_date_next = datetime.date(current_year + 1, 12, 1)

while crate_date.weekday() != 5:
	crate_date += datetime.timedelta(days = 1)

while crate_date_next.weekday() != 5:
	crate_date_next += datetime.timedelta(days = 1)

crate_date = str(crate_date)
crate_date_next = str(crate_date_next)


#get todays date
todays_date = str(datetime.datetime.today()).split()[0]

#for testing
#todays_date = '2020-12-5'

#get all dates as same-formatted date objects
todays_date = (datetime.datetime.strptime(todays_date, '%Y-%m-%d')).date()
crate_date = (datetime.datetime.strptime(crate_date, '%Y-%m-%d')).date()
crate_date_next = (datetime.datetime.strptime(crate_date_next, '%Y-%m-%d')).date()

#if today is crate day, say so
if todays_date == crate_date:
	days_to_crate_day = 0
	finalHTML(days_to_crate_day, crate_date)
elif todays_date < crate_date:
	#get the days until this years crate day
	days_to_crate_day = (crate_date - todays_date).days
	finalHTML(days_to_crate_day, crate_date)
elif todays_date > crate_date:
	#get the days until next years crate day
	days_to_crate_day = (crate_date_next - todays_date).days
	finalHTML(days_to_crate_day, crate_date_next)

