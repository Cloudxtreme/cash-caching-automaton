#!/usr/bin/python
from cash_api import *

user = getuser(username="machine") 
receiver = ['tyler.crumpton@gmail.com', 'nathan@frcv.net']

sql = '''select u.username, t.usd from users as u join transactions t on u.id=t.users_id where ( t.users_id != 1 OR t.usd > 0 ) and t.timestamp > strftime('%s','now','-1 day')'''
args = ()
ret = query(sql, args)

message = "From: CasCA <CasCA@makerslocal.org>\nTo: %s\nSubject: CasCA Balance $%.2f\n\nDear admin, \n\nI currently have a balance of $%.2f. I made %d transactions today.  They are listed below.\n\n" %(', '.join(receiver), round(user[3],2), round(user[3],2), len(ret))

message = message + "{0:>16s}{1:>16s}\n".format("User Name","Transaction")
message = message + "{0:>16s}{1:>16s}\n".format("---------","--------")
for trans in ret:
  message = message + "{0:>16s}{1:>16s}\n".format(str(trans['username']),str(trans['usd']))

sendemail( sender='cashmachine@makerslocal.org', receiver=receiver, message=message)
