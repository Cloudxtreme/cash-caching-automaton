#!/usr/bin/python
import sqlite3
import subprocess
import os
import sys
import re
import pprint
import signal
from cash_api import *

def showuserstatus():
  sql = '''select a.id, a.username, a.email, sum(b.usd) from users a left join transactions b on b.users_id = a.id GROUP  BY a.username;'''
  args = ()
  ret = query(sql, args)
  print "{0:>12s}{1:>12s}{2:>12s}{3:>25s}".format("Useer ID","User Name","Balance","Email")
  print "{0:>12s}{1:>12s}{2:>12s}{3:>25s}".format("--------","---------","--------","--------")
  for row in ret:
    if not row[3]: bal = 0.00
    else: bal = row[3]
    print "{0:>12d}{1:>12s}{2:>12.2f}{3:>25s}".format(row[0], row[1], bal, row[2])

def updateuser():
  showuserstatus()
  userid = raw_input("Please enter userid you wish to edit: ")
  user = getuser(userid=userid) 
  if user[0] == None:
    print "Not a valid userid"
    return
  username = raw_input("Enter new username ["+user[1]+"]: ")
  if not username:
    username = user[1]
  email = raw_input("Enter new email ["+user[2]+"]: ")
  if not email:
    email = user[2]
  usb = raw_input("Do you want to update the USBid? [Y/n]: ")
  if usb == "y" or usb == "Y": usbsn = getusbsn()
  else: usbsn = user[3]
  print "{0:>12s}{1:>12s}{2:>25s}{3:>20s}".format("Useer ID","User Name","Email","USB")
  print "{0:>12s}{1:>12s}{2:>25s}{3:>20s}".format("--------","---------","--------","--------")
  print "{0:>12s}{1:>12s}{2:>25s}{3:>20s}".format(userid, username, email, usbsn)
  answer = raw_input("Is this correct? [Y/n]: ")
  if not (answer == "y" or answer == "Y"):
    return
  sql = '''UPDATE users SET username = ?, email = ?, usb_sn = ? WHERE id = ?'''
  args = (username, email, usbsn, userid)
  if not query(sql, args):
    print "Something went wrong!"
  

def getusbsn():
  usb = raw_input("Did you plug in the usb stick? [Y/n]: ")
  if not (usb == "y" or usb == "Y"): 
    getusbsn()
  p1 = subprocess.Popen('dmesg', shell=False, stdout=subprocess.PIPE)
  p2 = subprocess.Popen('tac', shell=False, stdin=p1.stdout, stdout=subprocess.PIPE)
  usbsn = ''
  for line in p2.stdout:
    m = re.search(r"SerialNumber: (\w+)", line)
    if m and not usbsn:
      usbsn = m.group(1)
  return usbsn

def adduser():
  username = raw_input("Enter new username: ")
  email = raw_input("Enter new email: ")
  usbsn = getusbsn() 

  # print to verify
  print "{0:>12s}{1:>25s}{2:>25s}".format("User Name","Email","USB")
  print "{0:>12s}{1:>25s}{2:>25s}".format("---------","--------","--------")
  print "{0:>12s}{1:>25s}{2:>25s}".format(username, email, usbsn)
  answer = raw_input("Is this correct? [Y/n]: ")
  if not (answer == "y" or answer == "Y"):
    return
 
  # write to db
  sql = '''INSERT INTO users VALUES (NULL, ?, ?, ?)'''
  args = (username, email, usbsn)
  if not query(sql, args):
    print "Something went wrong!"
 
def newtrans():
  showuserstatus()
  userid = raw_input("Please enter userid you wish to edit: ")
  user = getuser(userid=userid) 
  if user[0] == None:
    print "Not a valid userid"
    return
  print "Please enter ammount of transaction: "
  ammount = raw_input("exapmle: 0.50 or -0.50: ")
  if not addtrans(user=user, ammount=ammount):
    print "Something went wrong!"

def menu():
  print "Type the number for the function you want to do"
  print "1. Show Users Status"
  print "2. Update user"
  print "3. Add user"
  print "4. Add Trasaction"
  return raw_input("Selection: ")

 
while True:
  try:
    x = menu()
    if x == "1":
      showuserstatus()
    elif x == "2":
      updateuser()
    elif x == "3":
      adduser()
    elif x == "4":
      newtrans()
    else:
      break
  except KeyboardInterrupt:
    print "\nBye\n"
    sys.exit()

