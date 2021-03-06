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
@app.route('/webhook', methods=['GET','POST'])
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
	rev=""
	if review=='a':
		rev="5-stars"
	elif rev=='b':
		rev="4-stars"
	elif review=='c':
		rev="3-stars"
	elif review=='d':
		rev="2-stars"
	elif review=='e':
		rev="1-star"
	else:
		rev= review
	

	user=mongo.db.LivePadhaiReview
	user.insert({ 'Review': rev})
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
		

	speech = "Thanks for contacting us. Your Question has been recorded \
	and our Tutors will provide with an optimum solution as soon as possible.\n Choose Any of the Options below to Rate our website.\n a) 5-Stars \n b)4-Stars \n c)3-Stars \n d)2-Stars \n e)1-Star" 
	

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

	speech = "Thank you so much. Your Review about the tutor has been recorded.\n Choose Any of the Options below to Rate our website.\n a) 5-Stars \n b)4-Stars \n c)3-Stars \n d)2-Stars \n e)1-Star" 
	
	#print("Response:")
	#print(speech)
	return {
       "speech": speech,
       "displayText": speech,
       # "data": data,
       # "contextOut": [],
       "source": "webhook"
  		}


if __name__ == '__main__':
	
	port = int(os.getenv('PORT', 5000))

	#print "Starting app on port %d" % port

	app.run(debug=True, port=port, host='0.0.0.0')

