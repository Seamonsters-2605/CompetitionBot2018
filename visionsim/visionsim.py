import tkinter as tk
import seamonsters as sea
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
import socket

from networktables import NetworkTables

def show_values():
    print(w1.get(), w2.get())
    #Set NetWorkTable values
    vision.putNumber('tx', w1.get())
    vision.putNumber('ty', w2.get())

master = Tk()
var = IntVar()


NetworkTables.initialize(server=socket.gethostbyname(socket.gethostname()))
vision = NetworkTables.getTable('limelight')

#Window Size
master.geometry("200x200".format(
    master.winfo_screenwidth(), master.winfo_screenheight()))


#Sliders (w1 is for tx, w2 is for ty)
w1 = Scale(master,from_=0,to=42,orient=HORIZONTAL)
w1.grid(row=3, column=5)

w2 = Scale(master, from_=0, to=20,orient=HORIZONTAL)
w2.grid(row=4, column=5)


#Slider Labels
s1 = Label(master, text ='xOffset')
s1.grid(row=3, column=6)

s2 = Label(master, text='yOffset')
s2.grid(row=4, column=6)

#Set-Button that shows slider input
Button(master, text='Set', command=show_values,fg = 'black',bg = 'sea green').grid(row=8,column=4) #Show values button


#Label Limelight
label = Label(master, text='Limelight',fg = 'sea green', font=('Helvetica',20))
label.grid(row=1, column=5)

#Label Config
msg = Label(master, text='Configuration', fg = 'blue', font=('Verdana',10))
msg.grid(row=2,column=5)

mainloop()