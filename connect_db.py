
# from dotenv import load_dotenv
from mongoengine import connect

from models import User

from models import User,IP_Details

import uuid
import os
from config_reader import ConfigReader

def connect_db():
    try:
        config_reader = ConfigReader()
        configuration = config_reader.read_config()
        connect(host=configuration['CLUSTER_URL'])
        print("Database cluster connected")

        return  connect(host=configuration['CLUSTER_URL'])


    except Exception as e:
        print(e.args)




def insert_into_UserDeatils_db(username, email, picture):
    try:
        try:
            user = User.objects.get(email=email)

            print({"_id": str(user["id"]), "message": "User already exists"})
        except:
            new_user = User(
                username=username, 
                uuid=uuid.uuid4().hex,
                email=email,
                picture=picture
            )
            new_user.save()
            print({"_id": str(new_user["id"]), "message": "User created"})
    except Exception as e:

        print({"error": e.args})

        print({"error": e.args})

def insert_into_IP_Details_db(country_code, country_name,city, postal,latitude,longitude,IPv4,state,search_count,login):
    try:
        try:
            IP_etails = IP_Details.objects.get(IPv4=IPv4)
            print({"_id": str(IP_etails["id"]), "message": "IP User already exists"})
        except:
            new_user = IP_Details(
                IPv4=IPv4, 
                country_code=country_code,
                country_name=country_name,
                city=city,
                postal=postal,
                latitude=latitude,
                longitude=longitude,
                state=state,
                search_count=search_count,
                login=login
            )
            new_user.save()
            print({"_id": str(new_user["id"]), "message": "IP_User created"})
    except Exception as e:
        print({"error": e.args})

    
def update_into_IP_Details_db(IPv4):
    conn=connect_db()
    db=conn.test
    collection=db.IP_Details
    ip_data=collection.find_one({'IPv4':IPv4})
    collection.update_one({"IPv4":IPv4},{"$set":{"search_count":ip_data['search_count']+1}})

def find_ip_details(IPv4):

    conn=connect_db()
    db=conn.test
    collection=db.IP_Details
    try:
        ip_data=collection.find_one({'IPv4':IPv4})
        
        if ip_data:
            ip_data['_id']=str(ip_data['_id'])
            return ip_data
        else:
            return str("IP does not exist in DB")
    except Exception as e:
        return e
    
    
    
