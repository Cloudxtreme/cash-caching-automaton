#!/usr/bin/python
import time, os, re, ldap
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
  if user[3] < 0.50:
    return False
  # connect to serial
  ser = serial.Serial("/dev/arduino", 9600)
  time.sleep(2)
  ser.write('dispense\n')
  time.sleep(2)
  # create transaction of change machine user
  addtrans(user=user, ammount='-0.50')
  lightoff()
  return True

def lighton():
  #print "light on"
  ser = serial.Serial("/dev/arduino", 9600)
  time.sleep(2)
  ser.write('light on\n')
  time.sleep(2)
  
def lightoff():
  #print "light off"
  ser = serial.Serial("/dev/arduino", 9600)
  time.sleep(2)
  ser.write('light off\n')
  time.sleep(2)

# blink light, default is 3
def lightblink(blink=3):
  #print "light blink"
  ser = serial.Serial("/dev/arduino", 9600)
  time.sleep(2)
  ser.write('light blink '+str(blink)+'\n')
  time.sleep(2)

def getUsernameFromUSB(usbsn):
  ld = ldap.initialize('ldap://10.56.0.8')
  name = "NO_USER"
  try:
    ld.simple_bind_s()
  except ldap.LDAPError, e:
    if type(e.message) == dict and e.message.has_key('desc'):
      print e.message['desc']
    else:
      print e
  else:
    basedn = "dc=makerslocal,dc=org"
    filter = "usbSerial="+usbsn
    results = ld.search_s(basedn,ldap.SCOPE_SUBTREE,filter)
    name = results[0][1]['uid'][0]
  finally:
    ld.unbind()
    return name

def process(usbsn):
  username = getUsernameFromUSB(usbsn)
  user = getuser(username=username)
  # If user has enough money
  if user[3] >= 0.50:
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
    where = file.tell()
    line = file.readline()
    if os.path.isfile("/storage/lock"):
      continue
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

