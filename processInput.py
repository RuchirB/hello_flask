import requests, datetime, dateTimeModule, json

#listOfThree = list()
class Helper:
	#listOfThree contains the three latest news story names
	listOfThree = []
	jsonRequest = []
	listOfHistory = []
	listOfCategories = ["World Affairs", "Politics", "Business", "Culture", "Science"]

	@staticmethod
	def init():
		resp = requests.get('https://newslens.berkeley.edu/api/lanes/recent2')
		Helper.jsonRequest = resp.json()
		#Grab top three stories in a list
		for x in range(3):
			Helper.listOfThree.append(Helper.jsonRequest[x]["story_name"])
		Helper.loadSavedHistory()

	@staticmethod
	def displayNewsStories():
		return "Hello! Today's important news stories are " +Helper.listOfThree[0] + ", " + Helper.listOfThree[1] + ", and " +Helper.listOfThree[2] +". (There's also been an update in W that we talked about last week. \n"

	@staticmethod
	def elaborateOnStory(storyIndex):
		#information needed: Date of story & summary of first event
		storyTime = Helper.jsonRequest[storyIndex]["extent"]["start"]
		year = int(storyTime[0:4])
		month = int(storyTime[5:7])
		day = int(storyTime[8:10])
		date = datetime.datetime(year, month, day)
		#story started @
		daysAgo = datetime.datetime.utcnow() - date
		storySummary = Helper.jsonRequest[storyIndex]["latest_highlights"][0]["summary"]

		#story name
		storyName = Helper.jsonRequest[storyIndex]["story_name"]



		#Last Update
		storyTimeLast = Helper.jsonRequest[storyIndex]["latest_highlights"][0]["pubtime"]
		yearLast = int(storyTimeLast[0:4])
		monthLast = int(storyTimeLast[5:7])
		dayLast = int(storyTimeLast[8:10])
		dateLast = datetime.datetime(yearLast, monthLast, dayLast)
		#story started @
		daysAgoLast = datetime.datetime.utcnow() - dateLast

		#Saving story
		Helper.saveStoryName(Helper.jsonRequest[storyIndex]["id"])

		return "The " +storyName + " story started " +dateTimeModule.constructTimeDeltaPhrase(daysAgo) +". The latest update from this story comes from " +dateTimeModule.constructTimeDeltaPhrase(daysAgoLast) +" when " + storySummary

	@staticmethod
	def last10Events(storyIndex):
		rv = ""
		rv += "_____________Here are the last ten events: _________________ \n" 
		storyEvents = Helper.jsonRequest[storyIndex]["latest_highlights"]
		for x in range (10):
			rv += str(x+1) +") "+storyEvents[x]["summary_title"] + "\n"

		return rv

	@staticmethod
	def peopleSaid(storyIndex):
		highlightInfoUrl = "https://newslens.berkeley.edu/api/highlight_info/" + str(Helper.jsonRequest[storyIndex]["latest_highlights"][0]["_id"] )
		peopleInfoUrl = "https://newslens.berkeley.edu/api/story/" + str(Helper.jsonRequest[storyIndex]["latest_highlights"][0]["ntopic"])+ "/people"
		highlightJson = requests.get(highlightInfoUrl).json()
		peopleList = requests.get(peopleInfoUrl).json()

		#totalPrintString += peopleList)
		return peopleList[0]["name"] +", " +peopleList[1]["name"] + ", and " +peopleList[2]["name"] +" commented on the issue. " + peopleList[2]["name"] 
		+" said \"" + highlightJson["descriptions"][2]["para"] +"\" \n" 

	@staticmethod
	def loadSavedHistory():
		storyFile = open("/Users/ruchirbaronia/Desktop/PythonProjects/JSONfun/storyInteractions.txt", "r")
		try:
			Helper.listOfHistory = json.load(storyFile)
		except ValueError as e:
			pass
		storyFile.close()

	@staticmethod
	def saveStoryName(storyId):
		Helper.loadSavedHistory()
		for y in range(len(Helper.jsonRequest)):
			if Helper.jsonRequest[y]["id"] == int(storyId):
				storyName= Helper.jsonRequest[y]["story_name"]


		myDict = {"story_name":storyName, "id":storyId, "accessTime":str(datetime.datetime.utcnow())}
		
		for jsonDict in Helper.listOfHistory:
			if jsonDict["story_name"] == storyName:
				Helper.listOfHistory.remove(jsonDict)

		Helper.listOfHistory.append(myDict)
		storyFile = open("/Users/ruchirbaronia/Desktop/PythonProjects/JSONfun/storyInteractions.txt", "w")
		storyFile.write(json.dumps(Helper.listOfHistory))
		storyFile.close()

#End class helper

def processIt(userInput):
	global totalPrintString
	totalPrintString = ""
	storyIndex = 0
	def elaborateOnStory(userInput):
		#if userInput contains something from listOfThree, get that index and call a method elaborate that further describes it
		elaborated = False
		elaboration = ""
		for x in Helper.listOfThree:
			breakLoop=False
			for individualWord in userInput.split():
				if individualWord.lower() in x.lower():
					#totalPrintString += "Found it in " +x +" print " +str(Helper.listOfThree.index(x)))
					storyIndex=Helper.listOfThree.index(x)
					elaboration = Helper.elaborateOnStory(storyIndex)
					elaborated = True
					breakLoop=True
					break
			if breakLoop is True:
				break
		return [elaborated, elaboration]

	def lastTenEventsOrPeople(userInput):
		if("last" in userInput or "10 events" in userInput):
			totalPrintString += Helper.last10Events(storyIndex)
			return True
		elif("people" in userInput or "said" in userInput):
			totalPrintString+= Helper.peopleSaid(storyIndex)	
			return True
		else:
			return False


	def giveUserHistory():
		storyFile = open("/Users/ruchirbaronia/Desktop/PythonProjects/JSONfun/storyInteractions.txt", "r")
		array = json.load(storyFile)
		totalPrintString += "Here are the stories you've asked about before: \n"
		for x in range(len(array)):
			id = array[x]["id"] #Pull out the ID from the line

			totalPrintString += array[x]["story_name"] +", accessed: " +array[x]["accessTime"] + "\n"
		storyFile.close()
		return True

	def getUpdatesOn(storyInput):
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
		focusCategory = ""
		focusCategoryList = []
		for category in Helper.listOfCategories:
			if category.lower() in userInput.lower():
				focusCategory = category
				totalPrintString += "Searching for stories under " +focusCategory + "..."+ "\n"
				break
		if focusCategory is "":
			return False
		else:
			for x in Helper.jsonRequest:
				if x["type"].lower() == focusCategory.lower():
					focusCategoryList.append(x)

		for newsStory in focusCategoryList:
			totalPrintString += newsStory["story_name"]+ "\n"
		

	def checkEveryArticleName(userInput):
		i = -1
		for article in Helper.jsonRequest:
			i = i+1
			if userInput.lower() in article["story_name"].lower():
				Helper.elaborateOnStory(i)


	def checkForHistory(userInput):
		storyFile = open("/Users/ruchirbaronia/Desktop/PythonProjects/JSONfun/storyInteractions.txt", "r")
		array = json.load(storyFile)
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
		givenUpdate = False
		storyDetailsUrl = "https://newslens.berkeley.edu/api/story/" + str(storyID)
		storyJson = requests.get(storyDetailsUrl).json()
		for index in range(len(storyJson["highlights"])):
			indexFromEnd = len(storyJson["highlights"]) - index -1
			pubTime = dateTimeModule.timeFormat(storyJson["highlights"][indexFromEnd]["pubtime"])
			totalPrintString += str(pubTime)+ "\n"
			if(pubTime > accessTime):
				totalPrintString += "One update you missed from " +dateTimeModule.constructTimeDeltaPhrase(pubtime - accessTime) +"is " +Helper.jsonRequest[y]["latest_highlights"][indexBackwards]["summary_title"]
				givenUpdate = True
		if givenUpdate is False:
			totalPrintString += "You're all up to date with " +storyJson[story_name]+ "\n"
	def checkForLocation(userInput):
		if "from" in userInput:
			userInput = userInput.split("from ")[1]
		if "in" in userInput:
			userInput = userInput.split("in ")[1]

		prompt = False
		number = 0
		for story in range(len(Helper.jsonRequest)):
			if userInput.lower() in Helper.jsonRequest[story]["geotext"].lower():
				number= number+1
				if prompt == False:
					totalPrintString += "Here are some stories from " +Helper.jsonRequest[story]["geotext"] +": \n"+ "\n"
					prompt = True
				totalPrintString += str(number) +") " +Helper.jsonRequest[story]["story_name"]+ "\n"



	#TODO:
	#Test that this code displays all the user history properly.
	#Create method that gets all updates for a certain story after a certain date. Parameters (Story_name, date_accessed). Then use this same function to allow the user to ask for give me updates on the XXX story from YYY date. search XXX in ALL storynames & pull updates from YYY
	#Allow user to ask for a specific person name, search for it in database and pull info about it
	#After implementing the above, store any specific people names in a separate history file with date accessed
	#implement the help command 
	Helper.init()
	totalPrintString += "Hi, I'm NewsLens! \n"
	exit = False
	while(exit != True):
		alreadyResponded = False

		if(alreadyResponded != True and "exit" in userInput):
			exit=True
			dateTimeModule.lastSpokeUpdate(datetime.datetime.utcnow()) #update the file with the time spoken now for later reference
		if("new" in userInput):
			totalPrintString += Helper.displayNewsStories()
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


	
