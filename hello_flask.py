
from flask import Flask, render_template, request
import processInput 


chat_history = {} #A dict in the format of {ID, chathistory}
global currentUser
currentUser = ""

# Create the application.
APP = Flask(__name__)

@APP.route('/')
def main():
	return render_template('master.html') 

@APP.route('/last_answer/<last_answer>', methods=['GET', 'POST'])
def index(last_answer):

	chatBotResponse = processInput.processIt(last_answer) #Store the response from the chatbot here

	if currentUser == "":
		currentUser = get_new_userid()
		chat_history.update({currentUser, last_answer + "\n" + response}) #Adding the user to the chat_history dict with the first chat request and response
	else: #user is already defined and has started the conversation 
		chat_history[currentUser] = chat_history[currentUser] + last_answer + "\n" + response 

	return render_template('master.html', chat=chat_history[currentUser]) 


@APP.route("/get_new_userid", methods=['GET', 'POST']) #simple function to generate a user ID
def get_new_userid():
	user_id = int(random.random()*10000)
	while user_id in chat_history:
		user_id = int(random.random()*10000)
	return "user_"+str(user_id) # Simple way of generating a "unique" id

if __name__ == '__main__':
	APP.debug=True
	APP.run()

