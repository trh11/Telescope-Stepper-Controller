<<<<<<< HEAD
import Tkinter, serial, string, codecs, time
from Tkinter import *

master = Tk()
master.title("Touch Stepper Control")
w, h = master.winfo_screenwidth(), master.winfo_screenheight()
master.overrideredirect(True)
master.geometry("%dx%d+0+0" % (w, h))
master.configure(background='gray20')
ser = serial.Serial('/dev/ttyACM0',9600,timeout=3)
ser.setDTR(level=False)
ser.open()
dig = StringVar()
stp = IntVar()
dir = IntVar()
frq = IntVar()
MS = IntVar()
go = StringVar()
halt = StringVar()
home = IntVar()
count =IntVar()
h = 0
send = 0
reseat = 0
    
def entslct(event):
    ent = int(str(event.widget).strip('.'))
    global entvar
    if ent == 1:
      entvar = s
    if ent == 2:
      entvar = f
    global stpdig
    stpdig = []
    
def entclr():
  global entvar
  entvar.delete(0,END)
  global stpdig
  stpdig = []

stpdig = []
def stpent(dig):
  global inc
  stpdig.append(dig)
  inc = ''.join(stpdig)
  global entvar
  entvar.delete(0,END)
  entvar.insert(INSERT,inc)
  
def scroll():
  RDO.see(END)
  
def scanning(): 
  for n in range(0, 1):
    global h, reseat, rot, send
    if h == 1:
      h = 0
      break
    else:
      global count
      count = ser.read(4)
      if count:
        if int(count) < send:
          RDO.insert(END, 'halted at '+str(count)+' steps')
          scroll()
        else:
          RDO.insert(END, 'move completed: '+str(count)+' steps')
          scroll()
      if rot == 1:
        sign = 1
      else:
        sign = -1
      reseat = reseat + sign*int(count)
      RDO.insert(END,str(reseat)+' steps to home')
      scroll()
    
# Defines the stop command, which simply resets the Arduino over serial.
def allhalt():
  global h, send, reseat
  send = stp.get()
  ser.close()
  ser.open()
  halt = str([128,0,0]).strip('[]')
  ser.write(str(127))
  RDO.insert(END,'halt sent: '+str(halt).strip('[]'))
  scroll()
  scanning()
  h = 1
  
# Defines serial string "go" resulting from all entry field and radio buttons.
# go is the string separated by commas. dir *4+MS sets the SET byte between 0
# and 15. stp is the second variable in the string setting the number of steps
# in the square wave. frq is the third variable and sets the frequency of the
# square wave in Hz.
def allgo():
  ser.close()
  ser.open()
  global send, stp, rot, h
  send = stp.get()
  rot = dir.get()
  go = str([dir.get()*4+MS.get(),stp.get(),frq.get()]).strip('[]')
  ser.write(go)
  RDO.insert(END,'sending: '+go)
  scroll()
  h = 0
  Wr.after(1005*stp.get()/frq.get(), scanning)
    
def rewind():
  global reseat, rot, send, h
  send = abs(reseat)
  if int(reseat) <= 0:
    rewdir = 4
    rot = 1
  else:
    rewdir = 0
    rot = 0
  home = [rewdir,send,50]
  ser.write(str(home).strip('[]'))
  RDO.insert(END,'rewinding: '+str(home).strip('[]'))
  scroll()
  h = 0
  REW.after(1005*abs(reseat)/50, scanning)

def slewstart(event):
  slw = int(str(event.widget).strip('.'))
  if slw == 68:
    ord = "up"
  if slw == 64:
    ord = "down"
  slwgo = [slw+MS.get(),0,frq.get()]
  ser.write(str(slwgo).strip('[]'))
  RDO.insert(END, "slewing "+ord+" at "+str(frq.get())+" steps/second")
  scroll()
#  slw = str([dir.get()*4+MS.get(),stp.get(),frq.get()]).strip('[]')
       
def slewstop(event):
  slwhlt = [32,0,0]
  ser.write(str(slwhlt).strip('[]'))
  print slwhlt
  RDO.insert(END, "halting")
  scroll()

def quit():
    master.destroy()
  
q = Button(master, text="x", width=1, height=1, command = quit)
q.grid(row=0, column=6)

# Entry field for the number of steps in the square wave. 
#Label(master, text='Steps',background='gray20',font=(16)).grid(row=0)
s = Entry(master,name='1',width=15,bg='black',fg='green',font=("Purisa",16),insertbackground='green',textvariable=stp)
s.grid(row=1,column=1,rowspan=1,columnspan=2,padx=5)
s.bind('<Button-1>',entslct)
stp.set(1)
entvar = s
s.focus()

# Entry field for the square wave freuency.
#Label(master, text="Frequency",background='gray20',font=(16)).grid(row=1)
f = Entry(master,name='2',width=15,bg='black',fg='green',font=("Purisa",16),insertbackground='green',textvariable=frq)
f.grid(row=2,column=1,rowspan=1,columnspan=2,padx=5)
f.bind('<Button-1>',entslct)
frq.set(1)

# A Radio button for selecting the direction of the stepper rotation (CW or CCW).
# To be replaced with Up and Down and Left and Right when running two steppers.
#Label(master, text="Direction",background='gray20',font=(14)).grid(row=2)
CW = Radiobutton(master,height=2,width=8,bg="gray35",text="CW",variable=dir,value=1,indicatoron=0)
CW.grid(row=3,column=1,sticky=W+E+N,padx=10,pady=5)

CCW = Radiobutton(master,height=2,width=8,bg="gray35",text="CCW",variable=dir,value=0,indicatoron=0)
CCW.grid(row=3,column=2,sticky=W+E+N,padx=10,pady=5)

# A Radio button for setting the microstepping option. In MSxx the "x"'s
# represent the M1 and M0 digits in the SET byte respectively. MS11=xxxxxx11
# and sets the microstepping at 1/16. To be replaced with speed settings.
#Label(master,text="Step Size",background='gray20',font=(14)).grid(row=3)
MS00 = Radiobutton(master,bg="gray35",text="1", variable=MS, value=0,indicatoron=0, height=1, width=3)
MS00.grid(row=3,column=1,sticky=W+S,padx=5,pady=5)

MS10 = Radiobutton(master,bg="gray35",text="1/2", variable=MS, value=2,indicatoron=0, height=1, width=3)
MS10.grid(row=3,column=1,sticky=E+S,padx=5,pady=5)

MS01 = Radiobutton(master,bg="gray35",text="1/8", variable=MS, value=1,indicatoron=0, height=1, width=3)
MS01.grid(row=3,column=2,sticky=W+S,padx=5,pady=5)

MS11 = Radiobutton(master,bg="gray35",text="1/16", variable=MS, value=3,indicatoron=0, height=1, width=3)
MS11.grid(row=3,column=2,sticky=E+S,padx=5,pady=5)

# A Button that sends serial string "go" to the Arduino.
Wr = Button(master,text="SEND",width=6,height=4,bg="green3",font=('bold',25),command=allgo)
Wr.grid(row=1,column=3,rowspan=3,padx=10,pady=10)
Wr.cget('state')

# A button that halts the current operation on the Arduino.
STP = Button(master, text="STOP",width=6,height=1,bg="red3",font=('bold',25),command=allhalt)
STP.grid(row=4,column=1,rowspan=1,columnspan=2,padx=10,pady=5) 

REW = Button(master,text="HOME",width=6,height=1,bg="blue3",font=('bold',25),command=rewind)
REW.grid(row=4,column=3,rowspan=1,columnspan=1,padx=10,pady=5)

ONE = Button(master,text="1",height=1,width=5,bg="gray35",fg="white",font=("bold",20),command=lambda: stpent("1"))
ONE.grid(row=1, column=4, rowspan=1, columnspan=1, padx=10,pady=5)

TWO = Button(master,text="2",height=1,width=5,bg="gray35",fg="white",font=("bold",20),command=lambda: stpent("2"))
TWO.grid(row=1, column=5, rowspan=1, columnspan=1, padx=10,pady=5)

THR = Button(master,text="3",height=1,width=5,bg="gray35",fg="white",font=("bold",20),command=lambda: stpent("3"))
THR.grid(row=1, column=6, rowspan=1, columnspan=1, padx=10, pady=5)

FOU = Button(master, text="4", height=1, width=5, bg="gray35",fg="white",font=("bold",20),command=lambda: stpent("4"))
FOU.grid(row=2, column=4, rowspan=1, columnspan=1, padx=10, pady=5)

FIV = Button(master, text="5", height=1, width=5, bg="gray35",fg="white",font=("bold",20),command=lambda: stpent("5"))
FIV.grid(row=2, column=5, rowspan=1, columnspan=1, padx=10, pady=5)

SIX = Button(master, text="6", height=1, width=5, bg="gray35",fg="white",font=("bold",20),command=lambda: stpent("6"))
SIX.grid(row=2, column=6, rowspan=1, columnspan=1, padx=10, pady=5)

SEV = Button(master, text="7", height=1, width=5, bg="gray35",fg="white",font=("bold",20),command=lambda: stpent("7"))
SEV.grid(row=3, column=4, rowspan=1, columnspan=1, padx=10, pady=5)

EIG = Button(master, text="8", height=1, width=5, bg="gray35",fg="white",font=("bold",20),command=lambda: stpent("8"))
EIG.grid(row=3, column=5, rowspan=1, columnspan=1, padx=10, pady=5)

NIN = Button(master, text="9", height=1, width=5, bg="gray35",fg="white",font=("bold",20),command=lambda: stpent("9"))
NIN.grid(row=3, column=6, rowspan=1, columnspan=1, padx=10, pady=5)

ZER = Button(master, text="0", height=1, width=5, bg="gray35",fg="white",font=("bold",20),command=lambda: stpent("0"))
ZER.grid(row=4,column=5,rowspan=1,columnspan=1,padx=10,pady=5,sticky=N)

CLR = Button(master, text="CLR", height=1, width=5, bg="gray35",fg="white",font=("bold",20),command=lambda: entclr())
CLR.grid(row=4, column=4, rowspan=1, columnspan=1, padx=10, pady=5,sticky=N)

BKS = Button(master, text="BKS", height=1, width=5, bg="gray35",fg="white",font=("bold",20),command=lambda: entclr())
BKS.grid(row=4, column=6, rowspan=1, columnspan=1, padx=10, pady=5,sticky=N)

iconu = PhotoImage(file="uarrow.gif")
iconr = PhotoImage(file="rarrow.gif")
icond = PhotoImage(file="darrow.gif")
iconl = PhotoImage(file="larrow.gif")

UPB=Button(master,name='68',image=iconu,bg="black",fg="white",font=("bold",20))
UPB.grid(row=5, column=5, rowspan=1, columnspan=1, padx=10,sticky=N)
UPB.bind('<Button-1>',slewstart)
UPB.bind('<ButtonRelease-1>',slewstop)

DNB=Button(master,name='64',image=icond,bg="black",fg="white",font=("bold",20))
DNB.grid(row=5, column=5, rowspan=1, columnspan=1, padx=10,sticky=S)
DNB.bind('<Button-1>',slewstart)
DNB.bind('<ButtonRelease-1>',slewstop)

LFB=Button(master,image=iconl,bg="black",fg="white",font=("bold",20))
LFB.grid(row=5, column=4, rowspan=1, columnspan=1, padx=10,sticky=W)

RTB=Button(master, image=iconr,bg="black",fg="white",font=("bold",20))
RTB.grid(row=5, column=6, rowspan=1, columnspan=1, padx=10,sticky=E)

#Label(master,text="Read Out",background='gray20',font=(14)).grid(row=4)
RDO = Listbox(master,width=39,height=8,bg='black',fg='green',font=("Purisa",12))
RDO.grid(row=5,column=1,rowspan=1,columnspan=3,padx=2,pady=2)
  
mainloop()
=======
import Tkinter, serial, string, codecs, time
from Tkinter import *

master = Tk()
master.title("Touch Stepper Control")
master.geometry('800x480')
master.configure(background='gray20')
ser = serial.Serial('COM3',9600,timeout=3)
dig = StringVar()
stp = IntVar()
dir = IntVar()
frq = IntVar()
MS = IntVar()
go = StringVar()
halt = StringVar()
home = IntVar()
count = IntVar()
h = 0
send = 0
reseat = 0
    
def entslct(event):
    ent = int(str(event.widget).strip('.'))
    global entvar
    if ent == 1:
      entvar = s
    if ent == 2:
      entvar = f
    global stpdig
    stpdig = []
    
def entclr():
  global entvar
  entvar.delete(0,END)
  global stpdig
  stpdig = []

stpdig = []
def stpent(dig):
  global inc
  stpdig.append(dig)
  inc = ''.join(stpdig)
  global entvar
  entvar.delete(0,END)
  entvar.insert(INSERT,inc)
  
def scroll():
  RDO.see(END)
  
def scanning(): 
  for n in range(0, 1):
    global h, reseat, rot, send
    if h == 1:
      h = 0
      break
    else:
      global count
      count = ser.read(4)
      if count:
        if int(count) < send:
          RDO.insert(END, 'halted at '+str(count)+' steps')
          scroll()
        else:
          RDO.insert(END, 'move completed: '+str(count)+' steps')
          scroll()
      if rot == 1:
        sign = 1
      else:
        sign = -1
      reseat = reseat + sign*int(count)
      RDO.insert(END,str(reseat)+' steps to home')
      scroll()
    
# Defines the stop command, which simply resets the Arduino over serial.
def allhalt():
  global h, send
  send = stp.get()
  ser.close()
  ser.open()
  halt = [128,0,0]
  RDO.insert(END,'halt sent: '+str(halt).strip('[]'))
  scroll()
  time.sleep(.1)
  ser.write(halt)
  scanning()
  h = 1
  
# Defines serial string "go" resulting from all entry field and radio buttons.
# go is the string separated by commas. dir *4+MS sets the SET byte between 0
# and 15. stp is the second variable in the string setting the number of steps
# in the square wave. frq is the third variable and sets the frequency of the
# square wave in Hz.
def allgo():
  ser.close()
  ser.open()
  global send, stp, rot, h
  send = stp.get()
  rot = dir.get()
  go = str([dir.get()*4+MS.get(),stp.get(),frq.get()]).strip('[]')
  ser.write(go)
  RDO.insert(END,'sending: '+go)
  scroll()
  h = 0
  Wr.after(1005*stp.get()/frq.get(), scanning)
    
def rewind():
  global reseat, rot, send, h
  send = abs(reseat)
  if int(reseat) <= 0:
    rewdir = 4
    rot = 1
  else:
    rewdir = 0
    rot = 0
  home = [rewdir,send,50]
  ser.write(str(home).strip('[]'))
  RDO.insert(END,'rewinding: '+str(home).strip('[]'))
  scroll()
  h = 0
  REW.after(1005*abs(reseat)/50, scanning)

def slewstart(event):
  slw = int(str(event.widget).strip('.'))
  if slw == 68:
    ord = "up"
  if slw == 64:
    ord = "down"
  slwgo = [slw+MS.get(),0,frq.get()]
  ser.write(str(slwgo).strip('[]'))
  RDO.insert(END, "slewing "+ord+" at "+str(frq.get())+" steps/second")
  scroll()
#  slw = str([dir.get()*4+MS.get(),stp.get(),frq.get()]).strip('[]')
       
def slewstop(event):
  slwhlt = [32,0,0]
  ser.write(str(slwhlt).strip('[]'))
  print slwhlt
  RDO.insert(END, "halting")
  scroll()
  

# Entry field for the number of steps in the square wave. 
Label(master, text='Steps',background='gray20',font=(16)).grid(row=0)
s = Entry(master,name='1',width=15,bg='black',fg='green',font=("Purisa",16),insertbackground='green',textvariable=stp)
s.grid(row=0,column=1,rowspan=1,columnspan=2,padx=5)
s.bind('<Button-1>',entslct)
stp.set(1)
entvar = s
s.focus()

# Entry field for the square wave freuency.
Label(master, text="Frequency",background='gray20',font=(16)).grid(row=1)
f = Entry(master,name='2',width=15,bg='black',fg='green',font=("Purisa",16),insertbackground='green',textvariable=frq)
f.grid(row=1,column=1,rowspan=1,columnspan=2,padx=5)
f.bind('<Button-1>',entslct)
frq.set(1)

# A Radio button for selecting the direction of the stepper rotation (CW or CCW).
# To be replaced with Up and Down and Left and Right when running two steppers.
Label(master, text="Direction",background='gray20',font=(14)).grid(row=2)
CW = Radiobutton(master,height=2,width=8,bg="gray35",text="CW",variable=dir,value=1,indicatoron=0)
CW.grid(row=2,column=1,sticky=W+E+N,padx=10,pady=5)

CCW = Radiobutton(master,height=2,width=8,bg="gray35",text="CCW",variable=dir,value=0,indicatoron=0)
CCW.grid(row=2,column=2,sticky=W+E+N,padx=10,pady=5)

# A Radio button for setting the microstepping option. In MSxx the "x"'s
# represent the M1 and M0 digits in the SET byte respectively. MS11=xxxxxx11
# and sets the microstepping at 1/16. To be replaced with speed settings.
Label(master,text="Step Size",background='gray20',font=(14)).grid(row=3)
MS00 = Radiobutton(master,bg="gray35",text="1", variable=MS, value=0,indicatoron=0, height=1, width=3)
MS00.grid(row=2,column=1,sticky=W+S,padx=5,pady=5)

MS10 = Radiobutton(master,bg="gray35",text="1/2", variable=MS, value=2,indicatoron=0, height=1, width=3)
MS10.grid(row=2,column=1,sticky=E+S,padx=5,pady=5)

MS01 = Radiobutton(master,bg="gray35",text="1/8", variable=MS, value=1,indicatoron=0, height=1, width=3)
MS01.grid(row=2,column=2,sticky=W+S,padx=5,pady=5)

MS11 = Radiobutton(master,bg="gray35",text="1/16", variable=MS, value=3,indicatoron=0, height=1, width=3)
MS11.grid(row=2,column=2,sticky=E+S,padx=5,pady=5)

# A Button that sends serial string "go" to the Arduino.
Wr = Button(master,text="SEND",width=8,height=4,bg="green3",font=('bold',25),command=allgo)
Wr.grid(row=0,column=3,rowspan=3,padx=10,pady=10)
Wr.cget('state')

# A button that halts the current operation on the Arduino.
STP = Button(master, text="STOP",width=8,height=1,bg="red3",font=('bold',25),command=allhalt)
STP.grid(row=3,column=1,rowspan=1,columnspan=2,padx=10,pady=10) 

REW = Button(master,text="HOME",width=8,height=1,bg="blue3",font=('bold',25),command=rewind)
REW.grid(row=3,column=3,rowspan=1,columnspan=1,padx=10,pady=10)

ONE = Button(master,text="1",height=1,width=5,bg="gray35",fg="white",font=("bold",20),command=lambda: stpent("1"))
ONE.grid(row=0, column=4, rowspan=1, columnspan=1, padx=10,pady=10)

TWO = Button(master,text="2",height=1,width=5,bg="gray35",fg="white",font=("bold",20),command=lambda: stpent("2"))
TWO.grid(row=0, column=5, rowspan=1, columnspan=1, padx=10,pady=10)

THR = Button(master,text="3",height=1,width=5,bg="gray35",fg="white",font=("bold",20),command=lambda: stpent("3"))
THR.grid(row=0, column=6, rowspan=1, columnspan=1, padx=10, pady=10)

FOU = Button(master, text="4", height=1, width=5, bg="gray35",fg="white",font=("bold",20),command=lambda: stpent("4"))
FOU.grid(row=1, column=4, rowspan=1, columnspan=1, padx=10, pady=10)

FIV = Button(master, text="5", height=1, width=5, bg="gray35",fg="white",font=("bold",20),command=lambda: stpent("5"))
FIV.grid(row=1, column=5, rowspan=1, columnspan=1, padx=10, pady=10)

SIX = Button(master, text="6", height=1, width=5, bg="gray35",fg="white",font=("bold",20),command=lambda: stpent("6"))
SIX.grid(row=1, column=6, rowspan=1, columnspan=1, padx=10, pady=10)

SEV = Button(master, text="7", height=1, width=5, bg="gray35",fg="white",font=("bold",20),command=lambda: stpent("7"))
SEV.grid(row=2, column=4, rowspan=1, columnspan=1, padx=10, pady=10)

EIG = Button(master, text="8", height=1, width=5, bg="gray35",fg="white",font=("bold",20),command=lambda: stpent("8"))
EIG.grid(row=2, column=5, rowspan=1, columnspan=1, padx=10, pady=10)

NIN = Button(master, text="9", height=1, width=5, bg="gray35",fg="white",font=("bold",20),command=lambda: stpent("9"))
NIN.grid(row=2, column=6, rowspan=1, columnspan=1, padx=10, pady=10)

ZER = Button(master, text="0", height=1, width=5, bg="gray35",fg="white",font=("bold",20),command=lambda: stpent("0"))
ZER.grid(row=3,column=5,rowspan=1,columnspan=1,padx=10,pady=10,sticky=N)

CLR = Button(master, text="CLR", height=1, width=5, bg="gray35",fg="white",font=("bold",20),command=lambda: entclr())
CLR.grid(row=3, column=4, rowspan=1, columnspan=1, padx=10, pady=10,sticky=N)

BKS = Button(master, text="BKS", height=1, width=5, bg="gray35",fg="white",font=("bold",20),command=lambda: entclr())
BKS.grid(row=3, column=6, rowspan=1, columnspan=1, padx=10, pady=10,sticky=N)

iconu = PhotoImage(file="uarrow.gif")
iconr = PhotoImage(file="rarrow.gif")
icond = PhotoImage(file="darrow.gif")
iconl = PhotoImage(file="larrow.gif")

UPB=Button(master,name='68',image=iconu,bg="black",fg="white",font=("bold",20))
UPB.grid(row=4, column=5, rowspan=1, columnspan=1, padx=10,sticky=N)
UPB.bind('<Button-1>',slewstart)
UPB.bind('<ButtonRelease-1>',slewstop)

DNB=Button(master,name='64',image=icond,bg="black",fg="white",font=("bold",20))
DNB.grid(row=4, column=5, rowspan=1, columnspan=1, padx=10,sticky=S)
DNB.bind('<Button-1>',slewstart)
DNB.bind('<ButtonRelease-1>',slewstop)

LFB=Button(master,image=iconl,bg="black",fg="white",font=("bold",20))
LFB.grid(row=4, column=4, rowspan=1, columnspan=1, padx=10,sticky=W)

RTB=Button(master, image=iconr,bg="black",fg="white",font=("bold",20))
RTB.grid(row=4, column=6, rowspan=1, columnspan=1, padx=10,sticky=E)

Label(master,text="Read Out",background='gray20',font=(14)).grid(row=4)
RDO = Listbox(master,width=39,height=8,bg='black',fg='green',font=("Purisa",12))
RDO.grid(row=4,column=1,rowspan=1,columnspan=3,padx=2,pady=2)
  
mainloop()
>>>>>>> 2b7846f22d7c48e2c4701fdf62a0ff80ac985a59
