#!/usr/bin/python
import time, os, re
import serial
from cash_api import *

#Set the filename and open the file
filename = '/var/log/kern.log'
file = open(filename,'r')

#Find the size of the file and move to the end
st_results = os.stat(filename)
st_size = st_results[6]
file.seek(st_size)

# call to dispense change
def dispense():
  user=getuser(userid=1)
  if user[4] < 0.50:
    return False
  # connect to serial
  ser = serial.Serial("/dev/ttyACM0", 9600)
  time.sleep(2)
  ser.write('dispense\n')
  time.sleep(2)
  # create transaction of change machine user
  addtrans(user=user, ammount='-0.50')
  lightoff()
  return True

def lighton():
  #print "light on"
  ser = serial.Serial("/dev/ttyACM0", 9600)
  time.sleep(2)
  ser.write('light on\n')
  time.sleep(2)
  
def lightoff():
  #print "light off"
  ser = serial.Serial("/dev/ttyACM0", 9600)
  time.sleep(2)
  ser.write('light off\n')
  time.sleep(2)

# blink light, default is 3
def lightblink(blink=3):
  #print "light blink"
  ser = serial.Serial("/dev/ttyACM0", 9600)
  time.sleep(2)
  ser.write('light blink '+str(blink)+'\n')
  time.sleep(2)

def process(usbsn):
  user = getuser(usbsn=usbsn)
  # If user has enought money
  if user[4] >= 0.50:
    if dispense():
      addtrans(user=user, ammount='-0.50')
      return True
    else:
      lighton()
  else:
    #print "no dispense"
    lightblink()
    return False

while 1:
  try:
    if os.path.isfile("/storage/lock"):
      continue
    where = file.tell()
    line = file.readline()
    if not line:
        time.sleep(1)
        file.seek(where)
    else:
        m = re.search('SerialNumber: (.*)$', line)
        if m is None:
          continue 
        # proccess receive usbsn
        process(m.group(1))
  except KeyboardInterrupt:
    print "\nBye\n"
    sys.exit()

