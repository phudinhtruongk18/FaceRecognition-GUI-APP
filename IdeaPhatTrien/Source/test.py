# import cv2
#
# face_cascade = cv2.CascadeClassifier('../Model/data/haarcascade_frontalface_default.xml')
#
# cap = cv2.VideoCapture("../Model/data/video/BeEm.mp4")
# while True:
#     bruuh, frame = cap.read()
#     gray = cv2.cvtColor(cv2.UMat(frame), cv2.COLOR_BGR2GRAY)
#     if frame is None:
#         break
#     faces = face_cascade.detectMultiScale(gray, 1.3, 5)
#     cv2.imshow("image", frame)
#     cv2.imshow("image3", gray)
#     if cv2.waitKey(20) & 0xFF == ord('q'):
#         break

# import numpy as np
#
# faces = [(2,2,2,2),(2,2,2,2)]
# list_users = ["phu","phu","phu","phu","phu","phu","phu","phu","phu","phu","phu","phu","phu","phu","phu"]
# arrayConfidence = np.zeros((len(faces), len(list_users)), dtype=np.int16)
# # arrayConfidence[0]
# arrayConfidence[0][0] = 1
# arrayConfidence[0][3] = 5
# arrayConfidence[1][0] = 8
# arrayConfidence[1][3] = 7
# print(arrayConfidence[0].argmin())

# from tkinter import *
# from PIL import ImageTk, Image
# import cv2
#
#
# root = Tk()
# # Create a frame
# app = Frame(root, bg="white")
# app.grid()
# # Create a label in the frame
# lmain = Label(app)
# lmain.grid()
#
# # Capture from camera
# cap = cv2.VideoCapture(0)

# function for video streaming
# def video_stream():
#     _, frame = cap.read()
#     gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#     blur = cv2.GaussianBlur(gray, (3, 5), 0)
#     retval, thresh = cv2.threshold(blur, 38, 300, cv2.THRESH_BINARY)
#
#     cv2image = cv2.cvtColor(thresh, cv2.COLOR_BGR2RGBA)
#     img = Image.fromarray(cv2image)
#     imgtk = ImageTk.PhotoImage(image=img)
#     lmain.imgtk = imgtk
#     lmain.configure(image=imgtk)
#     lmain.after(1, video_stream)
#
# video_stream()
# root.mainloop()

#!/usr/bin/env python

# listt = [1,3,6,2,32,32,3,42,7]
#
# if 32 in listt:
#     print(listt.index(32))

# from tkinter import *
# import tkinter
#
# top = tkinter.Tk()
#
# B1 = tkinter.Button(top, text ="circle", relief=RAISED, cursor="tcross")
#
# def on_start_hover(event=None):
#     B1.configure(bg="pink")
#
# def on_end_hover(event=None):
#     B1.configure(bg="black")
#
# B2 = tkinter.Button(top, text ="plus", relief=RAISED, cursor="trek")
# B3 = tkinter.Button(top, text ="mouse", relief=RAISED, cursor="watch")
# B4 = tkinter.Button(top, text ="pirate", relief=RAISED, cursor="arrow")
# B5 = tkinter.Button(top, text ="plus", relief=RAISED, cursor="shuttle")
# B6 = tkinter.Button(top, text ="shuttle", relief=RAISED, cursor="sizing")
# B7 = tkinter.Button(top, text ="sizing", relief=RAISED, cursor="spider")
# B8 = tkinter.Button(top, text ="spider", relief=RAISED, cursor="spraycan")
# B9 = tkinter.Button(top, text ="spraycan", relief=RAISED, cursor="star")
# B10 = tkinter.Button(top, text="star", relief=RAISED, cursor="target")
# B1.bind('<Enter>', on_start_hover)
# B1.bind('<Leave>', on_end_hover)
#
# B1.pack()
# B2.pack()
# B3.pack()
# B4.pack()
# B5.pack()
# B6.pack()
# B7.pack()
# B8.pack()
# B9.pack()
# B10.pack()
# top.mainloop()
#

# import glob
# import os
#
# os.chdir("../Model/data/saved_sessions/")
# myFiles = glob.glob('*.txt')
# print(myFiles)

# import tkinter as tk
#
# class App():
#     def __init__(self, parent):
#         self.parent = parent
#         self.options = ['one', 'two', 'three']
#
#         self.om_variable = tk.StringVar(self.parent)
#         self.om_variable.set(self.options[0])
#         self.om_variable.trace('w', self.option_select)
#
#         self.om = tk.OptionMenu(self.parent, self.om_variable, *self.options)
#         self.om.grid(column=0, row=0)
#
#         self.label = tk.Label(self.parent, text='Enter new option')
#         self.entry = tk.Entry(self.parent)
#         self.button = tk.Button(self.parent, text='Add option to list', command=self.add_option)
#
#         self.label.grid(column=1, row=0)
#         self.entry.grid(column=1, row=1)
#         self.button.grid(column=1, row=2)
#
#         self.update_button = tk.Button(self.parent, text='Update option menu', command=self.update_option_menu)
#         self.update_button.grid(column=0, row=2)
#
#     def update_option_menu(self):
#         menu = self.om["menu"]
#         menu.delete(0, "end")
#         for string in self.options:
#             menu.add_command(label=string,
#                              command=lambda value=string: self.om_variable.set(value))
#
#     def add_option(self):
#          self.options.append(self.entry.get())
#          self.entry.delete(0, 'end')
#          print(self.options)
#
#     def option_select(self, *args):
#         print(self.om_variable.get())
#
#
# root = tk.Tk()
# App(root)
# root.mainloop()

# import sqlite3
#
# def importdb(db):
#      conn = sqlite3.connect(db)
#      c = conn.cursor()
#      c.execute("""SELECT * FROM EMPLOYEE
#                     WHERE SEX like "MALE";
#                """)
#      return c.fetchall()
#
#
# dataget = importdb("./database/database.db")
# for temp in dataget:
#      print(temp)
#
#
# def testFunc( **kwargs ):
#     attribute = kwargs.pop('ID', "id CUA NHAN VIEN MOI LAM RA")
#     print(attribute)
#
#
# testFunc( ID='new_value1', option3='new_value3' )
# # {'option2': 'default_value2', 'option3': 'new_value3', 'option1': 'new_value1'}
#
# testFunc( option2='new_value2' )
# # {'option1': 'default_value1', 'option3': 'default_value3', 'option2': 'new_value2'}

def get_calen():
    print(cal.get()<cal2.get())
    print(cal.get())
    print(cal2.get())

import tkinter

import tkcalendar
from tkinter import *

from tkcalendar import DateEntry


root = Tk()

label = Label(root,width=30,text="Get 1")
label2 = Label(root,width=30,text="Get 2")
cal = DateEntry(root,width=30,bg="darkblue",fg="white",year=2021,month=6, date_pattern='y-mm-dd')
cal2 = DateEntry(root,width=30,bg="darkblue",fg="white",year=2021,month=6, date_pattern='y-mm-dd')
btn = Button(root,width=30,text="Get",command=get_calen)
label.grid()
cal.grid()
label2.grid()
cal2.grid()
btn.grid()

root.mainloop()# import os

#
#
# def taoThuMucTheoThoiGian(folder_name):
#     if os.path.isfile(folder_name):
#         os.mkdir(folder_name)
#         return False
#     return True
#
# isExist = taoThuMucTheoThoiGian(ID_Recorder)
# if isExist:
#     print("Exist So do nothing")
# else:
#     print("Create")
