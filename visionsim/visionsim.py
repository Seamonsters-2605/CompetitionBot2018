import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox

from networktables import NetworkTables

def show_values():
    print(w1.get(), w2.get())

master = Tk()
var = IntVar()
pad = 1
padplus = pad-20

#Sliders
w1 = Scale(master,from_=0,to=42,orient=HORIZONTAL)
#w1.pack(side=LEFT)
w1.grid(row=4, column=9)
w2 = Scale(master, from_=0, to=20,orient=HORIZONTAL)
w2.grid(row=5, column=9)
#w2.pack(side=LEFT)


#Message
msg = Message(master, text='Configuration', width=100)
msg.grid(row=1,column=5)

master.geometry("{1}x{1}+0+0".format(
    master.winfo_screenwidth()-padplus, master.winfo_screenheight()-padplus))
c = Checkbutton(master, text="Stuff", variable=var)  #Make Checkbutton
#c.pack(side=RIGHT)
c.grid(row=20, column=20)


Button(master, text='Show', command=show_values).grid(row=11,column=) #Show values button
mainloop()