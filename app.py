from flask import Flask
from flask import request, render_template
app = Flask(__name__)
import json


@app.route('/')
def hello_world():
    return 'LightHouse API : Open Endpoints -> []'


@app.route('/getinit',methods=['POST'])
def getinit():
    if request.method == 'GET':
        activatebool=request.args.get('activate')
        if activatebool == "true":
            # SEND REQUEST TO APP
                print("APP REQ")
        else:
            print("NO REQ")
    if request.method == 'POST':

        try:
            request_data = request.get_json()
            userid = request_data['uid']
            initCode = request_data['initCode']
            initHash = request_data['inithash']
            userid = request_data['userid']
            DATARET = contactsmp(initCode, initHash, userid)

            return json.dumps({'status':'true','DATA':DATARET},indent=4)
        except Exception:
            return json.dumps({'status':'error'},indent=4)

    return "OK"


def contactsmp(initCode,initHash,userid):
    RESULT=""
    # Send request to phone by searching DB for userID
    return RESULT


if __name__ == '__main__':
    app.run()
