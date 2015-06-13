#!/usr/bin/python

from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
import sqlite3
from contextlib import closing

DATABASE = 'blog.db'
DRBUT = True
SECRET_KEY = 'pablo'
USERNAME = 'admin'
PASSWORD = 'default'

app = Flask(__name__)
app.config.from_object(__name__)
# app.config.from_envvar('path', silent=True)

def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

def get_data():
    con = connect_db()
    c = con.cursor()
    data = c.execute('select * from blogdb order by id desc')
    data = data.fetchall()
    con.close()
    return data

def put_data(title, text):
    con = connect_db()
    c = con.cursor()
    lastId = c.execute('select max(id) from blogdb')
    Id = lastId.fetchone()
    if Id[-1] is None:
	Id = '1'
    else:
        Id = Id[-1] + 1
    c.execute('insert into blogdb values('+str(Id)+', "'+title+'", "'+text+'")')
    con.commit()
    con.close()

@app.route('/')
def index():
    cur = get_data()
    entries = [dict(title=row[1], text=row[2]) for row in cur]
    return render_template('show_entries.html', entries=entries)

@app.route('/add', methods=['GET'])
def add_entry():
    if request.args.get('title') and request.args.get('text'):
        put_data(request.args.get('title'), request.args.get('text'))    
        content = dict(title=request.args.get("title"), text=request.args.get("text"))
    else:
        content = 'Nic nie dodano'
    return render_template('test_post.html')

@app.route('/del', methods=['GET'])
def del_entry():
    con = connect_db()
    c = con.cursor()
    if request.args.get('id'):
	#maks = c.execute('select max(id) from blogdb')
	#Id = maks.fetchone()[-1]
	Id = str(request.args.get('id'))
	c.execute('delete from blogdb where id = '+Id)
	data = {}
    else:
	data = c.execute('select id, title from blogdb')	
	data = data.fetchall()
	data = [dict(num=d[0], tit=d[1]) for d in data]
    con.commit()
    con.close()
    return render_template('del_entry.html', data=data)   

@app.route('/link')
def link_test():
    return 'LINK'

if __name__ == '__main__':
    app.run(debug=True)
