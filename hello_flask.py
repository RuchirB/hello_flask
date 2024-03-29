
from flask import Flask, render_template, request, jsonify
import processInput
import random 
import logging
import sys
from datetime import datetime
from flask_cors import CORS




chat_history = {} #A dict in the format of {ID, chathistory}

global currentUser
currentUser = ""

# Create the application.
APP = Flask(__name__)
CORS(APP)

@APP.route('/', methods=['GET', 'POST'])
def main():
	return render_template('master.html') 

@APP.route('/last_answer/<last_answer>', methods=['GET', 'POST'])
def index(last_answer):
	global currentUser
	global chat_history
	sys.stdout.write("Looking for response")


	chatBotResponse = processInput.processIt(last_answer, currentUser) #Store the response from the chatbot here


	#processInput.updateLastSpokenString(datetime.utcnow(), currentUser) #Save current time 

	if currentUser not in chat_history: #First chat
		chat_history.update({currentUser: last_answer + "\n" + chatBotResponse}) #Adding the user to the chat_history dict with the first chat request and response
	else: #Chat history is already defined
		chat_history[currentUser] = chat_history[currentUser] + last_answer + "\n" + chatBotResponse 

	response = jsonify({"chatbot_response": chatBotResponse})
	response.headers.add('Access-Control-Allow-Origin', '*')
	return response


@APP.route("/get_new_userid", methods=['GET', 'POST']) #simple function to generate a user ID
def get_new_userid():
	global currentUser
	if currentUser != "":
		response= jsonify({"user_id":"Already Defined", "defined_id" : currentUser})
		response.headers.add('Access-Control-Allow-Origin', '*')
		return response
	else:
		user_id = int(random.random()*10000)
		while user_id in chat_history:
			user_id = int(random.random()*10000)
			currentUser = "user_"+str(user_id)
		response= jsonify({"user_id": "user_"+str(user_id)}) # Simple way of generating a "unique" id
		response.headers.add('Access-Control-Allow-Origin', '*')
		return response


@APP.route('/set_old_userid/<user_id>', methods=['GET', 'POST'])
def setId(user_id):
	global currentUser
	currentUser = user_id
	response = jsonify({"user_id": currentUser})
	response.headers.add('Access-Control-Allow-Origin', '*')
	return response

@APP.route('/getLastTime/<user_id>', methods=['GET', 'POST'])
def getLastTime(user_id):
	#lastTime = processInput.sendBackLastSpokenString(user_id)
	#return jsonify({"lastTime": lastTime})
	response = jsonify({"user_id": "2019-07-14 21:21:59.441900"})
	response.headers.add('Access-Control-Allow-Origin', '*')
	pass

if __name__ == '__main__':
	APP.debug=True
	APP.run(host='0.0.0.0')
	APP.run()

if __name__ != '__main__':
	gunicorn_error_logger = logging.getLogger('gunicorn.error')
	APP.logger.handlers.extend(gunicorn_error_logger.handlers)
	APP.logger.setLevel(logging.DEBUG)
	sys.stdout.write("LOGGING HERE ")


