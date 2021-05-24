# Connection between Flask and MySQL will require to install flask_mysqldb
# 1 indicates failure in processing request / timeout for captcha
# whereas 0 indicates success
# default route of api has been used for registering a new user
# /auth is for authenticating the user and then generating captcha for the registered user
# /check is used for verifying the captcha within time limit (3 mins)
# Stored Procedures and their use has been mentioned in sql files!
# This file will be ready to use with args actually taking the real time inputs and then responding in real time


# EDIT ---->
# 2 routes have been added for extracting details and Authentication
# /details for fetching details given the email_id (userid)
# /auth2 for authentication of user based on userid and hashcode
# /insert to insert the captcha in captcha table

from flask import Flask,render_template,request
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '********'
app.config['MYSQL_DB'] = 'lighthouse'

mysql = MySQL(app)
@app.route('/')
def default_Route():
    cursor = mysql.connection.cursor()
    args=('abc@gmail','!12Abc21!',1)
    cursor.callproc('Create_User',args)
    cursor.execute('SELECT @_Create_User_2')
    dd=cursor.fetchall()
    print(dd[0][0]) # Success=0 Failure=1
    mysql.connection.commit()
    cursor.close()
    return 'Hello World'

@app.route('/details')
def fetch_details():
    cursor = mysql.connection.cursor()
    args = ('abc@gmail','_','_')
    cursor.callproc('extract_details',args)
    cursor.execute('SELECT @_extract_details_1,@_extract_details_2')
    dd = cursor.fetchall() #dd[0][0] is Hash (password) and dd[0][1] is Captcha (initcode)
    print(dd) #dd[0][0]='1' signifies timeout
    return 'extract world'

@app.route('/auth2')
def validate_User():
    cursor = mysql.connection.cursor()
    args = ('abc@gmail','ab234rt',1)
    cursor.callproc('AuthenticateUser2',args)
    cursor.execute('SELECT @_AuthenticateUser2_2')
    dd = cursor.fetchall()
    print(dd) #0=Success 1=Failure
    return 'Auth2 world'

@app.route('/auth')
def authenticate_Generate():
    cursor = mysql.connection.cursor()
    args = ('abc@gmail', 0)
    cursor.callproc('AuthenticateUser', args)
    cursor.execute('SELECT @_AuthenticateUser_1')
    dd = cursor.fetchall()
    # print(dd) device id in dd[0][0] ... 0 indicates no user
    if dd[0][0]:
        cursor.callproc('Generate_Captcha',(dd[0][0],'0000'))
        cursor.execute('SELECT @_Generate_Captcha_1')
        ee=cursor.fetchall()
        print(ee[0][0])
        #ee[0][0] contains captcha
    mysql.connection.commit()
    cursor.close()
    return 'Auth world'

@app.route('/check')
def authenticate_Check():
    cursor = mysql.connection.cursor()
    args = ('abc@gmail','5EFE', 0)
    cursor.callproc('AuthenticateUser', (args[0],args[2]))
    cursor.execute('SELECT @_AuthenticateUser_1')
    dd = cursor.fetchall()
    args1=(dd[0][0],args[1],0)
    cursor.callproc('CptCheck',args1)
    cursor.execute('SELECT @_CptCheck_2')
    dd=cursor.fetchall()
    print(dd[0][0]) # 0 indicates success
    return 'check world'

if __name__ == '__main__':
    app.run(port=7000)
