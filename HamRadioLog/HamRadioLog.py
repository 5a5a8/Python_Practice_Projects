#this tool provides logbook functionality for amateur radio.
#it should write to an Amateur Data Interchange Format (ADIF) file.

import sys
import time
import datetime
import pandas as pd

#prints out the existing profiles in profiles.txt
def print_existing_profiles():
	profiles = open('profiles.txt')
	i = 1
	for line in profiles:
		profile_data = line.split('| ')
		print('\tProfile: ' + str(i)) 
		print('\t\tCallsign: ' + profile_data[0])
		print('\t\tName: ' + profile_data[1])
		print('\t\tPreferred Tx Freq: ' + profile_data[2])
		print('\t\tPreferred Rx Freq: ' + profile_data[3])
		print('\t\tPreferred Mode: ' + profile_data[4])
		i += 1
	profiles.close()
	return

def edit_profiles():
	
	def add_new_profile():
		#appends a new profile to the profiles.txt
		print('\n'*100)
		print('Enter the details of the profile: ')
		callsign = input('\tCallsign: ')
		name = input('\tName: ')
		freq_out = input('\tTx Freq: ')
		freq_in = input('\tRx Freq: ')
		mode = input('\tOperating Mode: ')

		with open('profiles.txt', 'a') as f:
			f.write(callsign + '| ' + name + '| ' + freq_out + '| ' + freq_in + '| ' + mode + '\n')
			f.close()
		print('Changes written to profiles.txt\nReturning...')
		time.sleep(3)
		return


	#stored in pipe separated file as: callsign| name| freq out| freq in| mode
	def edit_existing_profile():
		def edit_specific_profile(line):
			#edits the profile once the user has specified a profile to edit

			profile_data = line.split('| ')
			print('\n'*100)
			print('Type a new value for each field. To keep the value as it is, press <enter> without typing anything\n')
			callsign = input('Callsign\n\tCurrent Value: ' + profile_data[0] + '\n\tNew Value: ')
			if callsign == '':
				callsign = profile_data[0]
			name = input('\nName\n\tCurrent Value: ' + profile_data[1] + '\n\tNew Value: ')
			if name == '':
				name = profile_data[1]
			freq_out = input('\nTx Freq\n\tCurrent Value: ' + profile_data[2] + '\n\tNew Value: ')
			if freq_out == '':
				freq_out = profile_data[2]
			freq_in = input('\nRx Freq\n\tCurrent Value: ' + profile_data[3] + '\n\tNew Value: ')
			if freq_in == '':
				freq_in = profile_data[3]
			mode = input('\nOperating Mode\n\tCurrent Value: ' + profile_data[4].rstrip('\n') + '\n\tNew Value: ')
			if mode == '':
				mode = profile_data[4]
			
			new_profile = callsign + '| ' + name + '| ' + freq_out + '| ' + freq_in + '| ' + mode
			if new_profile[-1] != '\n':
				return new_profile + '\n'
			else:
				return new_profile
		
		#read existing profiles into a list
		profiles = open('profiles.txt')
		lines = profiles.readlines()
		profiles.close()

		#which profile does the user want to edit
		while True:
			print('\n'*100)
			print_existing_profiles()
			print('\nEnter a profile number to edit, Q to go back')
			selection = input('\n>>> ')
			
			if (selection.isnumeric() and int(selection) in range(1, len(lines)+1)):
				new_profile = edit_specific_profile(lines[int(selection)-1])
				lines[int(selection)-1] = new_profile
				with open('profiles.txt', 'w') as f:
					for line in lines:
						f.write(line)
				print('Profile updated successfully\nReturning...')
				time.sleep(3)
				return
			elif selection.isalpha() and selection.lower() == 'q':
				return



	def delete_existing_profile():
		#read existing profiles into list
		profiles = open('profiles.txt')
		lines = profiles.readlines()
		profiles.close()

		while True:
			print('\n'*100)
			print_existing_profiles()
			print('\nEnter a profile number to delete, Q to go back')
			selection = input('\n>>> ')
			
			#if input is invalid, repeat the loop
			if (selection.isnumeric() and int(selection) not in range(1, len(lines)+1)) or (selection.isalpha() and selection.lower() != 'q'):
				continue
			elif selection.lower() == 'q':
				return
			else:
				del lines[int(selection) - 1]
				with open('profiles.txt', 'w') as f:
					for line in lines:
						f.write(line)
				print('Changes written, returning...')
				time.sleep(3)
				return
				


	while True:
		print('\n'*100)
		print_existing_profiles()

		#show options to user - add, edit, delete, go back
		print('\nWhat would you like to do?\n')
		print('\t1. Add a new profile')
		print('\t2. Edit an existing profile')
		print('\t3. Delete an existing profile')
		print('\t4. Go back')

		#get user input and call appropriate function
		selection = input('\n>>> ')
		if selection == '1':
			add_new_profile()
		elif selection == '2':
			edit_existing_profile()
		elif selection == '3':
			delete_existing_profile()
		elif selection == '4':
			return

def manual_log():
	
	log_file = open('contact_log.txt', 'a')

	#create new entry or go back
	while True:
		print('\n'*100, 'What would you like to do?\n\t1. Create new entry in logbook\n\t2. Go Back')
		selection = input('\n>>> ')
		if selection == '1':
			#get all the details of the entry. date time group must be formatted correctly, input cannot contain | symbol
			while True:
				try:
					dtg = input('Enter date time group (DD HHMMz Mon YY): ')
					time.strptime(dtg, '%d %H%Mz %b %y')
					break
				except:
					print('\n'*100, 'Invalid date format, must be zulu date time group')

			call_to = input('Callsign of contact: ')
			name_to = input('Name of contact: ')
			call_from = input('Your callsign: ')
			freq_out = input('Tx frequency: ')
			freq_in = input('Rx frequency: ')
			mode = input('Mode: ')
			notes = input('Notes: ')

			#don't allow pipe symbol as it is used as delimiter in the log file
			if '|' in dtg + call_to + name_to + call_from + freq_out + freq_in + mode + notes:
				print('\n\nError: One of your inputs contained the pipe symbol (|), this is not allowed\nGoing back...\n')
				time.sleep(5)
				continue

			#join inputs together to pipe separated values and write to file
			contact_log = '| '.join([dtg, call_to, name_to, call_from, freq_out, freq_in, mode, notes]) + '\n'
			log_file.write(contact_log)
			print('\nQSO written to log file contact_log.txt\n')
			time.sleep(3)

		elif selection == '2':
			log_file.close()
			return

def auto_log(profile):
	if profile == True:
		#the user wants to use an existing profile, but which one?
		profiles = open('profiles.txt')
		lines = profiles.readlines()
		profiles.close()

		while True:
			print('\n'*100)
			print_existing_profiles()
			print('\nEnter the number of the profile you want to use, or enter Q to go back')
			selection = input('\n\n>>> ')
			if selection.isnumeric() and int(selection) in range(1, len(lines)+1):
				selected_profile = lines[int(selection)-1].split('| ')
				
				#wait for the user to say they have made a new contact
				#when they do, we can autofill much of the log data from the profile they are using
				while True:
					print('\n'*100, 'Enter s to start a new contact, or press q to quit')
					new_contact = input('\n>>> ')
					if new_contact == 'q' or new_contact == 'Q':
						return
					elif new_contact == 's' or new_contact == 'S':
						dtg = datetime.datetime.strftime(datetime.datetime.utcnow(), '%d %H%Mz %b %y') 
						call_to = input('Callsign contacted: ')
						name_to = input('Name of contact: ')
						call_from = selected_profile[0]
						freq_out = selected_profile[2]
						freq_in = selected_profile[3]
						mode = selected_profile[4].rstrip('\n')
						notes = input('Notes: ')
						if '|' in call_to + name_to + notes:
							print('Error: pipe symbol (|) found in input')
							time.sleep(3)
							continue

						#join data to pipe sep values and append to file
						contact = '| '.join([dtg, call_to, name_to, call_from, freq_out, freq_in, mode, notes])
						with open('contact_log.txt', 'a') as f:
							f.write(contact + '\n')
							f.close()
						print('\n\nContact written to log')
						time.sleep(2)
	
			elif selection.isalpha() and selection.lower() == 'q':
				return

	#when the user doesn't use a profile, they will need to enter the contact data themselves except the time.
	elif profile == False:
		while True:
			print('\n'*100, 'Enter s to start a new contact, or q to quit')
			selection = input('\n>>> ')
			if selection == 'q' or selection == 'Q':
				return
			elif selection == 's' or selection == 'S':
				dtg = datetime.datetime.strftime(datetime.datetime.utcnow(), '%d %H%Mz %b %y')
				call_to = input('Callsign contacted: ')
				name_to = input('Name of contact: ')
				call_from = input('Your callsign: ')
				freq_out = input('Tx Freq: ')
				freq_in = input('Rx Freq: ')
				mode = input('Operating mode: ')
				notes = input('Notes: ')

				#pipe symbol not allowed in input
				if '|' in call_to + name_to + call_from + freq_out + freq_in + mode + notes:
					print('\n\nError: Pipe symbol (|) found in input, this is not allowed\nGoing back...\n')
					time.sleep(3)
					continue

				contact = '| '.join([dtg, call_to, name_to, call_from, freq_out, freq_in, mode, notes])
				with open('contact_log.txt', 'a') as f:
					f.write(contact + '\n')
					f.close()
				print('\n\nWrote contact to log file')
				time.sleep(2)


def view_log_file():
	print('\n'*100)
	df = pd.read_csv('contact_log.txt', sep = '|')
	pd.options.display.max_columns = len(df.columns)+2
	print(df)

	input('\n\nPress any key to return')

def sort_log_file():
	log_file = open('contact_log.txt')
	log_file_list = log_file.readlines()
	log_headers = log_file_list[0]
	log_lines = log_file_list[1:]
	log_file.close
	
	sorted_log = []
	for i in range(len(log_lines)):
		split_entry = log_lines[i].split('| ')
		date_time_group = time.strptime(split_entry[0], '%d %H%Mz %b %y')
		split_entry[0] = date_time_group
		sorted_log.append(split_entry)
	
	sorted_log.sort(key = lambda x: (x[0]))
	for i in range(len(sorted_log)):
		sorted_log[i][0] = time.strftime('%d %H%Mz %b %y', sorted_log[i][0])
		sorted_log[i] = '| '.join(sorted_log[i])
		
	sorted_log = [log_headers] + sorted_log
	with open('contact_log.txt', 'w') as f:
		for line in sorted_log:
			f.write(line)
		f.close()
	print('\n\nLog file sorted, returning...\n')
	time.sleep(3)

def main():
	#find out what the user wants to do and call the appropriate function
	while True:
		print('\n'*100, 'Welcome to HamRadioLog, please enter a number:\n')
		print('\t1. Add or edit your operating profiles')
		print('\t2. Log previously made QSOs')
		print('\t3. Start an operating session using an existing profile')
		print('\t4. Start an operating session without any profile')
		print('\t5. View the log file')
		print('\t6. Sort the log file by date')
		print('\t7. Quit')

		selection = input('\n>>> ')
		if selection == '1':
			edit_profiles()
		elif selection == '2':
			manual_log()
		elif selection == '3':
			auto_log(profile = True)
		elif selection == '4':
			auto_log(profile = False)
		elif selection == '5':
			view_log_file()
		elif selection == '6':
			sort_log_file()
		elif selection == '7' or selection == 'q' or selection == 'Q':
			print('Quitting...')
			sys.exit()

main()
