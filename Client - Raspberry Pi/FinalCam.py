import cv2
import numpy as np
import math
import ctypes
import argparse
import imutils 
import time
from os.path import dirname, join
from imutils.video import VideoStream
import os
import re
import warnings
import sys
import pathlib
import transferssh

from tkinter import *
from PIL import Image, ImageTk
from threading import Thread
import io
import socket
import struct
import time
import pickle




window = Tk()
window.title("Check in")
window.geometry('1050x800')
video = cv2.VideoCapture(0)
canvas_w = video.get(cv2.CAP_PROP_FRAME_WIDTH) 
canvas_h = video.get(cv2.CAP_PROP_FRAME_HEIGHT)
canvas = Canvas(window, width = canvas_w, height= canvas_h , bg= "red")
canvas.place(x=10, y=10)

labelName = Label(window, font=('arial', 15, 'bold'), text ="It's you:", fg='black')
labelName.place(x=750, y=0)

labelName = Label(window, font=('arial', 15, 'bold'), text ="The most similar:", fg='black')
labelName.place(x=750, y=380)

load = Image.open("unnamed.jpg")
load = load.resize((360, 330), Image.ANTIALIAS)
render = ImageTk.PhotoImage(load)
img = Label(window, image=render)
img.image = render
img.place(x=670, y=30)

load1 = Image.open("unnamed.jpg")
load1 = load1.resize((360, 360), Image.ANTIALIAS)
render1 = ImageTk.PhotoImage(load1)
img1 = Label(window, image=render1)
img1.image = render1
img1.place(x=670, y=410)

status = StringVar()

labelStatus = Label(window, font=('arial', 40, 'bold'), textvariable=status, bg='gray')
labelStatus.place(x=40, y=500)

# name = StringVar()
# name.set("Tran Xuan Phuc")
# labelName = Label(window, font=('arial', 35, 'bold'), textvariable=name, fg='blue')
# labelName.place(x=100, y=500)

# dob = StringVar()
# dob.set("Ngay sinh: " + "20/02/1997")
# labelDob = Label(window, font=('arial', 20, 'bold'), textvariable=dob, fg='black')
# labelDob.place(x=100, y=610)

mssv = StringVar()
mssv.set("MSSV       : " + "unknown")
labelMssv = Label(window, font=('arial', 30, 'bold'), textvariable=mssv, fg='blue')
labelMssv.place(x=100, y=600)

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('192.168.43.83', 8485))
connection = client_socket.makefile('wb')


# img_counter = 0
encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]

def update_frame():
    try:
        global canvas, photo, video
        flag = client_socket.recv(4096)
        flag = pickle.loads(flag, fix_imports=True, encoding="bytes")
        print(flag)
        labelStatus.configure(bg = 'gray')
        status.set('Waiting for next one...')
       
        
        if flag == 'stop':
            video.release()
            status.set('Detected! Processing...')
            window.update()
            time.sleep(12)
            resstr = transferssh.readconfig()
            idsv = resstr[1].strip()
            res = resstr[0].strip()
            print(res)

            # res = "false"
            # idsv = '102180277'
            if res == "true" :
                status.set('               Pass              ')
                labelStatus.configure(bg = 'green')
                url = "./pic/" + idsv + ".jpg"

                load = Image.open("face.jpg")
                load = load.resize((360, 330), Image.ANTIALIAS)
                render = ImageTk.PhotoImage(load)
                img = Label(window, image=render)
                img.image = render
                img.place(x=670, y=30)

                load1 = Image.open(url)
                load1 = load1.resize((360, 360), Image.ANTIALIAS)
                render1 = ImageTk.PhotoImage(load1)
                img1 = Label(window, image=render1)
                img1.image = render1
                img1.place(x=670, y=410)
                mssv.set("MSSV       :"+idsv)

                window.update()
                time.sleep(3)
            else:
                status.set('            Not Pass           ')
                labelStatus.configure(bg = 'red')

                url = "./pic/" + idsv + ".jpg"
                load = Image.open("face.jpg")
                load = load.resize((360, 330), Image.ANTIALIAS)
                render = ImageTk.PhotoImage(load)
                img = Label(window, image=render)
                img.image = render
                img.place(x=670, y=30)

                load1 = Image.open(url)
                load1 = load1.resize((360, 360), Image.ANTIALIAS)
                render1 = ImageTk.PhotoImage(load1)
                img1 = Label(window, image=render1)
                img1.image = render1
                img1.place(x=670, y=410)
                
                mssv.set("MSSV       :"+"unknown")
            
                window.update()
                time.sleep(3)
                #os.remove('face.jpg')
            # window.update()
            # time.sleep(5)
            labelStatus.configure(bg = 'gray')

            load = Image.open("unnamed.jpg")
            load = load.resize((360, 330), Image.ANTIALIAS)
            render = ImageTk.PhotoImage(load)
            img = Label(window, image=render)
            img.image = render
            img.place(x=670, y=30)

            load1 = Image.open("unnamed.jpg")
            load1 = load1.resize((360, 360), Image.ANTIALIAS)
            render1 = ImageTk.PhotoImage(load1)
            img1 = Label(window, image=
                         render1)
            img1.image = render1
            img1.place(x=670, y=410)
            
            mssv.set("MSSV       : " + "unknown")
            labelMssv = Label(window, font=('arial', 30, 'bold'), textvariable=mssv, fg='blue')
            os.remove('face.jpg')
        else:
            ret, frame = video.read()
            if not ret:
                video = cv2.VideoCapture(0)
        #     cam = cv2.VideoCapture(0)
            data = pickle.dumps(frame)
            size = len(data)
                
        #     print("{}: {}".format(img_counter, size))
#             print(size) 
            client_socket.sendall(struct.pack(">L", size) + data)
        #    img_counter += 1
        ret, frame = video.read()
        if not ret:
            video = cv2.VideoCapture(0)
            ret, frame = video.read()
        frame1 = cv2.resize(frame, dsize=None, fx=1, fy=1)
        frame1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2RGB)
        photo = ImageTk.PhotoImage(image=Image.fromarray(frame1))
        canvas.create_image(0,0, image = photo, anchor=NW)
        
        window.after(19, update_frame)
    except:
         labelStatus.configure(bg = 'yellow')
         status.set('Warning! Try again!')
         window.update()
         time.sleep(3)
         update_frame()
         
update_frame()

window.mainloop()
