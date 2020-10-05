import requests
import time
from datetime import datetime
import smtplib

###SETTINGS###
domains_file = 'domains.txt' 
time_interval = 30							#check status every x seconds 
notify_at = 10								#email the user after the site has been down for x time intervals
gmail_username = 'example@gmail.com' 		#'allow less secure apps' should be set to yes in gmail settings
gmail_password = 'password123' 				#recommend using a dedicated account for security reasons
email_recipient = 'example@example.com' 	#who to notify if a site is down


#open the domains file and return data as a list
def get_domains(domains_file = 'domains.txt'):
	domains = open(domains_file)
	list_of_domains = [domain.rstrip('\n') for domain in domains.readlines()]
	domains.close()

	return list_of_domains

#send a request to a domain, return True if OK
def test_domain(domain):
	try:
		response = requests.get(domain)
		if response.status_code == requests.codes.ok:
			domains_down_time[domain] = 0
			return True
		else:
			domains_down_time[domain] += 1
			domain_down(domain)
			return False
	except: 
		domains_down_time[domain] += 1
		domain_down(domain)
		return False
	
	

#if a domain goes down, log it and notify the user
def domain_down(domain):
	#log downtime to log file
	down_log = open('downlog.log', 'a')
	down_log.write(domain + ' was down at UTC: ' + datetime.utcnow().strftime('%Y %b %d %H:%M:%S') + '\n')
	down_log.close()

	#if the domain has been down equal to specified number of allowed intervals, send an email to the user
	#we don't use > otherwise it will send more than one email
	if domains_down_time[domain] == notify_at:
		notify_user(domain)


def notify_user(domain):
	#start the smtp session
	#need to add better error catching here specific to smtplib
	print('[INFO] Notifying recipient of outage at ' + domain)
	try:
		smtp_notify = smtplib.SMTP('smtp.gmail.com', 587) 
		smtp_notify.ehlo()
		smtp_notify.starttls()
		smtp_notify.login(gmail_username, gmail_password)
		smtp_notify.sendmail(gmail_username, email_recipient, 'Subject: ' + domain + ' is down \n ')
		smtp_notify.quit()
	except:
		print('[FAIL] Failed to send email to recipient')
		return
	else:
		print(email_recipient + ' has been notified of the outage at ' + domain)

#list of domains
domains = get_domains(domains_file)

#dictionary of domains with down time
domains_down_time = {domain: 0 for domain in domains}

while True:
	#test each domain
	for domain in domains:
		status = test_domain(domain)
		if status == True:
			status = '[UP]  '
		elif status == False:
			status = '[DOWN]'
		print(status + ' ' + domain)
	time.sleep(time_interval)


