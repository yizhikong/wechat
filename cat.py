import hashlib
import json
import lib
from flask import Flask
from flask import g
from flask import render_template
from flask import request

app = Flask(__name__)
app.debug = True

@app.route('/')
def welcome():
	return 'hello, world!'

@app.route('/translation', methods=['GET', 'POST'])
def translation():
    ans = ''
    if request.method == 'POST':
        req = request.form['req']
        ans = ans + lib.translation(req)
    return render_template('translation.html', ans = ans)

@app.route('/weiXin', methods = ['GET','POST'])
def reply():
    res = lib.xmlParse(request.data)
    return res
    signature = request.args.get('signature', '')
    timestamp = request.args.get('timestamp', '')
    echostr = request.args.get('echostr', '')
    token = 'Your_token'
    message = [token, timestamp, echostr]
    message.sort()
    sha1 = hashlib.sha1()
    sha1.update(message[0] + message[1] + message[2])
    value = sha1.hexdigest()
    if value == signature:
        res = lib.xmlParse(request.data)
        return res
