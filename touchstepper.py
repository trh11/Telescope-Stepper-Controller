from Tkinter import*
import Tkinter, serial, string, codecs, time

master = Tk()
master.title("Stepper Control")
master.geometry('800x480')
ser = serial.Serial('COM3',9600,timeout=3)
dig = StringVar()
stp = IntVar()
DIR = IntVar()
frq = IntVar()
MS = IntVar()
go = StringVar()
halt = StringVar()
home = IntVar()
count = IntVar()
h = 0
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
  
def scanning(): 
  for n in range(0, 1):
    global h
    if h == 1:
      h = 0
      break
    global count
    count = ser.read(4)
    if count:
      if int(count) < stp.get():
        print 'halted at', count
      else:
        print count
        print 'DONE'
    if DIR.get() == 1:
      sign = 1
    else:
      sign = -1
    global reseat
    reseat = reseat + sign*int(count)
    print reseat, 'steps to home'
    
# Defines the stop command, which simply resets the Arduino over serial.
def allhalt():
  ser.close()
  ser.open()
  halt = [128,0,0]
  ser.write(halt)
  print str(halt).strip('[]')
  ser.write(str(halt).strip('[]'))
  scanning()
  global h
  h = 1
  
# Defines serial string "go" resulting from all entry field and radio buttons.
# go is the string separated by commas. DIR *4+MS sets the SET byte between 0
# and 15. stp is the second variable in the string setting the number of steps
# in the square wave. frq is the third variable and sets the frequency of the
# square wave in Hz.
def allgo():
  ser.close()
  ser.open()
  global stp
  go = [DIR.get()*4+MS.get(),stp.get(),frq.get()]
  ser.write(str(go).strip('[]'))
  print str(go).strip('[]')
  time.sleep(.5)
  h = 0
  Wr.after(1005*stp.get()/frq.get(), scanning)
    
def rewind():
  ser.close()
  ser.open()
  home = [64,0,0]
  ser.write(str(home).strip('[]'))
  print str(home).strip('[]')
  time.sleep(.1)
  ser.write(str(home).strip('[]'))
  while True:
    ser.close()
    ser.open()
    count = ser.read()
    if count:
      print count
      break
  reseat = reseat + count
  ser.close()
  REW.config(state=DISABLED)
  time.sleep(3)
  REW.config(state=NORMAL)
  print reseat
 
# Entry field for the number of steps in the square wave. 
Label(master, text='Steps').grid(row=0)
s = Entry(master,textvariable=stp,name='1')
s.grid(row=0, column=1,columnspan=2)
s.bind('<Button-1>',entslct)
stp.set(1)
entvar = s
s.focus()

# Entry field for the square wave freuency.
Label(master, text="Frequency").grid(row=1)
f = Entry(master,name='2',textvariable=frq)
f.grid(row=1, column=1,columnspan=2)
f.bind('<Button-1>',entslct)
frq.set(1)

# A Radio button for selecting the direction of the stepper rotation (CW or CCW).
# To be replaced with Up and Down and Left and Right when running two steppers.
Label(master, text="Direction").grid(row=2)
CW = Radiobutton(
  master, text="CW", variable=DIR, value=1,
  indicatoron=0, height=2, width=8).grid(
  row=2,column=1,sticky=W+E,padx=5,pady=5)
CCW = Radiobutton(
  master, text="CCW", variable=DIR, value=0,
  indicatoron=0, height=2, width=8).grid(
  row=2,column=2,sticky=W+E,padx=5,pady=5)

# A Radio button for setting the microstepping option. In MSxx the "x"'s
# represent the M1 and M0 digits in the SET byte respectively. MS11=xxxxxx11
# and sets the microstepping at 1/16. To be replaced with speed settings.
Label(master, text="Step Size").grid(row=3)
MS00 = Radiobutton(master, text="1", variable=MS, value=0,
  indicatoron=0, height=1, width=3).grid(
  row=3,column=1,sticky=W,padx=5,pady=5)
MS10 = Radiobutton(master, text="1/2", variable=MS, value=2,
  indicatoron=0, height=1, width=3).grid(
  row=3,column=1,sticky=E,padx=5,pady=5)
MS01 = Radiobutton(master, text="1/8", variable=MS, value=1,
  indicatoron=0, height=1, width=3).grid(
  row=3,column=2,sticky=W,padx=5,pady=5)
MS11 = Radiobutton(master, text="1/16", variable=MS, value=3,
  indicatoron=0, height=1, width=3).grid(
  row=3,column=2,sticky=E,padx=5,pady=5)

# A button that halts the current operation on the Arduino.
STP = Button(master, text="STOP",bg="red",command=allhalt)
STP.grid(row=5,column=1,rowspan=2,columnspan=2,sticky=W+E+N+S)
  
# A Button that sends serial string "go" to the Arduino.
Wr = Button(master, text="Send", width=10, bg="green",command=allgo)
Wr.grid(row=0,column=3,rowspan=4,sticky=W+E+N+S,padx=5,pady=5)
Wr.cget('state')

REW = Button(master, text="HOME", width=10, bg="blue", command=rewind)
REW.grid(row=5, column=3, rowspan=2, columnspan=1)

  
ONE = Button(master, text="1",height=3, width=6, bg="white",command=lambda: stpent("1"))
ONE.grid(row=0, column=4, rowspan=2, columnspan=1, padx=5,pady=5)

TWO = Button(master, text="2",height=3, width=6, bg="white",command=lambda: stpent("2"))
TWO.grid(row=0, column=5, rowspan=2, columnspan=1, padx=5,pady=5)

THR = Button(master, text="3", height=3, width=6, bg="white",command=lambda: stpent("3"))
THR.grid(row=0, column=6, rowspan=2, columnspan=1, padx=5, pady=5)

FOU = Button(master, text="4", height=3, width=6, bg="white",command=lambda: stpent("4"))
FOU.grid(row=2, column=4, rowspan=2, columnspan=1, padx=5, pady=5)

FIV = Button(master, text="5", height=3, width=6, bg="white",command=lambda: stpent("5"))
FIV.grid(row=2, column=5, rowspan=2, columnspan=1, padx=5, pady=5)

SIX = Button(master, text="6", height=3, width=6, bg="white",command=lambda: stpent("6"))
SIX.grid(row=2, column=6, rowspan=2, columnspan=1, padx=5, pady=5)

SEV = Button(master, text="7", height=3, width=6, bg="white",command=lambda: stpent("7"))
SEV.grid(row=4, column=4, rowspan=2, columnspan=1, padx=5, pady=5)

EIG = Button(master, text="8", height=3, width=6, bg="white",command=lambda: stpent("8"))
EIG.grid(row=4, column=5, rowspan=2, columnspan=1, padx=5, pady=5)

NIN = Button(master, text="9", height=3, width=6, bg="white",command=lambda: stpent("9"))
NIN.grid(row=4, column=6, rowspan=2, columnspan=1, padx=5, pady=5)

ZER = Button(master, text="0", height=3, width=6, bg="white",command=lambda: stpent("0"))
ZER.grid(row=6, column=5, rowspan=2, columnspan=1, padx=5, pady=5)

CLR = Button(master, text="CLR", height=3, width=6, bg="white",command=lambda: entclr())
CLR.grid(row=6, column=4, rowspan=2, columnspan=1, padx=5, pady=5)

BKS = Button(master, text="<|", height=3, width=6, bg="white",command=lambda: entclr())
BKS.grid(row=6, column=6, rowspan=2, columnspan=1, padx=5, pady=5)
  
mainloop()