# -*- coding: cp936 -*-
#import sqlite3
import time
import MySQLdb
import sae.const

con = MySQLdb.connect(host = sae.const.MYSQL_HOST, user = sae.const.MYSQL_USER, 
                      passwd = sae.const.MYSQL_PASS, port = int(sae.const.MYSQL_PORT),
                      db = sae.const.MYSQL_DB)
curs = con.cursor()

def createTable(username):
    con = MySQLdb.connect(host = sae.const.MYSQL_HOST, user = sae.const.MYSQL_USER, 
                      passwd = sae.const.MYSQL_PASS, port = int(sae.const.MYSQL_PORT),
                      db = sae.const.MYSQL_DB)
    curs = con.cursor()
    curs.execute('''CREATE TABLE IF NOT EXISTS %s (
            value CHAR(40) PRIMARY KEY,
            date CHAR(40)
            )''' % username)
    con.commit()
    con.close()

def dropTable(username):
    curs.execute("DROP TABLE IF EXISTS " + username)
    con.commit()
    
def insertWord(username, word):
    con = MySQLdb.connect(host = sae.const.MYSQL_HOST, user = sae.const.MYSQL_USER, 
                      passwd = sae.const.MYSQL_PASS, port = int(sae.const.MYSQL_PORT),
                      db = sae.const.MYSQL_DB)
    curs = con.cursor()
    if checkWord(username, word) is True:
        return
    date = time.strftime("%Y%m%d",time.localtime())
    command = "INSERT INTO %s(value, date) VALUES('%s', '%s')" % (username, word, date)
    curs.execute(command)
    con.commit()
    con.close()

def checkWord(username, word):
    con = MySQLdb.connect(host = sae.const.MYSQL_HOST, user = sae.const.MYSQL_USER, 
                      passwd = sae.const.MYSQL_PASS, port = int(sae.const.MYSQL_PORT),
                      db = sae.const.MYSQL_DB)
    curs = con.cursor()
    try:
        command = "SELECT * FROM %s WHERE value='%s'" % (username, word)
        curs.execute(command)
    except:
        createTable(username)
        return False
    if curs.fetchone() is None:
        con.close()
        return False
    con.close()
    return True

def listWords(username):
    con = MySQLdb.connect(host = sae.const.MYSQL_HOST, user = sae.const.MYSQL_USER, 
                      passwd = sae.const.MYSQL_PASS, port = int(sae.const.MYSQL_PORT),
                      db = sae.const.MYSQL_DB)
    curs = con.cursor()
    res = []
    try:
        command = "SELECT * FROM %s ORDER BY date" % username
        curs.execute(command)
        wordList = curs.fetchall()
        for u, v in wordList:
            res.append(u)
    except:
        createTable(username)
    con.close()
    return res

