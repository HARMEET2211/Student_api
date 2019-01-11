from flask import Flask, request
from pymongo import MongoClient
from bson import json_util as json

MONGODB_URI = "mongodb://test:test123@ds141209.mlab.com:41209/student_db"#URI is uniform resouce identifier
client = MongoClient(MONGODB_URI)
db = client.get_database("student_db")
student_record = db.student_record

app = Flask(__name__)

@app.route('/')
def index():
	return "Welcome to student Records Api"

@app.route('/students/',methods=['GET','POST'])
def student_list():
	if request.method == 'GET':
		data=list(student_record.find({}))
		return json.dumps(data)
	else:
		try:
			data = dict(request.form)	#return the data in dictionary format from post request
			data['roll_no']= int(data['roll_no'])
			roll_no=request.form.get('roll_no')# to create a unique roll no as data 
			if student_record.count_documents({'roll_no':data['roll_no']}):
				return json.dumps({'error':'this record already exist!!!!!!!!'})

			student_record.insert_one(data)
			return json.dumps({'result':'successfully added'})
		except	Exception as e:
			return json.dumps({'error':str(e)})


@app.route('/students/<int:roll_no>/',methods=['GET','PATCH','DELETE'])
def student_detail(roll_no):
	if student_record.count_documents({'roll_no':roll_no})is 0:
		return json.dumps('record not found')
	elif request.method == 'PATCH':
		record = student_record.find_one({'roll_no':roll_no})
		record.update(dict(request.form))
		student_record.update_one({'roll_no':roll_no},{'$set':record})
		return json.dumps({'result':"successfully updated the record"})
	else:
		student_record.delete_one({'roll_no':roll_no})
		return json.dumps({'result':"successfully added the record"})	
			
	
if __name__=="__main__":
	app.run(port=8000,debug=True,use_reloader=True)
