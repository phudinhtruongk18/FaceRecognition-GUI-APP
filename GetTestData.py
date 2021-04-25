import os
import tkinter as jra
from tkinter import messagebox

import cv2
import numpy as np
from PIL import Image


# def train_classifer(name):
#     # Read all the images in custom data-set
#     path = os.path.join(os.getcwd()+"/data/"+name+"/")
#
#     faces = []
#     ids = []
#     labels = []
#     pictures = {}
#
#     # Store images in a numpy format and ids of the user on the same index in imageNp and id lists
#     for root,dirs,files in os.walk(path):
#             pictures = files
#
#     for pic in pictures :
#
#             imgpath = path+pic
#             img = Image.open(imgpath).convert('L')
#             imageNp = np.array(img, 'uint8')
#             id = int(pic.split(name)[0])
#             #names[name].append(id)
#             faces.append(imageNp)
#             ids.append(id)
#             print(imgpath)
#
#     ids = np.array(ids)
#
#     #Train and save classifier
#     clf = cv2.face.LBPHFaceRecognizer_create()
#     clf.train(faces, ids)
#     clf.write("./data/classifiers/"+name+"_classifier.xml")


def start_capture(name):
    face_classifier = cv2.CascadeClassifier("./testdata/haarcascade_frontalface_default.xml")
    path = "./testdata/" + name

    try:
        os.makedirs(path)
    except:
        print('Directory Already Created')

    def face_cropped(img):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_classifier.detectMultiScale(gray, 1.3, 5)
        if faces is ():
            return None
        for (x, y, w, h) in faces:
            cropped_face = img[y:y + h, x:x + w]
            return cropped_face

    cap = cv2.VideoCapture(0)
    img_id = 0
    while True:
        ret, frame = cap.read()
        cv2.imshow("real", frame)
        if face_cropped(frame) is not None:
            face = cv2.resize(face_cropped(frame), (200, 200))
            face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
            file_name_path = path + "/" + str(img_id) + name + ".jpg"
            cv2.imwrite(file_name_path, face)
            cv2.putText(face, str(img_id), (50, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
            img_id += 1

            cv2.imshow("Cropped_Face", face)
        else:
            print("hi")
            # cv2.putText(frame, str("emty"), (50, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q") or key == 27 or img_id > 200:
            break
    cap.release()
    cv2.destroyAllWindows()
    print("Collecting samples is completed !!!")
    return img_id


class CropTool(jra.Frame):
    def __init__(self, master, **kw):
        super().__init__(master, **kw)
        self.master = master
        self.master.title("Get Face Tool")
        master.iconbitmap("logo.ico")
        w = 420  # width for the Tk root
        h = 150  # height for the Tk root
        ws = master.winfo_screenwidth()  # width of the screen
        hs = master.winfo_screenheight()  # height of the screen
        x = ws/2 - w/2
        y = (hs / 2) - (h / 2) * 2
        master.geometry('%dx%d+%d+%d' % (w, h, x, y))
        hang = 0
        cot = 0
        self.name = ""

        self.canvas = jra.Frame(self.master)
        self.canvas.pack()
        self.guideSpaceNham = jra.Label(self.canvas)
        self.guideSpaceNham.pack()
        self.guideSpaceNham2 = jra.Label(self.canvas, text="Nhập tên của bạn (Không Dấu-Không cách)")
        self.guideSpaceNham2.pack()
        self.entryNhapTen = jra.Entry(self.canvas)
        self.entryNhapTen.pack()
        self.khoiDongGetDataSet = jra.Button(self.canvas, text="Lấy dữ liệu",bg="pink", font="Helvetica 15 bold italic")
        self.khoiDongGetDataSet["command"] = self.getDataSet
        self.khoiDongGetDataSet.pack()
        # self.khoiDongTraning = jra.Button(self.canvas, text="Traning data",bg="pink", font="Helvetica 15 bold italic")
        # self.khoiDongTraning["command"] = self.getDataSet
        # self.khoiDongTraning.pack()

        # self.guideSpaceNham2 = jra.Label(self.canvas)
        # self.guideSpaceNham2.pack()
        # self.khoiDonNhanDien = jra.Button(self.canvas, text="Test Nhận Diện",bg="pink", font="Helvetica 13 bold italic")
        # self.khoiDonNhanDien["command"] = self.nhanDien
        # self.khoiDonNhanDien.pack()
        self.string1 = jra.StringVar(master)
        self.guideSpaceNham1 = jra.Label(self.canvas, text=0, textvariable=self.string1, fg="light green",
                                         bg="dark green", font="Helvetica 16 bold italic")
        self.moThuMucDuLieu = jra.Button(self.canvas, text="Mở Thư Mục để gửi cho Tui\nqua driver", bg="pink", font="Helvetica 13 bold italic")
        self.moThuMucDuLieu["command"] = self.openThuMuc

        # self.master.bind("<space>", self.getLocation)
        self.master.mainloop()

    def openThuMuc(self):
        os.startfile(f'{os.path.realpath("")}/testdata')

    def getDataSet(self):
        try:
            name = self.entryNhapTen.get()
            if name == "":
                messagebox.showinfo("Lỗi","Vui lòng không bỏ trống")
                return
            self.entryNhapTen.delete(0, 'end')
            self.name = name
            start_capture(self.name)
            self.string1.set("Well Done! Cám ơn "+self.name+" vì đã giúp Phú")
            self.guideSpaceNham2.pack_forget()
            self.entryNhapTen.pack_forget()
            self.khoiDongGetDataSet.pack_forget()
            self.moThuMucDuLieu.pack()
            self.guideSpaceNham1.pack()
        except:
            messagebox.showinfo("Lỗi","Vui lòng nhập kí tự phù hợp")
            return
        print(name)



giaoDien = jra.Tk()
croptool = CropTool(giaoDien)