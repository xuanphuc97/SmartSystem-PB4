import socket
import sys
import cv2
import pickle
import numpy as np
import struct ## new
import zlib

import math
import ctypes
import argparse
import imutils
import time
from os.path import dirname, join
from imutils.video import VideoStream
from PIL import Image, ImageTk
import os
import re

import warnings


HOST=''
PORT=8485

s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
print('Socket created')

s.bind((HOST,PORT))
print('Socket bind complete')
s.listen(10)
print('Socket now listening')

conn,addr=s.accept()

data = b""
payload_size = struct.calcsize(">L")
print("payload_size: {}".format(payload_size))

ap = argparse.ArgumentParser()
ap.add_argument("-c", "--confidence", type=float, default=0.5,
    help="minimum probability to filter weak detections")
args = vars(ap.parse_args())
caffeModel = join(dirname(__file__), "res10_300x300_ssd_iter_140000.caffemodel") 
prototextPath = join(dirname(__file__), "deploy.prototxt.txt")

print("[INFO] loading model...")
net = cv2.dnn.readNetFromCaffe(prototextPath, caffeModel)
print("[INFO] starting video stream...")

while True:
    try:
        flag = "play"
        flag = pickle.dumps(flag)
        conn.send(flag)
        while len(data) < payload_size:
            # print("Recv: {}".format(len(data)))
            data += conn.recv(4096)

        # print("Done Recv: {}".format(len(data)))
        packed_msg_size = data[:payload_size]
        data = data[payload_size:]
        msg_size = struct.unpack(">L", packed_msg_size)[0]
        # print("msg_size: {}".format(msg_size))
        while len(data) < msg_size:
            data += conn.recv(4096)
        frame_data = data[:msg_size]
        data = data[msg_size:]

        frame=pickle.loads(frame_data, fix_imports=True, encoding="bytes")

        
        frame = imutils.resize(frame, width=400)
        (h, w) = frame.shape[:2]
        blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 1.0,
            (300, 300), (104.0, 177.0, 123.0))

        net.setInput(blob)
        detections = net.forward()
        percent = 0
        for i in range(0, 1):
            confidence = detections[0, 0, i, 2]
            if confidence < args["confidence"]:
                continue
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")
            text = "{:.2f}%".format(confidence * 100)
            percent = np.max(confidence) * 100
            y = startY - 10 if startY - 10 > 10 else startY + 10
        print(percent)
        # cv2.imshow("Frame", frame)
        if (percent > 99.9):
            flag = "stop"
            flag = pickle.dumps(flag)
            conn.send(flag)
            cv2.imwrite("face_test.jpg",frame)
            time.sleep(9)
    except: pass
