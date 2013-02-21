#!/usr/bin/python
import sqlite3
import os
import sys
import datetime
import time
import pprint

DB = 'cash_db'
# connect to database located in current directory
def dbconnect():
  pathname = os.path.dirname(sys.argv[0])
  dbfile = os.path.abspath(pathname)+'/'+DB
  return sqlite3.connect(dbfile)

# Run the qery and return all if it is a selct, or lastrowid if it is insert
def query(sql,args):
    # create connection and set curser
    conn = dbconnect()
    curs = conn.cursor()
    # execute sql passed in
    curs.execute(sql,args)
    # rowcount is funny
    # if select
    if curs.rowcount == -1:
      ret = curs.fetchall()
    # if insert
    else:
      ret = curs.lastrowid
      conn.commit()
    conn.close()
    return ret

# return an array with id, username, email, usbsn, and balance
def getuser(userid='', username='', usbsn='', email=''):
  if userid:
    sql = '''SELECT a.*, SUM(b.usd) FROM users a LEFT JOIN transactions b ON b.users_id = a.id WHERE a.id = ?'''
    args = (userid,)
    user =  query(sql, args)
  elif username:
    sql = '''SELECT a.*, SUM(b.usd) FROM users a LEFT JOIN transactions b ON b.users_id = a.id WHERE a.username = ?'''
    args = (username,)
    user =  query(sql, args)
  elif usbsn:
    sql = '''SELECT a.*, SUM(b.usd) FROM users a LEFT JOIN transactions b ON b.users_id = a.id WHERE a.usb_sn = ?'''
    args = (usbsn,)
    user = query(sql, args)
  elif email:
    sql = '''SELECT a.*, SUM(b.usd) FROM users a LEFT JOIN transactions b ON b.users_id = a.id WHERE a.email = ?'''
    args = (email,)
    user = query(sql, args)
  else:
    return
  return user[0]

# takes a user object from getuser and adds a transaction to the database
def addtrans(user='', ammount=''):
  sql = '''INSERT INTO transactions VALUES (NULL, ?, ?, ?)'''
  args = (user[0], int(time.time()), ammount)
  return query(sql, args)
