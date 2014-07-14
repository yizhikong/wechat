# -*- coding: utf-8 -*-
import urllib
import urllib2
import lib
from flask import Flask
from flask import g
from flask import render_template
from flask import request

app = Flask(__name__)
app.debug = True

@app.route('/')
def welcome():
    return 'Hello world!'

@app.route('/weiXin', methods = ['GET','POST'])
def reply():
    # return request.args.get('echostr')
    res = lib.xmlParse(request.data)
    return res
