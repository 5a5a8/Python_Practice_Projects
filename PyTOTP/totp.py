import time
import hashlib

key = '9c688f3b7cf1728a08041ce9d4fa4c233585fd2b'

while True:
	timeRemaining = 30*(int(time.time()) // 30 + 1) - int(time.time())
	print("\n"*100,'\tTime to expiry: ', timeRemaining, 'seconds')


	#get the number of 30 second intervals since epoch in hex format
	timeInterval = int(time.time()) // 30
	hexTimeInterval = str(hex(timeInterval))[2:]

	#append the key to the time interval
	timeKeyPair = key + hexTimeInterval

	#string must be encoded before hashing
	fullHash = hashlib.sha1(timeKeyPair.encode('utf-8')).hexdigest()
	
	#get the last 4 bits as a decimal integer
	lastFourBits = int(fullHash[-1], 16)

	#use the last 4 bits as an index in the hash (dynamic truncation)
	rawCode = fullHash[2*lastFourBits:2*lastFourBits+8]
	print('\n\tCode: ' + str(int(rawCode, 16))[-7:-1] + '\n'*20)

	time.sleep(1)


