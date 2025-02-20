from tkinter import *
from tkinter import ttk

GUI=Tk()
GUI.geometry('500x300+50+50')


B1=Button(GUI,text='Hello')
B1.pack(ipadx=20,ipady=20)

F1=Frame(GUI)
F1.place(x=200,y=50)

def Hello():
     print('สวัสดี')

B2=ttk.Button(F1,text='Hello',command=Hello)
B2.pack(ipadx=50)



GUI.mainloop()
