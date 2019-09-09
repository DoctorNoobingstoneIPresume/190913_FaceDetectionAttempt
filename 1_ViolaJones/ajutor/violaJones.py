import cv2 as cv
import numpy as np
import argparse

## haar cascades -> massive xml files with features sets (= coresponding to a specific object: face, eyes, etc)

ap = argparse.ArgumentParser()
ap.add_argument("-t", "--tip", required = False, help = "1 - given photo, 2 - given video, 3 - camera", default = "3")
ap.add_argument("-p", "--path", required = False, help = "path to image/video")
args = vars(ap.parse_args())


face_cascade = cv.CascadeClassifier('haarcascade_frontalface_default.xml')

# functie pt detetctarea fetelor in imagini/cadre
def detectFaces (image):
    gray     = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    faces    = face_cascade.detectMultiScale(gray) # depending on the size and the likelyhood...1.3,5

    for (x,y,w,h) in faces:
        cv.rectangle(image, (x,y), (x+w,y+h), (255,0,0), 2) # desenam fata

    cv.imshow('img',image)

# functie pt detectarea fetelor in video=uri
def detectFacesVideo (video):
    while True:
        ret, img = video.read()
        detectFaces(img)
        keyExit = cv.waitKey(30) & 0xff
        if keyExit == ord('q'):  # == 27  => pt esc
            break
    video.release()

# in functie de ce optiune se alege => se stie tipul
if args["tip"] == "1":
    imgPath = args["path"]
    if imgPath:
        img = cv.imread(imgPath)
        detectFaces(img)
        cv.waitKey(0)
    else:
        print("Mai incearca...nu ai dat o cale")

elif args["tip"] == "2":
    videoPath = args["path"]

    if videoPath:
        video = cv.VideoCapture(videoPath)
        detectFacesVideo(video)
    else:
        print("Mai incearca...nu ai dat o cale")

elif args["tip"] == "3":
    video = cv.VideoCapture(0)
    detectFacesVideo(video)
else:
    print ("--help daca nu stii")

cv.destroyAllWindows()
