import cv2
import os


def start_capture(name):
    face_classifier = cv2.CascadeClassifier("../Model/data/haarcascade_frontalface_default.xml")
    # load
    path = "../Model/data/users_photos/" + name

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
    numOfData = 0

    while True:
        ret, frame = cap.read()
        cv2.imshow("real", frame)
        if face_cropped(frame) is not None:
            # face = cv2.resize(face_cropped(frame), (200, 200))
            face = face_cropped(frame)
            face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
            file_name_path = path+"/"+str(numOfData)+name+".jpg"
            cv2.imwrite(file_name_path, face)
            cv2.putText(face, str(numOfData), (50, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
            numOfData += 1

            cv2.imshow("Cropped_Face", face)
        else:
            print("hi")
            # cv2.putText(frame, str("emty"), (50, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q") or key == 27 or numOfData > 300:
            break

    cap.release()
    cv2.destroyAllWindows()
    print("Got enough data !")
    return numOfData

# start_capture("PhuDinh2")
