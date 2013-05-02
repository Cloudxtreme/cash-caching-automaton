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
  print "{0:>12s}{1:>16s}{2:>12s}{3:>25s}".format("User ID","User Name","Balance","Email")
  print "{0:>12s}{1:>16s}{2:>12s}{3:>25s}".format("--------","---------","--------","--------")
  for row in ret:
    if not row[3]: bal = 0.00
    else: bal = row[3]
    print "{0:>12d}{1:>16s}{2:>12.2f}{3:>25s}".format(row[0], row[1], bal, row[2])

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
  print "{0:>12s}{1:>16s}{2:>25s}".format("User ID","User Name","Email")
  print "{0:>12s}{1:>16s}{2:>25s}".format("--------","---------","--------")
  print "{0:>12s}{1:>16s}{2:>25s}".format(userid, username, email)
  answer = raw_input("Is this correct? [Y/n]: ")
  if not (answer == "y" or answer == "Y"):
    return
  sql = '''UPDATE users SET username = ?, email = ? WHERE id = ?'''
  args = (username, email, userid)
  if not query(sql, args):
    print "Something went wrong!"

def adduser():
  username = raw_input("Enter username: ")
  email = raw_input("Enter new email: ")

  # print to verify
  print "{0:>16s}{1:>25s}".format("User Name","Email")
  print "{0:>16s}{1:>25s}".format("---------","--------")
  print "{0:>16s}{1:>25s}".format(username, email)
  answer = raw_input("Is this correct? [Y/n]: ")
  if not (answer == "y" or answer == "Y"):
    return
 
  # write to db
  sql = '''INSERT INTO users VALUES (NULL, ?, ?)'''
  args = (username, email)
  if not query(sql, args):
    print "Something went wrong!"
 
def newtrans():
  showuserstatus()
  userid = raw_input("Please enter userid you wish to edit: ")
  user = getuser(userid=userid) 
  if user[0] == None:
    print "Not a valid userid"
    return
  print "Please enter amount of transaction: "
  ammount = raw_input("example: 0.50 or -0.50: ")
  if not addtrans(user=user, ammount=ammount):
    print "Something went wrong!"

def menu():
  print "Type the number for the function you want to do"
  print "1. Show Users Status"
  print "2. Update User"
  print "3. Add User"
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

