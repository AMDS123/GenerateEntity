#coding:utf-8
'''
Created on 2014/4/11

@author: zhuxinxin
'''

import sqlite3
import time

# "/Users/zhuxinxin/Desktop/drm.sqlite"
#  /Users/zhuxinxin/Desktop/

prefix = "SZ"
path = "/Users/zhuxinxin/Desktop/DRM/"

def initSqlite(path):
    conn = sqlite3.connect(path)
    return conn.cursor()

def getAllTables(cur):
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")    
    return cur.fetchall()

def getAllColumns1(cur,table):
    cur.execute("PRAGMA table_info(" + table + ")")
    return cur.fetchall()

def getAllColumns2(cur,table):
    sql = "select * from " + table
    cur.execute(sql)
    return [tuple[0] for tuple in cur.description]


def writeColumns(name,columns):
    
    fileH = prefix + name + ".h"
    fileM = prefix + name + ".m"
    
    pathH = path + fileH
    pathM = path + fileM
    
    # 写头文件
    fileHandle = open(pathH,'w')
    fileHandle.write(getHeader(fileH))
    
    strImport = "#import \"SZBase.h\"\n\n\n"
    fileHandle.write(strImport)
    
    strInterface = "@interface %s : SZBase\n\n\n" % name
    fileHandle.write(strInterface)
    
    for column in columns:
        
        strName = column[1].lower()
        strType = column[2]
        
        if strType == "VARCHAR":
            strElement = "@property (nonatomic,strong) NSString * %s;\n\n" % strName
        elif strType == "DOUBLE" or strType == "FLOAT":
            strElement = "@property (nonatomic,strong) NSNumber * %s;\n\n" % strName

        fileHandle.write(strElement)
        
        
    strEnd = "\n@end"
    fileHandle.write(strEnd)
    
    
    fileHandle.close()
    
    
    # 写源文件
    fileHandle = open(pathM,'w')
    
    fileHandle.write(getHeader(fileM))
    
    strImport = "#import \"%s\"\n\n\n" % fileH
    fileHandle.write(strImport)
    
    
    strImplementation = "@implementation %s\n" % name
    fileHandle.write(strImplementation)
    
    strEnd = "\n@end"
    fileHandle.write(strEnd)
    
    fileHandle.close()
    
    
    
def getHeader(filename):
    return "//\n" + \
    "// %s\n" % filename + \
    "//\n" + \
    "// Created by AMDS on %s.\n" % time.strftime("%Y-%m-%d") + \
    "// Copyright (c) 2014 AMDS. All rights reserved.\n" + \
    "//\n\n\n"
    
def writeTable(table,cur):
    columns = getAllColumns1(cur,table)
    writeColumns(table.capitalize(),columns)
    
    
def writeDatabase():
    cur = initSqlite("/Users/zhuxinxin/Desktop/drm.sqlite")
    tables = getAllTables(cur)
    index = 0
    for table in tables:
        tableName =  table[0]
        writeTable(tableName,cur)
        print "---> %03d %s" % (index,tableName)
        index = index + 1
    

if __name__ == "__main__":
    
    
#     cur = initSqlite("/Users/zhuxinxin/Desktop/drm.sqlite")
#     table = "ACCOUNT"
#     columns = getAllColumns1(cur,table)
#     parseColumns(table,columns)

    #print "hello %s" % "amds"
    
    #cur = initSqlite("/Users/zhuxinxin/Desktop/drm.sqlite")
    #writeTable("ACCOUNT",cur)
    
    writeDatabase()

    
    

