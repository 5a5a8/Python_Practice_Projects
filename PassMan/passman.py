from cryptography.fernet import Fernet
import base64
import bcrypt
import copy
import getpass
import hashlib
import os
import requests
import sys

#SETTINGS
master_file = 'master'
data_file = 'data'

# ~~~~~ start of classes for the types of data we are going to store ~~~~~
class Password:
	def __init__(self, identifier='Login', title=None, username=None, password=None, url=None, notes=None):
		self.identifier = identifier
		self.title = title
		self.username = username
		self.password = password
		self.url = url
		self.notes = notes
	
	def create_new(self):
		clear_screen()
		print('Creating new password entry\n')
		while True:
			self.title = input('Enter a title: ')
			self.username = input('Enter a username: ')
			self.password = input('Enter a password: ')
			self.url = input('Enter a URL: ')
			self.notes = input('Enter any notes: ')
			if check_for_pipe([self.title, self.username, self.password, self.url, self.notes]) == True:
				continue
			else:
				clear_screen()
				print('New login created\n')
				return [self.identifier, self.title, self.username, self.password, self.url, self.notes]

class CreditCard:
	def __init__(self, identifier='Credit Card', title=None, card_type=None, name_on_card=None, card_number=None, expiry=None, cvn=None, notes=None):
		self.identifier = identifier
		self.title = title
		self.card_type = card_type
		self.name_on_card = name_on_card
		self.card_number = card_number
		self.expiry = expiry
		self.cvn = cvn
		self.notes = notes

	def create_new(self):
		clear_screen()
		print('Creating new credit card type\n')
		while True:
			self.title = input('Enter a title: ')
			self.card_type = input('Enter a card type: ')
			self.name_on_card = input('Enter the name on the credit card: ')
			self.card_number = input('Enter the card number: ')
			self.expiry = input('Enter the expiry date: ')
			self.cvn = input('Enter the verification number: ')
			self.notes = input('Enter any notes: ')
			if check_for_pipe([self.title, self.name_on_card, self.card_number, self.expiry, self.notes]) == True:
				continue
			else:
				clear_screen()
				print('New credit card created\n')
				return [self.identifier, self.title, self.name_on_card, self.card_number, self.expiry, self.cvn, self.notes]
# ~~~~~ end of classes for the types of data we are going to store ~~~~~
		

# ~~~~~ start of helper functions ~~~~~
def clear_screen():
	print('\n' * 100)

def check_for_pipe(text):
	#we don't allow pipe | in user input since the data will be written to a pipe separated file
	if type(text) == str:
		if '|' in text:
			print('\nThe pipe symbol (|) was found in your input. This is not allowed. Support may be added later.')
			print('Try again.\n')
			return True
		else:
			return False
	elif type(text) == list:
		for item in text:
			return check_for_pipe(item)
# ~~~~~ end of helper functions ~~~~~

# ~~~~~ start of master account creation and authentication functions ~~~~~
def create_master_account():
	#we could just try unlock the data directly rather than authenticating separately using hashing, but I like this better
	clear_screen()
	print('Enter the credentials for the new master account')
	while True:
		username = input('Username: ')
		#password1 = input('Password: ')
		#password2 = input('Confirm Password: ')
		password1 = getpass.getpass('Password: ')
		password2 = getpass.getpass('Confirm Password: ')

		if password1 == password2:
			#hash and write to file
			salt = bcrypt.gensalt()
			hashed_password = bcrypt.hashpw(password1.encode('utf-8'), salt).hex()
			with open(master_file, 'w') as f:
				f.write(username + '\n')
				f.write(hashed_password)
				f.close()
			print('Master created successfully.')
			return get_key_from_pass(password1, hashed_password)
			break
		else:
			clear_screen()
			print('Passwords did not match.')

def edit_master_account():
	key = create_master_account()
	write_encrypted_data(copy.deepcopy(master_data), key)
	clear_screen()
	print('Credentials updated, data re-encrypted with new key\n')

def authenticate_master_account():
	#get credentials from file and compare to user input. If success, return a key from KDF
	clear_screen()
	print('Master account found, please authenticate.')
	with open(master_file) as f:
		user_and_hash = [s.rstrip('\n') for s in f.readlines()]
		f.close()

	while True:
		username = input('Username: ')
		#password = input('Password: ')
		password = getpass.getpass('Password: ')

		if username == user_and_hash[0] and bcrypt.checkpw(password.encode('utf-8'), bytes.fromhex(user_and_hash[1])):
			print('Authentication Success')
			return get_key_from_pass(password, user_and_hash[1])
		else:
			clear_screen()
			print('Invalid Credentials')
			continue
# ~~~~~ end of master account creation and authentication functions ~~~~~


# ~~~~~ start of functions for create, edit delete items ~~~~~
def create_new_item():
	clear_screen()
	while True:
		print('What item would you like to create?\n')
		print('1. Password')
		print('2. Credit Card')
		print('3. Go back')
		user_selection = input('\nEnter a number: ')
		if user_selection == '1':
			new_password = Password()
			master_data.append(new_password.create_new())
			write_encrypted_data(copy.deepcopy(master_data), key)
			return

		elif user_selection == '2':
			new_credit_card = CreditCard()
			master_data.append(new_credit_card.create_new())
			write_encrypted_data(copy.deepcopy(master_data), key)
			return

		elif user_selection == '3':
			clear_screen()
			return
		else:
			clear_screen()
			print('Please enter a valid selection\n')
			continue
		

def view_existing_items():
	def view_specific_item(item):
		clear_screen()

		#print each item in the entry e.g. username, password
		print('Viewing ' + item[0] + ' data for: ' + item[1] + '\n')
		if item[0] == 'Login':
			print('Username:  ' + item[2])
			print('Password:  ' + item[3])
			print('URL:       ' + item[4])
			print('Notes:     ' + item[5])
		
		elif item[0] == 'Credit Card':
			print('Name on Card:  ' + item[2])
			print('Card Number:   ' + item[3])
			print('Expiry:        ' + item[4])
			print('CVN:           ' + item[5])
			print('Notes:         ' + item[6])

		input('\nPress <ENTER> to go back')
		clear_screen()
		return

	clear_screen()
	while True:
		#show all saved entries
		print('  \tType\t'.ljust(20) + '\tTitle\n')
		for i in range(len(master_data)):
			print(str(i+1) + ':\t' +  master_data[i][0].ljust(20) + '\t' + master_data[i][1])

		print('\nEnter the number of the item you want to view')
		print('Enter E to edit an item, D to delete an item, or Q to go back')
		choice = input('\nInput: ')

		#view, edit, delete the selected item, go back, or error
		try:
			item_to_view = master_data[int(choice) - 1]
			view_specific_item(item_to_view)
		except:
			if choice.lower() == 'e':
				edit_existing_items()
			elif choice.lower() == 'd':
				delete_existing_items()
			elif choice.lower() == 'q':
				clear_screen()
				return
			else:
				clear_screen()
				print('Please enter a valid selection\n')
				continue
def edit_existing_items():
	def edit_specific_item(index):
		clear_screen()
		while True:
			#If the entry is a login, ask which field they want to update
			#then update that field in master_data and rewrite the encrypted data

			print('Now editing ' + master_data[index][0] + ' item with title: ' + master_data[index][1] + '\n')
			if master_data[index][0] == 'Login':
				print('1. Title\n2. Username\n3. Password\n4. URL\n5. Notes\n')
				choice = input('\nEnter a number or Q to go back: ')
				if choice in ['1', '2', '3', '4', '5']:
					new_val = input('\nEnter the new value: ')
					if check_for_pipe(new_val) == True:
						continue
					else:
						master_data[index][int(choice)] = new_val
						write_encrypted_data(copy.deepcopy(master_data), key)
						clear_screen()
						print('Item updated\n')
						return
				elif choice.lower() == 'q':
					clear_screen()
					return
				else:
					clear_screen()
					print('Invalid Input\n')
					continue
			#do the same for credit card
			elif master_data[index][0] == 'Credit Card':
				print('1. Title\n2. Name on Card\n3. Card Number\n4. Expiry\n5. CVN\n6. Notes')
				choice = input('\nEnter a number or Q to go back: ')
				if choice in [str(i) for i in range(1,7)]:
					new_val = input('\nEnter the new value: ')
					if check_for_pipe(new_val) == True:
						continue
					else:
						master_data[index][int(choice)] = new_val
						write_encrypted_data(copy.deepcopy(master_data), key)
						clear_screen()
						print('Item updated\n')
						return
				elif choice.lower() == 'q':
					clear_screen()
					return
				else:
					clear_screen()
					print('Invalid Input\n')
					continue
				

	while True:
		try:
			choice = input('Enter the number of the item to edit, Q to go back: ')
			edit_index = int(choice) - 1
			master_data[edit_index]
		except:
			if choice.lower() == 'q':
				clear_screen()
				return
			else:
				print('Invalid Selection\n')
				continue
		else:
			edit_specific_item(edit_index)
			clear_screen()
			print('Updated successfully\n')
			return
	
	#if Login, print 'which field would you like to update, username, password, url etc and then update that field
	#repeat for credit card
	
		
		

def delete_existing_items():
	#we find out which item the user wants to delete, delete from master_data, and rewrite the encrypted file
	while True:
		try:
			choice = input('Enter the number of the item to delete, Q to go back: ')
			delete_index = int(choice) - 1
			master_data[delete_index]
		except:
			if choice.lower() == 'q':
				clear_screen()
				return
			else:
				print('Invalid selection\n')
				continue
		else:
			continue_y_n = input('\nWARNING: This cannot be reversed. Continue? Y/N: ')
			if continue_y_n.lower() == 'y':
				del master_data[delete_index]
				write_encrypted_data(copy.deepcopy(master_data), key)
				clear_screen()
				print('Item deleted\n')
				return
			else:
				clear_screen()
				return
# ~~~~~ end of functions for create, edit, delete items ~~~~~

# ~~~~~ start of functions for data encryption ~~~~~
def get_key_from_pass(password, hashed_password):
	#extract the salt and convert from hex to bytes
	salt = bytes.fromhex(hashed_password[:58])
	
	#run password and salt through bcrypt KDF for 100 rounds to produce a 32 byte key, encoded as base64
	key = base64.urlsafe_b64encode(bcrypt.kdf(password.encode('utf-8'), salt, 32, 100))
	return key

def encrypt_all_data(plaintext_data, key): 
	#takes a list of strings and returns an encrypted list
	try:
		encryptor = Fernet(key)
		encrypted_data = []
		for line in plaintext_data:
			encrypted_data.append(encryptor.encrypt(bytes(line.encode('utf-8'))))
	except:
		print('An error occurred, possibly a problem with your key')
		print('Quitting...')
	else:
		return encrypted_data
		
def decrypt_all_data(ciphertext_data, key):
	#takes a list of ciphertext strings and converts to plaintext strings
	try:
		decryptor = Fernet(key)
		decrypted_data = []
		for line in ciphertext_data:
			decrypted_data.append(decryptor.decrypt(line))
	except: 
		print('An error occurred...\nProbably your key was incorrect - don\'t edit your master account file directly.')
		print('Quitting...')
		quit_program()
	else:
		return decrypted_data
# ~~~~~ end of functions for data encryption ~~~~~

# ~~~~~ start of functions for file I/O ~~~~~
def read_encrypted_data(key):
	#read the encrypted file
	try:
		with open(data_file, 'rb') as f:
			ciphertext = f.readlines()
			f.close()
	except:
		print('Data file not found...\nQuitting...')
		quit_program()

	#decrypt the file and split it out by pipe
	plaintext = decrypt_all_data(ciphertext, key)
	tidy_plaintext = [str(plaintext_line, 'utf-8').split('| ') for plaintext_line in plaintext]

	return tidy_plaintext

def write_encrypted_data(plaintext, key):
	#join by pipe
	for i in range(0, len(plaintext)):
		plaintext[i] = '| '.join(plaintext[i])
	
	#encrypt each string
	ciphertext_for_file = encrypt_all_data(plaintext, key)

	#add newline if not last item in list
	for i in range(0, len(ciphertext_for_file) - 1):
		ciphertext_for_file[i] = ciphertext_for_file[i] + b'\n'

	#write each line to file
	with open(data_file, 'wb') as f:
		for line in ciphertext_for_file:
			f.write(line)
		f.close()

# ~~~~~ end of functions for file I/O ~~~~~

# ~~~~~ start of functions for checking for breached passwords ~~~~~
def check_breached():
	clear_screen()
	#get all the SHA1 hashed passwords in a list (we need the first 5 chars to send to the api)
	count_breached = 0
	for entry in master_data:
		if entry[0] == 'Login':
			hashed_password = hashlib.sha1(entry[3].encode('utf-8')).hexdigest()

			#send first 5 chars of hash to api, they will return a list of breached hash suffixes
			try:
				response = requests.get('https://api.pwnedpasswords.com/range/' + hashed_password[:5])
			except:
				clear_screen()
				print('Something went wrong, do you have an internet connection?')
				return
			else:
				#get the hash suffix and append to the full hash. if it matches our hashed password earlier, we've been breached
				list_response = response.text.split('\r\n')
				for item in list_response:
					suffix = item.split(':')[0]
					full_hash = hashed_password[:5] + suffix
					if hashed_password.lower() == full_hash.lower():
						print('Password for Login entry ' + entry[1] + ' has been breached ' + item.split(':')[1] + ' times')
						count_breached += 1
	print('\nA total of', count_breached, 'breached passwords were found\n\n')
			


# ~~~~~ end of functions for checking for breached passwords ~~~~~

def quit_program():
	sys.exit()

def start_main_program(key):
	clear_screen()
	while True:
		print('1. Create New Item')
		print('2. View and Edit Existing Items')
		print('3. Check for Breached Passwords')
		print('4. Modify Master Credentials')
		print('5. Quit')
		user_selection = input('\n Enter a number: ')
		if user_selection == '1':
			create_new_item()
		elif user_selection == '2':
			view_existing_items()
		elif user_selection == '3':
			check_breached()
		elif user_selection == '4':
			edit_master_account()
		elif user_selection == '5':
			quit_program()
		else:
			clear_screen()
			print('Please enter a valid selection\n')
			continue

def main():
	try:
		open(master_file)
	except:
		create_master_account()
	else: 
		global key
		key = authenticate_master_account()

		global master_data
		master_data = read_encrypted_data(key)

		start_main_program(key)
		
		

if __name__ == '__main__':
	main()
