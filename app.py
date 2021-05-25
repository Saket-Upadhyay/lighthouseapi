from flask import Flask
from flask import request, render_template
import json
import time
import csv
app = Flask(__name__)

global AppRequest
global UIDmanager
UIDmanager={'active':False,'uid':''}
AppRequest={'uid':None}


def contactdb(initHash, userid):
    global AppRequest
    global UIDmanager
    setvaliduser=False
    # check userid in database
    with open('DB/data.csv','r') as datsv:
        csvr=csv.reader(datsv,delimiter=',')
        line_count=0
        for row in csvr:
            if row[0] == userid and row[1] == initHash:
                setvaliduser=True
            else:
                setvaliduser=False

    #set uid activated to True
    if setvaliduser:
        AppRequest.update({'uid':userid})
        # Send request to phone by searching DB for userID
        time.sleep(4.0)
        if UIDmanager.get('uid') == AppRequest.get('uid'):
            if UIDmanager.get('active') == True:
                return True
        else:
            return False
    else:
        return False



#Update the Android Request to Global Paramaters
def testActivationFunction(activatedata):
    global AppRequest
    global UIDmanager
    if "true" in activatedata:
        if activatedata in AppRequest.get('uid'):
            tempdict={'active':True,'uid':AppRequest.get('uid')}
            UIDmanager.update(tempdict)
            return "STORED"
        else:
            return "NO REQ"
    else:
        tempdict = {'active':False, 'uid': AppRequest['uid']}
        UIDmanager.update(tempdict)
        return "NO REQ"

@app.route('/')
def hello_world():
    return 'LightHouse API : Open Endpoints -> [<strong>/getinit</strong> (POST and GET)]'

@app.route('/getinit', methods=['GET','POST'])
def getinit():
    global AppRequest
    global UIDmanager
    UIDmanager = {'active': False, 'uid': ''}
    AppRequest = {'uid': ''}
    if request.method == 'GET':
        activatedata = request.args.get('activate')

        return testActivationFunction(activatedata)

    if request.method == 'POST':

        try:
            request_data = request.form.to_dict()
            initCode = request_data['initCode']
            initHash = request_data['inithash']
            userid = request_data['userid']
            DATARET = contactdb(initHash, userid)

            return json.dumps({'status': DATARET, 'initcode': initCode}, indent=4)
        except Exception:
            return json.dumps({'status': 'ERROR'}, indent=4)

    return "OK"




if __name__ == '__main__':
    app.run()
