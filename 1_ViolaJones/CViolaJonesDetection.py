# #################################################################################################
# Andra Tomi 2019
# #################################################################################################

import cv2 as cv
import numpy as np
import sys
import os
import glob


## haar cascades -> massive xml files with features sets (= coresponding to a specific object: face, eyes, etc)
class CViolaJonesDetection:

    #  --------------------------------------------------------------------------------------------
    def __init__(self, tip, cale, id = 0, index = 0): # Initializare
    #  --------------------------------------------------------------------------------------------
        self.tip = tip
        self.cale = cale
        self.face_cascade = cv.CascadeClassifier('1_ViolaJones\\haarcascade_frontalface_default.xml')
        self.id = id
        self.index = index

    # #  --------------------------------------------------------------------------------------------
    # def __del__(self):   # Destructor
    # #  --------------------------------------------------------------------------------------------
    #     print('Destructor called')

    #  --------------------------------------------------------------------------------------------
    def generate_dataset(self, img):
    #  --------------------------------------------------------------------------------------------
        # write image in data dir
        cv.imwrite("antrenare/output1/user." + str(self.id) + "." + str(self.index) + ".jpg", img)


    #  --------------------------------------------------------------------------------------------
    def detectFaces (self, image):   # functie pt detetctarea fetelor in imagini/cadre
    # --------------------------------------------------------------------------------------------
        # variavile locale folositoare
        colors = {"blue":(255,0,0), "red":(0,0,255), "green":(0,255,0), "white":(255,255,255)}
        scaleFactor = 1.05
        minNeighbors = 3
        color = colors['blue']
        text = "Fataaaa"
        # transformare in grayscale
        gray_img = cv.cvtColor(image, cv.COLOR_BGR2GRAY)

        # extragere trasaturi
        features = self.face_cascade.detectMultiScale(gray_img, scaleFactor, minNeighbors)
        coords = []

        # desenare contur fata
        for (x, y, w, h) in features:
            # cv.rectangle(image, (x,y), (x+w, y+h), color, 2)
            # cv.putText(image, text, (x, y-4), cv.FONT_HERSHEY_SIMPLEX, 0.8, color, 1, cv.LINE_AA)
            coords = [x, y, w, h]

            # in cazul in care o apelam ca sa salvam imagini
            if len(coords) == 4 and self.id != 0:
                # cropam fata
                face = image[coords[1]:coords[1]+coords[3], coords[0]:coords[0]+coords[2]]
                # salvam fata cu nume
                self.generate_dataset(face)


    #  --------------------------------------------------------------------------------------------
    def detectFacesVideo (self, video):   # functie pt detectarea fetelor in video=uri
    #  --------------------------------------------------------------------------------------------
        while True:
            ret, img = video.read()
            self.detectFaces(img)
            keyExit = cv.waitKey(30) & 0xff
            if keyExit == ord('q'):  # == 27  => pt esc
                break


    #  --------------------------------------------------------------------------------------------
    def detectAllFaces (self):   # functie de detectare fete care alege pe ce sa detecteze: img, video, live
    #  --------------------------------------------------------------------------------------------
        # in functie de ce optiune se alege => se stie tipul
        # 1. IMAGINE
        if self.tip == "1":
            imgPath = self.cale
            if imgPath:
                img = cv.imread(imgPath)
                self.detectFaces(img)
                cv.waitKey(0)
            else:
                print("Mai incearca...nu ai dat o cale")

        # 2. VIDEO
        elif self.tip == "2":
            videoPath = self.cale
            if videoPath:
                video = cv.VideoCapture(videoPath)
                self.detectFacesVideo(video)
                video.release()
            else:
                print("Mai incearca...nu ai dat o cale")

        # 3. LIVE --- REAL-TIME
        elif self.tip == "3":
            video = cv.VideoCapture(0)
            self.detectFacesVideo(video)
            video.release()

        else:
            print ("--help daca nu stii")

        cv.destroyAllWindows()


# def checkAndRenameFiles (myfolder_path="1_ViolaJones/dataInput/*"):
#     i = 1
#     for dir in glob.glob(myfolder_path):
#         for f in glob.glob(os.path.join(dir, "*.jpg")):
#             try:
#                 img = cv.imread(f)
#                 img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
#             except:
#                 shutil.copy2(f, dir + 'temp.jpg' + str(i))
#                 img = cv.imread(dir + 'temp.jpg')
#                 img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
#                 os.remove(myfolder_path + 'temp.jpg')
#                 i = i + 1

# functie ca sa imi ia din toate folderelefete si sa mi le salveze cum trebuie
def saveFaceFromImage (myfolder_path="antrenare/dataset/*"):
    id = 1
    for dir in glob.glob("antrenare/dataset/*"):
        index = 1
        for filename in glob.glob(os.path.join(dir, "*.jpg")):
            try:
                print (dir + " " + filename)
                face = CViolaJonesDetection("1", filename, id, index)
                face.detectAllFaces()
                index = index + 1
            except:
                print("Nasol")
        id = id + 1
