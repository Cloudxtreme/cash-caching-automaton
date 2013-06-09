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
  ser.close()
  return True

def lighton():
  #print "light on"
  ser = serial.Serial("/dev/arduino", 9600)
  time.sleep(2)
  ser.write('light on\n')
  time.sleep(2)
  ser.close()
  
def lightoff():
  #print "light off"
  ser = serial.Serial("/dev/arduino", 9600)
  time.sleep(2)
  ser.write('light off\n')
  time.sleep(2)
  ser.close()

# blink light, default is 3
def lightblink(blink=3):
  #print "light blink"
  ser = serial.Serial("/dev/arduino", 9600)
  time.sleep(2)
  ser.write('light blink '+str(blink)+'\n')
  time.sleep(2)
  ser.close()

def process(usbsn):
  ldapuser = getuserfromldap(usbsn=usbsn)
  user = getuser(username=ldapuser['username'])
  # If user has enough money
  if user[3] >= 0.50:
    if dispense():
      addtrans(user=user, ammount='-0.50')
      user = getuser(username=ldapuser['username'])
      message = "From: CasCA <CasCA@makerslocal.org>\nTo: %s\nSubject: CasCA Status $%.2f\n\nDear %s, \n\nThis is your neighborhood cash machine.  I am emailing to let you know that your current account balance is $%.2f.  If you would like to add more money please contact Tyler Crumpton aka. tylercrumpton in IRC or tyler.crumpton@gmail.com\n\nThanks\nCasCA" %(ldapuser['email'], round(user[3],2), user[1], round(user[3],2))
      sendemail( sender='cashmachine@makerslocal.org', receiver=ldapuser['email'], message=message)
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

