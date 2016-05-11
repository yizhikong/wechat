# -*- coding: utf-8 -*-
import urllib
import urllib2
import lib
from flask import Flask
from flask import g
from flask import render_template
from flask import request
from flask import redirect, url_for

app = Flask(__name__)
app.debug = True

@app.route('/')
def welcome():
    return 'Hello world!'

@app.route('/weiXin', methods = ['GET','POST'])
def reply():
    #return request.args.get('echostr')
    res = lib.xmlParse(request.data)
    return res

@app.route('/img/<name>')
def getimage(name):
    return redirect(url_for('static', filename=name), code=301)

if __name__ == '__main__':
    app.run(host = '0.0.0.0', port=80)
