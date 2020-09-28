import itertools
import sys
import hashlib
import string

class AttackSettings:
	def __init__(self, attackMode=1, hashType=1, saltTrueFalse=False, dictFile=None, hashFile=None):
		self.attackMode = self.getAttackMode()
		self.hashType = self.getHashType()
		self.saltTrueFalse = self.getSaltStatus()
		if 'Dictionary' in self.attackMode.values():
			self.dictFile = self.getDictionaryFile()
		else:
			self.dictFile = None
		self.hashFile = self.getHashFile()
		self.proceedTrueFalse = self.confirmSettings()

	def getAttackMode(self):
		#get the attack mode from the user. 1=brute force, 2= dictionary, 3=mask, no input = default (bruteforce)
		#we return a dictionary with key=number of attack mode, and value=description of attack mode
		
		allowedModes = {'1': 'Brute Force', '2': 'Dictionary', '3': 'Mask'}
		while True:
			
			print(' Please enter an attack mode:\n\n')
			for modes in allowedModes:
				print('\t' + modes + '. ' + allowedModes[modes])
			mode = input('\n >>> ')
			if mode not in allowedModes:
				print('\n'*50, 'Please enter a valid choice\n')
				continue
			
			return {mode : allowedModes[mode]}

	def getHashType(self):
		#get the hashtype from the user, return a dictionary with the hash number and hash type

		allowedHashes = {'1': 'MD5', '2': 'SHA1', '3': 'SHA2'}
		while True:
			print(' Which type of hash are you trying to crack?\n')
			for hashType in allowedHashes:
				print('\t' + hashType + '. ' + allowedHashes[hashType])
			selectedHash = input('\n >>> ')
			if selectedHash not in allowedHashes:
				print('\n'*50, 'Please enter a valid choice\n')
				continue
			
			return {selectedHash : allowedHashes[selectedHash]}

	def getSaltStatus(self):
		#we need to find out if the hashes have salts, if yes, we'll append the salt to the password later
		while True:
			print(' Do your hashes have salts?\n\n\t1. Yes\n\t2. No\n')
			saltStatus = input(' >>> ')
			if saltStatus not in ['1', '2']:
				print('\n'*50, 'Please enter a valid choice\n')
				continue
			elif saltStatus == '1':
				return True
			elif saltStatus == '2':
				return False

	def getDictionaryFile(self):
		#should only be called in dictionary attack mode
		#note that this only returns the filename, not the file object
		while True:
			print(' Please enter the dictionary filename:\n\n')
			filename = input(' >>> ')
			try:
				dictionaryFile = open(filename)
			except:
				print('\n'*50, 'Failed to open file, please enter a valid file name')
				continue
			else:
				dictionaryFile.close()
				return filename
			
	def getHashFile(self):
		#get the filename of the hashfile
		while True:
			print(' Please enter the name of the file containing the hashes:\n\n')
			filename = input(' >>> ')
			try:
				hashFile = open(filename)
			except:
				print('\n'*50, 'Failed to open file, please enter a valid file name')
			else:
				hashFile.close()
				return filename
	
	def confirmSettings(self):
		#confirm the settings with the user and return true if the wish to proceed
		print('\n'*50, ' You have selected the following settings:\n')
		print('Attack Mode: ', self.attackMode)
		print('Hash Type: ', self.hashType)
		print('Salts: ', self.saltTrueFalse)
		print('Dictionary File: ', self.dictFile)
		print('Hash File: ', self.hashFile)
		print('\n\nPress Y to continue, or any other key to quit:\n')
		proceed = input(' >>> ')
		if proceed == 'y' or proceed == 'Y':
			return True
		else:
			print('Exiting...')
			sys.exit()




#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#
class Attacks:
	def getHashList(self, hashFile):
		#this gets a list of hashes from the text file
		#at the moment it just does one hash and only a hash on each line
		#eventually add functionality to extract the hash from each line so usernames etc can be stored in the file
		print('Opening hashes file...')
		hashes = open(hashFile)
		hashesList = hashes.read().split('\n')
		hashes.close()
		return hashesList


	def dictionaryAttack(self, dictFile, hashFile, hashFunc, salt=False):
		#we use the set of hashes as we don't need to search the entire list that way
		#we find the hash:password pairs, and then we can append the passwords to ALL of the matching hashes later
		print('Starting dictionary attack...')
		print('Opening dictionary file...')
		passes = open(dictFile)
		hashesList = self.getHashList(hashFile)
		hashesSet = set(hashesList)
		countUniqueHashes = len(hashesSet)

		crackedCount = 0
		print('Cracking hashes...\nCracked', crackedCount, '/', countUniqueHashes, 'unique hashes')
		
		for password in passes:
			password = password.rstrip('\n')
			if hashFunc(password.encode('utf-8')).hexdigest() in hashesSet:
				crackedCount += 1
				self.crackedPass(password, crackedCount, countUniqueHashes, hashFunc)

		print('Dictionary exhausted, cracking is complete.\nCracked', crackedCount, '/', countUniqueHashes, 'unique hashes')
		passes.close()
		return


	def bruteForce(self, hashFile, hashFunc):
		print(' Enter charset:\n\n')
		charset = input(' >>> ')
		while True:
			print(' Enter max password length: ')
			length = input(' >>> ')
			try:
				int(length)
			except:
				print('Please enter a valid length\n')
				continue
			else:
				break

		hashList = self.getHashList(hashFile)
		hashSet = set(hashList)
		countUniqueHashes = len(hashSet)
		countCracked = 0
		def brute(hashSet, countCracked, hashFunc, charset = string.printable, length = 10, curString = ''):
			if len(curString) == length:
				return
			for char in charset:
				passGuess = curString + char
				if hashFunc(passGuess.encode('utf-8')).hexdigest() in hashSet:
					countCracked += 1
					self.crackedPass(passGuess, countCracked, len(hashSet), hashFunc)
				brute(hashSet, countCracked, hashFunc, charset, length, passGuess)

		brute(hashSet, countCracked, hashFunc, charset, int(length))


	def crackedPass(self, password, crackedCount, countUniqueHashes, hashFunc):
		#we count the number of cracked passwords so far, and append the password and hash to a new file
		crackedFile = open('cracked.text', 'a')
		crackedFile.write((hashFunc(password.rstrip('\n').encode('utf-8')).hexdigest()) + ': ' + password)
		print('Successfully cracked password: ' + password + '\n')
		print('Continuing...')
		crackedFile.close()
		return







#get the settings from the user
settings = AttackSettings()

#start the attack based on the settings
#eventually need to put this in the Attacks __init__()
attack = Attacks()
if settings.hashType == {'1': 'MD5'}:
	hashFunc = hashlib.md5
elif settings.hashType == {'2': 'SHA1'}:
	hashFunc = hashlib.sha1
elif settings.hashType == {'3': 'SHA2'}:
	hashFunc = hashlib.sha2


if settings.attackMode == {'1': 'Brute Force'}:
	attack.bruteForce(settings.hashFile, hashFunc)
if settings.attackMode == {'2': 'Dictionary'}:
	attack.dictionaryAttack(settings.dictFile, settings.hashFile, hashFunc, settings.saltTrueFalse)

