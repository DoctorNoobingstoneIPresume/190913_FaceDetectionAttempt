# #################################################################################################
# Andra Tomi 2019
# #################################################################################################

import dlib
import cv2 as cv
import sys
import math

import sys
sys.path.insert(1,'../')
from CBaseMethod import CBaseMethod


# =================================================================================================
#                                            CLASS HOG
# =================================================================================================
class CHOG(CBaseMethod):
    #  --------------------------------------------------------------------------------------------
    def __init__(self, tip, cale):
    #  --------------------------------------------------------------------------------------------
        CBaseMethod.__init__(self, tip, cale)

        self.detector = dlib.get_frontal_face_detector()
        #self.dets     = detector(img, 2)

        # clasificator custom
        self.classifier = cv.face.LBPHFaceRecognizer_create()
        self.classifier.read("1_ViolaJones\\classifier.xml")

    #  --------------------------------------------------------------------------------------------
    def recognizeFaces (self,image):
    #  --------------------------------------------------------------------------------------------
        # variavile locale folositoare
        colors = {"blue":(255,0,0), "red":(0,0,255), "green":(0,255,0), "white":(255,255,255)}
        scaleFactor = 1.1
        minNeighbors = 10
        color = colors['green']
        text = "Fataaaa"

        #img   = dlib.load_rgb_image(image)
        # The 1 in the second argument indicates that we should upsample the image
        # 1 time.  This will make everything bigger and allow us to detect more
        # faces.
        img = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
        dets = self.detector(img, 1)
        # coords = []

        for k, d in enumerate(dets):
            x = d.left()
            y = d.top()
            xw = d.right() # x + w
            yh = d.bottom() # y  + h
            # print ("Detection {}: Left: {} Top: {} Right: {} Bottom: {}".format(k, d.left(), d.top(), d.right(), d.bottom()))
            cv.rectangle(image, (x, y), (xw, yh), color, 2)

            # Predicting the id of the user
            id, ceva = self.classifier.predict(img[y:yh, x:xw])   # vezi cu confidence
            confidence = 1.0 / (1.0 + math.exp(-id));

            if confidence > 0.8:
                # Check for id of user and label the rectangle accordingly
                # Aici poate pun ceva cu baza de date
                if id == 1:
                    cv.putText(image, "Andra", (x, y-4), cv.FONT_HERSHEY_SIMPLEX, 0.4, color, 1, cv.LINE_AA)
                elif id == 2:
                    cv.putText(image, "Alexandra", (x, y-4), cv.FONT_HERSHEY_SIMPLEX, 0.4, color, 1, cv.LINE_AA)
                elif id == 3:
                    cv.putText(image, "Cosmin", (x, y-4), cv.FONT_HERSHEY_SIMPLEX, 0.4, color, 1, cv.LINE_AA)
                elif id == 5:
                    cv.putText(image, "Demet", (x, y-4), cv.FONT_HERSHEY_SIMPLEX, 0.4, color, 1, cv.LINE_AA)
                # coords = [x, y, w, h]
            else:
                cv.putText(image, "Unknown", (x, y-4), cv.FONT_HERSHEY_SIMPLEX, 0.4, color, 1, cv.LINE_AA)
        return image

    #  --------------------------------------------------------------------------------------------
    def detectFaces (self):
    #  --------------------------------------------------------------------------------------------
        # variavile locale folositoare
        colors = {"blue":(255,0,0), "red":(0,0,255), "green":(0,255,0), "white":(255,255,255)}
        scaleFactor = 1.1
        minNeighbors = 10
        color = colors['green']
        text = "Fataaaa"

        #img   = dlib.load_rgb_image(image)
        # The 1 in the second argument indicates that we should upsample the image
        # 1 time.  This will make everything bigger and allow us to detect more
        # faces.
        img = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
        dets = self.detector(img, 3)
        # coords = []

        for k, d in enumerate(dets):
            x = d.left()
            y = d.top()
            xw = d.right() # x + w
            yh = d.bottom() # y  + h
            # print ("Detection {}: Left: {} Top: {} Right: {} Bottom: {}".format(k, d.left(), d.top(), d.right(), d.bottom()))
            cv.rectangle(image, (x, y), (xw, yh), color, 2)
