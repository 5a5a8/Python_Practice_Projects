import time 
import random

class workouts:
	def __init__(self, name = 'Default Name', exercises = ''):
		self.name = name
		self.exercises = exercises


def create_new_workout():
	print('Enter a name for the workout: ')
	name = input('>>> ')
	line = name + ', '
	
	user_in = None
	while user_in != 'done':
		print('Enter an exercise or type \'done\' when finished')
		user_in = input('>>> ')
		if user_in == 'done':
			break
		line += user_in + '/'
		print('Enter a rep range for that exercise:')
		line += input('>>> ') + '|'
	line = line[0:-1]

	#write to csv in the correct format
	with open('workouts.csv', 'a') as f:
		f.write(line)
		f.close()


def existing_workout():
	#workouts will be stored as csv
	try:
		workoutsFile = open('workouts.csv')
	except:
		print('Failed to open file')
	
	
	#read the workouts file to a list and print it to the screen so the user can choose one
	workoutsList = workoutsFile.readlines()
	workoutsFile.close()
	for i in range(0, len(workoutsList)):
		workoutsList[i] = workoutsList[i].rstrip('\n')
		workoutsList[i] = workoutsList[i].split(', ')

	for workout in workoutsList:
		workout[1] = workout[1].split('|')
	
	#print the workouts in a user friendly manner
	i=1
	for workout in workoutsList[1:]:
		print('\n\n\t', i, '. ', workout[0], '\n\t\tExercise/Rep Range: ', end = '')
		for exercise in workout[1]:
				print('\n\t\t ', exercise, end='')
		i+=1

	#which workout does the user want to do?
	#add input validation here later
	selected_workout = int(input('\n\n\tEnter a number\n\n\t>>> '))

	#put the workout into new workouts class and send to start_workout function
	exercises = workoutsList[selected_workout][1]
	finalWorkout = workouts(workoutsList[selected_workout][0], exercises)
	start_workout(finalWorkout)

	
def start_workout(work_out):
	#get the exercise and rep range in a form we can work with (dictionary with list of lower and upper rep limits
	exercises = {work_out.exercises[i].partition('/')[0]: [int(work_out.exercises[i].partition('/')[2].partition('-')[0]), int(work_out.exercises[i].partition('/')[2].partition('-')[2])] for i in range(len(work_out.exercises))}

	#create exercise list with reps shuffled
	finalList = []
	for key in exercises:
		for reps in range(exercises[key][0], exercises[key][1]+1):
			finalList.append([key, reps]) 
	random.shuffle(finalList)

	#start timer
	startTime = int(time.time())
	
	#select an exercise from the list
	j = 0
	for i in finalList:
		print('\n'*100, '\t\t', i[0], ' | ', i[1], ' reps')
		timer = int(time.time()) - startTime
		minutes = timer // 60
		seconds = timer % 60
		print('\t\t', minutes, 'Minutes and', seconds, 'seconds elapsed.')
		print('\t\t', j, ' / ', len(finalList), 'completed')
		print('\n\t\tPress <ENTER> to go to the next set')
		print('\n'*5)
		input()
		j+=1
	
	#once done, print result
	timer = int(time.time()) - startTime
	minutes = timer // 60
	seconds = timer % 60
	print('\n'*100, '\t\tYou completed', work_out.name)
	print('\t\tIt took you', minutes, 'minutes and', seconds, 'seconds')
	print('\t\tYou completed', j, 'sets in total', '\n'*5)

#new workout or existing
print('1. Create new workout\n2. Do an existing workout')
selected = input('>>> ')
if selected == '1':
	create_new_workout()
elif selected == '2':
	existing_workout()
