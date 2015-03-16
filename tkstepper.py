from Tkinter import*
import Tkinter, serial, string, codecs, time

master = Tk()
master.title("Stepper Control")
ser = serial.Serial('COM3',9600,timeout=3)
DIR = IntVar()
stp = IntVar()
frq = IntVar()
MS = IntVar()
go = StringVar()
halt = StringVar()
home = IntVar()
count = IntVar()
h = IntVar()

# Entry field for the number of steps in the square wave. 
Label(master, text="Steps").grid(row=0)
s = Entry(master,textvariable=stp)
s.grid(row=0, column=1,columnspan=2)
s.focus_set()
stp.set(10)

# Entry field for the square wave freuency.
Label(master, text="Frequency").grid(row=1)
f = Entry(master,textvariable=frq)
f.grid(row=1, column=1,columnspan=2)
f.focus_set()
frq.set(1)

# A Radio button for selecting the direction of the stepper rotation (CW or CCW).
# To be replaced with Up and Down and Left and Right when running two steppers.
Label(master, text="Direction").grid(row=2)
CW = Radiobutton(
  master, text="CW", variable=DIR, value=1,
  indicatoron=0, height=2, width=8).grid(
  row=2,column=1,sticky=W+E,padx=2,pady=2)
CCW = Radiobutton(
  master, text="CCW", variable=DIR, value=0,
  indicatoron=0, height=2, width=8).grid(
  row=2,column=2,sticky=W+E,padx=2,pady=2)

# A Radio button for setting the microstepping option. In MSxx the "x"'s
# represent the M1 and M0 digits in the SET byte respectively. MS11=xxxxxx11
# and sets the microstepping at 1/16. To be replaced with speed settings.
Label(master, text="Step Size").grid(row=3)
MS00 = Radiobutton(master, text="1", variable=MS, value=0,
  indicatoron=0, height=1, width=3).grid(
  row=3,column=1,sticky=W,padx=2,pady=2)
MS10 = Radiobutton(master, text="1/2", variable=MS, value=2,
  indicatoron=0, height=1, width=3).grid(
  row=3,column=1,sticky=E,padx=2,pady=2)
MS01 = Radiobutton(master, text="1/8", variable=MS, value=1,
  indicatoron=0, height=1, width=3).grid(
  row=3,column=2,sticky=W,padx=2,pady=2)
MS11 = Radiobutton(master, text="1/16", variable=MS, value=3,
  indicatoron=0, height=1, width=3).grid(
  row=3,column=2,sticky=E,padx=2,pady=2)

def scanning(): 
  for n in range(0,1):
    global h
    if h == 1:
      h = 0
      break
    count = ser.read(4)
    if count:
      if int(count) < stp.get():
        print count
        print "HALTED"
        time.sleep(.1)
      else:
        print count
        print 'DONE'
        time.sleep(.1)
  
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

# A button that halts the current operation on the Arduino.
STP = Button(master, text="STOP",bg="red",command=allhalt)
STP.grid(row=5,column=1,rowspan=2,columnspan=2,sticky=W+E+N+S)
  
# Defines serial string "go" resulting from all entry field and radio buttons.
# go is the string separated by commas. DIR *4+MS sets the SET byte between 0
# and 15. stp is the second variable in the string setting the number of steps
# in the square wave. frq is the third variable and sets the frequency of the
# square wave in Hz.
def allgo():
  global h
  h = 0
  ser.close()
  ser.open()
  go = [DIR.get()*4+MS.get(),stp.get(),frq.get()]
  ser.write(str(go).strip('[]'))
  print str(go).strip('[]')
  time.sleep(.5)
#  while True:
#    count = ser.read(4)
#    if count:
#      if int(count) < stp.get():
#        print count
#      else:
#        print count
#        ser.close()
#        break
  Wr.after(1005*stp.get()/frq.get(), scanning)
    
# A Button that sends serial string "go" to the Arduino.
Wr = Button(master, text="Send", width=10, bg="green",command=allgo)
Wr.grid(row=0,column=3,rowspan=4,sticky=W+E+N+S,padx=5,pady=5)
Wr.cget('state')

reseat = 0
   
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

REW = Button(master, text="HOME", width=10, bg="blue", command=rewind)
REW.grid(row=5,column=3,rowspan=2,columnspan=1)

mainloop()