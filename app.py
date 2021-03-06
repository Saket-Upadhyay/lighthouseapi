from flask import Flask, make_response
from flask import request, render_template
import json
from flask import jsonify
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
        print("WAITING FOR USER")
        # print(AppRequest.get('uid'))
        time.sleep(8.0)
        print("== UID STAT == ")
        print(UIDmanager.get('uid'))
        print(UIDmanager.get('active'))
        print("== UID STAT EOS == ")
        if UIDmanager.get('uid') == AppRequest.get('uid'):
            if UIDmanager.get('active') == True:
                return True
        else:
            return False
    else:
        return False



#Update the Android Request to Global Paramaters
def testActivationFunction(activatedata):
    print("==== testActivation Called ====")
    global AppRequest
    global UIDmanager
    if activatedata[0] == 'true' and AppRequest.get('uid') != None:
        print(AppRequest.get('uid'))
        if activatedata[1] in AppRequest.get('uid'):
            tempdict={'active':True,'uid':AppRequest.get('uid')}
            UIDmanager.update(tempdict)
            return "STORED"
        else:
            return "NO REQ"
    else:
        tempdict = {'active':False, 'uid': AppRequest['uid']}
        UIDmanager.update(tempdict)
        return "NO REQ 2"

@app.route('/')
def hello_world():
    global AppRequest
    global UIDmanager
    UIDmanager = {'active': False, 'uid': ''}
    return render_template('index.html')

@app.route('/gui')
def gui():
    global AppRequest
    global UIDmanager
    UIDmanager = {'active': False, 'uid': ''}
    AppRequest = {'uid': ''}
    return render_template('layout.html')

@app.route('/getinit', methods=['GET','POST'])
def getinit():
    global AppRequest
    global UIDmanager
    UIDmanager = {'active': False, 'uid': ''}
    if request.method == 'GET':
        activatedata=[]
        activatedata.append(request.args.get('activate'))
        activatedata.append(request.args.get('uid'))
        print(activatedata)

        return testActivationFunction(activatedata)

    if request.method == 'POST':
        try:
            request_data = request.form.to_dict()
            initCode = request_data['initCode']
            initHash = request_data['inithash']
            userid = request_data['userid']

            print(AppRequest.get('uid'))
            AppRequest.update({'uid': userid})
            print(AppRequest.get('uid'))
            print(initHash)

            DATARET = contactdb(initHash, userid)

            RET={'status': DATARET, 'initcode': int(initCode)}
            response = make_response(
                jsonify(
                    RET
                ),
                200,
            )
            response.headers["Content-Type"] = "application/json"
            return response
        except Exception:
            response = make_response(
                jsonify(
                    {'status': 'ERROR'}
                ),
                200,
            )
            response.headers["Content-Type"] = "application/json"
            return response

    return "OK"


@app.route('/welcome')
def welcome():
    global AppRequest
    global UIDmanager
    UIDmanager = {'active': False, 'uid': ''}
    return render_template('welcome.html')

if __name__ == '__main__':
    app.run(debug=False,host='0.0.0.0', port=5000, threaded=True)
