import urllib
import json
import os

from flask import Flask
from flask import request
from flask import make_response
from flask_pymongo import PyMongo

# Flask app should start in global layout
app = Flask(__name__)

app.config['MONGO_DBNAME']= 'webhook_database'
app.config['MONGO_URI']= 'mongodb://nikita:live_padhai1@ds123029.mlab.com:23029/webhook_database'

mongo = PyMongo(app)

@app.route('/add')
def add():
	user=mongo.db.users
	user.insert({'Name': 'nikita', 'Review': 'nice'})
	return 'Added!'

@app.route('/')
def index():
		return 'welcome user!'
@app.route('/webhook', methods=['POST'])
def webhook():
		req = request.get_json(silent=True, force=True)

		#print("Request:")
		#print(json.dumps(req, indent=4))


		if req.get("result").get("action") == "website_review":

			res = makeWebhookResult1(req)
			res = json.dumps(res, indent=4)
			#print(res)
			r = make_response(res)
			r.headers['Content-Type'] = 'application/json'
			return r

		elif req.get("result").get("action") == "Question_to_Tutor":

			res = makeWebhookResult2(req)
			res = json.dumps(res, indent=4)
			#print(res)
			r = make_response(res)
			r.headers['Content-Type'] = 'application/json'
			return r

		elif req.get("result").get("action") == "Tutor_Review":
			res = makeWebhookResult3(req)
			res = json.dumps(res, indent=4)
			#print(res)
			r = make_response(res)
			r.headers['Content-Type'] = 'application/json'
			return r

		else:
			return {}





def makeWebhookResult1(req):
	 
		parameters = req.get("result").get("parameters")
		review = parameters.get("review_on_website")

		user=mongo.db.LivePadhaiReview
		user.insert({ 'Review': review})
		print( 'Added!')
		

		speech = "Thank you for your valuable Feedback, come visit us again soon:)"

		#print("Response:")
		#print(speech)

		return {
        "speech": speech,
        "displayText": speech,
        # "data": data,
        # "contextOut": [],
        "source": "webhook"
    			}

def makeWebhookResult2(req):
	 
		parameters = req.get("result").get("parameters")
		subj = parameters.get("subject")
		ques = parameters.get("Question")

		user=mongo.db.Question_to_Tutor
		user.insert({ 'Subject': subj, 'Question': ques})
		print( 'Added!')
		

		speech = "Thanks for contacting us. Your Question has been recorded and our Tutors will provide with an optimum solution as soon as possible. Please Share your views on Live Padhai.:)"

		#print("Response:")
		#print(speech)

		return {
        "speech": speech,
        "displayText": speech,
        # "data": data,
        # "contextOut": [],
        "source": "webhook"
    }
def makeWebhookResult3(req):
	 
		parameters = req.get("result").get("parameters")
		fname = parameters.get("tutor-first-name")
		lname = parameters.get("tutor-last-name")
		rev = parameters.get("review")

		user=mongo.db.Review_on_Tutor
		user.insert({ 'Name': str(fname)+str(lname), 'Review': rev})
		print( 'Added!')

		speech = "The information provided by you has been recorded. Thanks alot!Please provide your valuable Review about Live Padhai:)"

		#print("Response:")
		#print(speech)

		return {
        "speech": speech,
        "displayText": speech,
        # "data": data,
        # "contextOut": [],
        "source": "webhook"
    }


