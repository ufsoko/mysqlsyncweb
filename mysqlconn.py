import MySQLdb
class Mysqldb():
    def __init__(self):
        self.db = None
        self.isInit = False
        self.saveD = {}

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