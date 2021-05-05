from datetime import datetime
import cv2
import threading
import numpy as np

from Model.UserClass import ListUserDetector

COLOR_FACE = (250, 128, 114)
COLOR_FACE_DETECT = (0, 255, 0)
COLOR_FACE_COMPLETE = (255, 255, 0)
# COLOR OF TEXT OF RECTANGLE AROUND FACE
FIRST_CONFIDENCE = 65
SECOND_CONFIDENCE = 57
# 2 POWERFUL NUM THAT DECIDE IS THAT OUR USER OR NOT


class Detector:
    def __init__(self, names):
        # List users
        self.list_users = ListUserDetector(names)
        self.list_users.show_list_users()
        # List recognizer
        self.recognizer = []
        # List value confidence after 1 frame
        self.confidence = []

        self.frame = None
        self.font = cv2.FONT_HERSHEY_PLAIN
        self.face_cascade = cv2.CascadeClassifier('../Model/data/haarcascade_frontalface_default.xml')

    def thread_recog(self, gray, faces, index):
        for (x, y, w, h) in faces:
            # Recognize name of face
            roi_gray = gray[y:y + h, x:x + w]
            # diff is distance between two vectors
            id, diff = self.recognizer[index].predict(roi_gray)

            confidence = 100 - int(diff)
            self.confidence[index].append(confidence)

    def detected_user(self, index_min, x, y, w, h):
        text = self.list_users[index_min].name + " Detect complete !"
        self.frame = cv2.rectangle(self.frame, (x, y), (x + w, y + h), COLOR_FACE_COMPLETE, 2)
        self.frame = cv2.putText(self.frame, str(datetime.now().time()), (x, y - 20), self.font, 1, COLOR_FACE_COMPLETE,
                                 1,
                                 cv2.LINE_AA)
        self.frame = cv2.putText(self.frame, text, (x, y - 4), self.font, 1, COLOR_FACE_COMPLETE, 1,
                                 cv2.LINE_AA)
        # get name of customer and write on the frame
        cv2.imwrite("../View/Detected/" + self.list_users[index_min].name + ".jpg", self.frame)
        # save that frame to show later
        self.list_users.pop(index_min)
        self.recognizer.pop(index_min)
        # pop that user out so the program will be smoother

    def read_single_classifier(self, list_index):
        for index_to_read in list_index:
            path_t = "../Model/data/classifiers/" + self.list_users[index_to_read].name + "_classifier.xml"
            self.recognizer[index_to_read].read(path_t)
            print("Load ", index_to_read + 1, "on", self.list_users.__len__())

    def read_necessary_classifiers(self):
        # Create this list to Multithreading
        list_index_user = []
        # init recognizers to detect for each users
        for index_user in range(len(self.list_users)):
            self.recognizer.append([])
            self.recognizer[index_user] = cv2.face.LBPHFaceRecognizer_create()
            # Create LBPHFaceRecognizer to Read
            list_index_user.append(index_user)

        # one thread take about 10% of my cpu so i get 8 thread to read classifiers faster 8x
        list1, list2, list3, list4, list5, list6, list7, list8 = np.array_split(list_index_user, 8)
        read_threads = list()
        for list_temp in [list1, list2, list3, list4, list5, list6, list7, list8]:
            temp_reading_thread = threading.Thread(target=self.read_single_classifier, args=(list_temp,))
            read_threads.append(temp_reading_thread)
            temp_reading_thread.start()

        # Wait to end all threads
        for thread_read in read_threads:
            thread_read.join()
        print("Complete Reading!")

    def main_app(self):
        self.read_necessary_classifiers()

        # use this line of code for detect from video
        # cap = cv2.VideoCapture("../Model/data/video/BeEm.mp4")
        # cv2.CAP_DSHOW for releasing the handle to the webcam to stop warning when close
        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        while True:
            # list that have confidence of all user
            self.confidence = []
            # READ FRAME
            ret, self.frame = cap.read()

            # ROTATE FRAME 90 CLOCKWISE
            # self.frame = cv2.rotate(self.frame, cv2.ROTATE_90_CLOCKWISE)

            if self.frame is None:
                break
            cv2.imshow("image", self.frame)

            gray = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)

            # Create threads to recognize
            # One thread run one recognizer to detect faces then predict with it's user

            threads = list()
            for index in range(len(self.list_users)):
                self.confidence.append([])
                x = threading.Thread(target=self.thread_recog, args=(gray, faces, index,))
                threads.append(x)
                x.start()

            # Wait to end all threads
            for index, thread in enumerate(threads):
                thread.join()

            # If found face then do
            if len(faces) > 0:
                for index_face, (x, y, w, h) in enumerate(faces):
                    max_conf = self.confidence[0][index_face]
                    index_min = 0
                    for i in range(len(self.list_users)):
                        if self.confidence[i][index_face] > max_conf:
                            max_conf = self.confidence[i][index_face]
                            print(max_conf)
                            index_min = i

                    # Draw rectangles
                    # Draw the best match names
                    text = "Unknown"
                    colorRectangle = COLOR_FACE
                    # -> upper confidence to maximum but still got the user name
                    # turn it between 40 and 90 based on situation
                    if self.confidence[index_min][index_face] > SECOND_CONFIDENCE:
                        self.list_users[index_min].detect_user()
                        # if detect more than 10 point then begin to show
                        if self.list_users[index_min].counter > 10:
                            text = self.list_users[index_min].name + " " + str(self.list_users[index_min].counter) + "%"
                            colorRectangle = COLOR_FACE_DETECT
                            if self.list_users[index_min].counter > 100:
                                # if detect more than 100 point frame then pop that user out and save the frame
                                self.detected_user(index_min, x, y, w, h)
                    self.frame = cv2.rectangle(self.frame, (x, y), (x + w, y + h), colorRectangle, 2)
                    self.frame = cv2.putText(self.frame, text, (x, y - 4), self.font, 1, colorRectangle, 1, cv2.LINE_AA)

            cv2.imshow("image", self.frame)
            # show the result
            if cv2.waitKey(20) & 0xFF == ord('q'):
                break
            # stop the program if press q

        cap.release()
        cv2.destroyAllWindows()
        # release the camera and close cv2 window
