import tkinter
import tkMessageBox


top = tkinter.Tk()
def mousecontrol():
    tkMessageBox.showinfo("Sit back and relax... now mouse pointer can be controlled by moving head and click by blinking eyes.")


def readingmode():
    tkMessageBox.showinfo("Now open any document on pdf and read.. It will automatically browse according to face movements")

def image():
    tkMessageBox.showinfo("Scroll through images with nodding head left or right")

B = Tkinter.Button(top, text ="Mouse Control", command = mousecontrol)

B.pack()
B1 = Tkinter.Button(top, text ="Reading mode", command = readingmode)

B1.pack()
B2 = Tkinter.Button(top, text ="Image scroll", command = helloCallBack)

B2.pack()

top.mainloop()
