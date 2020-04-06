import obd
from obd import OBDCommand
from obd.protocols import ECU
from obd.utils import bytes_to_int
from time import sleep
import xlwt
import subprocess
import datetime
import RPi.GPIO as GPIO
from Tkinter import *
import tkFont
import signal
import os

GPIO.setmode(GPIO.BOARD)
gear1=35
gear2=36
gear3=37
gear4=38
gear5=40
rev=33
rf=32
alco=31
GPIO.setup(gear1,GPIO.IN)
GPIO.setup(gear2,GPIO.IN)
GPIO.setup(gear3,GPIO.IN)
GPIO.setup(gear4,GPIO.IN)
GPIO.setup(gear5,GPIO.IN)
GPIO.setup(rev,GPIO.IN)
GPIO.setup(rf,GPIO.IN)
GPIO.setup(alco,GPIO.IN)




process = subprocess.call('sudo rfcomm connect 0 00:00:00:00:00:01 1&',shell = True)

c = obd.OBD()



def rpm(messages):
    d = messages[0].data
    v= bytes_to_int(d)/4.0
    return v

def speed(messages):
    d = messages[0].data
    v= bytes_to_int(d)
    return v

def engine_load(messages):
    d = messages[0].data
    v= bytes_to_int(d)/2.55
    return v

def engine_temp(messages):
    d = messages[0].data
    v= bytes_to_int(d)-40
    return v

def control_module_vtg(messages):
    d = messages[0].data
    v= bytes_to_int(d)/1000
    return v

def distance_w_mil(messages):
    d = messages[0].data
    v= bytes_to_int(d)
    return v

rp = OBDCommand("RPM","Engine RPM", b"010C",2,rpm,ECU.ENGINE,True)

sp = OBDCommand("SPEED","Engine SPEED", b"010d",1,speed,ECU.ENGINE,True)

tem = OBDCommand("COOLANT_TEMP","Engine COOLANT_TEMP", b"0105",1,engine_temp,ECU.ENGINE,True)

el = OBDCommand("ENGINE_LOAD","Engine ENGINE_LOAD", b"0104",1,engine_load,ECU.ENGINE,True)

alt_vtg = OBDCommand("CONTROL_MODULE_VOLTAGE","Engine CONTROL_MODULE_VOLTAGE", b"0142",2,control_module_vtg,ECU.ENGINE,True)

dwm = OBDCommand("DISTANCE_W_MIL","Engine DISTANCE_W_MIL", b"0121",2,distance_w_mil,ECU.ENGINE,True)
x=1



def handler(signum,frame):
    global sheet1
    global book
    global x
    global now
    if GPIO.input(rf)==0:
        print("connect your seatbelt")
        cb3.select()
        T.delete('1.0',END)
        T.insert(END,"apply seat belt")
    else:
        if GPIO.input(alco)==0:
            print("Dont drive the car")
            cb3.select()
            T.delete('1.0',END)
            T.insert(END,"alcohol detected")
        else:
            #print("alco not detected")
            cb3.deselect()
            cb2.deselect()
            cb1.select()
            global c
            global count1,count2,count3,count4,count5,count6
            T.delete('1.0',END)
            a=c.query(rp ,force = True)
            i=c.query(sp, force = True)
            aa=c.query(el, force = True)
            ab=c.query(tem, force = True)
            ac=c.query(alt_vtg, force = True)
            ad=c.query(dwm, force = True)
            sheet1.write(x,0,str(a))
            sheet1.write(x,1,str(i))
            sheet1.write(x,2,str(aa))
            sheet1.write(x,3,str(ab))
            sheet1.write(x,4,str(ac))
            sheet1.write(x,5,str(ad))
            #print 'rpm =',a.value
            #print 'speed=',i.value
            #print 'engine_load=',aa.value
            #print 'temp=',ab.value
            #print 'alt_vtg=',ac.value
            #print 'dwm=',ad.value
            T1.delete('1.0',END)
            T1.insert(END,str(i))
            T2.delete('1.0',END)
            T2.insert(END,str(a))
            #print x
            if GPIO.input(gear1)==1:
                T3.delete('1.0',END)
                T3.insert(END,"1")
                sheet1.write(x,6,'Gear 1')
                if i.value > 15:
                    T.insert(END,"Speed is exceeding change the gear\n")
                    sheet1.write(x,12,"Speed is exceeding")
                    count1=count1+1
                    cb2.select()
            elif GPIO.input(gear2)==1:        
                T3.delete('1.0',END)
                T3.insert(END,"2")
                sheet1.write(x,6,'Gear 2')
                if i.value > 30:
                    T.insert(END,"Speed is exceeding change the gear\n")
                    sheet1.write(x,12,"Speed is exceeding")
                    count1=count1+1
                    cb2.select()
            elif GPIO.input(gear3)==1:        
                T3.delete('1.0',END)
                T3.insert(END,"3")
                sheet1.write(x,6,'Gear 3')
                if i.value > 40:
                    T.insert(END,"Speed is exceeding change the gear\n")
                    sheet1.write(x,12,"Speed is exceeding")
                    count1=count1+1
                    cb2.select()
            elif GPIO.input(gear4)==1:        
                T3.delete('1.0',END)
                T3.insert(END,"4")
                sheet1.write(x,6,'Gear 4')
                if i.value > 60:
                    T.insert(END,"Speed is exceeding change the gear\n")
                    sheet1.write(x,12,"Speed is exceeding")
                    count1=count1+1
                    cb2.select()
            elif GPIO.input(gear5)==1:       
                T3.delete('1.0',END)
                T3.insert(END,"5")
                sheet1.write(x,6,'Gear 5')
                if i.value > 80:
                    T.insert(END,"Speed is exceeding\n")
                    sheet1.write(x,12,"Speed is exceeding")
                    count1=count1+1
                    cb2.select()
            elif GPIO.input(rev)==1:        
                T3.delete('1.0',END)
                T3.insert(END,"R")
                sheet1.write(x,6,'Reverse Gear')
                if i.value > 30:
                    T.insert(END,"Speed is exceeding\n")
                    sheet1.write(x,12,"Speed is exceeding")
                    count1=count1+1
                    cb2.select()
            else:
                T3.delete('1.0',END)
                T3.insert(END,"N")
                sheet1.write(x,6,'Neutral')
            if a.value > 2200 :
            #print 'RPM IS HIGHER AND AFFECTING FUEL ECONOMY'
                T.insert(END,"RPM IS HIGHER AND AFFECTING FUEL ECONOMY\n")
                sheet1.write(x,11,'RPM IS HIGHER')
                count2=count2+1
                cb2.select()
            if aa.value < 30 :
                if a.value > 2200 :
                #print 'Release the clutch or accelerator pedal '
                    T.insert(END,"Release the clutch or accelerator pedal\n")            
                    count3=count3+1
                    sheet1.write(x,8,'release the cutch or acclerator')
                    cb2.select()
            if ac.value > 14 :
                #print 'Alternator voltage is greater ,and it is affecting battery'
                T.insert(END,"Alternator voltage is greater ,and it is affecting battery\n")        
                count4=count4+1
                cb3.select()
                sheet1.write(x,9,'Alternator voltage is greater')
            if ac.value < 14 :
                #print 'Alternator voltage is lower ,and it is not charging battery'
                T.insert(END,"Alternator voltage is lower ,and it is not charging battery\n")        
                count5=count5+1
                sheet1.write(x,10,'Alternator voltage is lower')
                cb3.select()
            if ab.value > 98 :#& i.value == 0 :
                #print 'check the coolant and visit to service centre'
                T.insert(END,"Check the coolant and visit to service centre\n")        
                count6=count6+1
                sheet1.write(x,7,'check the coolant')
                cb3.select()

            book.save("/home/pi/Desktop/program1/"+now+".xls")
            x=x+1
            

            
    signal.signal(signal.SIGALRM,handler)
    signal.setitimer(signal.ITIMER_REAL,0.001)
   
    
    
    

win = Tk()

myFont = tkFont.Font(family = 'Helvetica', size = 8, weight = 'bold')  

def startprogram():
    global count1,count2,count3,count4,count5,count6,x
    global now
    global book
    global sheet1
    count1= 0
    count2= 0
    count3= 0
    count4= 0
    count5= 0
    count6= 0
    x=1
    now = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    book = xlwt.Workbook(encoding="utf-8")
    sheet1= book.add_sheet("sheet 1")
    sheet1.write(0,0,"RPM")
    sheet1.write(0,1,"SPEED")
    sheet1.write(0,2,"ENGINE LOAD")
    sheet1.write(0,3,"TEMP")
    sheet1.write(0,4,"ALTERNATOR VOLTAGE")
    sheet1.write(0,5,"MIL DIST")
    sheet1.write(0,6,"GEAR")
    sheet1.write(0,13,"gear error= ")
    sheet1.write(0,14,"RPM error= " )
    sheet1.write(0,15,"Clutch error= ")
    sheet1.write(0,16,"Alternator voltage grater= ")
    sheet1.write(0,17,"battery not charging= ")
    sheet1.write(0,18,"coolant temp error= ")
    if GPIO.input(rf)==1:
        if GPIO.input(alco)==1:
            signal.signal(signal.SIGALRM,handler)
            signal.setitimer(signal.ITIMER_REAL,0.01)
        else :
            T.delete('1.0',END)
            T.insert(END,'alcohol is detected\n')
    else:
        T.delete('1.0',END)
        T.insert(END,'Apply the seat belt\n')
                           

def exitProgram():
        win.destroy()


def stopProgram():
    global count1,count2,count3,count4,count5,count6
    signal.setitimer(signal.ITIMER_REAL,0)
    print ('gear error=',count1)
    print ('RPM error=',count2)
    print ('clutch error=',count3)
    print ('alternator voltage greater=',count4)
    print ('battery not charging=',count5)
    print ('coolant temp=',count6)
    sheet1.write(1,13, str(count1))
    sheet1.write(1,14, str(count2))
    sheet1.write(1,15, str(count3))
    sheet1.write(1,16, str(count4))
    sheet1.write(1,17, str(count5))
    sheet1.write(1,18, str(count6))
    book.save("/home/pi/Desktop/program1/"+now+".xls")

    root = Tk()
    root.title("Bar Graph")
    count4 = count4 + count5
    z_width = 320
    z_height = 180
    z = Canvas(root, width=z_width, height=z_height)
    z.pack()

    if ((count1 > 400) | (count2 > 400) | (count3 > 400) | (count4 > 400) | (count6 > 400) ):
        q=6
        z.create_text(20 , 127, text="200")
        z.create_text(20 , 93, text="400")
        z.create_text(20 , 60, text="600")
        z.create_text(20 , 27, text="800")
        z.create_text(20 , 10, text="Count")
    else:
        q=3
        z.create_text(20 , 127, text="100")
        z.create_text(20 , 93, text="200")
        z.create_text(20 , 60, text="300")
        z.create_text(20 , 27, text="400")
        z.create_text(20 , 10, text="Count")    

    speed1 = 160-(count1/q)
    rpm1 = 160-(count2/q)
    C_T1 = 160-(count6/q)
    Alt_Vtg1 = 160-(count4/q)
    Clutch1 = 160-(count3/q)

 
    z.create_rectangle(60, speed1, 90, 160, fill="red")
    z.create_text(75, 168, text="speed")
    z.create_rectangle(100, rpm1, 130, 160, fill="blue")
    z.create_text(115, 168, text="rpm")
    z.create_rectangle(140, C_T1, 170, 160, fill="green")
    z.create_text(155, 168, text="C_T")
    z.create_rectangle(180, Alt_Vtg1, 210, 160, fill="orange")
    z.create_text(195, 168, text="Alt_vtg")
    z.create_rectangle(220, Clutch1, 250, 160, fill="yellow")
    z.create_text(255, 168, text="clutch error")
    z.create_line(0, 160, 500, 160)
    z.create_line(40, 0, 40, 500)

    z.create_text(75, (speed1-10), text= count1)
    z.create_text(115, (rpm1-10), text= count2)
    z.create_text(155, (C_T1-10), text= count6)
    z.create_text(195, (Alt_Vtg1-10), text= count4)
    z.create_text(235, (Clutch1-10), text= count3)
    
    root.after(30000, lambda: root.destroy())
    root.mainloop()
    
    

win.title("Driving Monitoring System")
win.geometry('320x240')

exitButton  = Button(win, text = "Exit", font = myFont, command = exitProgram, height =1 , width = 6) 
exitButton.grid(row =1 , column = 2)

startButton  = Button(win, text = "start", font = myFont, command = startprogram, height =1 , width = 6) 
startButton.grid(row =1 , column = 0)

stopButton  = Button(win, text = "stop", font = myFont, command = stopProgram, height =1 , width = 6) 
stopButton.grid(row =1 , column = 1)

l=Label(win,text="comment",font=myFont)
l.grid(row = 1000, column = 0)
T= Text(win,height=5, width= 30,font=myFont)
T.grid(row = 1000 , column = 1)

l1=Label(win,text="speed",font=myFont)
l1.grid(row = 6,column = 0)
T1= Text(win,height=1, width= 10,font=myFont)
T1.grid(row =6,column = 1)

l2=Label(win,text="RPM",font=myFont)
l2.grid(row = 7,column = 0)
T2= Text(win,height=1, width= 10,font=myFont)
T2.grid(row =7,column = 1)

l3=Label(win,text="Gear",font=myFont)
l3.grid(row = 8,column = 0)
T3= Text(win,height=1, width= 10,font=myFont)
T3.grid(row =8,column = 1)

cb1 = Radiobutton(win,text="Green",value=1,font=myFont,width=6)
cb1.grid(row = 3, column=0)
cb2 = Radiobutton(win,text="Yellow",value=2,font=myFont,width=6)
cb2.grid(row = 3, column=1)
cb3 = Radiobutton(win,text="Red",value=3,font=myFont,width=6)
cb3.grid(row = 3, column=2)
cb1.select()


win.mainloop()
