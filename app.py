
import json
from flask import Flask,jsonify,send_file
from flask.wrappers import Response
from flask.globals import request, session
import requests
from dotenv import load_dotenv
from werkzeug.exceptions import abort
from werkzeug.utils import redirect
import google
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
import os, pathlib
from functools import wraps
from connect_db import connect_db, insert_into_UserDeatils_db,insert_into_IP_Details_db,update_into_IP_Details_db,find_ip_details
import jwt
from flask_cors import CORS
from all_scraping_data import main_output
from config_reader import ConfigReader
import datetime
from datetime import timedelta


config_reader = ConfigReader()
configuration = config_reader.read_config()
app = Flask(__name__)

CORS(app)
app.config['Access-Control-Allow-Origin'] = '*'
app.config["Access-Control-Allow-Headers"]="Content-Type"
app.config['SECRET_KEY'] = configuration["SECRET_KEY"]
# bypass http
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

GOOGLE_CLIENT_ID = configuration["GOOGLE_CLIENT_ID"]
client_secrets_file = os.path.join(pathlib.Path(__file__).parent, "client_secret.json")
algorithm = configuration["ALGORITHM"]
BACKEND_URL=configuration["BACKEND_URL"]
FRONTEND_URL=configuration["FRONTEND_URL"]
print('BACKEND_URL',BACKEND_URL)
#database connection
connect_db()

flow = Flow.from_client_secrets_file(
    client_secrets_file=client_secrets_file,
    scopes=[
        "https://www.googleapis.com/auth/userinfo.profile",
        "https://www.googleapis.com/auth/userinfo.email",
        "openid",
    ],
    redirect_uri=BACKEND_URL+"/callback",
)


# wrapper
def login_required(function):
    def wrapper(*args, **kwargs):
        
        encoded_jwt=request.headers.get("Authorization").split("Bearer ")[1]
        if encoded_jwt==None:
            return abort(401)
        else:
            return function()
    wrapper.__name__ = function.__name__
    return wrapper

def Generate_JWT(payload):
    encoded_jwt = jwt.encode(payload, app.secret_key,algorithm=algorithm,)
    return encoded_jwt




@app.route("/api/generate_token",methods=["POST"])
def token():
    payload=request.get_json()
    now=datetime.datetime.utcnow()
    payload['exp']=(now+timedelta(hours=24)).timestamp()
    jwt_token=Generate_JWT(payload)
    insert_into_UserDeatils_db(
        payload['name'],
        payload['email'],
        payload['picture']
    )
    
    return Response(
        response=json.dumps({'token':jwt_token}),
        status=200,
        mimetype='application/json'
    )



@app.route("/")
@login_required

def home_page_user():
    # print('i am in home')
    # print(request.headers.get("Authorization").split("Bearer ")[1])
    encoded_jwt=request.headers.get("Authorization").split("Bearer ")[1]
    try:
        decoded_jwt=jwt.decode(encoded_jwt, app.secret_key,algorithms=algorithm)
        print(decoded_jwt)
    except Exception as e: 
        return Response(
            response=json.dumps({"message":"Decoding JWT Failed", "exception":e.args}),
            status=500,
            mimetype='application/json'
        )
    return Response(
        response=json.dumps(decoded_jwt),
        status=200,
        mimetype='application/json'
    )

@app.route("/api/getResult_outside",methods=['POST'])
def ip_count():
    
    # print("get result", request.get_json())
    payloadData = request.get_json()
    keyword = payloadData["keyword"]
    country = payloadData["country"]
    region =payloadData["region"]
    # data = payloadData["data"]
    gl_record={'united states':"us",'india':"in",'united kingdom':"uk"}
    gl=gl_record[country.lower()]
    
    if payloadData["region"]=="":

        location=payloadData["country"]
    else:
        location = region

    


       

    # jwt_token=Generate_JWT(data)
    
    result=main_output(keyword,location,gl)
    


    # update_into_IP_Details_db(data['IPv4'])

    return Response(
        response=json.dumps({"result":result}),
        status=202,
        mimetype='application/json'
    )

# @app.route("/api/find_ip_count",methods=['POST'])
# def find_ip_count():
#     #clear the local storage from frontend

   
#     # print("get login ", request.get_json())
#     data=request.get_json()

#     ip_data=find_ip_details(data['IPv4'])
#     print('ip data:',ip_data)
#     return Response(
#         response=json.dumps({'result':ip_data}),
#         status=202,
#         mimetype='application/json'
#     )

@app.route('/get_csv')
def get_csv():
    """ 
    Returns the monthly weather csv file (Montreal, year=2019)
    corresponding to the month passed as parameter.
    """
    # Checking that the month parameter has been supplied
    # if not "month" in request.args:
    #     return "ERROR: value for 'month' is missing"
    # # Also make sure that the value provided is numeric
    # try:
    #     month = int(request.args["month"])
    # except:
    #     return "ERROR: value for 'month' should be between 1 and 12"
    csv_dir  = ".\static_files"
    csv_file = "test.csv"
    csv_path = os.path.join(csv_dir, csv_file)
    print(csv_path)
    
    # Also make sure the requested csv file does exist
    if not os.path.isfile(csv_path):
        return "ERROR: file %s was not found on the server" % csv_file
    # Send the file back to the client
    return send_file(csv_path, mimetype='text/csv',as_attachment=True, download_name=csv_file)



@app.route("/api/getResult",methods=['POST'])
@login_required

def result_data():
    
    
    payloadData = request.get_json()
    keyword = payloadData["keyword"]
    country = payloadData["country"]
    region =payloadData["region"]
    # data = payloadData["data"]
    
    if payloadData["region"]=="":


        location=payloadData["country"]
    else:
        location = region+","+country

    result=main_output(keyword,location)
            
    return Response(
        response=json.dumps({"result":result}),
        status=200,
        mimetype='application/json'
    )


if __name__ == "__main__":

    app.run()   
    


