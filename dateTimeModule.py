from datetime import datetime
import os
import json, os.path

global userId

def init(id):
	global userId
	userId = id

	#if first time ever interacting with chatbot
	path = "/Users/ruchirbaronia/Desktop/PythonProjects/JSONfun/hello_flask/lastAccessed.txt"

	
	if not lastSpoke():
		lastSpokeUpdate(datetime.utcnow())
		return "Welcome to NewsLens for the first time!" "\n"

	else:
		timeAgo = datetime.utcnow()-lastSpoke() #constructs a timedelta object
		return "Last session with NewsLens was " +constructTimeDeltaPhrase(timeAgo)
	


	

def timeFormat(timeStamp):
	if(type(timeStamp) is str):
		year = int(timeStamp[0:4])
		month = int(timeStamp[5:7])
		day = int(timeStamp[8:10])
		hour = int(timeStamp[11:13])
		minute = int(timeStamp[14:16])
		sec = int(timeStamp[17:19])
		dateTimeObj = datetime(year, month, day)
		return dateTimeObj
def lastSpokeUpdate(input): #Updates lastAccessed.txt with latest time, which is input
	global userId
	listOfTimes = []
	path = "/Users/ruchirbaronia/Desktop/PythonProjects/JSONfun/hello_flask/lastAccessed.txt"

	if(os.path.isfile(path)): #if the file exists, grab the list of JSON in listOfTimes so that we can append to it before editing the file
			lastAccessed = open(path, "r")
			try:
				listOfTimes = json.load(lastAccessed) #Load previous list of JSON
			except ValueError as e:
				pass
			lastAccessed.close()


	

	if len(listOfTimes) == 0:
		print("Appending " +userId + " for the first time")
		listOfTimes.append({userId : str(input)})
	else:
		for x in range (len(listOfTimes)):
			if userId in listOfTimes[x]:
				listOfTimes[x][userId] = str(input)
			else:
				listOfTimes.append({userId : str(input)})


	lastAccessed = open("/Users/ruchirbaronia/Desktop/PythonProjects/JSONfun/hello_flask/lastAccessed.txt", "w")
	lastAccessed.write(json.dumps(listOfTimes))

	lastAccessed.close()
	pass
def lastSpoke(): #Gets the value of the last spoken value from the chatbot
	global userId
	dateString = ""
	listOfTimes = []
	lastAccessed = open("/Users/ruchirbaronia/Desktop/PythonProjects/JSONfun/hello_flask/lastAccessed.txt", "r")
	try:
		listOfTimes = json.load(lastAccessed)
		for x in range(len(listOfTimes)):
			if userId in listOfTimes[x]:
				dateString = listOfTimes[x][userId]

	except:
		print("Cant load json")
	

	if not dateString:
		return dateString
	else:
		return datetime.strptime(dateString[0:19], "%Y-%m-%d %H:%M:%S") #reads string from file in teh format of "%Y-%m-%d %H:%M:%S" and puts in datetime object

def constructDatePhrase(date):
	if date.strftime("%y") != 0:
		phrase = date.strftime("%y years, %m months, and %d ago")
	elif date.strftime("%m") != 0:
		phrase = date.strftime("%m months, and %d ago")
	elif date.strftime("%d") != 0:
		phrase = date.strftime("%d days ago")
	elif date.strftime("%H") != 0:
		phrase = date.strftime("%H hours and %M minutes ago")
	elif date.strftime("%M") != 0:
		phrase = date.strftime("%M minutes and %S seconds ago")
	elif date.strftime("%S") != 0:
		phrase = date.strftime("%S seconds ago")
	return phrase

def constructTimeDeltaPhrase(timeDelta):
	
	days = str(timeDelta.days)
	secs = timeDelta.total_seconds()
	hours = str(int(secs / 3600) % 24)
	minutes = str(int(secs / 60) % 60)
	seconds = str(secs%60).split(".", 1)[0]
	
	if int(days) > 0:
		return(days + " days and " +hours+ " hours ago")
	if int(hours) != 0:
		return(hours + " hours, " + minutes + " minutes ago")
	elif int(minutes) != 0:
		return(minutes + " minutes " + "and " + seconds + " seconds ago")
	elif int(minutes) != 0 or int(seconds) > 0:
		return(seconds + " seconds ago")
	else:
		return(" UNKNOWN")


def updateUserTime(input, userId): #Updates lastAccessed.txt with latest time, which is input
	listOfTimes = []
	path = "/Users/ruchirbaronia/Desktop/PythonProjects/JSONfun/hello_flask/lastAccessed.txt"

	if(os.path.isfile(path)): #if the file exists, grab the list of JSON in listOfTimes so that we can append to it before editing the file
			lastAccessed = open(path, "r")
			try:
				listOfTimes = json.load(lastAccessed) #Load previous list of JSON
			except ValueError as e:
				pass
			lastAccessed.close()

	if len(listOfTimes) == 0:
		print("Appending " +userId + " for the first time")
		listOfTimes.append({userId : str(input)})
	else:
		for dict in listOfTimes[:]: #makes copy so that i can remove from list
			for key in dict:
				if userId == key:
					print(userId +" already in listOftimes @ " + str(listOfTimes.remove(dict)))
				print("Checkign key " +key +" versus " +userId)
		listOfTimes.append({userId : str(input)})


	lastAccessed = open("/Users/ruchirbaronia/Desktop/PythonProjects/JSONfun/hello_flask/lastAccessed.txt", "w")
	lastAccessed.write(json.dumps(listOfTimes))

	lastAccessed.close()
	pass


