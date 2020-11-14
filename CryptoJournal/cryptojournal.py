#!/usr/bin/python

import bcrypt
import dropbox
import getpass
import os
import sys
import tarfile
import time

from Crypto import Random
from Crypto.Cipher import AES

class Crypto:

	def encrypt(infile: str, outfile: str) -> str:
		"""Encrypts a file and removes the file passed to it"""
		
		#get the plaintext file, read as bytes
		with open(infile, 'rb') as f:
			pt_filebytes = b''.join(f.readlines())
			f.close()
		
		#we need to pad the plaintext to the aes block size
		#we also need the key and an initialisation vector
		pt_filebytes = Crypto.pad(pt_filebytes)
		aes_iv = Random.new().read(aes_initv_len)
		key = Helpers.derive_key()

		#encrypt our data, the IV will be stored with the ciphertext
		#so that we can decrypt it later
		aes_cipher = AES.new(key, AES.MODE_CBC, aes_iv)
		ct_filebytes = aes_iv + aes_cipher.encrypt(pt_filebytes)

		with open(outfile, 'wb') as f:
			f.write(ct_filebytes)
			f.close()

		os.remove(infile)
		return outfile


	def decrypt(infile: str, outfile: str) -> str:
		"""Decrypts a file and removes the file passed to it"""
		
		with open(infile, 'rb') as f:
			ct_filebytes = b''.join(f.readlines())
			f.close()

		#retrieve the initialisation vector
		aes_iv = ct_filebytes[:aes_initv_len]
		key = Helpers.derive_key()

		aes_cipher = AES.new(key, AES.MODE_CBC, aes_iv)
		pt_filebytes = aes_cipher.decrypt(ct_filebytes[aes_initv_len:])
		pt_filebytes = Crypto.unpad(pt_filebytes)

		with open(outfile, 'wb') as f:
			f.write(pt_filebytes)
			f.close()

		os.remove(infile)
		return outfile
		

	def pad(s):
		padding = (aes_bs - len(s) % aes_bs) * chr(aes_bs - len(s) % aes_bs)
		padding = padding.encode('utf-8')
		return s + padding

	def unpad(s):
		return s[:-ord(s[len(s) - 1:])]

class Archive:
	
	def compress() -> str:
		"""Sends all .md files to a .tar.gz file, returns outfile name"""

		#we only want the markdown files
		mdfiles = []
		for filename in os.listdir():
			if filename.lower().endswith('.md'):
				mdfiles.append(filename)
		
		outfile_name = journal_name + '.tar.gz'
		with tarfile.open(outfile_name, 'w:gz') as outfile:
			for mdfile in mdfiles:
				outfile.add(mdfile)
			outfile.close()

		#remove the md files, keep just the archive
		for mdfile in mdfiles:
			os.remove(mdfile)

		return outfile_name
		

	def extract(infile_name: str):
		"""Extracts an archive and then removes it"""

		with tarfile.open(infile_name, 'r:gz') as infile:
			infile.extractall()
			infile.close()
		
		os.remove(infile_name)
		

class Remote:
	
	def send_to_dropbox(infile: str) -> bool:
		"""Sends a file to dropbox""" 
		
		#to authenticate to dropbox
		print('Retrieving Dropbox token from ' + dbxfile)
		with open(dbxfile, 'r') as f:
			dbx_token = f.readlines()[0].rstrip('\n')
			f.close()
		dbx = dropbox.Dropbox(dbx_token)
		try:
			print('Authenticating to Dropbox')
			dbx.users_get_current_account()
		except:
			print('Dropbox authentication failed\n') 
			sys.exit()
		else:
			print('Authentication success')

		#try to send the file to dropbox
		print('Writing ' + infile + ' to Dropbox')
		with open(infile, 'rb') as f:
			dbx_mode = dropbox.files.WriteMode('overwrite')
			try:
				dbx.files_upload(f.read(), dbx_backuppath, mode=dbx_mode)
			except:
				print('Failed to send file to Dropbox')
			else:
				print('Encrypted journal sent to Dropbox')

		os.remove(infile)
		
	def get_from_dropbox():
		"""Gets a file from dropbox"""

		print('Retrieving Dropbox token from ' + dbxfile)
		with open(dbxfile, 'r') as f:
			dbx_token = f.readlines()[0].rstrip('\n')
			f.close()
		dbx = dropbox.Dropbox(dbx_token)
		try:
			print('Authenticating to Dropbox')
			dbx.users_get_current_account()
		except:
			print('Dropbox authentication failed\n')
			sys.exit()
		else:
			print('Authentication success')

		print('Retrieving journal from Dropbox')
		outfile = journal_name + '.aes'
		with open(outfile, 'wb') as f:
			meta, res = dbx.files_download(path = dbx_backuppath)
			f.write(res.content)
			f.close()
		return outfile
			

class Helpers:
	
	def show_help():
		"""Prints basic usage information"""

		msg = """
			--init
				Initialises the necessary files.
				We need a password, dropbox token, and journal name.

			--push
				Archive all *.md files in the directory and encrypt.
				The encrypted file will be sent to Dropbox.
				This will remove *.md files when done.
				
			--pull
				The inverse of push.
				The encrypted journal will be retrieved from Dropbox.
				It will then be decrypted and decompressed.

			--localpush
				Same as --push, but doesn't send anything to Dropbox.

			--localpull
				Same as --pull, but doesn't retrieve from Dropbox.
				
			--help
				Prints this help message
		"""
		print(msg)
	
	def initialise():
		"""Gets password and dropbox information from the user"""

		#check if the directory is already intialised
		try:
			open(initfile)
		except:
			#password creation
			password1 = getpass.getpass('Enter a password: ')
			password2 = getpass.getpass('Confirm password: ')
			if password1 != password2:
				print('Passwords did not match\n')
				sys.exit()

				
			#otherwise, hash it and store
			salt = bcrypt.gensalt(bcrypt_logrounds)
			hash = bcrypt.hashpw(password1.encode('utf-8'), salt).hex()
			with open(initfile, 'w') as f:
				f.write(hash)
				f.close()

			#get drive credentials from user and journal name
			dbx_token = input('Paste your DropBox Token: ')
			journal_name = input('Enter a name for the journal: ')
			with open(dbxfile, 'w') as f:
				f.write(dbx_token)
				f.write('\n')
				f.write(journal_name)
				f.close()

		else:
			print('Directory is already initialised.')
			sys.exit()

	def derive_key():
		"""Gets a key for encryption and decryption"""

		password = getpass.getpass('Enter your password: ')
		with open(initfile) as f:
			hash = f.readlines()[0]
			f.close()
		if bcrypt.checkpw(password.encode('utf-8'), bytes.fromhex(hash)):
			salt = bytes.fromhex(hash[:58]) #bcrypt first 58 is salt
			password = password.encode('utf-8')
			key = bcrypt.kdf(password, salt, bcrypt_keylen, bcrypt_kdf_rounds)
			return key
		else:
			print('Invalid Password\n')
			sys.exit()
			


def main():

	try:
		sys.argv[1]
	except:
		print('No arguments supplied, use --help')
		sys.exit()

	if sys.argv[1] == '--init':
		Helpers.initialise()

	elif sys.argv[1] == '--push':
		print('Archiving .md files')
		archive_name = Archive.compress()
		print('Encrypting with AES 256')
		aes_file = Crypto.encrypt(archive_name, archive_name + '.aes')
		Remote.send_to_dropbox(aes_file)

	elif sys.argv[1] == '--pull':
		aes_file = Remote.get_from_dropbox()
		print('Decrypting journal')
		tar = Crypto.decrypt(aes_file, aes_file.rstrip('.aes'))
		print('Extracting data')
		Archive.extract(tar)

	elif sys.argv[1] == '--localpush':
		print('Archiving .md files')
		archive_name = Archive.compress()
		print('Encrypting with AES 256')
		aes_file = Crypto.encrypt(archive_name, archive_name + '.aes')

	elif sys.argv[1] == '--localpull':
		print('Decrypting journal')
		aes_file = journal_name + '.tar.gz.aes'
		tar = Crypto.decrypt(aes_file, aes_file.rstrip('.aes'))
		print('Extracting data')
		Archive.extract(tar)

	elif sys.argv[1] == '--help':
		Helpers.show_help()

	else:
		print('Invalid argument, use --help')


if __name__ == '__main__':
	global initfile
	initfile = '.initfile'

	global dbxfile
	dbxfile = '.dbx'

	global bcrypt_logrounds
	bcrypt_logrounds = 15

	global bcrypt_kdf_rounds
	bcrypt_kdf_rounds = 1000

	global bcrypt_keylen
	bcrypt_keylen = 32 #generated by bcrypt and used for AES256

	global aes_initv_len
	aes_initv_len = 16 #AES uses 128 bit initalisation vector

	global aes_bs
	aes_bs = 16 #AES uses 128 bit block size

	global dbx_backuppath
	global journal_name
	try:
		open(initfile)
		open(dbxfile)
	except:
		if len(sys.argv) > 1 and sys.argv[1] == '--init':
			main()
		else:
			print('Directory is not initialised. Use --init')
		sys.exit()
	else:
		with open(dbxfile, 'r') as f:
			journal_name = f.readlines()[1].rstrip('\n')
			dbx_backuppath = '/' + journal_name
			f.close()

	main()
