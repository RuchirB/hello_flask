
from flask import Flask, render_template, request, jsonify
import processInput
import random 
from datetime import datetime



chat_history = {} #A dict in the format of {ID, chathistory}

global currentUser
currentUser = ""

# Create the application.
APP = Flask(__name__)

@APP.route('/', methods=['GET', 'POST'])
def main():
	return render_template('master.html') 

@APP.route('/last_answer/<last_answer>', methods=['GET', 'POST'])
def index(last_answer):
	global currentUser
	global chat_history
	chatBotResponse = processInput.processIt(last_answer, currentUser) #Store the response from the chatbot here

	processInput.updateLastSpokenString(datetime.utcnow(), currentUser) #Save current time 

	if currentUser not in chat_history: #First chat
		chat_history.update({currentUser: last_answer + "\n" + chatBotResponse}) #Adding the user to the chat_history dict with the first chat request and response
	else: #Chat history is already defined
		chat_history[currentUser] = chat_history[currentUser] + last_answer + "\n" + chatBotResponse 

	return jsonify({"chatbot_response": chatBotResponse})


@APP.route("/get_new_userid", methods=['GET', 'POST']) #simple function to generate a user ID
def get_new_userid():
	global currentUser
	if currentUser != "":
		return jsonify({"user_id":"Already Defined", "defined_id" : currentUser})
	else:
		user_id = int(random.random()*10000)
		while user_id in chat_history:
			user_id = int(random.random()*10000)
			currentUser = "user_"+str(user_id)
		return jsonify({"user_id": "user_"+str(user_id)}) # Simple way of generating a "unique" id


@APP.route('/set_old_userid/<user_id>', methods=['GET', 'POST'])
def setId(user_id):
	global currentUser
	currentUser = user_id
	return jsonify({"user_id": currentUser})

@APP.route('/getLastTime/<user_id>', methods=['GET', 'POST'])
def getLastTime(user_id):
	lastTime = processInput.sendBackLastSpokenString(user_id)
	return jsonify({"lastTime": lastTime})


if __name__ == '__main__':
	APP.debug=True
	APP.run(host='0.0.0.0')
	APP.run()

