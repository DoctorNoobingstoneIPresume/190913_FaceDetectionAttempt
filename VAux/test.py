# import tkinter as tk
# from tkinter import *
#
# def add():
#     x.set(x.get() + 1)
#     y.set(y.get()+1)
#
#
# def subtract():
#     x.set(x.get() - 5)
#
# def trace_var(*args):
#     if x.get() < 5 or y.get() < 6:
#         subtractB.configure(state=DISABLED)
#     else:
#         subtractB.configure(state=NORMAL)
#
#
# main = Tk()
#
# addB = Button(main, text="Add", command=add)
# addB.pack()
# subtractB = Button(main, text="Subtract", command=subtract)
# subtractB.pack()
#
#
# y = IntVar()
# y.trace('w', trace_var)
# y.set(0)
# Label(main, textvariable=y).pack()
#
# x = IntVar()
# x.trace('w', trace_var)
# x.set(0)
# Label(main, textvariable=x).pack()
#
# main.mainloop()
#
# import sys
# from tkinter import *



# ABOUT_TEXT = """About
#
# SPIES will search your chosen directory for photographs containing
# GPS information. SPIES will then plot the co-ordinates on Google
# maps so you can see where each photograph was taken."""
#
# DISCLAIMER = """
# Disclaimer
#
# Simon's Portable iPhone Exif-extraction Software (SPIES)
# software was made by Simon. This software
# comes with no guarantee. Use at your own risk"""
#
# def clickAbout():
#     toplevel = Toplevel()
#     label1 = Label(toplevel, text=ABOUT_TEXT, height=0, width=100)
#     label1.pack()
#     label2 = Label(toplevel, text=DISCLAIMER, height=0, width=100)
#     label2.pack()
#
#
# app = Tk()
# app.title("SPIES")
# app.geometry("500x300+200+200")
#
# label = Label(app, text="Please browse to the directory you wish to scan", height=0, width=100)
# b = Button(app, text="Quit", width=20, command=app.destroy)
# button1 = Button(app, text="About SPIES", width=20, command=clickAbout)
# label.pack()
# b.pack(side='bottom',padx=0,pady=0)
# button1.pack(side='bottom',padx=5,pady=5)
#
# app.mainloop()





#### AURRRRRR
# root = Tk()
#
# def move_window(event):
#     root.geometry('+{0}+{1}'.format(event.x_root, event.y_root))
#
# root.overrideredirect(True) # turns off title bar, geometry
# root.geometry('400x100+200+200') # set new geometry
#
# # make a frame for the title bar
# title_bar = Frame(root, bg='white', relief='raised', bd=2)
#
# # put a close button on the title bar
# close_button = Button(title_bar, text='X', command=root.destroy)
#
# # a canvas for the main area of the window
# window = Canvas(root, bg='black')
#
# # pack the widgets
# title_bar.pack(expand=1, fill=X)
# close_button.pack(side=RIGHT)
# window.pack(expand=1, fill=BOTH)
#
# # bind title bar motion to the move window function
# title_bar.bind('<B1-Motion>', move_window)
#
# root.mainloop()






# from tkinter import *
# from tkinter.filedialog import *
#
# root = Tk()
# root.wm_title("Pages to PDF")
# w = Label(root, text="Please choose a .pages file to convert.")
# y = askopenfilename(parent=root)
# y.pack()
# w.pack()
# root.mainloop()



import tkinter
import cv2
import PIL.Image, PIL.ImageTk
import time


class MyVideoCapture:
    def __init__(self, video_source=0):
        # Open the video source
        self.vid = cv2.VideoCapture(video_source)
        if not self.vid.isOpened():
            raise ValueError("Unable to open video source", video_source)

        # Get video source width and height
        self.width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)

    def get_frame(self):
        if self.vid.isOpened():
            ret, frame = self.vid.read()
            if ret:
                # Return a boolean success flag and the current frame converted to BGR
                return (ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            else:
                return (ret, None)
        else:
            return (ret, None)

    # Release the video source when the object is destroyed
    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()

class Appi:
    def __init__(self, window, window_title, video_source=0):
        self.window = window
        self.window.title(window_title)
        self.video_source = video_source

        # open video source (by default this will try to open the computer webcam)
        self.vid = MyVideoCapture(self.video_source)

        # Create a canvas that can fit the above video source size
        self.canvas = tkinter.Canvas(window, width = self.vid.width, height = self.vid.height)
        self.canvas.pack()

        # Button that lets the user take a snapshot
        self.btn_snapshot=tkinter.Button(window, text="Snapshot", width=50, command=self.snapshot)
        self.btn_snapshot.pack(anchor=tkinter.CENTER, expand=True)

        # After it is called once, the update method will be automatically called every delay milliseconds
        self.delay = 15
        self.update()

        self.window.mainloop()

    def snapshot(self):
        # Get a frame from the video source
        ret, frame = self.vid.get_frame()

        if ret:
            cv2.imwrite("frame-" + time.strftime("%d-%m-%Y-%H-%M-%S") + ".jpg", cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))

    def update(self):
        # Get a frame from the video source
        ret, frame = self.vid.get_frame()

        if ret:
            self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
            self.canvas.create_image(0, 0, image = self.photo, anchor = tkinter.NW)

        self.window.after(self.delay, self.update)




    # Create a window and pass it to the Application object
    Appi(tkinter.Tk(), "Tkinter and OpenCV")
