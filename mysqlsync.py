import MySQLdb
from flask import Flask,render_template,flash,request
from mysqlconn import *

app = Flask(__name__)
app.secret_key='ldx'

my = Mysqldb()
if my.setInfo('172.16.0.56', 'root', 'root'):
    my.getDb()
    my.createDb(['qwe'])
    my.getDb()
    my.closeDb()


@app.route("/",methods=["GET","POST"])
def index():
    if request.method == "POST":
        pass
    return render_template('show_entries.html',entries=[],getdb='F')


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=1238)
    pass
