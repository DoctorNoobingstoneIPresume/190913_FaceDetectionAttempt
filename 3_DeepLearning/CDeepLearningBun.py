# #################################################################################################
# Andra Tomi 2019
# #################################################################################################

import face_recognition
import pickle
import numpy as np
import cv2 as cv
from train import *

import sys
sys.path.insert(1,'../')
from CBaseMethod import CBaseMethod


# =================================================================================================
#                                       CLASS DEEP LEARNING
# =================================================================================================
class CDeepLearning(CBaseMethod):
    #  --------------------------------------------------------------------------------------------
    def __init__(self, tip, cale):
    #  --------------------------------------------------------------------------------------------
        CBaseMethod.__init__(self, tip, cale)

        # Initialize some variables
        face_locations = []
        face_encodings = []
        face_names = []

        self.ok = 0;

    #  --------------------------------------------------------------------------------------------
    def recognizeFaces(self):  # functie pt recunoasterea fetelor in imagini/cadre
    #  --------------------------------------------------------------------------------------------
        colors = {"blue":(255,0,0), "red":(0,0,255), "green":(0,255,0), "white":(255,255,255)}
        color = colors['green']

        if self.ok % 3 == 0:
            small_frame = cv.resize(self.img, (0, 0), fx=0.25, fy=0.25)
            # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
            rgb_small_frame = small_frame[:, :, ::-1]

            # construire blob din imagine
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
            face_names = []

            for face_encoding in face_encodings:
                # See if the face is a match for the known face(s)
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                name = "Unknown"

                # # If a match was found in known_face_encodings, just use the first one.
                # if True in matches:
                #     first_match_index = matches.index(True)
                #     name = known_face_names[first_match_index]

                # Or instead, use the known face with the smallest distance to the new face
                face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = known_face_names[best_match_index]

                face_names.append(name)

                for (top, right, bottom, left), name in zip(face_locations, face_names):
                    # Scale back up face locations since the frame we detected in was scaled to 1/4 size
                    top *= 4
                    right *= 4
                    bottom *= 4
                    left *= 4

                    # Draw a box around the face
                    cv.rectangle(self.img, (left, top), (right, bottom), (0, 0, 255), 2)

                    # Draw a label with a name below the face
                    cv.rectangle(self.img, (left, bottom - 35), (right, bottom), (0, 0, 255), cv.FILLED)
                    font = cv.FONT_HERSHEY_SIMPLEX
                    cv.putText(self.img, name, (left - 6, top - 6), font, 1.0, (255, 255, 255), 1)

            self.ok += 1

            #
            # # draw the bounding box of the face along with the associated
            # # probability
            # text = "{}: {:.2f}%".format(name, proba * 100)
            # y = startY - 10 if startY - 10 > 10 else startY + 10
            # cv.rectangle(image, (startX, startY), (endX, endY),
            #               color, 2)
            # cv.putText(image, text, (startX, y),
            #             cv.FONT_HERSHEY_SIMPLEX, 0.45, color, 2)

            # # draw the bounding box of the face along with the associated
            # # probability
            # text = "{:.2f}%".format(confidence * 100)
            # y = startY - 10 if startY - 10 > 10 else startY + 10
            # cv.rectangle(image, (startX, startY), (endX, endY),
            # 	(0, 0, 255), 2)
            # cv.putText(image, text, (startX, y),
            # 	cv.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)
