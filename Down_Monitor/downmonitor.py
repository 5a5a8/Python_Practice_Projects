import requests
import time
from datetime import datetime

domains_file = 'domains.txt' 
time_interval = 30 

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
		return response.status_code == requests.codes.ok
	except: 
		domain_down(domain)
		return False
	

#if a domain goes down, log it and notify the user
def domain_down(domain):
	#log downtime to log file
	down_log = open('downlog.log', 'a')
	down_log.write(domain + ' was down at UTC: ' + datetime.utcnow().strftime('%Y %b %d %H:%M:%S') + '\n')
	down_log.close()



domains = get_domains(domains_file)
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


