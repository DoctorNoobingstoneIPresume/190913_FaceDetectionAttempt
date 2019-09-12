# #################################################################################################
# Andra Tomi 2019
# #################################################################################################

import cv2 as cv
import numpy as np
import math
import concurrent.futures
from datetime import datetime

import sys
sys.path.insert(1,'../')
from CBaseMethod import CBaseMethod

# =================================================================================================
#                                       CLASS VIOLA JONES
# =================================================================================================
class CViolaJonesRecognition(CBaseMethod): ## haar cascades -> massive xml files with features sets (= coresponding to a specific object: face, eyes, etc)
    #  --------------------------------------------------------------------------------------------
    def __init__(self, tip, cale): # Initializare
    #  --------------------------------------------------------------------------------------------
        CBaseMethod.__init__(self, tip, cale)

        self.detector = cv.CascadeClassifier('1_ViolaJones\\haarcascade_frontalface_default.xml')

        # clasificator custom
        self.classifier = cv.face.LBPHFaceRecognizer_create()
        self.classifier.read("1_ViolaJones\\classifier.yml")


    #  --------------------------------------------------------------------------------------------
    def recognizeFaces (self, image):   # functie pt detetctarea fetelor in imagini/cadre
    # --------------------------------------------------------------------------------------------
        # variavile locale folositoare
        colors = {"blue":(255,0,0), "red":(0,0,255), "green":(0,255,0), "white":(255,255,255)}
        scaleFactor = 1.1
        minNeighbors = 10
        color = colors['green']
        text = "Fataaaa"

        # transformare in grayscale
        gray_img = cv.cvtColor(image, cv.COLOR_BGR2GRAY)

        # extragere trasaturi
        features = self.detector.detectMultiScale(gray_img, scaleFactor, minNeighbors)
        coords = []

        # desenare contur fata
        for (x, y, w, h) in features:
            cv.rectangle(image, (x,y), (x+w, y+h), color, 2)
            # Predicting the id of the user
            id, _ = self.classifier.predict(gray_img[y:y+h, x:x+w])   # vezi cu confidence
            confidence = 1.0 / (1.0 + math.exp(-id));



            if confidence > 0.9:
                # Check for id of user and label the rectangle accordingly
                # Aici poate pun ceva cu baza de date
                now = datetime.now()
                dt_string = now.strftime("%d-%m-%Y %H:%M:%S")
                self.bd.updateTable(id,1,dt_string)

                if id == 1:
                    cv.putText(image, "Beyonce", (x, y-4), cv.FONT_HERSHEY_SIMPLEX, 0.4, color, 1, cv.LINE_AA)
                elif id == 2:
                    cv.putText(image, "Rachel", (x, y-4), cv.FONT_HERSHEY_SIMPLEX, 0.4, color, 1, cv.LINE_AA)
                elif id == 3:
                    cv.putText(image, "Steve", (x, y-4), cv.FONT_HERSHEY_SIMPLEX, 0.4, color, 1, cv.LINE_AA)
                coords = [x, y, w, h]
            else:
                cv.putText(image, "Unknown", (x, y-4), cv.FONT_HERSHEY_SIMPLEX, 0.4, color, 1, cv.LINE_AA)
        return image

    #  --------------------------------------------------------------------------------------------
    def detectFaces (self, image):   # functie pt detetctarea fetelor in imagini/cadre
    # --------------------------------------------------------------------------------------------
        # variavile locale folositoare
        colors = {"blue":(255,0,0), "red":(0,0,255), "green":(0,255,0), "white":(255,255,255)}
        scaleFactor = 1.05   # reduce cu 5% imaginea la fiecare parcurgere
        minNeighbors = 3     # intre 3-6
        color = colors['green']

        # transformare in grayscale
        gray_img = cv.cvtColor(image, cv.COLOR_BGR2GRAY)

        # extragere trasaturi
        features = self.detector.detectMultiScale(gray_img, scaleFactor, minNeighbors)
        coords = []

        # desenare contur fata
        for (x, y, w, h) in features:
            cv.rectangle(image, (x,y), (x+w, y+h), color, 2)
        return image


# def saveFaceFromImage (myfolder_path="antrenare/dataset/*"):
#     id = 1
#     for dir in glob.glob("antrenare/dataset/*"):
#         index = 1
#         for filename in glob.glob(os.path.join(dir, "*.jpg")):
#             try:
#                 print (dir + " " + filename)
#                 face = CViolaJonesDetection("1", filename, id, index)
#                 face.getIma()
#                 index = index + 1
#             except:
#                 print("Nasol")
#         id = id + 1
