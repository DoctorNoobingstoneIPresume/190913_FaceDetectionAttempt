from tkinter import *
import PIL.Image, PIL.ImageTk
import math

# root = Tk()
#

# canvas = Canvas(root, height=550, width=670, bg="#111111", bd=0, highlightthickness=0, relief='ridge') # width = self.input.width, height = self.input.height)
# canvas.place(anchor="nw")
#
# image = PIL.Image.open('../InterfataButoane/imaginePornire.jpg')
# pic = PIL.ImageTk.PhotoImage(image)
#
#
# canvas.create_image(0, 0, image = pic, anchor = NW)

# canvas = Canvas(root, height=550, width=670, bg="#111111", bd=0, highlightthickness=0, relief='ridge') # width = self.input.width, height = self.input.height)
# canvas.place(anchor="nw")
#
# personInfo = Frame(canvas, height=183, width=134, bg="blue", bd=2)
# personInfo.place(anchor="nw")
#
# image =  Canvas(personInfo, height=135, width=123, bg="yellow", bd=2) # width = self.input.width, height = self.input.height)
# image.place(anchor="nw")
#
# text = Label(personInfo, text="Numele pesroanei", bg="white", fg="black")
# text.pack(expand=1, anchor="nw", ipady=135)


def make_label(master, x, y, w, h, tn, td):
    textNume = StringVar()
    textNume.set(tn)
    textData = StringVar()
    textData.set(td)

    personInfo = Frame(master, height=h, width=w, bg="blue", bd=2)
    personInfo.pack_propagate(0) # don't shrink
    personInfo.place(x=x, y=y, anchor="nw")

    image =  Canvas(personInfo, height=130, width=123, bg="yellow", bd=2) # width = self.input.width, height = self.input.height)
    image.pack()

    name = Label(personInfo, text=textNume.get(), bg="red", bd=2)
    name.pack(fill=X)

    dateIdent = Label(personInfo, text=textData.get(), bg="red",bd=2)

    dateIdent.pack(fill=X)

### -
root = Tk()
root.geometry('670x550')

# sa vedem cat de fereastra
elementsNo = 18
height = math.ceil((elementsNo/5)*h)
frame=Frame(root,width=670,height=550)
frame.grid(row=0,column=0)


## Canvas-ul
canvas = Canvas(frame, width=650, height=550, bg="#111111", bd=0, highlightthickness=0, relief='ridge')# width = self.input.width, height = self.input.height)
# canvas.place(anchor="nw")
canvasWidth = canvas.winfo_width()
canvasHeight = canvas.winfo_height()


## var
x = 0
y = 0
w = 130
h = 183

name = "name"
date = "date"

# check if window is enough
height = math.ceil((elementsNo/5)*h)
# if height > canvasHeight:
#     newCanvasHeight = height
#     canvas.configure(scrollregion=(0,0,canvasWidth,newCanvasHeight))
#
#     vbar=Scrollbar(frame,orient=VERTICAL)
#     vbar.pack(side=RIGHT,fill=Y)
#
#     vbar.config(command=canvas.yview)
#     canvas.config(width=650,height=550)
#     canvas.config(yscrollcommand=vbar.set)
#     canvas.pack(side=LEFT,expand=True,fill=Y)
#
# i = elementsNo
# step = 1

while elementsNo:

    if step == 6:
        x = 0
        y += h
        step = 1

    make_label(canvas, x, y, w, h, "nume", "data")
    x += w
    elementsNo -= 1
    step += 1

root.mainloop()


# from tkinter import *
# import cv2 as cv
# import PIL.Image, PIL.ImageTk
# import time
# from skimage.transform import resize
#
# import sys
# sys.path.insert(1,'1_ViolaJones/')
# from CViolaJonesRecognition import CViolaJonesRecognition
# sys.path.insert(2,'2_HOGs/')
# from CHOG import HOG
# sys.path.insert(3,'3_DeepLearning/')
# from CDeepLearning import DeepLearning
#
# class App:
#     def __init__(self, window, window_title, video_source=0):
#         self.window = window
#         self.window.title(window_title)
#         self.video_source = video_source
#
#         # open video source (by default this will try to open the computer webcam)
#         self.vid = CViolaJonesRecognition("2",self.video_source)
#         # self.vid.recognizeAllFaces()
#
#
#         # Create a canvas that can fit the above video source size
#         self.canvas = Canvas(window, height=470, width=500) # width = self.vid.width, height = self.vid.height)
#         self.canvas.pack()
#
#         W = 500
#         H = 470
#         # to set values for resize images/frames
#         if self.vid.video.isOpened():
#             w = self.vid.video.get(3)   # float
#             h = self.vid.video.get(4) # float
#
#         if w > W:
#             h = (W/w)*h
#             w = W
#         if h > H:
#             w = (H/h)*w
#             h = H
#         if w < W and h < H:
#             if w > h:
#                 h = (W/w)*h
#                 w = W
#             else:
#                 w = (H/h)*w
#                 h = H
#
#         self.width = int(w)
#         self.height = int(h)
#
#         # After it is called once, the update method will be automatically called every delay milliseconds
#         self.timerr = 0
#         self.update()
#
#
#     def update(self):
#         # Get a frame from the video source
#         ret, frame = self.vid.getFrame()
#
#         # height, width, channels = frame.shape
#         # im = frame.resize((self.width, self.height), PIL.Image.ANTIALIAS)
#         im = cv.resize(frame , (self.width, self.height))
#         im = cv.cvtColor(im, cv.COLOR_BGR2RGB)
#         # im.save("aux.jpg")
#         if ret:
#             self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
#             self.canvas.create_image(0, 0, image = self.photo, anchor = NW)
#
#         self.window.after(5, self.update)
#
# App(Tk(), "Tkinter and OpenCV", "00videos/lunch_scene.mp4")
