import face_recognition
import pickle
import numpy as np
import cv2 as cv

## haar cascades -> massive xml files with features sets (= coresponding to a specific object: face, eyes, etc)
class CDeepLearning:
    def __init__(self, tip, cale):
        self.tip = tip
        self.cale = cale
        self.net = cv.dnn.readNetFromCaffe("3_DeepLearning/deploy.prototxt.txt", "3_DeepLearning/res10_300x300_ssd_iter_140000.caffemodel")

    # functie pt detetctarea fetelor in imagini/cadre
    def detectFaces (self, image):
        img = cv.cvtColor(image, cv.COLOR_BGR2RGB)
        (h, w) = img.shape[:2]
        blob = cv.dnn.blobFromImage(cv.resize(image, (300, 300)), 1.0,
        	(300, 300), (104.0, 177.0, 123.0))

        # pasam blob-ul in retea si obtinem detectia si predictiile
        self.net.setInput(blob)
        detections = self.net.forward()

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

        		# draw the bounding box of the face along with the associated
        		# probability
        		text = "{:.2f}%".format(confidence * 100)
        		y = startY - 10 if startY - 10 > 10 else startY + 10
        		cv.rectangle(image, (startX, startY), (endX, endY),
        			(0, 0, 255), 2)
        		cv.putText(image, text, (startX, y),
        			cv.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)
        cv.imshow('img',image)

    # functie pt detectarea fetelor in video=uri
    def detectFacesVideo (self, video):
        while True:
            ret, img = video.read()
            self.detectFaces(img)
            keyExit = cv.waitKey(30) & 0xff
            if keyExit == ord('q'):  # == 27  => pt esc
                break
        video.release()

    # functie de detectare fete care alege pe ce sa detecteze: img, video, live
    def detectAllFaces (self):
        # in functie de ce optiune se alege => se stie tipul
        if self.tip == "1":
            imgPath = self.cale
            if imgPath:
                img = cv.imread(imgPath)
                self.detectFaces(img)
                cv.waitKey(0)
            else:
                print("Mai incearca...nu ai dat o cale")

        elif self.tip == "2":
            videoPath = self.cale
            if videoPath:
                video = cv.VideoCapture(videoPath)
                self.detectFacesVideo(video)
            else:
                print("Mai incearca...nu ai dat o cale")

        elif self.tip == "3":
            video = cv.VideoCapture(0)
            self.detectFacesVideo(video)

        else:
            print ("--help daca nu stii")

        cv.destroyAllWindows()
