#!/usr/bin/env python
# -*- coding: utf-8 -*-

import MySQLdb
from netmon_env import envi
from my_log import logger
from my_crypt import mycrypt

#### database setting
_HOST = envi['db_host']
_PORT = envi['db_port']
_USER = envi['db_usr']
_PWD  = envi['db_pwd']
_DB   = envi['db_name']
#_CHAR = envi['db_char']
_CHAR = 'utf8'

### get data from DB
def xgetall(sql):
   ret = ()
   try:
      db = MySQLdb.connect(host=_HOST,user=_USER,passwd=_PWD,
          db=_DB,charset=_CHAR)
   except MySQLdb.Error,e:
      logger.error(str(e))
   else:
      try:
         cur = db.cursor()
         cur.execute(sql)
         ret = cur.fetchall()
      except MySQLdb.Error,e:
         logger.error(str(e))
      cur.close()
      db.close()
   return ret


### get data from DB
def xgetone(sql):
   ret = ()
   try:
      db = MySQLdb.connect(host=_HOST,user=_USER,passwd=_PWD,
          db=_DB,charset=_CHAR)
   except MySQLdb.Error,e:
      logger.error(str(e))
   else:
      try:
         cur = db.cursor()
         cur.execute(sql)
         ret = cur.fetchone()
      except MySQLdb.Error,e:
         logger.error(str(e))
      cur.close()
      db.close()
   return ret



### 'CRUD' for DB
def xq(sql):
   ret = False
   try:
      db = MySQLdb.connect(host=_HOST,user=_USER,passwd=_PWD,
          db=_DB,charset=_CHAR)
   except MySQLdb.Error,e:
      logger.error(str(e))
   else:
      try:
         cur = db.cursor()
         cur.execute(sql)
         db.commit()
         ret = True
      except MySQLdb.Error,e:
         logger.error(str(e))
         db.rollback()
      cur.close()
      db.close()
   return ret

### batch updates for DB
def mupdate(list1, list2):
   ret = False
   try:
      db = MySQLdb.connect(host=_HOST,user=_USER,passwd=_PWD,
          db=_DB,charset=_CHAR)
   except MySQLdb.Error,e:
      logger.error(str(e))
   else:
      try:
         cur = db.cursor()
         for i in range(len(list1)):
            sql="update target set rtt=%d where tdes='%s'" % (list2[i],list1[i])
            cur.execute(sql)
         db.commit()
         ret = True
      except MySQLdb.Error,e:
         logger.error(str(e))
         db.rollback()
      cur.close()
      db.close()
   return ret

### batch encode password field for DB
def db_encode():
   ret = False
   list1 = xgetall('select rip, pass1, pass2, pass3 from router;')
   try:
      db = MySQLdb.connect(host=_HOST,user=_USER,passwd=_PWD,
          db=_DB,charset=_CHAR)
   except MySQLdb.Error,e:
      logger.error(str(e))
   else:
      try:
         cur = db.cursor()
         for i in range(len(list1)):
            p1 = mycrypt.encrypt(list1[i][1])
            p2 = mycrypt.encrypt(list1[i][2])
            p3 = mycrypt.encrypt(list1[i][3])
            sql="update router set pass1='%s',pass2='%s',pass3='%s' where rip='%s'" % (p1, p2, p3, list1[i][0])
            cur.execute(sql)
         db.commit()
         ret = True
      except MySQLdb.Error,e:
         logger.error(str(e))
         db.rollback()
      cur.close()
      db.close()
   return ret

if __name__ == '__main__':
   sql1 = "select * from city"
   sql2 = "insert into city (city) value ('NewYork')"
   xq(sql2)
   print xgetone(sql1),"\n-----------\n\n"
   print xgetall(sql1)
   #print envi
   #logger.debug('debug message')
   #logger.info('info message')
   #logger.warn('warn message')
   #logger.error('error message')
