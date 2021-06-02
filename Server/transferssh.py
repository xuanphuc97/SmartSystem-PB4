import os 

ipServer = "192.168.43.83"
ipPi = "192.168.43.131"

def sendpic(): 
	#imgurl = '/home/pi/Download/face_test.jpg'
	cmd = 'scp /home/pi/Desktop/PBL4/face_test.jpg mylinux@'+ipServer+':Desktop/PBL4'
	os.system(cmd)

def sendconfig(configstr): 
	f = open('config.txt', 'w')
	f.write(configstr)
	f.close()
	cmd = 'scp /home/mylinux/Desktop/PBL4/config.txt pi@'+ipPi+':Desktop/PBL4'
	os.system(cmd)
	cmd = 'scp /home/mylinux/Desktop/PBL4/face.jpg pi@'+ipPi+':Desktop/PBL4'
	os.system(cmd)

def readconfig(): 
	str = []
	f = open('config.txt', 'r')
	str.append(f.readline())
	str.append(f.readline())
	f.close()
	return str

def writenull(): 
	f = open('config.txt', 'w')
	f.write("")
	f.close()

def sendcut(): 
	cmd = 'scp /home/pi/Desktop/PBL4/face.jpg mylinux@'+ipServer+':Desktop/PBL4'
	os.system(cmd)

def toreal(student_id, status): 
	if status == 'true': 
		cmd = 'cp /home/mylinux/Desktop/PBL4/face.jpg /home/mylinux/Desktop/PBL4/realpic/' + student_id +  '.jpg'
	else: 
		cmd = 'cp /home/mylinux/Desktop/PBL4/face.jpg /home/mylinux/Desktop/PBL4/realpic/' + 'sus' + student_id +  '.jpg'
	os.system(cmd)

