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
#                                       CLASS DEEP LEARNING
# =================================================================================================
class CDeepLearning(CBaseMethod):
    #  --------------------------------------------------------------------------------------------
    def __init__(self, tip, cale):
    #  --------------------------------------------------------------------------------------------
        CBaseMethod.__init__(self, tip, cale)

        # load our serialized face detector from disk
        protoPath = "3_DeepLearning/face_detection_model/deploy.prototxt"
        modelPath = "3_DeepLearning/face_detection_model/res10_300x300_ssd_iter_140000.caffemodel"
        self.detector = cv.dnn.readNetFromCaffe(protoPath, modelPath)

        # load our serialized face embedding model from disk
        embeddingModel = "3_DeepLearning/openface_nn4.small2.v1.t7"
        self.embedder = cv.dnn.readNetFromTorch(embeddingModel)

        # load the actual face recognition model along with the label encoder
        recognizerPickle = "3_DeepLearning/output/recognizer.pickle"
        lePickle = "3_DeepLearning/output/le.pickle"
        self.recognizer = pickle.loads(open(recognizerPickle, "rb").read())
        self.le = pickle.loads(open(lePickle, "rb").read())

        self.counter = 0

    #  --------------------------------------------------------------------------------------------
    def recognizeFaces(self, image):  # functie pt recunoasterea fetelor in imagini/cadre
    #  --------------------------------------------------------------------------------------------
        colors = {"blue":(255,0,0), "red":(0,0,255), "green":(0,255,0), "white":(255,255,255)}
        color = colors['green']

        t0 = time.perf_counter()

        # construire blob din imagine
        (h, w) = image.shape[:2]
        # print(str(h) + " " + str(w))
        blob = cv.dnn.blobFromImage(cv.resize(image, (300, 300)), 1.0, (300, 300),
                                    (104.0, 177.0, 123.0), swapRB=False, crop=False)

        t1 = time.perf_counter()
        # pasam blob-ul in retea si obtinem detectia si predictiile
        self.detector.setInput(blob)
        t2 = time.perf_counter()
        detections = self.detector.forward()
        t3 = time.perf_counter()
        t4 = t3
        # Incarcam detectiile

        if self.counter % 5 == 0:
            for i in range(0, detections.shape[2]):
                # extragem "confidence"-probabilitatea-asociata cu predictia
                confidence = detections[0, 0, i, 2]

                # se exclud predictiile slabe asigurandu-ne ca probabilitatea ("confidence")
                # este mai mare decat cea mai mica probabilitate ("confidence")
                if confidence > 0.5:
                    # compute the (x, y)-coordinates of the bounding box for the
                    # object
                    box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                    (startX, startY, endX, endY) = box.astype("int")

                # extract the face ROI
                    face = image[startY:endY, startX:endX]
                    (fH, fW) = face.shape[:2]

                    # ensure the face width and height are sufficiently large
                    if fW < 20 or fH < 20:
                        continue

                # construire blob din fața ROI, apoi il pasam
                # prim modelul "embedding" de fete pt a obtine
                # cuantificarea 128-d a fetei
                if face.any():
                    t4 = time.perf_counter()
                    faceBlob = cv.dnn.blobFromImage(face, 1.0 / 255, (96, 96),
                                                    (0, 0, 0), swapRB=True, crop=False)

                    self.embedder.setInput(faceBlob)
                    vec = self.embedder.forward()

                    preds = self.recognizer.predict_proba(vec)[0]
                    j = np.argmax(preds)
                    proba = preds[j]
                    name = self.le.classes_[j]

                    # draw the bounding box of the face along with the associated
                    # probability
                    text = "{}: {:.2f}%".format(name, proba * 100)
                    y = startY - 10 if startY - 10 > 10 else startY + 10
                    cv.rectangle(image, (startX, startY), (endX, endY),
                                  color, 2)
                    cv.putText(image, text, (startX, y),
                                cv.FONT_HERSHEY_SIMPLEX, 0.45, color, 2)

                # # draw the bounding box of the face along with the associated
                # # probability
                # text = "{:.2f}%".format(confidence * 100)
                # y = startY - 10 if startY - 10 > 10 else startY + 10
                # cv.rectangle(image, (startX, startY), (endX, endY),
                # 	(0, 0, 255), 2)
                # cv.putText(image, text, (startX, y),
                # 	cv.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)
        self.counter += 1
        t5 = time.perf_counter()

        print ("             t0 {0:0.3f} t1 {1:0.3f} t2 {2:0.3f} t3 {3:0.3f} t4 {4:0.3f} t5".format (t1 - t0, t2 - t1, t3 - t2, t4 - t3, t5 - t4))


        return image

    #  --------------------------------------------------------------------------------------------
    def detectFaces(self):  # functie pt recunoasterea fetelor in imagini/cadre
    #  --------------------------------------------------------------------------------------------
        colors = {"blue":(255,0,0), "red":(0,0,255), "green":(0,255,0), "white":(255,255,255)}
        color = colors['green']

        # construire blob din imagine
        image = self.img
        (h, w) = image.shape[:2]
        blob = cv.dnn.blobFromImage(cv.resize(image, (300, 300)), 1.0, (300, 300),
                                    (104.0, 177.0, 123.0), swapRB=False, crop=False)

        # pasam blob-ul in retea si obtinem detectia si predictiile
        self.detector.setInput(blob)
        detections = self.detector.forward()

        # Incarcam detectiile
        for i in range(0, detections.shape[2]):
            # extragem "confidence"-probabilitatea-asociata cu predictia
            confidence = detections[0, 0, i, 2]

            # se exclud predictiile slabe asigurandu-ne ca probabilitatea ("confidence")
            # este mai mare decat cea mai mica probabilitate ("confidence")
            if confidence > 0.5:
                # compute the (x, y)-coordinates of the bounding box for the
                # object
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                (startX, startY, endX, endY) = box.astype("int")

            # extract the face ROI
                face = image[startY:endY, startX:endX]
                (fH, fW) = face.shape[:2]

                # ensure the face width and height are sufficiently large
                if fW < 20 or fH < 20:
                    continue

            # construire blob din fața ROI, apoi il pasam
            # prim modelul "embedding" de fete pt a obtine
            # cuantificarea 128-d a fetei
            faceBlob = cv.dnn.blobFromImage(face, 1.0 / 255, (96, 96),
                                            (0, 0, 0), swapRB=True, crop=False)
            self.embedder.setInput(faceBlob)
            vec = self.embedder.forward()

            preds = self.recognizer.predict_proba(vec)[0]
            j = np.argmax(preds)
            proba = preds[j]
            name = self.le.classes_[j]

            # draw the bounding box of the face along with the associated
            # probability
            text = "{}: {:.2f}%".format(name, proba * 100)
            y = startY - 10 if startY - 10 > 10 else startY + 10
            cv.rectangle(image, (startX, startY), (endX, endY),
                          color, 2)
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
        self.img = image
