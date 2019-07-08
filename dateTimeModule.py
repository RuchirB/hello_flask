from datetime import datetime
import os

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
def lastSpokeUpdate(input):
	lastAccessed = open("/Users/ruchirbaronia/Desktop/PythonProjects/JSONfun/lastAccessed.txt", "w")
	lastAccessed.write(str(input))
	lastAccessed.close()
	pass
def lastSpoke():
	lastAccessed = open("/Users/ruchirbaronia/Desktop/PythonProjects/JSONfun/lastAccessed.txt", "r")
	dateString = lastAccessed.read()
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



#if first time ever interacting with chatbot
if os.path.isfile("/Users/ruchirbaronia/Desktop/PythonProjects/JSONfun/lastAccessed.txt") is False:
	lastSpokeUpdate(datetime.utcnow())

timeAgo = datetime.utcnow()-lastSpoke() #constructs a timedelta object

print("Last Spoken to: " +constructTimeDeltaPhrase(timeAgo))