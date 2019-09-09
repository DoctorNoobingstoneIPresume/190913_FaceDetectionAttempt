from tkinter import *
import math


class ScrolledCanvas(Frame):
    def __init__(self, master=None, nrElem=0):

        self.master = master

        w = 650
        h = 550

        canv = Canvas(master, bg="#111111", bd=0, highlightthickness=0, relief='ridge')
        canv.config(width=w, height=h)
        self.canv = canv

        newHeight = math.ceil((nrElem/5)*h)

        if newHeight > h:
            self.scrollbar(newHeight)
        else:
            self.canv.pack(side=LEFT, expand=YES, fill=BOTH)


    def scrollbar(self, height):
        # scrollbar
        self.canv.config(scrollregion=(0,0,650, height))
        sbar = Scrollbar(self.master)
        sbar.config(command=self.canv.yview)
        self.canv.config(yscrollcommand=sbar.set)
        sbar.pack(side=RIGHT, fill=Y)
        self.canv.pack(side=LEFT, expand=YES, fill=BOTH)

        self.sbar = sbar

    def addPerson (self, x, y, w, h, tn, td):
        textNume = StringVar()
        textNume.set(tn)
        textData = StringVar()
        textData.set(td)

        personInfo = Frame(self.canv, height=h, width=w, bg="blue", bd=2)
        personInfo.pack_propagate(0) # don't shrink
        personInfo.place(x=x, y=y, anchor="nw")

        image =  Canvas(personInfo, height=130, width=123, bg="yellow", bd=2) # width = self.input.width, height = self.input.height)
        image.pack()

        name = Label(personInfo, text=textNume.get(), bg="#E6E6E6", bd=2)
        name.pack(fill=X)

        dateIdent = Label(personInfo, text=textData.get(), bg="#BDBDBD",bd=2)
        dateIdent.pack(fill=X)



root = Tk()

frame=Frame(root,width=670,height=550)
frame.pack(expand=YES, fill=BOTH)

## var
x = 0
y = 0
w = 130
h = 183
name = "name"
date = "date"
elementsNo = 2

canvas = ScrolledCanvas(frame, 20)

# step = 1
# while elementsNo:
#     if step == 6:
#         x = 0
#         y += h
#         step = 1

nume = "nume" + str(elementsNo)
canvas.addPerson(x, y, w, h, "Andreea C", "2019-09-08 20:12:32")
x += w
canvas.addPerson(x, y, w, h, "Cosmin C", "2019-09-08 20:12:34")
    # elementsNo -= 1
    # step += 1



root.mainloop()
