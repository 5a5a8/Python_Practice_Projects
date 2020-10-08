import re
import matplotlib.pyplot as plt

def import_data():
	#get the data file from the user and return as a list
	while True:
		data_file_name = input('Enter the name of the data file: ')
		try:
			data_file = open(data_file_name)
		except:
			print('Please enter a valid file name')
		else:
			return [data_item.rstrip('\n') for data_item in data_file.readlines()]

def clean_data(numbers_data):
	#clean out anything other than numbers from the data, remove empty strings
	
	#remove non-digits, strip leading and trailing zeros
	numbers_data[:] = [re.sub('\D', '', data_item).strip('0') for data_item in numbers_data]
	
	#remove empty strings from resulting list
	numbers_data = list(filter(lambda x: x != '', numbers_data))

	return numbers_data

def get_shortest_digits(numbers_data):
	#we will only go to the length of the shortest number in depth
	return len(sorted(numbers_data, key=len)[0])

def count_digit_occurrences(numbers_data, digit_index = 0):
	#counts how many times a given digit index (e.g. the first digit) was each number
	#initialise a dictionary of counts
	digit_counts = {i: 0 for i in range(1, 10)}

	#increment the count of each digit e.g. first digit
	for data_item in numbers_data:
		digit_counts[int(data_item[digit_index])] += 1
	
	return digit_counts

def calculate_percentages(digit_counts):
	total = sum([digit_counts[key] for key in digit_counts])
	digit_percentages = {key: 100 * digit_counts[key] / total for key in digit_counts}
	return digit_percentages

def output_result(digit_percentages):
	#print the result as a histogram with a line of benfords law overlaid on same plot
	#benford data to compare to
	benford = {1: 30.1, 2: 17.6, 3: 12.5, 4: 9.7, 5: 7.9, 6: 6.7, 7: 5.8, 8:5.1, 9: 4.6}

	keys = digit_percentages.keys()
	vals = digit_percentages.values()
	
	#plot the actual data
	plt.bar(keys, list(vals), label='Actual Data')
	plt.ylim(0, 100)
	plt.ylabel('Percentage')
	plt.xlabel('Digit')
	plt.xticks(list(keys))
	plt.title('Given Data vs. Benford Data')
	
	#plot the benford data
	plt.plot(benford.keys(), benford.values(), color = 'black', label = 'Benford Data')
	
	#set legend
	plt.legend(loc='upper right')

	plt.show()


def main():
	#import and clean the data 
	imported_data = clean_data(import_data())
	
	#find the number in the list that has the least digits
	shortest_number = get_shortest_digits(imported_data)

	#count the occurrences of the digits
	digit_percentages = calculate_percentages(count_digit_occurrences(imported_data))
		
	#print the result
	output_result(digit_percentages)

main()
