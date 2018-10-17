import MySQLdb
from flask import Flask,render_template,flash,request,redirect,url_for
from mysqlconn import *

app = Flask(__name__)
app.secret_key='ldx'

my = Mysqldb()
# if my.setInfo('172.16.0.56', 'root', 'root'):
#     my.getDb()
#     my.createDb(['qwe'])
#     my.getDb()
#     my.closeDb()

def createDb(info,dblist):
    if my.setInfo(info[0], info[1], info[2],int(info[3])):
        my.createDb(dblist)
        my.closeDb()
        return True
    else:
        return False

@app.route('/sync',methods=["GET","POST"])
def sync():
    if request.method == "POST":
        uids = request.form.getlist('uids',None)
        print uids
        if not uids:
            flash("Not choose db")
            return redirect(url_for("index"))
        desdb = my.getData('desdb')
        credb = []
        for db in uids:
            if db not in desdb:
                credb.append(db)
        if not credb:
            flash("not choose database!")
            return render_template('show_entries.html', sourcedb=my.getData('srcdb'), destdb=my.getData('desdb'), sourceinp=my.getData('src'),destinp=my.getData('des'), getdb='F')

        print "credb",credb
        if createDb(my.getData('des'),credb):
            flash("create sesscu")

        return render_template('show_entries.html', sourcedb=[], destdb=[], sourceinp=my.getData('src'),destinp=my.getData('des'), getdb='F')
    return redirect(url_for("index"))


def connDb(info):
    if my.setInfo(info[0], info[1], info[2],int(info[3])):
        data = my.getDb()
        my.closeDb()
        return data
    else:
        return []

@app.route("/",methods=["GET","POST"])
def index():
    if request.method == "POST":
        srsip = request.form['srsip']
        srcuser = request.form['srcuser']
        srcpass = request.form['srcpass']
        srcport = request.form['srcport']
        desip = request.form['desip']
        desuser = request.form['desuser']
        despass = request.form['despass']
        desport = request.form['desport']
        if not (my.setData('src', [srsip, srcuser, srcpass, srcport]) and my.setData('des', [desip, desuser, despass, desport])):
            flash("Input Data")
            return render_template('show_entries.html', sourceinp=[srsip, srcuser, srcpass, srcport], destinp=[desip, desuser, despass, desport], getdb='F')
        else:
            source = connDb(my.getData('src'))
            my.setData('srcdb',source)
            dest = connDb(my.getData('des'))
            my.setData('desdb',dest)
            return render_template('show_entries.html',sourcedb=source,destdb=dest,sourceinp=my.getData('src'),destinp=my.getData('des'),getdb='N')
    return render_template('show_entries.html',getdb='F')

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=1231)
    pass
