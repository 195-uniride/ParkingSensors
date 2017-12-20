import sys
import subprocess
import os
import time
import numpy as np
import aws_sensor
import keyboard

#/Arduino/read_output.py
#/home/akshat/Arduino/sketch/dfrobot/t.txt

path = "/home/akshat/Arduino/sketch/dfrobot/"
array_a = []
t_end_file = time.time()
t_end_calculator = 0
line_counter = 0


state = 0
#fpath = os.path.join(path, "t.txt")
def delay():
	global t_end_calculator
	if t_end_calculator<=time.time():
		t_end_calculator = time.time() + 15
		detect_change()
	return

def readFile():
	global line_counter
	global array_a
	
	#file_clear_check()

	f = open(os.path.join(path, "t.txt"), "r")

	i = 0
	for line in iter(f):
		s = float(line)
		if i>=line_counter:
			array_a.append(s)
			print(s)
	    		line_counter += 1
	    	i += 1
	f.close()
	delay()
	return

def detect_change():
	global array_a

	clean_array()

	if(len(array_a)==0):
		return
	regression()
	return

def regression():
	global array_a
	global state
	time_x=[]

	for i,n in enumerate(array_a):
		time_x.append(i)

	distance_y = array_a

	if (len(time_x)==0):
		return

	m,b = np.polyfit(time_x, distance_y, 1)
	previous_state = state

	if m < -1:			#car coming in
		state = 1

	elif m > 1:			#car moving out
		state = 2
	else:				#no change
		state = 0

	if previous_state!=state:
		aws_broadcast()
	else:
		clear_array()
	return

def aws_broadcast():
	global state
	aws_sensor.broadcast(state)
	return

#Helper Functions
def file_clear_check():
	global t_end_file
	global line_counter
	if(t_end_file <= time.time()):
		t_end_file = time.time() + 900
		f = open(os.path.join(path, "t.txt"), "w").close()
		line_counter = 0
	return

def clean_array():
	global array_a

	for n in array_a:
		if (n>200):
			array_a.remove(n)
	return

def clear_array():
	global array_a
	array_a = []
	return

while True:
	readFile()
	time.sleep(2)
		