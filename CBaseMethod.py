# #################################################################################################
# Andra Tomi 2019
# #################################################################################################

import cv2 as cv
import numpy as np
import imutils
import sys
import math
import concurrent.futures


# =================================================================================================
#                                       CLASS  BASE METHOD
# =================================================================================================
class CBaseMethod:
    #  --------------------------------------------------------------------------------------------
    def __init__(self, tip, cale): # Initializare
    #  --------------------------------------------------------------------------------------------
        self.tip = tip
        self.cale = cale
        self.recognizeAllFaces()



    #  --------------------------------------------------------------------------------------------
    def recognizeFaces(self, image):
    #  --------------------------------------------------------------------------------------------
        raise NotImplementedError()


    # --------------------------------------------------------------------------------------------
    def detectFaces(self, image):
    #  --------------------------------------------------------------------------------------------
        raise NotImplementedError()



    #  --------------------------------------------------------------------------------------------
    def getImage(self, width=670):
    #  --------------------------------------------------------------------------------------------
        self.img = imutils.resize(self.img, width)
        image = self.recognizeFaces(self.img)
        return cv.cvtColor(image, cv.COLOR_BGR2RGB)


    #  --------------------------------------------------------------------------------------------
    def getFrame (self, width=670):   # functie pt recunoasterea fetelor in video=uri
    #  --------------------------------------------------------------------------------------------
    # After it is called once, the update method will be automatically called every delay milliseconds
        if self.video.isOpened():
            ret, img  = self.video.read()
            # h, w, c = img.shape
            # print(str(ret) + " -- width:" + str(w) + " height: " + str(h))
            # self.img = imutils.resize(img, width)
            image = self.detectFaces(img)
            if ret:
                # Return a boolean success flag and the current frame converted to BGR
                return (ret, cv.cvtColor(image, cv.COLOR_BGR2RGB))
            else:
                return (ret, None)
        else:
            return (ret, None)


    #  --------------------------------------------------------------------------------------------
    def recognizeFacesVideo (self):   # functie pt recunoasterea fetelor in video=uri
    #  --------------------------------------------------------------------------------------------
    # After it is called once, the update method will be automatically called every delay milliseconds
        while True:
            # self.delay = 30
            self.ret, self.img = self.video.read()
            self.recognizeFaces()

            keyExit = cv.waitKey(30) & 0xff
            if keyExit == ord('q'):  # == 27  => pt esc
                break


    #  --------------------------------------------------------------------------------------------
    def recognizeAllFaces (self):   # functie de recunoastere a fetelor
    #  --------------------------------------------------------------------------------------------
        # in functie de ce optiune se alege => se stie tipul
        # 1. IMAGINE
        if self.tip == "1":
            if self.cale:
                self.img = cv.imread(self.cale)
                # self.recognizeFaces()
                # cv.waitKey(0)
            else:
                print("Mai incearca...nu ai dat o cale")

        # 2. VIDEO
        elif self.tip == "2":
            if self.cale:
                self.video = cv.VideoCapture(self.cale)
                # self.recognizeFacesVideo()
                # self.video.release()
            else:
                print("Mai incearca...nu ai dat o cale")

        # 3. LIVE --- REAL-TIME
        elif self.tip == "3":
            self.video = cv.VideoCapture(0) #'http:192.168.43.1:8080/video'
            # if video:
            #     self.recognizeFacesVideo()
            #     self.video.release()
        else:
            print ("--help daca nu stii")
        # cv.destroyAllWindows()

    #  --------------------------------------------------------------------------------------------
    def getSize(self):
    #  --------------------------------------------------------------------------------------------
        if self.tip == "1":
            h, w, c = self.img.shape
        else:
            w = self.video.get(3)
            h = self.video.get(4)

        return (w, h)

    #  --------------------------------------------------------------------------------------------
    def __del__(self):
    #  --------------------------------------------------------------------------------------------
        if self.tip == "2" or self.tip == "3":
            if self.video.isOpened():
                self.video.release()
        cv.destroyAllWindows()
