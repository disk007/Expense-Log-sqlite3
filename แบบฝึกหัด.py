from tkinter import *
from tkinter import ttk,messagebox
import csv
from datetime import datetime

###########Sql##############
import sqlite3

conn=sqlite3.connect('expense.sqlite3')
c=conn.cursor()#สร้างตัวดำเนินการ (อยากได้อะไรใช้ตัวนี้)

c.execute("""CREATE TABLE IF NOT EXISTS expenselist (
                    ID INTEGER PRIMARY KEY AUTOINCREMENT,
                    transactionid TEXT,
                    datetime TEXT,
                    title TEXT,
                    expense INTEGER,
                    amount INTEGER,
                    total INTEGER

               )""")

def insert_expense(transactionid,datetime,title,expense,amount,total):
     ID=None
     with conn:
          c.execute("""INSERT INTO expenselist VALUES (?,?,?,?,?,?,?)""",
               (ID,transactionid,datetime,title,expense,amount,total))
     conn.commit()#บันทึกข้อมูลงในฐานข้อมูล
     #print("Inser Success")

def show_expense():
     with conn:
          c.execute("SELECT * FROM expenselist")
          expense=c.fetchall()#คำสั่งให้ดึงข้อมูลออกมา
          #print(expense)
     return expense

def update_expense(transactionid,title,expense,amount,total):
     with conn:
          c.execute("""UPDATE expenselist SET title=?,expense=?,amount=?,total=? WHERE transactionid=?""",
               ([title,expense,amount,total,transactionid]))
     conn.commit()
    # print("Data Update")

def delete_expense(transactionid):
     with conn:
          c.execute("DELETE FROM expenselist WHERE transactionid=?",([transactionid]))
     conn.commit()
     #print("Data Deleted")
######################################################


GUI=Tk()
GUI.title('โปรแกรมบันทึกค่าใช้จ่าย By Disk.')
#GUI.geometry('750x600+50+50')

w=720
h=600

ws=GUI.winfo_screenwidth()
hs=GUI.winfo_screenheight()

x=(ws/2)-(w/2)
y=(hs/2)-(h/2)-50

GUI.geometry(f'{w}x{h}+{x:.0f}+{y:.0f}')


############## Menu bar ###############
menubar = Menu(GUI)
GUI.config(menu=menubar)

# File menu
filemenu=Menu(menubar,tearoff=0)
menubar.add_cascade(label='File',menu=filemenu)
filemenu.add_command(label='Import CSV')
filemenu.add_command(label='Export to Googlesheet')

# Help
def About():
     messagebox.showinfo('About','สวัสดีครับ โปรแกรมนี้คือโปรแกรมบันทึกค่าใช้จ่าย')

helpmenu=Menu(menubar,tearoff=0)
menubar.add_cascade(label='Help',menu=helpmenu)
helpmenu.add_command(label='About',command=About)

# Donate
def Donate():
     messagebox.showinfo('Donate','โดเนทให้หน่อยนะครับ บัญชี XXXXXXXXXXXXXXXX')

donatemenu=Menu(menubar,tearoff=0)
menubar.add_cascade(label='Donate',menu=donatemenu)
donatemenu.add_command(label='About',command=Donate)

#######################################

my_notebook=ttk.Notebook(GUI)


bg3=PhotoImage(file="wallet.png")#.subsample(4)ย่อรูปภาพ
bg4=PhotoImage(file="List-icon.png")#.subsample(4)

T1=Frame(my_notebook)
T2=Frame(my_notebook)

my_notebook.pack(fill=BOTH,expand=1)

my_notebook.add(T1,text=f'{"Add Expense": ^{30}}',image=bg3,compound="top")
my_notebook.add(T2,text=f'{"Expense List": ^{30}}',image=bg4,compound="top")
#B1=Button(GUI,text='Hello')
#B1.pack(ipadx=20,ipady=20)

F1=Frame(T1)
F1.pack()

#F2=Frame(T2)
#F2.pack()

day={'Mon':'จันทร์',
     'Tue':'อังคาร',
     'Wed':'พุธ',
     'Thu':'พฤหัสบดี',
     'Fri':'ศุกร์',
     'Sat':'เสาร์',
     'Sun':'อาทิตย์'}

def Save(event=None):
     expense=v_expense.get()
     price=v_price.get()
     amount=v_amount.get()

     if expense == '':
          messagebox.showwarning('Error','กรุณากรอกข้อมูลค่าใช้จ่าย')
          return 
     elif price == '':
          messagebox.showwarning('Error','กรุณากรอกราคา')
          return
     elif amount == '':
          amount=1

     try:
          total=(int(price)*int(amount))
          #print('รายการ: {} ราคา: {}'.format(expense,price))
          #print('จำนวน(สินค้า):{} ราคารวมทั้งหมด: {}'.format(amount,total))

          text1='รายการ: {} ราคา: {}\n'.format(expense,price)
          text1=text1+'จำนวน(สินค้า):{} ราคารวมทั้งหมด: {}'.format(amount,total)
          v_result1.set(text1)

          v_expense.set('')
          v_price.set('')
          v_amount.set('')

          today=datetime.now().strftime('%a')
          #print(today)
          stamp=datetime.now()
          dt = stamp.strftime('%Y-%m-%d %H:%M:%S')
          transactionid=stamp.strftime('%Y%m%d%H%M%f')
          dt=day[today]+'-'+dt

          insert_expense(transactionid,dt,expense,int(price),int(amount),total)

          with open('savedata.csv','a',encoding='utf-8',newline='')as f:
               fw=csv.writer(f)
               data=[transactionid,dt,expense,price,amount,total]
               fw.writerow(data)

          E1.focus()
          update_table()
     except Exception as e:
          print("ERROR",e)    
          messagebox.showwarning('Error','กรุณากรอกข้อมูลใหม่ คุณกรอกข้อมูลผิด')
          #messagebox.showinfo('Error','กรุณากรอกข้อมูลใหม่ คุณกรอกข้อมูลผิด')
          v_expense.set('')
          v_price.set('')
          v_amount.set('')

GUI.bind('<Return>',Save)



FONT1=(None,20)
FONT2=(None,30)

main_icon=PhotoImage(file="dollar-icon.png")
Mainicon=ttk.Label(F1,image=main_icon)
Mainicon.pack()

L=ttk.Label(F1,text='รายการค่าใช้จ่าย',font=FONT1)
L.pack(pady=20)
v_expense=StringVar()
E1=ttk.Entry(F1,textvariable=v_expense,font=FONT1)
E1.pack()


L=ttk.Label(F1,text='ราคา (บาท)',font=FONT1)
L.pack()
v_price=StringVar()
E2=ttk.Entry(F1,textvariable=v_price,font=FONT1)
E2.pack()

L=ttk.Label(F1,text='จำนวน (สินค้า)',font=FONT1)
L.pack()
v_amount=StringVar()
E2=ttk.Entry(F1,textvariable=v_amount,font=FONT1)
E2.pack()

icon_b1=PhotoImage(file="save_icon.png")
B2=ttk.Button(F1,text=f'{"Save":^{10}}',image=icon_b1,command=Save,compound="top")
B2.pack(pady=20,ipadx=20)

v_result1=StringVar()
v_result1.set("----------ผลลัพธ์----------")
result1=ttk.Label(F1,textvariable=v_result1,font=FONT1,foreground="green")
result1.pack(pady=20)


def read_csv():
     with open ('savedata.csv',encoding='utf-8',newline='') as f:
          fr=csv.reader(f)
          data=list(fr)
          return data
          #for i in data:
           #    print(i)
          #return i

########### All Record #################

'''def update_record():
     getdata=read_csv()
     v_allrecord.set('')
     text=''
     for d in getdata:
          txt="{}---{}---{}---{}---{}\n".format(d[0],d[1],d[2],d[3],d[4])
          text=text+txt

          v_allrecord.set(text)

v_allrecord=StringVar()
v_allrecord.set("--------All Record--------")
update_record()
Allrecord=ttk.Label(T2,textvariable=v_allrecord,font=(None,15),foreground='green')
Allrecord.pack()'''
###################################################

############## TreeView ##################

L=ttk.Label(T2,text="ตารางแสดงผลลัพธ์ทั้งหมด",font=FONT1,foreground="black").pack(pady=20)

header=['รหัสรายการ','วัน-เวลา','รายการ','ค่าใช้จ่าย','จำนวน','รวม']
resulttable = ttk.Treeview(T2,columns=header,show='headings',height=20)
resulttable.pack()

###ใส่หัวข้อแบบที่ 1###
#resulttable.heading(header[0],text=header[0])
#resulttable.heading(header[1],text=header[1])
#resulttable.heading(header[2],text=header[2])
#resulttable.heading(header[3],text=header[3])
#resulttable.heading(header[4],text=header[4])


###### ใส่หัวข้อแบบที่ 2###
#for i in range(len(header)):
 #    resulttable.heading(header[i],text=header[i])

for h in header:
     resulttable.heading(h,text=h)

headerwidth=[120,160,170,80,80,80]

for h,w in zip(header,headerwidth):
     resulttable.column(h,width=w)

#resulttable.insert('','end',value=['จันทร์','น้ำดื่ม',30,5,150]) เพิ่มข้อมูล

alltransactionid={}

def Update_CSV():
     with open('savedata.csv','w',encoding='utf-8',newline='')as f:
          fw=csv.writer(f)
          data=list(alltransactionid.values())
          fw.writerows(data) #multiple line from nested list [[],[],[]]
          print("Table was update")

def UpdateSQL():
     data=list(alltransactionid.values())
     for d in data:
          update_expense(d[0],d[2],d[3],d[4],d[5])

def DeleteRecord(event=None):
     check=messagebox.askyesno('confirm?','คุณต้องการลบข้อมูลหรือไม่')
     #print('YES/NO:',check)
     if check==True:
          #print('Delete')
          select=resulttable.selection()
          #print(select)
          data=resulttable.item(select)
          data=data['values']
          transactionid=data[0] # transactionid คนละตัวแปรที่อยู่ในฟังก์ชัน Save
          #print(transactionid)
          del alltransactionid[str(transactionid)]
          #print(alltransactionid)
          #Update_CSV()
          delete_expense(str(transactionid))
          update_table()
     else:
          pass
          #print('cancel')

BDelete=ttk.Button(T2,text='Delete',command=DeleteRecord)
BDelete.place(x=50,y=520)

resulttable.bind('<Delete>',DeleteRecord)


def update_table():
     resulttable.delete(*resulttable.get_children())
     #for c in resulttable.get_children():
          #resulttable.delete(c)
     try:
          data= show_expense()#read_csv()
          #print('Data ',data)
          for d in data:
               alltransactionid[d[1]]=d[1:] # d[0]=transactionid
               resulttable.insert('','0',value=d[1:])
          #print('Ts',alltransactionid)
     except Exception as e:
          print("No File")
          print("ERROR: ",e)



################Right Click Menu################

leftclick=False

def leftclick(event):
     #print(event.x_root,event.y_root)
     global leftclick
     leftclick=True
     resulttable.bind('<Button-3>',menupopup)
     


def EditRecord():
     POPUP=Toplevel()
     #POPUP.geometry('500x400')

     w=500
     h=400

     ws=GUI.winfo_screenwidth()
     hs=GUI.winfo_screenheight()

     x=(ws/2)-(w/2)
     y=(hs/2)-(h/2)-50

     POPUP.geometry(f'{w}x{h}+{x:.0f}+{y:.0f}')

     POPUP.title('EditRecord')

     L=ttk.Label(POPUP,text='รายการค่าใช้จ่าย',font=FONT1)
     L.pack(pady=20)
     v_expense=StringVar()
     E1=ttk.Entry(POPUP,textvariable=v_expense,font=FONT1)
     E1.pack()


     L=ttk.Label(POPUP,text='ราคา (บาท)',font=FONT1)
     L.pack()
     v_price=StringVar()
     E2=ttk.Entry(POPUP,textvariable=v_price,font=FONT1)
     E2.pack()

     L=ttk.Label(POPUP,text='จำนวน (สินค้า)',font=FONT1)
     L.pack()
     v_amount=StringVar()
     E3=ttk.Entry(POPUP,textvariable=v_amount,font=FONT1)
     E3.pack()

     def Edit():
          #print(transactionid)
          #print(alltransactionid)
          olddata=alltransactionid[str(transactionid)]
          #print("OLD ",olddata)
          v1=v_expense.get()
          v2=int(v_price.get())
          v3=int(v_amount.get())
          total=v2*v3
          newdata=[olddata[0],olddata[1],v1,v2,v3,total]
          alltransactionid[str(transactionid)]=newdata
          #Update_CSV()
          UpdateSQL()
          update_table()
          POPUP.destroy()#สั่งปิด Popup


     icon_b1=PhotoImage(file="save_icon.png")
     B2=ttk.Button(POPUP,text=f'{"Save":^{10}}',image=icon_b1,command=Edit,compound="top")
     B2.pack(pady=20,ipadx=20)

     select=resulttable.selection()
     #print(select)
     data=resulttable.item(select)
     data=data['values']
     #print(data)
     transactionid=data[0]

     v_expense.set(data[2])
     v_price.set(data[3])
     v_amount.set(data[4])

     POPUP.mainloop()

rightclick=Menu(GUI,tearoff=0)
rightclick.add_command(label='Edit',command=EditRecord)
rightclick.add_command(label='Delete',command=DeleteRecord)

def menupopup(event):
     #print(event.x_root,event.y_root)
     if leftclick==True:
          rightclick.post(event.x_root,event.y_root)


resulttable.bind('<Button-1>',leftclick)


update_table()
#print('GET CHILD:',resulttable.get_children())

GUI.mainloop()
