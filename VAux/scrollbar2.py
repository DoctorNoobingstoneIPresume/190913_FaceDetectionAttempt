from tkinter import *

class ScrolledCanvas(Frame):
    def __init__(self, master=None, nrElem=0):
        self.master = master

        canv = Canvas(master, bg="#111111", bd=0, highlightthickness=0, relief='ridge')
        canv.config(width=650, height=550)
        canv.config(scrollregion=(0,0,650, 1000))

        sbar = Scrollbar(master)
        sbar.config(command=canv.yview)
        canv.config(yscrollcommand=sbar.set)
        sbar.pack(side=RIGHT, fill=Y)
        canv.pack(side=LEFT, expand=YES, fill=BOTH)

        for i in range(10):
            canv.create_text(150, 50+(i*100), text='spam'+str(i), fill='beige')
        # canv.bind('<Double-1>', self.onDoubleClick)       # set event handler
        self.canvas = canv

    def onDoubleClick(self, event):
        print (event.x, event.y)
        print (self.canvas.canvasx(event.x), self.canvas.canvasy(event.y))


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



root = Tk()

frame=Frame(root,width=670,height=550)
frame.pack(expand=YES, fill=BOTH)

ScrolledCanvas(frame)



root.mainloop()
