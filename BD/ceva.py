from tkinter import *
import math
import sqlite3
import cv2 as cv
import PIL.Image, PIL.ImageTk


class ShowPeople:
    def __init__(self, master):
        self.master = master

    def addPerson (self, x, y, w, h, tn, ti, isIdent, td):
        textNume = StringVar()
        textNume.set(tn)
        textPath = ti
        textData = StringVar()
        textData.set(td)

        personInfo = Frame(self.master, height=h, width=w, bg="blue", bd=2)
        personInfo.pack_propagate(0) # don't shrink
        personInfo.place(x=x, y=y, anchor="nw")

        canvas =  Canvas(personInfo, height=130, width=130) # width = self.input.width, height = self.input.height
        image = cv.imread(textPath)
        if isIdent == 0:
            img = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
        else:
            img = cv.cvtColor(image, cv.COLOR_BGR2RGB)

        resized = cv.resize(img, (130,130))

        self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(resized))
        canvas.create_image(0,0, anchor=NW, image = self.photo)
        canvas.pack()


        name = Label(personInfo, text=textNume.get(), bg="#E6E6E6", bd=2)
        name.pack(fill=X)

        dateIdent = Label(personInfo, text=textData.get(), bg="#BDBDBD",bd=2)
        dateIdent.pack(fill=X)



class dbOp:
    def __init__(self, database='../BD/database.db'):
        self.conn = sqlite3.connect(database)
        self.c = self.conn.cursor()

    def __delete__(self):
        self.conn.commit()
        self.conn.close()

    def getData (self, uid):
        c = self.c
        c.execute("SELECT name FROM usersTest WHERE id = {id}".format(id=uid))
        nume = str(c.fetchall())[3:-4]
        c.execute("SELECT image FROM usersTest WHERE id = {id}".format(id=uid))
        image = str(c.fetchall())[3:-4]
        c.execute("SELECT ident FROM usersTest WHERE id = {id}".format(id=uid))
        found = str(c.fetchall())[2:-3]
        c.execute("SELECT date FROM usersTest WHERE id = {id}".format(id=uid))
        date = str(c.fetchall())[3:-4]
        return (nume, image, found, date)

    def getAllDbEntries(self):
        c = self.c
        c.execute("SELECT COUNT(*) FROM usersTest")
        nr = str(c.fetchall())[2:-3]
        return nr


def display_people_in_DB(master, w=134, h=183, W=670, H=550):

    db = dbOp()
    nr = int(db.getAllDbEntries()) + 1

    x = 0
    y = 0
    i = 1

    while i < nr:
        canvas = ShowPeople(master)
        if x == W:
            x = 0
            y = y + h
        (nume, image, found, date) = db.getData(i)
        canvas.addPerson(x, y, w, h, nume, image, found, date)
        x += w
        i += 1


root = Tk()
frame=Canvas(root,width=670,height=550)
frame.pack(expand=YES, fill=BOTH)
display_people_in_DB(frame)
root.mainloop()
