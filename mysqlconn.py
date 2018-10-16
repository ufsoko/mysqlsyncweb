import MySQLdb
class Mysqldb():
    def __init__(self):
        self.db = None
        self.isInit = False

    def setInfo(self,hostdb,userdb,passwddb,portdb=3306):
        if self.db:
            self.closeDb()
        self.isInit = True
        try:
            self.db = MySQLdb.connect(host=hostdb,port=portdb,user=userdb,passwd=passwddb)
        except:
            print "connect seeor"
            return False
        self.initCur()
        return True

    def initCur(self):
        self.cursor = self.db.cursor()

    def closeDb(self):
        self.db.close()
        self.cursor.close()
        self.db = None
    def getDb(self):
        if not self.isInit:
            print "Not set info!"
        sql = "show databases;"
        self.cursor.execute(sql)
        dblist =[db[0] for db in self.cursor.fetchall() if db[0] != 'information_schema' and db[0] != 'test' and db[0] != 'performance_schema' and db[0] != 'mysql' ]
        print dblist

    def createDb(self,dblist):
        for db in dblist:
            sql = "create database "+str(db)+";"
            self.cursor.execute(sql)
