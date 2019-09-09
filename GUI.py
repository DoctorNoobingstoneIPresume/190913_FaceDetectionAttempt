
# #################################################################################################
# Andra Tomi 2019
# #################################################################################################

# import tkinter as tk
from tkinter import *
from tkinter.filedialog import *
from CStart import CStart

# ==============================================================================
#                               CLASE
# ==============================================================================
# ------------------------------------------------------------------------------
class HoverButton(Button):
# ------------------------------------------------------------------------------
    def __init__(self, master, **kw ):
        Button.__init__(self, master=master,**kw, fg="white", bg="#212121", activebackground="#212121", relief=FLAT)
        self.defaultForeground = self["foreground"]
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    def on_enter(self, e):
        self['foreground'] = self['activeforeground']

    def on_leave(self, e):
        self['foreground'] = self.defaultForeground

# ------------------------------------------------------------------------------
class HoverButtonBottom(Button):
# ------------------------------------------------------------------------------
    def __init__(self, master, **kw, ):
        Button.__init__(self, master=master,**kw, fg="white", bg="#4A4A4A", activebackground="#4A4A4A", relief=FLAT)
        self.defaultForeground = self["foreground"]
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    def on_enter(self, e):
        self['foreground'] = self['activeforeground']

    def on_leave(self, e):
        self['foreground'] = self.defaultForeground

# ------------------------------------------------------------------------------
class HoverButtonPopUp(Button):   #1A6E74   #205053
# ------------------------------------------------------------------------------
    def __init__(self, master, **kw, ):
        Button.__init__(self, master=master,**kw, fg="white", background="#9A9A9A", activebackground="#205053", relief=FLAT)
        self.defaultBackground = self["background"]
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    def on_enter(self, e):
        self['background'] = self['activebackground']

    def on_leave(self, e):
        self['background'] = self.defaultBackground

# ------------------------------------------------------------------------------
class DialogBox:
# ------------------------------------------------------------------------------
    def __init__(self, parent, textu):

        toplevel = self.top = Toplevel(parent)
        toplevel.geometry('300x100')
        # toplevel.configure(background='#94ACAE')
        toplevel.attributes('-alpha', 0.85)
        toplevel.grab_set()  # in mod normal tb sa revii...dar se distruge oricum cand dai x sau ok :D

        Label(toplevel, text=textu).pack(pady=30)
        center(toplevel)


# ------------------------------------------------------------------------------
class MyDialogInput:
# ------------------------------------------------------------------------------
    def __init__(self, parent):

        toplevel = self.top = Toplevel(parent)
        toplevel.geometry('270x100')
        # toplevel.configure(background='#94ACAE')
        toplevel.attributes('-alpha', 0.85)

        toplevel.grab_set()  # in mod normal tb sa revii...dar se distruge oricum cand dai x sau ok :D

        btn1 = HoverButtonPopUp(toplevel, text="Select file from disk", activeforeground='white')
        btn1.config(height="2", width="20", command=addPath)
        btn1.place(x=15, y=28, anchor="nw")

        btn2 = HoverButtonPopUp(toplevel, text="OK", activeforeground='white')
        btn2.config(height="2", width="10", command=self.ok)
        btn2.place(x=175, y=28, anchor="nw")

        self.path = ""

        center(toplevel)

    def ok(self):
        self.top.destroy()

        filepath = file_path.get()
        if varInput.get() == 1 and (filepath[-3:] == 'jpg' or filepath[-3:] == 'png'):
            selInput.set(1)
        elif varInput.get() == 2 and (filepath[-3:] == 'mp4' or filepath[-3:] == 'avi'):
            selInput.set(1)
        else:
            selInput.set(0)
            filepath=""
            DialogBox(root, "Wrong format inserted!")


# ==============================================================================
#                                   FUNCTII
# ==============================================================================
def center(win):
    """
    centers a tkinter window
    :param win: the root or Toplevel window to center
    """
    win.update_idletasks()
    width = win.winfo_width()
    frm_width = win.winfo_rootx() - win.winfo_x()
    win_width = width + 2 * frm_width
    height = win.winfo_height()
    titlebar_height = win.winfo_rooty() - win.winfo_y()
    win_height = height + titlebar_height + frm_width
    x = win.winfo_screenwidth() // 2 - win_width // 2
    y = win.winfo_screenheight() // 2 - win_height // 2
    win.geometry('{}x{}+{}+{}'.format(width, height, x, y))
    win.deiconify()


def trace_var(*args):
    if selMethod.get()==1 and selInput.get()==1:
        b6.configure(state=NORMAL)
    else:
        b6.configure(state=DISABLED)


def addPath():
    file = askopenfilename(initialdir = "/",title = "Select file",filetypes = (("jpeg files","*.jpg"),("mp4 files","*.mp4"),("avi files","*.avi"),("all files","*.*")))
    file_path.set(file)


def selMethod():
    selMethod.set(1)

def selInput():
    if varInput.get() == 1 or varInput.get() == 2:
        d = MyDialogInput(root)
        #root.wait_window(d.top)
    if varInput.get() == 3:
        selInput.set(1)

def start():
    if startFile.get() % 2 == 1:
        b6.config(image = buttonStop)
        output.selectMethod(varMethod.get(),varInput.get(),str(file_path.get()))
    else:
        b6.config(image = buttonStart)
        output.delete()
        # output.setStartImage('InterfataButoane/imaginePornire.jpg')
    startFile.set(startFile.get() + 1)

def cleanAll():
    varMethod.set(0)
    varInput.set(0)
    selMethod.set(0)
    selInput.set(0)
    output.delete()
    output.setStartImage('InterfataButoane/imaginePornire.jpg')


# ==============================================================================
#                            DE AICI INCEPE APLICATIA
# ==============================================================================
# -----------------------------------
# fereastra aplicatie
root = Tk()
root.geometry('900x590') #900x600
root.configure(background='#111111')
root.title("FC")

output = CStart(root)
output.setStartImage('InterfataButoane/imaginePornire1.jpg')

# -----------------------------------
# variabile folositoare
# buttonStart = PhotoImage(file = 'InterfataButoane/ButtonPlay5.png')
# small_start = buttonStart.subsample(13,13)
#
# buttonStop = PhotoImage(file = 'InterfataButoane/ButtonStop.png')
# small_stop = buttonStop.subsample(13,13)


buttonStart = PhotoImage(file = 'InterfataButoane/b3.png')

buttonStop = PhotoImage(file = 'InterfataButoane/bs3.png')


# -----------------------------------
frameLeft = Frame(root, height=600,width=230,bg="#212121").place(anchor="nw")
frameBottom= Frame(root, height=40, width=900,bg="#4A4A4A").place(y=550, anchor="nw")

# text pt butoanele de radio
label1 = Label(frameLeft, text="Select method", bg="#212121", activebackground="#212121",  fg="white", activeforeground='#5ED2E5', font=("arial",9,"bold")).place(x=30, y=40, anchor="nw")
label1 = Label(frameLeft, text="Select input", bg="#212121", activebackground="#212121",  fg="white", activeforeground='#5ED2E5', font=("arial",9,"bold")).place(x=30, y=190, anchor="nw")

# pt butonoanele radio
varMethod = IntVar()
R1 = Radiobutton(frameLeft, text="Basic Recognision", variable=varMethod, value=1, command=selMethod, bg="#212121", fg="white", activebackground="#212121", activeforeground="white", selectcolor="black")
R1.place(x=40, y=70, anchor="nw")
R2 = Radiobutton(frameLeft, text="Semi-profile Recognision", variable=varMethod, value=2, command=selMethod, bg="#212121", fg="white", activebackground="#212121", activeforeground="white", selectcolor="black")
R2.place(x=40, y=100, anchor="nw")
R3 = Radiobutton(frameLeft, text="Complex Recognition", variable=varMethod, value=3, command=selMethod, bg="#212121", fg="white", activebackground="#212121", activeforeground="white", selectcolor="black")
R3.place(x=40, y=130, anchor="nw")

varInput = IntVar()
R1 = Radiobutton(frameLeft, text="Image from path", variable=varInput, value=1, command=selInput, bg="#212121", fg="white", activebackground="#212121", activeforeground="white", selectcolor="black")
R1.place(x=40, y=220, anchor="nw")
R2 = Radiobutton(frameLeft, text="Video from path", variable=varInput, value=2, command=selInput, bg="#212121", fg="white", activebackground="#212121", activeforeground="white", selectcolor="black")
R2.place(x=40, y=250, anchor="nw")
R3 = Radiobutton(frameLeft, text="Live - Realtime", variable=varInput, value=3, command=selInput, bg="#212121", fg="white", activebackground="#212121", activeforeground="white", selectcolor="black")
R3.place(x=40, y=280, anchor="nw")



# buotanele de jos
b3 = HoverButton(frameLeft, text="Save data", activeforeground='#5ED2E5')
b3.place(x=30, y=470, anchor="nw")

b4 = HoverButton(frameLeft, text="Change face data", activeforeground='#5ED2E5')
b4.place(x=30, y=500, anchor="nw")

b5 = HoverButtonBottom(frameBottom, text="Start new session", activeforeground='#5ED2E5')
b5.config(command=cleanAll)
b5.place(x=30, y=558, anchor="nw")

startFile = IntVar()
startFile.set(1)
b6 = HoverButtonBottom(frameBottom, width=70, height=40, activeforeground='#5ED2E5', command=start)
b6.config(image = buttonStart , compound = LEFT )
b6.place(x=790, y=550, anchor="nw")



# -----------------------------------
# variabile pentru play -pause
selMethod = IntVar()
selMethod.trace('w', trace_var)
selMethod.set(0)

selInput = IntVar()
selInput.trace('w', trace_var)
selInput.set(0)

setPath = IntVar()
setPath.trace('w', trace_var)
setPath.set(0)

file_path = StringVar()


# frameRight = Frame(root, height=470, width=500, bg="yellow")
# frameRight.place(x=280,y=15, anchor="nw")



center(root)
# -----------------------------------
root.mainloop()
# -----------------------------------
