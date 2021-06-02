import face_recognition.api as face_recognition
import transferssh
import numpy as np
import scipy.misc
import myfirebase
import warnings
import datetime
import pathlib
import dlib
import time
import math
import cv2
import os
import re
import api
from skimage import io as io
# Load the detector
detector =dlib.get_frontal_face_detector()
# Load the predictor
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
def scan_known_people(known_people_folder):
    known_names = []
    known_face_encodings = []

    basename = known_people_folder 
    img = face_recognition.load_image_file(known_people_folder)
    encodings = face_recognition.face_encodings(img)
    if len(encodings) == 1:
        known_names.append(basename)
        known_face_encodings.append(encodings[0])   
    return known_names, known_face_encodings


def test_image(image_to_check, known_names, known_face_encodings):
    unknown_image = face_recognition.load_image_file(image_to_check)

    # Scale down image if it's giant so things run a little faster
    if unknown_image.shape[1] > 1600:
        scale_factor = 1600.0 / unknown_image.shape[1]
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            unknown_image = scipy.misc.imresize(unknown_image, scale_factor)

    unknown_encodings = face_recognition.face_encodings(unknown_image)
    if len(unknown_encodings)==1:
        for unknown_encoding in unknown_encodings:
            result = face_recognition.compare_faces(known_face_encodings, unknown_encoding)
            distance = face_recognition.face_distance(known_face_encodings, unknown_encoding)
        return distance[0],result[0]
    else:
        return 1 , False



def image_files_in_folder(folder):
    return [os.path.join(folder, f) for f in os.listdir(folder) if re.match(r'.*\.(jpg|jpeg|png)', f, flags=re.I)]


def main(known_people_folder, image_to_check):
    known_names, known_face_encodings = scan_known_people(known_people_folder)
    distance,result=test_image(image_to_check, known_names, known_face_encodings)
    result = result
    return distance

def euclid(a, b):
    res = 0
    for i in range(len(a)):
        res += (a[i]-b[i])**2
    return math.sqrt(res)

app = myfirebase.connect_database()

while True:
    try:
        fname = pathlib.Path('face_test.jpg')
        if fname.exists():
            time.sleep(1)
            transferssh.writenull()
            anh1 = 'face_test.jpg'
            # FACE1
            # read the image
            img_raw = cv2.imread(anh1)
            os.remove("face_test.jpg")
            # Convert image into grayscale
            gray_raw = cv2.cvtColor(src=img_raw, code=cv2.COLOR_BGR2GRAY)
            # Use detector to find landmarks
            img = []
            faces_raw = detector(gray_raw)
            for face in faces_raw:
                x1 = face.left()  # left point
                y1 = face.top()  # top point
                x2 = face.right()  # right point
                y2 = face.bottom()  # bottom point
                img = img_raw[y1-25:y2+25, x1-25:x2+25]
            new_width = 500
            new_height = 500
            img_resized = cv2.resize(src=img, dsize=(new_width, new_height))
            cv2.imwrite("face.jpg", img_resized)
            img = cv2.imread("face.jpg")
            gray = cv2.cvtColor(src=img, code=cv2.COLOR_BGR2GRAY)
            # Use detector to find landmarks
            faces = detector(gray)
            landmarks = predictor(image=gray, box=face)
            for face in faces:
                x1 = face.left()  # left point
                y1 = face.top()  # top point
                x2 = face.right()  # right point
                y2 = face.bottom()  # bottom point
                # Create landmark object
                landmarks = predictor(image=gray, box=face)
                # Loop through all the points
                for n in range(0, 68):
                    x = landmarks.part(n).x
                    y = landmarks.part(n).y
                    # Draw a circle
                    cv2.circle(img=img, center=(x, y), radius=3, color=(0, 255, 0), thickness=-1)
            # show the image
            # cv2.imshow(winname="Face", mat=img)
            x = np.array(list((landmarks.part(n).x, landmarks.part(n).y) for n in range(0, 68)))
            # FACE2
            # read the image
            dist = []
            start = 102180248
            end = 102180269
            for i in range(start, end):
                anh2 = "./data/"+str(i)+".jpg"
                dist.append(main(anh2,"face.jpg"))

            # print(dist)
            chosenOne = 0
            minDist = 10
            for i in range(len(dist)):
                if dist[i] < minDist:
                    chosenOne = i
                    minDist = dist[i]
            imgChosen =  "./pic/"+str(chosenOne + start)+".jpg"
            print(dist)

            img2 = cv2.imread(imgChosen)
            gray2 = cv2.cvtColor(src=img2, code=cv2.COLOR_BGR2GRAY)
            # Use detector to find landmarks
            faces2 = detector(gray2)
            for face in faces2:
                x1 = face.left()  # left point
                y1 = face.top()  # top point
                x2 = face.right()  # right point
                y2 = face.bottom()  # bottom point
                # Create landmark object
                landmarks2 = predictor(image=gray2, box=face)
                # Loop through all the points
                for n in range(0, 68):
                    x = landmarks2.part(n).x
                    y = landmarks2.part(n).y
                    # Draw a circle
                    cv2.circle(img=img2, center=(x, y), radius=3, color=(0, 255, 0), thickness=-1)
            # show the image
            # cv2.imshow(winname="Face2", mat=img2)
            y = np.array(list((landmarks2.part(n).x, landmarks2.part(n).y) for n in range(0, 68)))    

            # print("Khoang cach giua 2 khuon mat:",minDist)
            # print(imgChosen)
           
            res = ''
            stu_id_fb = str(chosenOne + start)
            status = ""
            print(minDist)
            if minDist < 0.4:
                res = 'true\n'+str(chosenOne + start)
                status = 'true'
            else:
                res = 'false\n'+str(chosenOne + start)
                status = 'false'
            
            img1_r = io.imread("face.jpg")
            img1_a = api.face_alignment(img1_r, scale = 1)
            cv2.imwrite("face.jpg",cv2.cvtColor(img1_a[0], cv2.COLOR_RGB2BGR))
            transferssh.sendconfig(res)
            transferssh.toreal(stu_id_fb, status)
            os.remove("face.jpg")
            myfirebase.upload_storage(stu_id_fb, status)
            myfirebase.update_firebase(stu_id_fb, status, app)
            print("Next")
            
            
            # Delay between every frame
            # cv2.waitKey(delay=10000)
            # Close all windows
            # cv2.destroyAllWindows()
    except:pass
