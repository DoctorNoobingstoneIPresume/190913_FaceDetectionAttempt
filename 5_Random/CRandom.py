# #################################################################################################
# Andra Tomi 2019
# #################################################################################################

import pickle
import numpy as np
import cv2 as cv
import time

import sys
sys.path.insert(1,'../')
from CBaseMethod import CBaseMethod


# =================================================================================================
#                                       CLASS RANDOM
# =================================================================================================
class CRandom(CBaseMethod):
    #  --------------------------------------------------------------------------------------------
    def __init__(self, tip, cale):
    #  --------------------------------------------------------------------------------------------
        CBaseMethod.__init__(self, tip, cale)

    #  --------------------------------------------------------------------------------------------
    def recognizeFaces(self, image):  # functie pt recunoasterea fetelor in imagini/cadre
    #  --------------------------------------------------------------------------------------------
        color = (255, 0, 0)
        (h, w) = image.shape [: 2]

        rc = self.detectFaces (image)

        cv.rectangle (image, (rc [0], rc [1]), (rc [2], rc [3]), color, 2)
        text = "Random"
        cv.putText (image, text, (int (1*w/4), int (1*h/4) - 20), cv.FONT_HERSHEY_SIMPLEX, 0.45, color, 2)
        return image

    #  --------------------------------------------------------------------------------------------
    def detectFaces(self, image):
    #  --------------------------------------------------------------------------------------------
        #color = (0, 255, 0)
        (h, w) = image.shape [: 2]

        # It is up to the caller to over-draw the rectangle we return.
        #cv.rectangle (image, (int (1*w/4), int (1*h/4)), (int (3*w/4), int (3*h/4)), color, 2)
        ##cv.rectangle (image, (200, 100), (400, 200), color, 2)
        #return image

        rc = [int (1*w/4), int (1*h/4), int (3*w/4), int (3*h/4)]
        time.sleep (0.25)
        return rc
