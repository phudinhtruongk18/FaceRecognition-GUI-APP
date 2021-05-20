import numpy as np
from PIL import Image
import os, cv2


# Method to train custom classifier to recognize face
def train_one_classifer(name):
    # Read all the images in custom data-set
    path = os.path.join("Model\\data\\users_photos\\"+name+"\\")
    faces = []
    ids = []
    pictures = {}

    # Store images in a numpy format and ids of the user on the same index in imageNp and id lists

    for root, dirs, files in os.walk(path):
        pictures = files

    for pic in pictures:
        imgpath = path + pic
        img = Image.open(imgpath).convert('L')
        imageNp = np.array(img, 'uint8')
        print(pic)
        id = int(pic.split(name)[0])
        faces.append(imageNp)
        ids.append(id)
    # Input: Training Image set.

    ids = np.array(ids)


    # Train and save classifier
    clf = cv2.face.LBPHFaceRecognizer_create()
    clf.train(faces, ids)
    # Output: Feature extracted from face image and
    clf.write("Model/data/classifiers/" + name + "_classifier.xml")

    print("We have already trained.")


# train_one_classifer("PhuDinh2")
'''
Train function will apply the basic LBP operation by changing each pixel based on its neighbors using a default radius 
defined by the user. 
The basic LBP operation can be seen in the following image (using 8 neighbors and radius equal to 1):
from https://towardsdatascience.com/face-recognition-how-lbph-works-90ec258c3d6b
Radius: the radius is used to build the circular local binary pattern and represents the radius around the central pixel. It is usually set to 1.
Neighbors: the number of sample points to build the circular local binary pattern. Keep in mind: the more sample points you include, the higher the computational cost. It is usually set to 8.
Grid X: the number of cells in the horizontal direction. The more cells, the finer the grid, the higher the dimensionality of the resulting feature vector. It is usually set to 8.
Grid Y: the number of cells in the vertical direction. The more cells, the finer the grid, the higher the dimensionality of the resulting feature vector. It is usually set to 8.
    # some another algothim
    # class  	cv::face::BasicFaceRecognizer
    # class  	cv::face::EigenFaceRecognizer
    # class  	cv::face::FisherFaceRecognizer
    # class  	cv::face::LBPHFaceRecognizer
'''