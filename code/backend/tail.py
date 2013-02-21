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
  # connect to serial
  ser = serial.Serial("/dev/ttyACM0", 9600)
  time.sleep(.5)
  ser.write('refill\n')
  time.sleep(.5)
  ser.write('dispense\n')
  time.sleep(.5)
  # create transaction of change machine user
  #addtrans(user=getuser(usbid=1), ammount='-.50')
  

while 1:
  try:
    where = file.tell()
    line = file.readline()
    if not line:
        time.sleep(1)
        file.seek(where)
    else:
        m = re.search('SerialNumber: (.*)$', line)
        if m is None:
          continue 
        user = getuser(usbsn=m.group(1))
        if user[4] > .50:
          dispense()
          addtrans(user=user, ammount='-.50')
        else:
          # flash light
          print "flash light"
  except KeyboardInterrupt:
    print "\nBye\n"
    sys.exit()

