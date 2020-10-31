import os
import random
import re
import sys
import time

def clear_screen():
	if os.name == 'posix':
		os.system('clear')
	else:
		os.system('cls')

def get_data():
	#open the data file to be searched and return as a list
	try:
		with open('data.txt', 'r') as f:
			data = f.readlines()
			f.close
	except:
		print('Failed to open file: data.txt\n')
		sys.exit()
	else:
		for i in range(len(data)):
			data[i] = data[i].rstrip('\n')
		return data

def get_random_question():
	#choose a random question from the question bank.
	#the format of the questions file is like 'question delim answer' so we split by ' delim ' and return the Q and A in a list
	try:
		with open('questions.csv', 'r') as f:
			questions = f.readlines()
			f.close()
	except:
		print('Failed to open file: questions.csv')
		sys.exit()
	else:
		question_line = random.choice(questions).rstrip('\n')
		question = question_line.split(' delim ')[0]
		regex_answer = question_line.split(' delim ')[1]
		return [question, regex_answer]
	
def present_question(question, answer, data):
	#show the question to the user, along with the expected result (line) and match group
	#we will then prompt the user for an answer (a regex) and return that regex
	#we also return the expected data so that we can compare it against what the users regex returned
	print('\n\n\t' + question)
	print('\nExpected result:\n')
	padding = 10 + len(max(data, key=len)) #how much to pad our string in the output
	print('Line Returned'.ljust(padding, ' ') + 'Text Matched\n')

	#search for matches and print expected results table
	expected_data = []
	for line in data:
		matches = re.findall(answer, line)
		if matches:
			expected_data.append(line)
			print(line.ljust(padding, ' '), matches[0])
	

	regex_from_user = input('\nEnter your regular expression in the prompt\nR for random question, Q to quit\n\n>>> ')
	return [regex_from_user, expected_data]

def cmp_users_regex(regex, expected_data, data_to_search):
	actual_data = []

	print('\n\nActual result:\n')
	padding = 10 + len(max(data_to_search, key=len)) #how much to pad our string in the output
	print('Line Returned'.ljust(padding, ' ') + 'Text Matched\n')

	#search the file using the user's regex
	for line in data_to_search:
		matches = re.findall(regex, line)
		if matches:
			actual_data.append(line)
			print(line.ljust(padding, ' '), matches[0])

	#check against expected data
	if actual_data == expected_data:
		print('\n\nWell done, that was correct\n')
		print('Moving to next question at random...')
		time.sleep(3)
		return True
	else:
		print('\n\nSorry, try again\n')
		time.sleep(3)
		return False

def main():
	while True:
		clear_screen()
		data_to_search = get_data()
		question, answer = get_random_question()

		correct = False
		while not correct:
			regex_from_user, expected_data = present_question(question, answer, data_to_search)
			if regex_from_user.lower() == 'q':
				clear_screen()
				sys.exit()
			elif regex_from_user.lower() == 'r':
				break
			else:
				correct = cmp_users_regex(regex_from_user, expected_data, data_to_search)

if __name__ == '__main__':
	main()
