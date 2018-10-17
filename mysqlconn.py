import MySQLdb
import json
import os
class Mysqldb():
    def __init__(self):
        self.db = None
        self.isInit = False
        self.saveD = {}
        self.jsonC = JsonFile("./bin/config")

    def setInfo(self,hostdb,userdb,passwddb,portdb=3306):
        if self.db:
            self.closeDb()
        try:
            self.db = MySQLdb.connect(host=hostdb,port=portdb,user=userdb,passwd=passwddb)
        except Exception as e:
            print "connect seeor"
            print e
            return False
        self.isInit = True
        self.initCur()
        return True

    def initCur(self):
        self.cursor = self.db.cursor()

    def closeDb(self):
        self.db.close()
        self.cursor.close()
        self.db = None
        self.isInit = False

    def getDb(self):
        if not self.isInit:
            print "Not set info!"
            return False
        sql = "show databases;"
        self.cursor.execute(sql)
        dblist =[db[0] for db in self.cursor.fetchall() if db[0] != 'information_schema' and db[0] != 'test' and db[0] != 'performance_schema' and db[0] != 'mysql' ]
        return dblist

    def createDb(self,dblist):
        for db in dblist:
            sql = "create database "+str(db)+";"
            self.cursor.execute(sql)

    def setData(self,k,v):
        for d in v:
            if d == '':
                return False
        self.saveD[k]=v
        return True

    def getData(self,k):
        if k in self.saveD.keys():
            return self.saveD[k]
        return None

class JsonFile():
    def __init__(self,file):
        self.bestjson = json.load(open(file,"r"))
        self.jsonfile = []

    def createJson(self,sourceinfo,destinfo,dbname):
        self.bestjson['source'] = str(sourceinfo[1])+":"+str(sourceinfo[2])+"@("+str(sourceinfo[0])+":"+str(sourceinfo[3])+")/"+str(dbname)
        self.bestjson['dest'] = str(destinfo[1]) + ":" + str(destinfo[2]) + "@(" + str(destinfo[0]) + ":" + str(destinfo[3]) + ")/" + str(dbname)
        file = './bin/'+ str(destinfo[0]) + '_'+ dbname+'-config.json'
        self.jsonfile.append(file)
        json.dump(self.bestjson, open(file, 'w'))

    def cleanJson(self):
        filelist = os.listdir('./bin/')
        for f in filelist:
            if 'json' in f.split('.',1):
                self.jsonfile.append('./bin/'+f)
        self.deleteJson()

    def getjsonFile(self):
        return self.jsonfile

    def deleteJson(self):
        for f in self.jsonfile:
            print "del"+f
            os.remove(f)
        self.jsonfile = []