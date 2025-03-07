import numpy as np
from PIL import Image
import os, cv2


# Method to train custom classifier to recognize face
def train_all_classifers():
    # Read all the images in custom data-set
    path = os.path.join("Model\\data\\users_photos\\")

    subdirectories = []

    # Store images in a numpy format and ids of the user on the same index in imageNp and id lists

    for root, dirs, files in os.walk(path):
        subdirectories = dirs
        break
    for indexTrain,sub in enumerate(subdirectories):
        faces = []
        ids = []
        pictures = {}
        for root2, dirs2, files2 in os.walk(os.path.join(path, sub)):
            pictures = files2
        for pic in pictures:
            imgpath = os.path.join(path, sub, pic)
            img = Image.open(imgpath)
            imageNp = np.array(img, 'uint8')

            id = int(pic.split(sub)[0])
            faces.append(imageNp)
            ids.append(id)

        ids = np.array(ids)

        # Train and save classifier
        clf = cv2.face.LBPHFaceRecognizer_create()
        clf.train(faces, ids)
        clf.write("Model/data/classifiers/" + sub + "_classifier.xml")
        print("Succes ", indexTrain+1, "on", subdirectories.__len__())

    print("We have already trained.")
    # Return number users in dataset trained
    return subdirectories
