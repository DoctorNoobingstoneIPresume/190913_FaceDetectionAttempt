# #################################################################################################
# Andra Tomi 2019
# #################################################################################################

from tkinter import *
import cv2 as cv
import PIL.Image, PIL.ImageTk
import time

import sys
sys.path.insert(1,'1_ViolaJones/')
from CViolaJonesRecognition import CViolaJonesRecognition
sys.path.insert(2,'2_HOGs/')
from CHOG import CHOG
sys.path.insert(3,'3_DeepLearning/')
from CDeepLearning import CDeepLearning
sys.path.insert(4,'BD/')
from dbMethods import *
sys.path.insert(5,'5_Random')
from CRandom import CRandom


class CStart(Canvas):
    # --------------------------------------------------------------------------
    def __init__(self, master):
    # --------------------------------------------------------------------------
        self.master = master

        # Create a canvas that can fit the above video source size
        self.canvas = Canvas(master, height=550, width=670, bg="#111111", bd=0, highlightthickness=0, relief='ridge') # width = self.input.width, height = self.input.height)
        self.canvas.place(x=230, anchor="nw")

        self.canvasBack = Canvas(self.canvas, height=550, width=670, bg="#111111", bd=0, highlightthickness=0, relief='ridge') # width = self.input.width, height = self.input.height)

        self.timeStart = time.perf_counter()
        self.timerID = 0

        self.myCanvas = []


    # --------------------------------------------------------------------------
    def selectMethod(self, method, typeInput, inputFile=""):
    # --------------------------------------------------------------------------
        self.input_type = typeInput
        self.input_path = inputFile

        if method == 1:
            print("metoda 1")
            self.method = CViolaJonesRecognition(str(typeInput),self.input_path)

        elif method == 2:
            print("metoda 2")
            self.method = CHOG(str(typeInput),self.input_path)

        elif method == 3:
            print("metoda 3")
            self.method = CDeepLearning(str(typeInput),self.input_path)

        elif method == 5:
            print("metoda 5")
            self.method = CRandom (str (typeInput), self.input_path)

        else:
            raise NotImplementedError ()

        self.timerr = 0
        # self.prepare()
        self.update()


    # --------------------------------------------------------------------------
    def update(self):
    # --------------------------------------------------------------------------
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        method = self.method

        # Get a frame from the video source
        if self.input_type==1:
            img = method.getImage()
            # img = cv.resize(img, (self.width, self.height))
            self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(img))
            self.canvas.create_image(width/2, height/2, anchor=CENTER, image = self.photo)
        else:
            ret, frame = method.getFrame()
            #img = cv.resize(frame, (self.width, self.height))
            # im = cv.cvtColor(im, cv.COLOR_BGR2RGB)
            if ret:
                self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
                self.canvas.create_image(width/2, height/2, anchor=CENTER, image = self.photo)

            timeAfter = time.perf_counter()
            timeBetweenFrames = timeAfter - self.timeStart
            self.timeStart = timeAfter

            print ("dt {0:0.3f}".format (timeBetweenFrames))
            sys.stdout.flush()
            self.timerID = self.master.after(max (1, int (1000 / 80 / method.fps)), self.update)

    # --------------------------------------------------------------------------
    def setStartImage(self, file):
    # --------------------------------------------------------------------------
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()

        image = cv.imread(file)
        img = cv.cvtColor(image, cv.COLOR_BGR2RGB)
        self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(img))
        self.canvas.create_image(0, 0, anchor=NW, image = self.photo)

        #
        # image = PIL.Image.open(file)
        # pic = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(image))
        # self.canvas.create_image(width/2, height/2, anchor=CENTER, image = pic)


    # --------------------------------------------------------------------------
    def showMeThePeople(self):
    # --------------------------------------------------------------------------
        self.canvasBack.place(x=0, anchor="nw")

        db = dbOp()
        nr = int(db.getAllDbEntries()) + 1

        w=134
        h=183
        W = 670
        H = 550

        x = 0
        y = 0
        i = 1

        while i < nr:
            canvas = ShowPeople(self.canvasBack,i)
            if x == W:
                x = 0
                y = y + h
            (nume, image, found, date) = db.getData(i)
            print (nume + " " + found)
            canvas.addPerson(x, y, w, h, nume, image, found, date)
            self.myCanvas.append(canvas)
            x += w
            i += 1


    # --------------------------------------------------------------------------
    def saveDataDB(self):
    # --------------------------------------------------------------------------
        db = dbOp()
        db.saveChangesToMainTable()

    # --------------------------------------------------------------------------
    def clearTable(self):
    # --------------------------------------------------------------------------
        db = dbOp()
        db.clearTable()



    # --------------------------------------------------------------------------
    def cleanCanvas(self):
    # --------------------------------------------------------------------------
        del self.myCanvas[:]
        self.canvasBack.place_forget()

    # --------------------------------------------------------------------------
    def delete(self):
    # --------------------------------------------------------------------------
        if self.timerID != 0:
            self.master.after_cancel(self.timerID)
        del self.method
        self.canvas.delete("all")




























# # App(Tk(), "Tkinter and OpenCV", "00videos/lunch_scene.mp4")
# # --------------------------------------------------------------------------
# def prepare(self):
# # --------------------------------------------------------------------------
#     # pregatiri
#     W = 670
#     H = 550
#
#     # to set values for resize images/frames
#     w, h = self.method.getSize()
#
#     if w > W:
#         aux = h
#         h = (W/w)*aux
#         w = W
#     if h > H:
#         aux = w
#         w = (H/h)*aux
#         h = H
#     if w < W and h < H:
#         if w > h:
#             h = (W/w)*h
#             w = W
#         else:
#             w = (H/h)*w
#             h = H
#
#     self.width = int(w)
#     self.height = int(h)
#
#     self.update()
#
#     # After it is called once, the update method will be automatically called every delay milliseconds
