import cv2
import threading

from Model.UserClass import ListUserDetector


class detector:
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
        self.face_cascade = cv2.CascadeClassifier('./Model/data/haarcascade_frontalface_default.xml')

    def thread_recog(self, gray, faces, index):
        for (x, y, w, h) in faces:
            # Recognize name of face
            roi_gray = gray[y:y + h, x:x + w]
            id, confidence = self.recognizer[index].predict(roi_gray)

            # confidence is distance between two vectors
            confidence = 100 - int(confidence)
            print(confidence)
            self.confidence[index].append(confidence)

    def main_app(self):
        # init recognizers to detect for each users
        print(self.list_users)
        for i in range(len(self.list_users)):
            self.recognizer.append([])
            self.recognizer[i] = cv2.face.LBPHFaceRecognizer_create()

            # Read  file classifier
            path_t = "./Model/data/classifiers/" + self.list_users[i].name + "_classifier.xml"
            self.recognizer[i].read(path_t)

        # cap = cv2.VideoCapture("./data/videos/clip0.mp4")
        cap = cv2.VideoCapture(0)

        while True:
            self.confidence = []
            ret, self.frame = cap.read()
            if self.frame is None:
                break
            # default_img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
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
                            index_min = i

                    # Draw rectangles
                    # Draw the best match names
                    text = "Unknown"
                    colorRectangle = (250,128,114)
                    # try to up confidence to give it more secure
                    # turn it to 40 if num of user more than 100
                    if self.confidence[index_min][index_face] > 60:
                        self.list_users[index_min].detect_user()
                        # if detect more than 10 frame then start couting to make sure
                        if self.list_users[index_min].counter > 10:
                            text = self.list_users[index_min].name + " " + str(self.list_users[index_min].counter) + "%"
                            colorRectangle = (0, 255, 0)
                            if self.list_users[index_min].counter > 100:
                                text = self.list_users[index_min].name + " Detect complete !"
                                colorRectangle = (255, 255, 0)

                    self.frame = cv2.rectangle(self.frame, (x, y), (x + w, y + h), colorRectangle, 2)
                    self.frame = cv2.putText(self.frame, text, (x, y - 4), self.font, 1, colorRectangle, 1, cv2.LINE_AA)

            cv2.imshow("image", self.frame)

            if cv2.waitKey(20) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()
