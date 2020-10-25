import numpy as np
import sys
from PIL import Image

def encode_steg(infile, secret, outfile):
	#open the image file and check if RGB or RGBA
	print('[INFO ]: Reading input file')
	img = Image.open(infile, 'r')
	img_width, img_height = img.size
	img_data_array = np.array(list(img.getdata()))

	if img.mode == 'RGB':
		n = 3
		m = 0
	elif img.mode == 'RGBA':
		n = 4
		m = 1
	
	#check if the infile is large enough to hold our data
	total_pixels_infile = img_data_array.size // n
	required_pixels = len(secret)

	if required_pixels > total_pixels_infile:
		print('[ERROR]: Image does not contain enough pixels to hide your data. Use a larger image or less data')
		sys.exit()
	
	#start writing the data to the LSB
	print('[INFO ]: Modifying LSB with hidden data')
	index = 0
	for i in range(total_pixels_infile):
		for j in range(m, n):
			if index < required_pixels:
				img_data_array[i][j] = int(bin(img_data_array[i][j])[2:9] + secret[index], 2)
				index += 1
	
	#reshape the array and write to outfile
	print('[INFO ]: Writing data to outfile')
	img_data_array = img_data_array.reshape(img_height, img_width, n)
	new_image = Image.fromarray(img_data_array.astype('uint8'), img.mode)
	new_image.save(outfile)
	print('[INFO ]: New image successfully written: ' + outfile)
	return

def decode_steg(infile, outfile):
	#we start of with pretty much the same as the encode function. open the image and check the mode, etc
	print('[INFO ]: Reading input file for decoding')
	img = Image.open(infile, 'r')
	img_width, img_height = img.size
	img_data_array = np.array(list(img.getdata()))

	if img.mode == 'RGB':
		n = 3
		m = 0
	elif img.mode == 'RGBA':
		n = 4
		m = 1
	
	total_pixels_infile = img_data_array.size // n

	#extract the least significant bits
	print('[INFO ]: Extracting the least significant bits from file')
	lsb_bits = ''
	for i in range(total_pixels_infile):
		for j in range(m, n):
			lsb_bits += (bin(img_data_array[i][j])[2:][-1])

	#check for the delimitter. if not found, just dump all the data to a file
	if file_delimiter in lsb_bits:
		print('[INFO ]: A file has been found')
		
		#we only need up to the delimitter
		delimiter_index = lsb_bits.index(file_delimiter)
		lsb_bits = lsb_bits[:delimiter_index]

		#convert from string to writeable bytes and write to outfile
		print('[INFO ]: Writing file to outfile')
		file_bytes = bytes([int(lsb_bits[i:i+8], 2) for i in range(0, len(lsb_bits), 8)])
		with open(outfile, 'wb') as f:
			f.write(file_bytes)


	elif message_delimiter in lsb_bits:
		print('[INFO ]: A message has been found')
		delimiter_index = lsb_bits.index(message_delimiter)
		lsb_bits = lsb_bits[:delimiter_index]
		lsb_bits = [lsb_bits[i:i+8] for i in range(0, len(lsb_bits), 8)]
		message = ''
		for i in range(len(lsb_bits)):
			message += chr(int(lsb_bits[i], 2))

		print('[INFO ]: Writing message to outfile')
		with open(outfile, 'w') as f:
			f.write(message)
		print('\n\n---START STEGANOGRAPHIC MESSAGE---')
		print(message)
		print('---END STEGANOGRAPHIC MESSAGE---')
		

	else:
		#nothing found so just dump the lsb to a file
		print('[INFO ]: No hidden data was found, dumping data to outfile for analysis')
		lsb_bits = [lsb_bits[i:i+8] for i in range(0, len(lsb_bits), 8)]
		message = ''
		for i in range(len(lsb_bits)):
			message += hex(int(lsb_bits[i], 2))[2:]
		
		with open(outfile, 'w') as f:
			f.write(message)


	


def get_data_from_user():
	#returns a binary string of the data that will be hidden

	data_to_hide = input('\n\n\tEnter the name of the file to hide or enter a secret message\n\n>>> ')
	
	try:
		data_file = open(data_to_hide, 'rb')
	except:
		#user entered a message, convert to binary
		message_binary = ''.join([format(ord(i), '08b') for i in data_to_hide])
		return message_binary + message_delimiter
		
	else:
		#user entered a filename, read and convert to binary
		data_file_binary = ''
		data_file_bytes = bytearray(data_file.read())
		for i in data_file_bytes:
			data_file_binary += str('{:08b}'.format(i))
		return data_file_binary + file_delimiter

def main():
	#secret_data = get_data_from_user()
	#encode_steg('image.png', secret_data, 'image_steg.png')
	#decode_steg('image_steg.png', 'steg.dump')

	while True:
		user_input = input('\n\nWhat would you like to do?\n\t1. Encode\n\t2. Decode\n\t3. Quit\n\n>>> ')
		if user_input == '1':
			infile = input('\nEnter the name of the infile e.g. image.png\n>>> ')
			outfile = input('\nEnter the name of the outfile e.g. image_steg.png\n>>> ')
			try:
				open(infile)
			except:
				print('\nInfile not found\n')
				continue
			else:
				secret_data = get_data_from_user()
				encode_steg(infile, secret_data, outfile)

		elif user_input == '2':
			infile = input('\nEnter the name of the infile (containing hidden data)\n>>> ')
			outfile = input('\nEnter the name of the outfile e.g. message.txt, file.zip\n>>> ')
			try:
				open(infile)
			except:
				print('\nInfile not found\n')
				continue
			else:
				decode_steg(infile, outfile)

		elif user_input == '3':
			sys.exit()

		else:
			print('Invalid Input\n')
			continue

if __name__ == '__main__':
	global message_delimiter 
	message_delimiter = ''.join([format(ord(i), '08b') for i in '$$#212M3s']) #will be appended to the data so we know when to stop

	global file_delimiter
	file_delimiter = ''.join([format(ord(i), '08b') for i in '$$#f1L3']) #will be appended to the data so we know when to stop

	main()
