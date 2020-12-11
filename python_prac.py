
import sys
import csv
import time
import os.path
from os import path

import matplotlib.pyplot as plt
import numpy as np

batteryCharge = 200.0		#battery charge level

rechargeHalf = 0.25			#battery recharge rate

timeCounter = 0.0			#increases every half hour -> to detect day and night shift

distanceDriven = 0.0		#total distance driven

dayUsage=3					#energy effectivity

day=True

totalTime=0.0			#total driven in hours

batteryPercentage=100  #battery percentage

speed=0.0

lastValue=""

columns = ['Battery %', 'Time (H)', 'Distance']

data = []

csvFileName="driveData.csv"


def fileExists(fileName):			#Checks if file is created (meant for unit test)
	return path.exists(fileName)

def returnSpeed():			#Checks if file is created (meant for unit test)
	return speed



def checkLoop():			#checks input speed data to check for infinite loop

	batteryChargeDay=200.0
	batteryChargeNight=200.0
										#checks, if its recharges faster in day
	distance=speed/2
	batteryChargeDay-=distance/dayUsage
	batteryChargeDay+=rechargeHalf

	if batteryChargeDay>200.0:

		distance=speed/4				#checks, if its recharges faster in day
		batteryChargeNight-=distance/dayUsage

		batteryChargeDay-=200.0
		batteryChargeNight=200.0-batteryChargeNight		#checks, if its charges faster than discharges

		if batteryChargeDay>=batteryChargeNight:
			print("With this speed, car will drive forever!")
			exit()
		



def calculateCharge():
	global batteryCharge
	global batteryPercentage
	global dayUsage

	if day:							#calculates charge level, if its day or night
		distance=speed/2
		batteryCharge-=distance/dayUsage
		batteryCharge+=rechargeHalf
		batteryPercentage=round(batteryCharge/200*100)
	else:
		distance=speed/4
		batteryCharge-=distance/dayUsage
		batteryPercentage=round(batteryCharge/200*100)

	if batteryCharge<60.0:		#if below 30% battery
		dayUsage=2





def calculateDistance():
	global distanceDriven
	if day:									#depending day cycle calculates distance
		distanceDriven= distanceDriven + speed/2
	else:
		distanceDriven= distanceDriven + speed/4


def calculateTime():
	global timeCounter
	global day
	global totalTime
	timeCounter+=0.5
	totalTime+=0.5
	if timeCounter>12.0:		#detects when day switches to night
		day=False				
	if timeCounter>24.0:		#detects night -> day
		day=True
		timeCounter=0.5



print("Input your driving speed")

try:
	speed = float(input())					#Accepts only numeric values
except:
	print("Invalid speed value!")
	exit()

print("You are driving at speed: " + str(speed) + "Mi/h")


checkLoop()  #checks for input speed, if it is going to loop


while batteryCharge>0:		#handles drive calculations over time

	data.append([batteryPercentage,totalTime,distanceDriven])			#adds half-hour to data array
	lastValue = str(batteryPercentage) + " " + str(totalTime) + " " + str(distanceDriven) 

	calculateTime()
	calculateDistance()
	calculateCharge()




try:			#handles csv accessing errors

	with open(csvFileName, 'w', newline='') as csvfile:  #writes drive data to csv file
		csvwriter = csv.writer(csvfile)
		csvwriter.writerow(columns)
		csvwriter.writerows(data)
except (PermissionError) as error:
	print("Error accessing csv file:")
	print(error)



print("Last value: " + lastValue)		#prints last value of drive data


time=[]
battery=[]
distanceData=[]

with open('driveData.csv', 'r') as csvfile:			
    plots= csv.reader(csvfile, delimiter=',')
    i=0
    for row in plots:
    	if i==0:
    		i+=1
    		continue

    	time.append(float(row[1]))
    	battery.append(float(row[0]))
    	distanceData.append(float(row[2]))


fig, (ax1, ax2) = plt.subplots(1, 2)
fig.suptitle('Drive data')

ax1.plot(time, battery)						#plots battery vs time
ax1.set_title('Battery % vs Time (h)')
ax1.set(xlabel='Time (h)', ylabel='Battery %')

ax2.plot(time, distanceData)				#plots distance vs time
ax2.set_title('Distance vs Time (h)')
ax2.set(xlabel='Time (h)', ylabel='Distance')

print("Saving graphs: driveDataGraph.png")
plt.tight_layout()		#fixes image scaling 
plt.savefig('driveDataGraph.png')		#saves graphics to png file

print("Graphs saved!")

#plt.show()		#shows graphs


