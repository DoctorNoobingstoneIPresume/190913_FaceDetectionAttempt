# #################################################################################################
# Andra Tomi 2019
# #################################################################################################

from tkinter import *
import cv2 as cv
import PIL.Image, PIL.ImageTk
import time
import threading

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




#ImageEx: An image with attached information (its index in the video and its rectangle of detected faces).
class ImageEx:
    def __init__ (self, index, image):
        (h, w) = image.shape [: 2]
        print ("ImageEx: index {0:d}, image {1:d}x{2:d}.".format (index, w, h))

        self.index = index
        self.image = image
        self.rc    = [0, 0, 0, 0]



# m2w_queue: A queue of ImageEx objects passed from Master to Worker.
m2w_queue = []

# w2m_queue: A queue of ImageEx objects passed from Worker to Master.
w2m_queue = []

# condition: A mutex-and-condition-variable.
#   m2w_queue and w2m_queue should only be accessed while the mutex is acquired (after condition.acquire () and before condition.release ()).
#   When the Master places items for the Worker in m2w_queue, the Master should call condition.notify ().
#   This wakes up the Worker, who otherwise is deep in sleep by having called condition.wait ().
condition = threading.Condition ()

# workerthread:
workerthread = None

def stop_workerthread ():

    print ("stopWorkerThread 0...")

    global condition, m2w_queue, w2m_queue, workerthread
    condition.acquire ()
    m2w_queue.append (False)
    condition.notify ()
    condition.release ()

    sys.stdout.flush ()
    #workerthread.join ()
    workerthread = None
    print ("stopWorkerThread 1...")




class WorkerThread (threading.Thread):
    def __init__ (self, method):
        threading.Thread.__init__ (self)
        self.method = method

    def run (self):
        global m2w_queue, w2m_queue, lock, condition
        while True:
            condition.acquire ()

            while not len (m2w_queue):
                print ("WorkerThread: Nothing in m2w_queue... Calling condition.wait ()...")
                sys.stdout.flush ()
                condition.wait ()
                print ("WorkerThread: I'm awake, I'm awake ! len (m2w_queue) == {0:d}.".format (len (m2w_queue)))

            imageex = m2w_queue.pop ()
            if type (imageex) is bool:
                break

            condition.release ()

            sys.stdout.flush ()
            t0         = time.perf_counter ()
            imageex.rc = self.method.detectFaces (imageex.image)
            t1         = time.perf_counter ()
            print ("WorkerThread: dt {0:0.3f}".format (t1 - t0))

            condition.acquire ()
            w2m_queue.append (imageex)
            condition.release ()



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
        self.method   = None


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

        self.index = 0
        global workerthread
        if not workerthread:
            workerthread = WorkerThread (self.method)
            workerthread.start ()

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
                if True:
                    global condition, m2w_queue, w2m_queue

                    condition.acquire ()
                    if not len (m2w_queue):
                        m2w_queue.append (ImageEx (self.index, frame))
                        condition.notify ()
                    condition.release ()

                    #rc = method.detectFaces(frame)
                    #color = (0, 0, 255)
                    #cv.rectangle (frame, (rc [0], rc [1]), (rc [2], rc [3]), color, 2)

                frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
                self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
                self.canvas.create_image(width/2, height/2, anchor=CENTER, image = self.photo)

            timeAfter = time.perf_counter()
            timeBetweenFrames = timeAfter - self.timeStart
            self.timeStart = timeAfter

            #print ("dt {0:0.3f}".format (timeBetweenFrames))
            #sys.stdout.flush()

            self.index += 1

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

        print ("delete 0...")

        if self.timerID != 0:
            self.master.after_cancel(self.timerID)
        del self.method
        self.canvas.delete("all")

        print ("delete 2...")




























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
