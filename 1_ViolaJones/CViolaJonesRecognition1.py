# #################################################################################################
# Andra Tomi 2019
# #################################################################################################

import cv2 as cv
import numpy as np
import sys
import math
import concurrent.futures

class CViolaJonesRecognition:
    #  --------------------------------------------------------------------------------------------
    def __init__(self, tip, cale): # Initializare
    #  --------------------------------------------------------------------------------------------
        self.tip = tip
        self.cale = cale
        self.face_cascade = cv.CascadeClassifier('1_ViolaJones\\haarcascade_frontalface_default.xml')
        # clasificator custom
        self.classifier = cv.face.LBPHFaceRecognizer_create()
        self.classifier.read("1_ViolaJones\\classifier.xml")



    # #  --------------------------------------------------------------------------------------------
    # def __del__(self):   # Destructor
    # #  --------------------------------------------------------------------------------------------
    #     print('Destructor called')

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
        features = self.face_cascade.detectMultiScale(gray_img, scaleFactor, minNeighbors)
        coords = []

        # desenare contur fata
        for (x, y, w, h) in features:
            cv.rectangle(image, (x,y), (x+w, y+h), color, 2)
            # Predicting the id of the user
            id, _ = self.classifier.predict(gray_img[y:y+h, x:x+w])   # vezi cu confidence
            confidence = 1.0 / (1.0 + math.exp(-id));

            if confidence > 0.8:
                # Check for id of user and label the rectangle accordingly
                # Aici poate pun ceva cu baza de date
                if id == 1:
                    cv.putText(image, "Andra", (x, y-4), cv.FONT_HERSHEY_SIMPLEX, 0.3, color, 1, cv.LINE_AA)
                elif id == 2:
                    cv.putText(image, "Alexandra", (x, y-4), cv.FONT_HERSHEY_SIMPLEX, 0.3, color, 1, cv.LINE_AA)
                elif id == 3:
                    cv.putText(image, "Cosmin", (x, y-4), cv.FONT_HERSHEY_SIMPLEX, 0.3, color, 1, cv.LINE_AA)
                elif id == 5:
                    cv.putText(image, "Demet", (x, y-4), cv.FONT_HERSHEY_SIMPLEX, 0.3, color, 1, cv.LINE_AA)
                coords = [x, y, w, h]
            else:
                cv.putText(image, "Unknown", (x, y-4), cv.FONT_HERSHEY_SIMPLEX, 0.3, color, 1, cv.LINE_AA)

        return image


    #  --------------------------------------------------------------------------------------------
    def recognizeFacesVideo (self, video):   # functie pt recunoasterea fetelor in video=uri
    #  --------------------------------------------------------------------------------------------
        while True:
            ret, img = video.read()
            self.img = self.recognizeFaces(img)

            keyExit = cv.waitKey(30) & 0xff
            if keyExit == ord('q'):  # == 27  => pt esc
                break

    #  --------------------------------------------------------------------------------------------
    def get_frame(self):
    #  --------------------------------------------------------------------------------------------

            return cv2.cvtColor(self.img, cv2.COLOR_BGR2RGB)




    #  --------------------------------------------------------------------------------------------
    def runAlgorthm (self):   # functie de recunoastere a fetelor
    #  --------------------------------------------------------------------------------------------
        # in functie de ce optiune se alege => se stie tipul
        # 1. IMAGINE
        # if self.tip == "1":
        #     imgPath = self.cale
        #     if imgPath:
        #         img = cv.imread(imgPath)
        #         self.recognizeFaces(img)
        #         cv.waitKey(0)
        #     else:
        #         print("Mai incearca...nu ai dat o cale")
        #
        # # 2. VIDEO
        # elif self.tip == "2":
        videoPath = self.cale
        print ("video path:", videoPath)
        if videoPath:
            video = cv.VideoCapture(videoPath)

            if not video.isOpened():
                raise ValueError("Unable to open video source", videoPath)

            if video.isOpened():
                video.release()

            self.recognizeFacesVideo(video)

        else:
            print("Mai incearca...nu ai dat o cale")

        # # 3. LIVE --- REAL-TIME
        # elif self.tip == "3":
        #     video = cv.VideoCapture(0)  # 'http:192.168.43.1:8080/video'
        #     if video:
        #         return self.recognizeFacesVideo(video)
        #         video.release()
        #
        # else:
        #     print ("--help daca nu stii")

        cv.destroyAllWindows()
