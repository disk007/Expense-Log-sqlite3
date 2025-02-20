from tkinter import *
from tkinter import ttk
import csv

GUI=Tk()
GUI.title('โปรแกรมบันทึกค่าใช้จ่าย By Dis')
GUI.geometry('500x300+50+50')


#B1=Button(GUI,text='Hello')
#B1.pack(ipadx=20,ipady=20)

F1=Frame(GUI)
F1.place(x=100,y=50)

def Save(event=None):
     expense=v_expense.get()
     price=v_price.get()
     print('รายการ: {} ราคา: {}'.format(expense,price))
     v_expense.set('')
     v_price.set('')

     with open('savedata.csv','a',encoding='utf-8',newline='')as f:
          fw=csv.writer(f)
          data=[expense,price]
          fw.writerow(data)

     E1.focus()

GUI.bind('<Return>',Save)

FONT1=(None,20)

L=ttk.Label(F1,text='รายการค่าใช้จ่าย',font=FONT1)
L.pack()
v_expense=StringVar()
E1=ttk.Entry(F1,textvariable=v_expense,font=FONT1)
E1.pack()


L=ttk.Label(F1,text='ราคา (บาท)',font=FONT1)
L.pack()
v_price=StringVar()
E2=ttk.Entry(F1,textvariable=v_price,font=FONT1)
E2.pack()

B2=ttk.Button(F1,text='Save',command=Save)
B2.pack(ipadx=50)



GUI.mainloop()
