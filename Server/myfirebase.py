import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import initialize_app
from firebase_admin import storage
from datetime import datetime
from firebase import firebase
def connect_database():
	# Fetch the service account key JSON file contents
	cred = credentials.Certificate('py3s1-6a115-firebase-adminsdk-xvgxd-0c5b534a28.json')

	# Initialize the app with a custom auth variable, limiting the server's access
	initialize_app(cred, {
	    'databaseURL': 'https://py3s1-6a115.firebaseio.com/',
	    'databaseAuthVariableOverride': None,
	    'storageBucket': 'py3s1-6a115.appspot.com'
	})
	authentication = firebase.FirebaseAuthentication(
		secret='WlPXKHEM9uNeg1MnrdP9pEkOvFKbFhR1jofuquhx', 
		email='thloanth.dut@gmail.com',
	)
	app = firebase.FirebaseApplication('https://py3s1-6a115.firebaseio.com/', authentication=authentication)
	return app

def gettime(): 
	now = datetime.now()
	s = now.strftime("%d/%m/%Y, %H:%M:%S")
	# print(s)
	return s 

def update_firebase(student_id, appear, app):
	# The app only has access as defined in the Security Rules
	info = db.reference('/info')
	#print(info.get())
	for i in range(0, 34): 
		candidate = info.child(str(i))
		#print(candidate)
		idcan = candidate.child('id').get()
		#print(idcan)
		if idcan == student_id: 
			if appear == 'true': 
				candidate.update({
					'appear' : 'true',
					'suspicious' : 'false',
					})
				update_time(app, i)
			else: 
				candidate.update({
					'suspicious' : 'true',
					})
				update_time(app, i)
			print("done") 
			print(candidate.get())
			break

def update_time(app, i): 
	# authentication = firebase.FirebaseAuthentication(
	# 	secret='WlPXKHEM9uNeg1MnrdP9pEkOvFKbFhR1jofuquhx', 
	# 	email='thloanth.dut@gmail.com',
	# )
	# app = firebase.FirebaseApplication('https://py3s1-6a115.firebaseio.com/', authentication=authentication)
	time = gettime()
	path = str(i) + '/time'
	result = app.put('/info', path, time)
	print(result)

def upload_storage(student_id, status): 
	if status == "true":
		fileName = '/home/mylinux/Desktop/PBL4/realpic/' + student_id + '.jpg'
		name = student_id + '.jpg'
	else:
		fileName = '/home/mylinux/Desktop/PBL4/realpic/' + 'sus' + student_id + '.jpg'
		name = 'sus' + student_id + '.jpg'
	
	bucket = storage.bucket()
	blob = bucket.blob(name)
	blob.upload_from_filename(fileName) 

	blob.make_public()
	print("url: ", blob.public_url)
