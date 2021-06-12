from datetime import datetime
import cv2
from threading import Thread
import numpy as np

from Model.ClassForSoftware import ListEmployee, Employee

# COLOR OF TEXT OF RECTANGLE AROUND FACE
from Model.data_manager import DataManager

COLOR_FACE = (250, 128, 114)
COLOR_FACE_DETECT = (0, 255, 0)
COLOR_FACE_COMPLETE = (255, 255, 0)

# 2 POWERFUL NUM THAT DECIDE IS THAT OUR USER OR NOT
FIRST_DIFF = 30
SECOND_DIFF = 50


class Detector(Thread):
    def __init__(self, ID_RECORDER, selected_employee, menu_UI):
        # List users
        super().__init__()
        self.ID_RECORDER = ID_RECORDER
        self.progress = 1
        self.menu_UI = menu_UI
        self.list_users = ListEmployee(selected_employee)
        self.list_users.show_list_users()
        # List recognizer
        self.recognizer = []
        # List value confidence after 1 frame
        self.num_of_user = 0
        self.frame = None
        self.font = cv2.FONT_HERSHEY_PLAIN
        self.face_cascade = cv2.CascadeClassifier('Model/data/haarcascade_frontalface_default.xml')
        self.gray_face_list = []
        self.is_out_of_time = False

    def run(self):
        self.main_app()

    def thread_recog(self, index_perdict, numpy_confidence_temp):
        # compute the distance between the two histograms
        # try:
        for indexFace, gray_face in enumerate(self.gray_face_list):
            # so if the  The algorithm should also return the calculated distance,
            #   which can be used as a ‘confidence’ measurement.
            # Note: don’t be fooled about the ‘confidence’ name, as lower confidences are better because
            #   it means the distance between the two histograms is closer.
            # We can then use a threshold and the ‘confidence’ to automatically estimate if the algorithm has correctly
            #   recognized the image. We can assume that the algorithm has successfully recognized if the confidence
            #   is lower than the threshold defined.
            # We can assume that the algorithm has successfully recognized
            #   if the diff is lower than the threshold defined.
            # read detail here -> https://towardsdatascience.com/face-recognition-how-lbph-works-90ec258c3d6b
            ID, diff = self.recognizer[index_perdict].predict(gray_face)
            # diff is distance distance between the Feature extracted and the pic histogram
            numpy_confidence_temp[indexFace][index_perdict] = int(diff)
            # use numpy to pack our value where index is the same with self.list user
        # except Exception as e

    def detected_user(self, index_min, x, y, w, h):
        user_name = self.list_users[index_min].name
        user_id = self.list_users[index_min].ID
        self.frame = cv2.rectangle(self.frame, (x, y), (x + w, y + h), COLOR_FACE_COMPLETE, 2)
        self.frame = cv2.putText(self.frame, str(datetime.now().time())[0:5], (x, y - 50), self.font, 3,
                                 COLOR_FACE_COMPLETE, 2, cv2.LINE_AA)
        self.frame = cv2.putText(self.frame, user_name + "!", (x, y - 4), self.font, 3,
                                 COLOR_FACE_COMPLETE, 2, cv2.LINE_AA)
        # get name of customer and write on the frame
        cv2.imwrite("View/Detected/" + user_id + ".jpg", self.frame)
        # working with database in table DETAIL_RECORD to insert this employee to database
        with DataManager('Model/data/database/database.db') as db:
            db.insert_new_record(IS_BACKUP=False, ID_EMPLOYEE=user_id, ID_RECORDER=self.ID_RECORDER)
        # add a new UI button right here
        self.menu_UI.add_detected_user(user_id)
        # save that frame to show later
        self.list_users.pop(index_min)
        self.recognizer.pop(index_min)
        # pop that user out so the program will be smoother
        self.menu_UI.update_detected_text(num_of_list=self.num_of_user, num_of_left=len(self.recognizer))

    def backup_detected_user_with_id(self, id_to_backup):
        index_input = self.list_users.find_index_by_id(id_to_backup)

        user_id = self.list_users[index_input].ID
        user_name = self.list_users[index_input].name
        self.frame = cv2.putText(self.frame, str(datetime.now().time())[0:5], (50, 50), self.font, 2,
                                 COLOR_FACE_COMPLETE, 2, cv2.LINE_AA)
        self.frame = cv2.putText(self.frame, user_name, (50, 100), self.font, 2,
                                 COLOR_FACE_COMPLETE, 2, cv2.LINE_AA)

        # get name of customer and write on the frame
        cv2.imwrite("View/Backup/" + user_id + ".jpg", self.frame)  # delete this line
        # working in database to backup in table DETAIL_RECORD to insert this employee to database
        with DataManager('Model/data/database/database.db') as db:
            db.insert_new_record(IS_BACKUP=False, ID_EMPLOYEE=user_id, ID_RECORDER=self.ID_RECORDER)
        # add a new UI button right here
        self.menu_UI.add_detected_user_backup(user_id)
        # save that frame to show later
        self.list_users.pop(index_input)
        self.recognizer.pop(index_input)
        # pop that user out so the program will be smoother
        self.menu_UI.update_detected_text(num_of_list=self.num_of_user, num_of_left=len(self.recognizer))

    def backup_detected_user_with_id_but_detected_before(self, id_backup, detected_times):
        with DataManager('Model/data/database/database.db') as db:
            user = db.get_employee_infor_by_id(id_backup)
        temp_user = Employee(*user)
        self.frame = cv2.putText(self.frame, str(datetime.now().time())[0:5], (50, 50), self.font, 2,
                                 COLOR_FACE_COMPLETE, 2, cv2.LINE_AA)
        self.frame = cv2.putText(self.frame, temp_user.name, (50, 100), self.font, 2,
                                 COLOR_FACE_COMPLETE, 2, cv2.LINE_AA)

        # get name of customer and write on the frame
        cv2.imwrite("View/Backup/" + temp_user.ID + "-times-" + str(detected_times) + ".jpg", self.frame)
        # work with database
        with DataManager('Model/data/database/database.db') as db:
            if db.insert_new_record(IS_BACKUP=False, ID_EMPLOYEE=id_backup, ID_RECORDER=self.ID_RECORDER):
                print("Success when create new DETAIL record ", self.ID_RECORDER, id_backup)
            else:
                print("Some thing Wrong when create DETAIL record ")
        # add a new UI button right here
        self.menu_UI.add_detected_user_backup(temp_user.ID)
        # save that frame to show later
        self.menu_UI.update_detected_text(num_of_list=self.num_of_user, num_of_left=len(self.recognizer))

    def read_single_classifier(self, list_index):
        for index_to_read in list_index:
            path_t = "Model/data/classifiers/" + self.list_users[index_to_read].ID + "_classifier.xml"
            self.recognizer[index_to_read].read(path_t)
            self.menu_UI.progress_bar['value'] += (self.progress + 1) / len(self.list_users) * 100

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
            temp_reading_thread = Thread(target=self.read_single_classifier, args=(list_temp,))
            read_threads.append(temp_reading_thread)
            temp_reading_thread.start()

        # Wait to end all threads
        for thread_read in read_threads:
            thread_read.join()
        print("Complete Reading!")
        self.num_of_user = len(self.list_users)

    def get_gray_face(self, faces, gray):
        self.gray_face_list.clear()
        for indexFace, (x, y, w, h) in enumerate(faces):
            # gray_face = gray[y:y + h, x:x + w]
            # self.gray_face_list.append(gray_face)
            self.gray_face_list.append(gray[y:y + h, x:x + w])

    def stop_detect(self):
        self.is_out_of_time = True

    def add_backup_user(self, id_to_add):
        self.list_users.add_backup_user(id_to_add)

    def find_state_of_users(self, id_to_check):
        with DataManager('Model/data/database/database.db') as db:
            times = db.get_state_of_employee(ID_RECORDER=self.ID_RECORDER, ID_EMPLOYEE=id_to_check)
        return times

    def main_app(self):
        self.read_necessary_classifiers()
        # to show detected employee
        self.menu_UI.open_detect_UI()
        # show num of employee on the screen
        self.menu_UI.update_detected_text(num_of_list=self.num_of_user, num_of_left=len(self.recognizer))
        # use this line of code for detect from video
        cap = cv2.VideoCapture("Model/data/video/dilam4.mp4")
        # cv2.CAP_DSHOW for releasing the handle to the webcam to stop warning when close
        # cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        while not self.is_out_of_time:

            # list that have confidence of all user
            # READ FRAME
            ret, self.frame = cap.read()
            # ROTATE FRAME 90 CLOCKWISE
            # self.frame = cv2.rotate(self.frame, cv2.ROTATE_90_CLOCKWISE)

            # if self.frame is None:
            #     break

            # convert to gray
            gray = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
            # use CascadeClassifier to detect face from frame
            faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)

            # If found face and still need to record attendance then do
            if len(faces) > 0 and self.list_users:

                self.get_gray_face(faces, gray)

                # create numpy with it's detected_face dimensions
                np_confidence = np.full((len(faces), len(self.list_users)), 100, dtype=np.int16)

                # Create threads to recognize
                # One list of thread to detect faces then predict diff between frame's face and user's face
                threads = list()
                for index in range(len(self.list_users)):
                    x = Thread(target=self.thread_recog, args=(index, np_confidence))
                    threads.append(x)
                    x.start()

                # Wait to end all threads
                for index, thread in enumerate(threads):
                    thread.join()

                for index_face, (x, y, w, h) in enumerate(faces):
                    # get min user face to start recognize
                    # print(faces)
                    # print(np_confidence)
                    min_diff = np_confidence[index_face].min()
                    index_min = np_confidence[index_face].argmin()

                    # Draw rectangles
                    # Draw the best match names
                    text = "Unknown"
                    colorRectangle = COLOR_FACE
                    # -> upper confidence to minimum but still got the user name
                    # turn it between 10 and 45 based on situation
                    print("min diff ", min_diff)
                    # if this user pass this SECOND_DIFF so plus this user some point
                    if min_diff < SECOND_DIFF:
                        self.list_users[index_min].detect_user()
                        # if pass FIRST_DIFF so we can surely know this is the user we want to Attendance
                        # so give this user more and more point to make process faster

                        # if min_diff < FIRST_DIFF:
                        #     self.list_users[index_min].detect_user()
                        #     self.list_users[index_min].detect_user()
                        # if detect more than 10 point then begin to show
                        if self.list_users[index_min].counter > 10:
                            text = self.list_users[index_min].name + " " + str(self.list_users[index_min].counter) + "%"
                            colorRectangle = COLOR_FACE_DETECT
                            if self.list_users[index_min].counter > 100:
                                # if detect more than 100 point frame then pop that user out and save the frame
                                self.detected_user(index_min, x, y, w, h)
                    # print(np_confidence)
                    self.frame = cv2.rectangle(self.frame, (x, y), (x + w, y + h), colorRectangle, 2)
                    self.frame = cv2.putText(self.frame, text, (x, y - 4), self.font, 1, colorRectangle, 1, cv2.LINE_AA)

            # change BGR2RGB because cv2 numpy format is different from tk
            imageRGB = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
            self.menu_UI.update_frame(imageRGB)

            # show the result
            # if cv2.waitKey(20) & 0xFF == ord('q'):
            #     break
            # stop the program if press q

        cap.release()
        cv2.destroyAllWindows()
        # release the camera and close cv2 window
