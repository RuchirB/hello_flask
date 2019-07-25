import requests, datetime, dateTimeModule, json, os.path
import sys
import logging

#listOfThree = list()
class Helper:
	#listOfThree contains the three latest news story names
	listOfThree = []
	jsonRequest = []
	listOfHistory = []
	listOfCategories = ["World Affairs", "Politics", "Business", "Culture", "Science"]
	global userId

	@staticmethod
	def init(myId):
		global userId
		userId= myId
		resp = requests.get('https://newslens.berkeley.edu/api/lanes/recent2')
		Helper.jsonRequest = resp.json()
		#Grab top three stories in a list
		for x in range(3):
			Helper.listOfThree.append(Helper.jsonRequest["tiles"][x]["story_name"])
		Helper.loadSavedHistory()

	@staticmethod
	def displayNewsStories():
		return "Hello! Today's important news stories are " +Helper.listOfThree[0] + ", " + Helper.listOfThree[1] + ", and " +Helper.listOfThree[2] +" \n"

	@staticmethod
	def elaborateOnStory(storyIndex):
		#information needed: Date of story & summary of first event
		storyTime = Helper.jsonRequest["tiles"][storyIndex]["extent"]["start"]
		year = int(storyTime[0:4])
		month = int(storyTime[5:7])
		day = int(storyTime[8:10])
		date = datetime.datetime(year, month, day)
		#story started @
		daysAgo = datetime.datetime.utcnow() - date
		storySummary = Helper.jsonRequest["tiles"][storyIndex]["latest_highlights"][0]["summary"]

		#story name
		storyName = Helper.jsonRequest["tiles"][storyIndex]["story_name"]



		#Last Update
		storyTimeLast = Helper.jsonRequest["tiles"][storyIndex]["latest_highlights"][0]["pubtime"]
		yearLast = int(storyTimeLast[0:4])
		monthLast = int(storyTimeLast[5:7])
		dayLast = int(storyTimeLast[8:10])
		dateLast = datetime.datetime(yearLast, monthLast, dayLast)
		#story started @
		daysAgoLast = datetime.datetime.utcnow() - dateLast

		#Saving story
		Helper.saveStoryName(Helper.jsonRequest["tiles"][storyIndex]["id"])

		return "The " +storyName + " story started " +dateTimeModule.constructTimeDeltaPhrase(daysAgo) +". The latest update from this story comes from " +dateTimeModule.constructTimeDeltaPhrase(daysAgoLast) +" when " + storySummary

	@staticmethod
	def last10Events(storyIndex): #After the user asks for a story, they can ask for the last 10 events
		rv = ""
		rv += "Here are the last ten events for " +Helper.jsonRequest["tiles"][storyIndex]["story_name"] +":"+"\n"
		storyEvents = Helper.jsonRequest["tiles"][storyIndex]["latest_highlights"]
		for x in range (10):
			try:
				rv += str(x+1) +") "+storyEvents[x]["summary_title"] + "\n"
			except:
				sys.stdout.write(" Error in top 10" )

		return rv

	@staticmethod
	def peopleSaid(storyIndex):
		highlightInfoUrl = "https://newslens.berkeley.edu/api/highlight_info/" + str(Helper.jsonRequest["tiles"][storyIndex]["latest_highlights"][0]["_id"] )
		peopleInfoUrl = "https://newslens.berkeley.edu/api/story/" + str(Helper.jsonRequest["tiles"][storyIndex]["latest_highlights"][0]["ntopic"])+ "/people"
		highlightJson = requests.get(highlightInfoUrl).json()
		peopleList = requests.get(peopleInfoUrl).json()

		#totalPrintString += peopleList)
		return peopleList[0]["name"] +", " +peopleList[1]["name"] + ", and " +peopleList[2]["name"] +" commented on the issue. " + peopleList[2]["name"] +" said \"" + highlightJson["descriptions"][2]["para"] +"\" \n" 

	@staticmethod
	def loadSavedHistory():
		try:
			data_reloaded = requests.get("https://newslens.berkeley.edu/api/ruchir/load/"+str(userId)).json()
			sys.stdout.write("Just retrieved data " +str(data_reloaded))
			Helper.listOfHistory = data_reloaded
		except:
			sys.stdout.write("Couldn't retrieve history")


		'''
		if(os.path.isfile(path)):
			storyFile = open(path, "r")
			try:
				Helper.listOfHistory = json.load(storyFile)
			except ValueError as e:
				pass
			storyFile.close()
		'''

	@staticmethod
	def saveStoryName(storyId):
		Helper.loadSavedHistory() 
		for y in range(len(Helper.jsonRequest)): #Look through stories in recent2 API for the name of the story the user needs to store
			if Helper.jsonRequest["tiles"][y]["id"] == int(storyId):
				storyName= Helper.jsonRequest["tiles"][y]["story_name"] 


		myDict = {"story_name":storyName, "id":storyId, "accessTime":str(datetime.datetime.utcnow())} 
		
		for jsonDict in Helper.listOfHistory: #remove any other instances of the same storyname in the user's history
			if jsonDict["story_name"] == storyName:
				Helper.listOfHistory.remove(jsonDict)

		Helper.listOfHistory.append(myDict) #Add dict of story to the list of JSON

		#Save to newslens:
		
		url = "https://newslens.berkeley.edu/api/ruchir/save/"+userId
		save_res = requests.post(url, data=json.dumps(Helper.listOfHistory))

		#Log results:
		sys.stdout.write("Just added" +str(userId) +"'s story to newslens with the following JSON: \n "
		 +json.dumps(Helper.listOfHistory) +" \n Response from API:" +save_res.text +" \n API URL: \n " +url + "\n")

		#Previous method of saving to a file (which worked)
		'''
		path = "/Users/ruchirbaronia/Desktop/PythonProjects/JSONfun/hello_flask/historyFiles/storyInteractions_" +str(userId) +".txt"
		storyFile = open(path, "w")
		storyFile.write(json.dumps(Helper.listOfHistory))
		storyFile.close()
		'''

#End class helper

def sendBackLastSpokenString(userId):
	lastSpoke = ""
	if len(userId) == 0:
		sys.stdout.write("USER ID IS NOT EXISTENT WHAT")
	else:
		lastSpoke = dateTimeModule.init(userId)
	return lastSpoke

def updateLastSpokenString(utcnow, userId):
	dateTimeModule.updateUserTime(utcnow, userId)
	return True

def processIt(userInput, userId):
	global totalPrintString
	totalPrintString = ""
	global storyIndex
	def elaborateOnStory(userInput):
		global storyIndex
		global totalPrintString
		sys.stdout.write("In elaborate on story")
		#if userInput contains something from listOfThree, get that index and call a method elaborate that further describes it
		elaborated = False
		elaboration = ""
		for x in Helper.listOfThree:
			breakLoop=False
			for individualWord in userInput.split():
				if individualWord.lower() in x.lower():
					storyIndex=Helper.listOfThree.index(x)
					sys.stdout.write("storyIndex is " + str(storyIndex))
					totalPrintString += Helper.elaborateOnStory(storyIndex)
					elaborated = True
					breakLoop=True
					break
			if breakLoop is True:
				break
		return [elaborated, elaboration]

	def lastTenEventsOrPeople(userInput):
		global totalPrintString
		global storyIndex

		if storyIndex is None:
			pass
		else:
			sys.stdout.write("storyIndex is " + str(storyIndex))

			if("last" in userInput.lower() or "10 events" in userInput):
				totalPrintString += Helper.last10Events(storyIndex)
				return True
			elif("people" in userInput or "said" in userInput):
				totalPrintString+= Helper.peopleSaid(storyIndex)	
				return True
			else:
				return False


	def giveUserHistory():
		global totalPrintString


		save_res = requests.get("https://newslens.berkeley.edu/api/ruchir/load/"+str(userId)).json()
		array = save_res

		'''
		path = "/Users/ruchirbaronia/Desktop/PythonProjects/JSONfun/hello_flask/historyFiles/storyInteractions_" +str(userId) +".txt"
		storyFile = open(path, "r")
		array = json.load(storyFile)
		'''
		totalPrintString += "Here are the stories you've asked about before: \n"
		for x in range(len(array)):
			id = array[x]["id"] #Pull out the ID from the line

			totalPrintString += array["tiles"][x]["story_name"] +", accessed: " +array[x]["accessTime"] + "\n"
		#storyFile.close()
		return True

	def getUpdatesOn(storyInput):
		global totalPrintString
		totalPrintString += "Would you like updates on any of these stories?"+ "\n"
		answer  = False
		while answer != True:
			userInput = input()
			if "yes" in userInput:
				totalPrintString += "Which story would you like updates on?"+ "\n"
				getUpdatesOn(input())
				answer = True
			elif "no" in userInput:
				totalPrintString += "Okay, sure! For a list of things you can ask, type help."+ "\n"
				answer= True
			else:
				totalPrintString += "What?"+ "\n"

	def displayCategoryNews(userInput):
		sys.stdout.write("Looking to see if " +userInput +" is a category")
		global totalPrintString
		focusCategory = ""
		focusCategoryList = []
		for category in Helper.listOfCategories:
			if category.lower() in userInput.lower():
				focusCategory = category
				totalPrintString += "Searching for stories under " +focusCategory + "..."+ "\n"
				break
		if focusCategory is "":
			sys.stdout.write("No Category Match")
			return False
		else:
			for x in Helper.jsonRequest["tiles"]:
				if x["type"].lower() == focusCategory.lower():
					focusCategoryList.append(x)

		for newsStory in focusCategoryList:
			totalPrintString += newsStory["story_name"]+ "\n"

		return True
		

	def checkEveryArticleName(userInput):
		i = -1
		for article in Helper.jsonRequest["tiles"]:
			i = i+1
			if userInput.lower() in article["story_name"].lower():
				Helper.elaborateOnStory(i)


	def checkForHistory(userInput):
		'''
		path = "/Users/ruchirbaronia/Desktop/PythonProjects/JSONfun/hello_flask/historyFiles/storyInteractions_" +str(userId) +".txt"
		storyFile = open(path, "r")
		array = json.load(storyFile)
		'''

		save_res = requests.get("https://newslens.berkeley.edu/api/ruchir/load/"+str(userId)).json()
		array = save_res

		id = ""
		for x in range(len(array)):
			if(userInput.lower() in array[x]["story_name"].lower()):
				id = array[x]["id"] #Pull out the ID from the line
				accessTimeString = array[x]["accessTime"]
				accessTime = datetime.datetime.strptime(accessTimeString, "%Y-%m-%d %H:%M:%S.%f")

		storyFile.close()

		if(id == ""):
			return False
		else:
			giveUpdateReport(storyID = id, accessTime = accessTime)
			return True

	def giveUpdateReport(storyID, accessTime):
		global totalPrintString
		givenUpdate = False
		storyDetailsUrl = "https://newslens.berkeley.edu/api/story/" + str(storyID)
		storyJson = requests.get(storyDetailsUrl).json()
		for index in range(len(storyJson["highlights"])):
			indexFromEnd = len(storyJson["highlights"]) - index -1
			pubTime = dateTimeModule.timeFormat(storyJson["highlights"][indexFromEnd]["pubtime"])
			totalPrintString += str(pubTime)+ "\n"
			if(pubTime > accessTime):
				totalPrintString += "One update you missed from " +dateTimeModule.constructTimeDeltaPhrase(pubtime - accessTime) +"is " +Helper.jsonRequest["tiles"][y]["latest_highlights"][indexBackwards]["summary_title"]
				givenUpdate = True
		if givenUpdate is False:
			totalPrintString += "You're all up to date with " +storyJson[story_name]+ "\n"

	def checkForLocation(userInput):
		global totalPrintString
		if "from" in userInput:
			userInput = userInput.split("from ")[1]
		if "in" in userInput:
			userInput = userInput.split("in ")[1]

		prompt = False
		number = 0
		for story in range(len(Helper.jsonRequest["tiles"])):
			if userInput.lower() in Helper.jsonRequest["tiles"][story]["geotext"].lower():
				number= number+1
				if prompt == False:
					totalPrintString += "Here are some stories from " +Helper.jsonRequest["tiles"][story]["geotext"] +": \n"+ "\n"
					prompt = True
				totalPrintString += str(number) +") " +Helper.jsonRequest["tiles"][story]["story_name"]+ "\n"



	#TODO:
	#Test that this code displays all the user history properly.
	#Create method that gets all updates for a certain story after a certain date. Parameters (Story_name, date_accessed). Then use this same function to allow the user to ask for give me updates on the XXX story from YYY date. search XXX in ALL storynames & pull updates from YYY
	#Allow user to ask for a specific person name, search for it in database and pull info about it
	#After implementing the above, store any specific people names in a separate history file with date accessed
	#implement the help command 
	Helper.init(userId)
	exit = False


	while(exit != True):
		alreadyResponded = False

		if(alreadyResponded != True and "exit" in userInput):
			exit=True
			#dateTimeModule.lastSpokeUpdate(datetime.datetime.utcnow()) #update the file with the time spoken now for later reference
		if("new" in userInput.lower()):
			totalPrintString += Helper.displayNewsStories()
			sys.stdout.write(userId)
			alreadyResponded = True

		if alreadyResponded != True:
			alreadyResponded = elaborateOnStory(userInput)[0]
		if alreadyResponded != True:
			alreadyResponded = lastTenEventsOrPeople(userInput)
		if alreadyResponded != True and "history" in userInput:
			alreadyResponded = giveUserHistory()
		if alreadyResponded != True:
			alreadyResponded = displayCategoryNews(userInput)
		if alreadyResponded != True:
			alreadyResponded = checkForHistory(userInput)

		if alreadyResponded != True:
			alreadyResponded = checkForLocation(userInput)

		if alreadyResponded != True:
			alreadyResponded = checkEveryArticleName(userInput)
		if alreadyResponded == True:
			return totalPrintString
		else:
			return "Unable to understand input"


	
