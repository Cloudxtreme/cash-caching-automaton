#!/usr/bin/python
import sqlite3
import ldap
import os
import sys
import datetime
import time
import pprint
import smtplib

DB = 'cash_db'
# connect to database located in current directory
def dbconnect():
  pathname = os.path.dirname(sys.argv[0])
  dbfile = os.path.abspath(pathname)+'/'+DB
  con = sqlite3.connect(dbfile)
  con.row_factory = sqlite3.Row
  return con

# Run the query and return all if it is a select, or lastrowid if it is insert
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

# return an array with id, username, email, uid, and balance
def getuser(userid='', username='', email=''):
  if userid:
    sql = '''SELECT a.*, SUM(b.usd) FROM users a LEFT JOIN transactions b ON b.users_id = a.id WHERE a.id = ?'''
    args = (userid,)
    user =  query(sql, args)
  elif username:
    sql = '''SELECT a.*, SUM(b.usd) FROM users a LEFT JOIN transactions b ON b.users_id = a.id WHERE a.username = ?'''
    args = (username,)
    user =  query(sql, args)
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

def getuserfromldap(usbsn='', username='', email=''):
  user = {}
  try:
    ld = ldap.initialize('ldap://10.56.0.8')
    basedn = "dc=makerslocal,dc=org"
    ld.simple_bind_s()
  except:
    return
  if usbsn:
    ldapfilter = "usbSerial="+usbsn
  elif username:
    ldapfilter = "uid="+username
  elif email:
    ldapfilter = "zimbraPrefMailForwardingAddress="+email
  results = ld.search_s(basedn,ldap.SCOPE_SUBTREE,ldapfilter)
  if len(results) != 1:
    return
  pprint.pprint(results)
  user['usbsn'] = results[0][1]['usbSerial'][0]
  user['username'] = results[0][1]['uid'][0]
  user['email'] = results[0][1]['zimbraPrefMailForwardingAddress'][0]
  user['givenName'] = results[0][1]['givenName'][-1]
  ld.unbind()
  return user

def sendemail(sender='', receiver='', message=''):
  try:
    smtpObj = smtplib.SMTP('10.56.0.4')
    smtpObj.sendmail(sender, receiver, message)
  except:
    return
