from PIL import Image, ImageTk
from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import font as tkFont
import mysql.connector
from mysql.connector import Error
import time 
import threading
import pyttsx3



root=Tk()
root.geometry('2000x700')


    
def DestroyPage(*x):
    for n in x:
        n.place_forget()

    
def Save_msg():
    messagebox.showinfo("Successful","Your event has been successfully saved!!")
    entry1.delete(0, 'end')
    entry2.delete(0, 'end')
    entry3.delete(0, 'end')
    entry4.delete(0, 'end')
    DestroyPage(label4,SaveButton,entry1,entry2,entry3,entry4)
    OpenHomePage()

monthvar = tk.StringVar(root)
checkboxStateList = []
buttonsList=[]


def DeleteEventsProceed():
    global buttonsList
    global checkboxStateList
    

    for i in buttonsList:
        if i.instate(['selected'])==True:
            checkboxStateList.append(1)
        else:
            checkboxStateList.append(0)
   

    for j in range(0,len(checkboxStateList)):
        if checkboxStateList[j] == 1:
            eventDetails.pop(j)

    
    
    con = mysql.connector.connect(host='localhost',
                                       database='sys',
                                       user='root',
                                       password='')                                   
    cur=con.cursor()
    cur.execute("DELETE FROM Event")

    for k in eventDetails:
        firstvalue = str(k[0])
        secondvalue = str(k[1])
        thirdvalue = str(k[2])
        fourthvalue = str(k[3])
        fifthvalue = str(k[4])
        cur.execute("INSERT INTO Event(Event_name,Date_of_event,Start_Time_of_event,End_Time_of_event,Description)VALUES(%s,%s,%s,%s,%s)",
                    (firstvalue,secondvalue,thirdvalue,fourthvalue,fifthvalue))
                        
    con.commit()
    tk.messagebox.showinfo("Deleted","The selected event(s) has been successfully deleted",icon='info')
    DestroyPage(NextButton, label5)

    for i in range(0,len(buttonsList)):
        buttonsList[i].pack_forget()
    buttonsList.clear()
    checkboxStateList.clear()
    OpenHomePage()
    

    
    

bgimage4= PhotoImage(file ="image_files/event.png")
label5 = Label(root, image=bgimage4)
Next= PhotoImage(file="image_files/Next.png")
NextButton = Button(root,image = Next,height="39",width = "99",command= DeleteEventsProceed)
eventDetails = []

def Delete_Events():
    DestroyPage(label1,buttonx,buttony,buttonz,buttonw,buttonv)
    label5.place(relwidth=1,relheight=1)
    
    con = mysql.connector.connect(host='localhost',
                                   database='sys',
                                   user='root',
                                   password='')
     
    cur=con.cursor()

    cur.execute("SELECT*FROM Event")
    global eventDetails
    eventDetails = cur.fetchall()
    
    con.close()

    NextButton.place(x=647,y=580)
    
    global buttonsList   
    for i in eventDetails:
        globals()["var{}".format(eventDetails.index(i))] = tk.IntVar()
        globals()["C{}".format(eventDetails.index(i))]=ttk.Checkbutton(root,text=i)
        globals()["C{}".format(eventDetails.index(i))].pack()
        buttonsList.append(globals()["C{}".format(eventDetails.index(i))])
            
            
ViewEventsImg= PhotoImage(file = "image_files/Event.png")
ViewEventsbg = Label(root, image=ViewEventsImg)
listbox = Listbox(root, height = 18,  
                  width = 50,  
                  bg = "deep sky blue", 
                  activestyle = 'none',  
                  font = "Helvetica", 
                  fg = "mint cream")
GoBack= PhotoImage(file='image_files/Go back.png')
BackButton = Button(root,image = GoBack,command= lambda:[DestroyPage(ViewEventsbg,listbox,BackButton),listbox.delete(0, tk.END),OpenHomePage()])

def View_events():
    DestroyPage(label1,buttonx,buttony,buttonz,buttonw,buttonv)
    ViewEventsbg.place(relwidth=1,relheight=1)
    BackButton.place(x=647,y=580)
    
    con = mysql.connector.connect(host='localhost',
                                       database='sys',
                                       user='root',
                                       password='')
     
    cur=con.cursor()
    cur.execute("SELECT*FROM Event")
    
    event_details = cur.fetchall()
    for i in range(0,len(event_details)):
        listbox.insert(i+1,event_details[i])
    listbox.place(x=500,y=100)
              
            
              
 
    
        
def Clear_History():
    con = mysql.connector.connect(host='localhost',
                                       database='sys',
                                       user='root',
                                       password='')                                   
    cur=con.cursor()
    cur.execute("DELETE FROM Event")
    con.commit()

def Delete_record():
    MsgBox=tk.messagebox.askquestion("Clear History","Are u sure u want to clear the events stored completely?",icon="question")
    if MsgBox == 'yes':
        Clear_History()
        tk.messagebox.showinfo("Deleted","Your data has been successfully deleted",icon='info')
    else:
        tk.messagebox.showinfo("Return","You will return to the homepage",icon='info')




month = ""
day=""
FinalDate=""

value_one=""
value_two=""
value_three=""
value_four=""

def Save_Event():

    global FinalDate
    global value_one
    global value_two
    global value_three
    global value_four

    FinalDate = str(year) + "\\" + month + "\\" + day
    value_one=entry1.get()
    value_two=entry2.get()
    value_three=entry3.get()
    value_four=entry4.get()


    
    conn = None
    try:
        conn = mysql.connector.connect(host='localhost',
                                       database='sys',
                                       user='root',
                                       password='')
        if conn.is_connected():
            db_cursor=conn.cursor()
            db_cursor.execute("INSERT INTO Event(Event_name,Date_of_event,Start_Time_of_event,End_Time_of_event,Description)VALUES(%s,%s,%s,%s,%s)",
                              (value_one,FinalDate,value_two,value_three,value_four))
            conn.commit()
            Save_msg()
            
    except Error as e:
        tk.messagebox.showinfo("Error",e,icon='error')



bgimage= ImageTk.PhotoImage(file = "image_files/Super.jpg")
label4 = Label(root, image=bgimage)
Save= PhotoImage(file="image_files/Save.png")
SaveButton=Button(root,image = Save,command= Save_Event)


entry1 = Entry (root,font = ("Century Gothic", 32))
entry2 = Entry (root,font = ("Century Gothic", 32))
entry3 = Entry (root,font = ("Century Gothic", 32))
entry4 = Entry (root,font = ("Century Gothic", 32))


def OpenNewWindow():
    DestroyPage(B1,B2,B3,B4,B5,
                B6,B7,B8,B9,B10,
                B11,B12,B13,B14,B15,
                B16,B17,B18,B19,B20,
                B21,B22,B23,B24,B25,
                B26,B27,B28,B29,B30,B31,
                label3)
    
    label4.place(relwidth=1,relheight=1)
    SaveButton.place(x=730,y=700)
    entry1.place(x=570,y=120)
    entry2.place(x=570,y=280)
    entry3.place(x=570,y=400)
    entry4.place(x=570,y=600)
    

#functions for changing day on clicking day buttons

def d1():
    global day
    day = "1"

def d2():
    global day
    day = "2"

def d3():
    global day
    day = "3"
    
def d4():
    global day
    day = "4"
    
def d5():
    global day
    day = "5"

def d6():
    global day
    day = "6"

def d7():
    global day
    day = "7"

def d8():
    global day
    day = "8"
    
def d9():
    global day
    day = "9"
    
def d10():
    global day
    day = "10"

def d11():
    global day
    day = "11"

def d12():
    global day
    day = "12"

def d13():
    global day
    day = "13"
    
def d14():
    global day
    day = "14"
    
def d15():
    global day
    day = "15"

def d16():
    global day
    day = "16"

def d17():
    global day
    day = "17"

def d18():
    global day
    day = "18"
    
def d19():
    global day
    day = "19"
    
def d20():
    global day
    day = "20"

def d21():
    global day
    day = "21"

def d22():
    global day
    day = "22"

def d23():
    global day
    day = "23"
    
def d24():
    global day
    day = "24"
    
def d25():
    global day
    day = "25"

def d26():
    global day
    day = "26"

def d27():
    global day
    day = "27"

def d28():
    global day
    day = "28"
    
def d29():
    global day
    day = "29"
    
def d30():
    global day
    day = "30"

def d31():
    global day
    day = "31"    



bgimage3= ImageTk.PhotoImage(file = 'image_files/Yellow.png')
label3 = Label(root, image=bgimage3)
B1=Button(root,text="1",font = ("Century Gothic", 20, 'bold'),height=2,width=8,bg="black",fg="firebrick3",command=lambda:[OpenNewWindow(),d1()])
B2=Button(root,text="2",font = ("Century Gothic", 20, 'bold'),height=2,width=8,bg="black",fg="firebrick3",command=lambda:[OpenNewWindow(),d2()])
B3=Button(root,text="3",font = ("Century Gothic", 20, 'bold'),height=2,width=8,bg="black",fg="firebrick3",command=lambda:[OpenNewWindow(),d3()])
B4=Button(root,text="4",font = ("Century Gothic", 20, 'bold'),height=2,width=8,bg="black",fg="firebrick3",command=lambda:[OpenNewWindow(),d4()])
B5=Button(root,text="5",font = ("Century Gothic", 20, 'bold'),height=2,width=8,bg="black",fg="firebrick3",command=lambda:[OpenNewWindow(),d5()])
B6=Button(root,text="6",font = ("Century Gothic", 20, 'bold'),height=2,width=8,bg="black",fg="firebrick3",command=lambda:[OpenNewWindow(),d6()])
B7=Button(root,text="7",font = ("Century Gothic", 20, 'bold'),height=2,width=8,bg="black",fg="firebrick3",command=lambda:[OpenNewWindow(),d7()])

B8=Button(root,text="8",font = ("Century Gothic", 20, 'bold'),height=2,width=8,bg="black",fg="firebrick3",command=lambda:[OpenNewWindow(),d8()])
B9=Button(root,text="9",font = ("Century Gothic", 20, 'bold'),height=2,width=8,bg="black",fg="firebrick3",command=lambda:[OpenNewWindow(),d9()])
B10=Button(root,text="10",font = ("Century Gothic", 20, 'bold'),height=2,width=8,bg="black",fg="firebrick3",command=lambda:[OpenNewWindow(),d10()])
B11=Button(root,text="11",font = ("Century Gothic", 20, 'bold'),height=2,width=8,bg="black",fg="firebrick3",command=lambda:[OpenNewWindow(),d11()])
B12=Button(root,text="12",font = ("Century Gothic", 20, 'bold'),height=2,width=8,bg="black",fg="firebrick3",command=lambda:[OpenNewWindow(),d12()])
B13=Button(root,text="13",font = ("Century Gothic", 20, 'bold'),height=2,width=8,bg="black",fg="firebrick3",command=lambda:[OpenNewWindow(),d13()])
B14=Button(root,text="14",font = ("Century Gothic", 20, 'bold'),height=2,width=8,bg="black",fg="firebrick3",command=lambda:[OpenNewWindow(),d14()])

B15=Button(root,text="15",font = ("Century Gothic", 20, 'bold'),height=2,width=8,bg="black",fg="firebrick3",command=lambda:[OpenNewWindow(),d15()])
B16=Button(root,text="16",font = ("Century Gothic", 20, 'bold'),height=2,width=8,bg="black",fg="firebrick3",command=lambda:[OpenNewWindow(),d16()])
B17=Button(root,text="17",font = ("Century Gothic", 20, 'bold'),height=2,width=8,bg="black",fg="firebrick3",command=lambda:[OpenNewWindow(),d17()])
B18=Button(root,text="18",font = ("Century Gothic", 20, 'bold'),height=2,width=8,bg="black",fg="firebrick3",command=lambda:[OpenNewWindow(),d18()])
B19=Button(root,text="19",font = ("Century Gothic", 20, 'bold'),height=2,width=8,bg="black",fg="firebrick3",command=lambda:[OpenNewWindow(),d19()])
B20=Button(root,text="20",font = ("Century Gothic", 20, 'bold'),height=2,width=8,bg="black",fg="firebrick3",command=lambda:[OpenNewWindow(),d20()])
B21=Button(root,text="21",font = ("Century Gothic", 20, 'bold'),height=2,width=8,bg="black",fg="firebrick3",command=lambda:[OpenNewWindow(),d21()])

B22=Button(root,text="22",font = ("Century Gothic", 20, 'bold'),height=2,width=8,bg="black",fg="firebrick3",command=lambda:[OpenNewWindow(),d22()])
B23=Button(root,text="23",font = ("Century Gothic", 20, 'bold'),height=2,width=8,bg="black",fg="firebrick3",command=lambda:[OpenNewWindow(),d23()])
B24=Button(root,text="24",font = ("Century Gothic", 20, 'bold'),height=2,width=8,bg="black",fg="firebrick3",command=lambda:[OpenNewWindow(),d24()])
B25=Button(root,text="25",font = ("Century Gothic", 20, 'bold'),height=2,width=8,bg="black",fg="firebrick3",command=lambda:[OpenNewWindow(),d25()])
B26=Button(root,text="26",font = ("Century Gothic", 20, 'bold'),height=2,width=8,bg="black",fg="firebrick3",command=lambda:[OpenNewWindow(),d26()])
B27=Button(root,text="27",font = ("Century Gothic", 20, 'bold'),height=2,width=8,bg="black",fg="firebrick3",command=lambda:[OpenNewWindow(),d27()])
B28=Button(root,text="28",font = ("Century Gothic", 20, 'bold'),height=2,width=8,bg="black",fg="firebrick3",command=lambda:[OpenNewWindow(),d28()])

B29=Button(root,text="29",font = ("Century Gothic", 20, 'bold'),height=2,width=8,bg="black",fg="firebrick3",command=lambda:[OpenNewWindow(),d29()])
B30=Button(root,text="30",font = ("Century Gothic", 20, 'bold'),height=2,width=8,bg="black",fg="firebrick3",command=lambda:[OpenNewWindow(),d30()])
B31=Button(root,text="31",font = ("Century Gothic", 20, 'bold'),height=2,width=8,bg="black",fg="firebrick3",command=lambda:[OpenNewWindow(),d31()])
    
def SelectDate28():
    DestroyPage(LabelYear,ButtonBack,ButtonForw,labelm,jan,feb,march,april,may,june,july,august,september,october,nov,dec)
    label3.place(relheight=1,relwidth=1)
    B1.place(x=50,y=70)
    B2.place(x=220,y=70)
    B3.place(x=390,y=70)
    B4.place(x=560,y=70)
    B5.place(x=730,y=70)
    B6.place(x=900,y=70)
    B7.place(x=1070,y=70)

    B8.place(x=50,y=170)
    B9.place(x=220,y=170)
    B10.place(x=390,y=170)
    B11.place(x=560,y=170)
    B12.place(x=730,y=170)
    B13.place(x=900,y=170)
    B14.place(x=1070,y=170)

    B15.place(x=50,y=270)
    B16.place(x=220,y=270)
    B17.place(x=390,y=270)
    B18.place(x=560,y=270)
    B19.place(x=730,y=270)
    B20.place(x=900,y=270)
    B21.place(x=1070,y=270)

    B22.place(x=50,y=370)
    B23.place(x=220,y=370)
    B24.place(x=390,y=370)
    B25.place(x=560,y=370)
    B26.place(x=730,y=370)
    B27.place(x=900,y=370)
    B28.place(x=1070,y=370)

def SelectDate29():
    DestroyPage(LabelYear,ButtonBack,ButtonForw,labelm,jan,feb,march,april,may,june,july,august,september,october,nov,dec)
    label3.place(relheight=1,relwidth=1)
    B1.place(x=50,y=70)
    B2.place(x=220,y=70)
    B3.place(x=390,y=70)
    B4.place(x=560,y=70)
    B5.place(x=730,y=70)
    B6.place(x=900,y=70)
    B7.place(x=1070,y=70)

    B8.place(x=50,y=170)
    B9.place(x=220,y=170)
    B10.place(x=390,y=170)
    B11.place(x=560,y=170)
    B12.place(x=730,y=170)
    B13.place(x=900,y=170)
    B14.place(x=1070,y=170)

    B15.place(x=50,y=270)
    B16.place(x=220,y=270)
    B17.place(x=390,y=270)
    B18.place(x=560,y=270)
    B19.place(x=730,y=270)
    B20.place(x=900,y=270)
    B21.place(x=1070,y=270)

    B22.place(x=50,y=370)
    B23.place(x=220,y=370)
    B24.place(x=390,y=370)
    B25.place(x=560,y=370)
    B26.place(x=730,y=370)
    B27.place(x=900,y=370)
    B28.place(x=1070,y=370)
    B29.place(x=50,y=470)
    
def SelectDate30():
    DestroyPage(LabelYear,ButtonBack,ButtonForw,labelm,jan,feb,march,april,may,june,july,august,september,october,nov,dec)
    label3.place(relheight=1,relwidth=1)
    B1.place(x=50,y=70)
    B2.place(x=220,y=70)
    B3.place(x=390,y=70)
    B4.place(x=560,y=70)
    B5.place(x=730,y=70)
    B6.place(x=900,y=70)
    B7.place(x=1070,y=70)

    B8.place(x=50,y=170)
    B9.place(x=220,y=170)
    B10.place(x=390,y=170)
    B11.place(x=560,y=170)
    B12.place(x=730,y=170)
    B13.place(x=900,y=170)
    B14.place(x=1070,y=170)

    B15.place(x=50,y=270)
    B16.place(x=220,y=270)
    B17.place(x=390,y=270)
    B18.place(x=560,y=270)
    B19.place(x=730,y=270)
    B20.place(x=900,y=270)
    B21.place(x=1070,y=270)

    B22.place(x=50,y=370)
    B23.place(x=220,y=370)
    B24.place(x=390,y=370)
    B25.place(x=560,y=370)
    B26.place(x=730,y=370)
    B27.place(x=900,y=370)
    B28.place(x=1070,y=370)

    B29.place(x=50,y=470)
    B30.place(x=220,y=470)
    
def SelectDate31():
    DestroyPage(LabelYear,ButtonBack,ButtonForw,labelm,jan,feb,march,april,may,june,july,august,september,october,nov,dec)
    label3.place(relheight=1,relwidth=1)
    B1.place(x=50,y=70)
    B2.place(x=220,y=70)
    B3.place(x=390,y=70)
    B4.place(x=560,y=70)
    B5.place(x=730,y=70)
    B6.place(x=900,y=70)
    B7.place(x=1070,y=70)

    B8.place(x=50,y=170)
    B9.place(x=220,y=170)
    B10.place(x=390,y=170)
    B11.place(x=560,y=170)
    B12.place(x=730,y=170)
    B13.place(x=900,y=170)
    B14.place(x=1070,y=170)

    B15.place(x=50,y=270)
    B16.place(x=220,y=270)
    B17.place(x=390,y=270)
    B18.place(x=560,y=270)
    B19.place(x=730,y=270)
    B20.place(x=900,y=270)
    B21.place(x=1070,y=270)

    B22.place(x=50,y=370)
    B23.place(x=220,y=370)
    B24.place(x=390,y=370)
    B25.place(x=560,y=370)
    B26.place(x=730,y=370)
    B27.place(x=900,y=370)
    B28.place(x=1070,y=370)

    B29.place(x=50,y=470)
    B30.place(x=220,y=470)

    B31.place(x=390,y=470)



year=2021
bgimage2= PhotoImage(file = 'image_files/CS.png')
labelm = Label(root, image=bgimage2)
LabelYear = Label(root, text = str(year), fg="grey91",bg="grey3", font=("Century Gothic", 36, 'bold'))


def year_back():
    global year
    year=year-1
    LabelYear.config(text=str(year))
    
def year_forw():
    global year
    year=year+1
    LabelYear.config(text=str(year))
    

def mJan():
    global month
    month = "01"

def mFeb():
    global month
    month = "02"

def mMar():
    global month
    month = "03"

def mApr():
    global month
    month = "04"

def mMay():
    global month
    month = "05"

def mJun():
    global month
    month = "06"

def mJul():
    global month
    month = "07"

def mAug():
    global month
    month = "08"
    
def mSep():
    global month
    month = "09"

def mOct():
    global month
    month = "10"

def mNov():
    global month
    month = "11"

def mDec():
    global month
    month = "12"

def FebruaryDays():
    if year%4==0:
        SelectDate29()
    else:
        SelectDate28()
        
ButtonBack = Button(root,text = "◀",font=("Century Gothic", 20, 'bold'),fg="grey91",bg="grey3",
                    activebackground="grey20",activeforeground="grey91",command=lambda:[year_back()])
ButtonForw = Button(root,text = "▶",font=("Century Gothic", 20, 'bold'),fg="grey91",bg="grey3",
                    activebackground="grey20",activeforeground="grey91",command=lambda:[year_forw()])


Jan=PhotoImage(file='image_files/January.png')
jan = Button(root,image = Jan, height = "49", width =  "218",bd=0, command=lambda:[SelectDate31(), mJan()])
Feb=PhotoImage(file='image_files/February.png')
feb= Button(root,image =Feb,height = "49", width =  "252",bd=0,command = lambda:[FebruaryDays(), mFeb()])
Mar=PhotoImage(file="image_files/March.png")
march=Button(root, image =Mar,height = "49", width =  "199",bd=0,command = lambda:[SelectDate31(),mMar()])
Apr=PhotoImage(file="image_files/April.png")
april=Button(root, image =Apr,height = "49", width =  "157",bd=0,command = lambda:[SelectDate30(),mApr()])
May=PhotoImage(file="image_files/May.png")
may=Button(root, image =May,height = "49", width =  "118",bd=0,command = lambda:[SelectDate31(),mMay()])
Jun=PhotoImage(file="image_files/June.png")           
june=Button(root,image =Jun,height = "49", width =  "121",bd=0,command = lambda:[SelectDate30(),mJun()])
Jul=PhotoImage(file="image_files/July.png")    
july=Button(root,image =Jul,height = "49", width =  "114",bd=0,command = lambda:[SelectDate31(),mJul()])
Aug=PhotoImage(file="image_files/August.png")           
august=Button(root,image =Aug,height = "49", width =  "202",bd=0,command = lambda:[SelectDate31(),mAug()])
Sep = PhotoImage(file="image_files/September.png")              
september=Button(root,image =Sep,height = "49", width =  "305",bd=0,command = lambda:[SelectDate30(),mSep()])
Oct=PhotoImage(file="image_files/October.png")
october=Button(root,image =Oct,height = "49", width =  "251",bd=0,command = lambda:[SelectDate31(),mOct()])
Nov=PhotoImage(file="image_files/November.png")
nov =Button(root, image =Nov,height = "49", width =  "273",bd=0,command = lambda:[SelectDate30(),mNov()])
Dec=PhotoImage(file="image_files/December.png")
dec=Button(root, image =Dec,height = "49", width =  "263",bd=0,command = lambda:[SelectDate31(),mDec()])
    

def OpenMonth():
    DestroyPage(label1,buttonx,buttony,buttonz,buttonw,buttonv)
    labelm.place(relheight=1,relwidth=1)
    ButtonBack.place(x=700,y=82)
    ButtonForw.place(x=870,y=82)
    LabelYear.place(x=750,y=80)
    jan.place(x=438,y=160)
    feb.place(x=427,y=230)
    march.place(x=445,y=300)
    april.place(x=470,y= 370)
    may.place(x=480,y=440)
    june.place(x=475,y=510)
    july.place(x=970,y=160)
    august.place(x=920,y=230)
    september.place(x=874,y=300)
    october.place(x=900,y=370)
    nov.place(x=895,y=440)
    dec.place(x=900,y=510)


bgimage1= ImageTk.PhotoImage(file = "image_files/INTRO.Png")
label1 = Label(root, image = bgimage1)
SaveEvent = PhotoImage(file="image_files/Save an event.png")
buttonx = Button(root,image = SaveEvent ,height="37",width = "210",command=OpenMonth)
ExitApp= PhotoImage(file="image_files/Exit application.png")
buttony=Button(root,image = ExitApp,height="37",width = "250",bd=0,command=root.destroy)
DeleteEvents = PhotoImage(file="image_files/Delete Events.png")
buttonz=Button(root,image = DeleteEvents,height="40",width = "210",bd=0,command=Delete_Events)
ClearHistory= PhotoImage(file="image_files/Clear History.png")
buttonw=Button(root,image=ClearHistory,height="40",width="170",bd=0,command=Delete_record)
ViewEvents = PhotoImage(file="image_files/View events.png")
buttonv = Button(root,image=ViewEvents,height = "39", width = "178", bd=0, command = View_events) 



def OpenHomePage():
    label1.place(relheight=1,relwidth=1)
    buttonx.place(x=650,y=400)
    buttony.place(x=647,y=640)
    buttonz.place(x=653,y=460)
    buttonw.place(x=650,y=520)
    buttonv.place(x=650,y=580)


def CheckTimeDateStart():

    while(1==1):
        con = mysql.connector.connect(host='localhost',
                                       database='sys',
                                       user='root',
                                       password='')
         
        cur=con.cursor()
    
        cur.execute("SELECT*FROM Event")
        event_details = cur.fetchall()
        con.close()
        for i in range(0,len(event_details)):
            if len(str(event_details[i][2]))<8:            
                if (("0"+str(event_details[i][2])) == time.strftime("%H:%M:%S") and str(event_details[i][1]) == time.strftime("%Y-%m-%d")):
                    engine1 = pyttsx3.init()
                    engine1.say("Reminder for start of event " + event_details[i][0])
                    engine1.runAndWait()
                    tk.messagebox.showinfo("Reminder","Time to start event → "+event_details[i][0],icon='info')
            else:
                if str(event_details[i][2]) == time.strftime("%H:%M:%S") and str(event_details[i][1]) == time.strftime("%Y-%m-%d"):
                    engine1 = pyttsx3.init()
                    engine1.say("Reminder for start of event " + event_details[i][0])
                    engine1.runAndWait()
                    tk.messagebox.showinfo("Reminder","Time to start event → "+event_details[i][0],icon='info')


                

def CheckTimeDateEnd():

    while(1==1):
        con = mysql.connector.connect(host='localhost',
                                       database='sys',
                                       user='root',
                                       password='')
         
        cur=con.cursor()
    
        cur.execute("SELECT*FROM Event")
        event_details = cur.fetchall()
        con.close()
        for i in range(0,len(event_details)):
            if len(str(event_details[i][3]))<8:
                if ("0"+str(event_details[i][3]) == time.strftime("%H:%M:%S") and str(event_details[i][1]) == time.strftime("%Y-%m-%d")):
                    tk.messagebox.showinfo("Reminder","Time to end event → "+event_details[i][0],icon='info')
            else:
                if (str(event_details[i][3]) == time.strftime("%H:%M:%S") and str(event_details[i][1]) == time.strftime("%Y-%m-%d")):
                    tk.messagebox.showinfo("Reminder","Time to end event → "+event_details[i][0],icon='info')

                
x1=threading.Thread(target=CheckTimeDateStart)
x1.start()


OpenHomePage()

root.mainloop()
    


        





















    
