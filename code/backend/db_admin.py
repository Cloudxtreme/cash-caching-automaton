#!/usr/bin/python
import sqlite3
import subprocess
import os
import sys
import re
import pprint
import signal
import time
from cash_api import *

def showuserstatus():
  sql = '''select a.id, a.username, sum(b.usd) from users a left join transactions b on b.users_id = a.id GROUP  BY a.username;'''
  args = ()
  ret = query(sql, args)
  print "{0:>12s}{1:>16s}{2:>12s}".format("User ID","User Name","Balance")
  print "{0:>12s}{1:>16s}{2:>12s}".format("--------","---------","--------")
  for row in ret:
    if not row[2]: bal = 0.00
    else: bal = row[2]
    print "{0:>12d}{1:>16s}{2:>12.2f}".format(row["id"], row["username"], bal)

def updateuser():
  showuserstatus()
  userid = raw_input("Please enter userid you wish to edit: ")
  user = getuser(userid=userid) 
  if user[0] == None:
    print "Not a valid userid"
    return
  username = raw_input("Enter new username ["+user["username"]+"]: ")
  if not username:
    username = user[1]
  print "{0:>12s}{1:>16s}".format("User ID","User Name")
  print "{0:>12s}{1:>16s}".format("--------","---------")
  print "{0:>12s}{1:>16s}".format(userid, username)
  answer = raw_input("Is this correct? [Y/n]: ")
  if not (answer == "y" or answer == "Y"):
    return
  sql = '''UPDATE users SET username = ? WHERE id = ?'''
  args = (username, userid)
  if not query(sql, args):
    print "Something went wrong!"

def adduser():
  username = raw_input("Enter username: ")

  # print to verify
  print "{0:>16s}".format("User Name")
  print "{0:>16s}".format("---------")
  print "{0:>16s}".format(username)
  answer = raw_input("Is this correct? [Y/n]: ")
  if not (answer == "y" or answer == "Y"):
    return
 
  # write to db
  sql = '''INSERT INTO users VALUES (NULL, ?, NULL)'''
  args = (username,)
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

def deletetrans():
  days = raw_input("How many days back should we list transactions?: ")
  days = "-" + str(days) + " day"
  sql = '''select t.id, u.username, t.usd, t.timestamp from users as u join transactions t on u.id=t.users_id where ( t.users_id != 1 OR t.usd > 0 ) and t.timestamp > strftime('%s','now',?)'''
  args = (days,)
  ret = query(sql, args)
  message = "{0:>16s}{1:>16s}{2:>16s}{3:>20s}\n".format("TransID", "User Name","Transaction","Time")
  message = message + "{0:>16s}{1:>16s}{2:>16s}{3:>20s}\n".format("---------", "---------","--------","---------")
  for trans in ret:
    message = message + "{0:>16s}{1:>16s}{2:>16s}{3:>20s}\n".format(str(trans['id']),str(trans['username']),str(trans['usd']),time.strftime("%D %H:%M", time.localtime(int(trans['timestamp']))))
  print message
  transid = raw_input("What is the TransID of the transaction you wish to delete?: ")
  for trans in transid.split():
    sql = '''SELECT users_id FROM transactions WHERE id = ?'''
    args = (trans, )
    ret = query(sql, args)
    user = getuser(userid=1)
    addtrans(user=user, ammount='0.50')
    user = getuser(userid=ret[0][0])
    addtrans(user=user, ammount='0.50')


def latesttrans(days=1):
  days = "-" + str(days) + " day"
  sql = '''select u.username, t.usd, t.timestamp from users as u join transactions t on u.id=t.users_id where ( t.users_id != 1 OR t.usd > 0 ) and t.timestamp > strftime('%s','now',?)'''
  args = (days,)
  ret = query(sql, args)
  message = "{0:>16s}{1:>16s}{2:>20s}\n".format("User Name","Transaction","Time")
  message = message + "{0:>16s}{1:>16s}{2:>20s}\n".format("---------","--------","---------")
  for trans in ret:
    message = message + "{0:>16s}{1:>16s}{2:>20s}\n".format(str(trans['username']),str(trans['usd']),time.strftime("%D %H:%M", time.localtime(int(trans['timestamp']))))
  print message

def menu():
  print "Type the number for the function you want to do"
  print "1. Show Users Status"
  print "2. Update User"
  print "3. Add User"
  print "4. Add Transaction"
  print "5. Delete Transaction"
  print "6. Transactions over the past day"
  print "7. Transactions over the past x days"
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
    elif x == "5":
      deletetrans()
    elif x == "6":
      latesttrans()
    elif x == "7":
      days = raw_input("Number of days: ")
      latesttrans(days)
    else:
      break
  except KeyboardInterrupt:
    print "\nBye\n"
    sys.exit()

