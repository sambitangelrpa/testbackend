

from mongoengine.document import Document
from mongoengine.fields import EmailField, ImageField, IntField, StringField, UUIDField

# inheriting from Document class
class User(Document):

    meta = {"collection": "User"}

    meta = {"collection": "UserDetails"}

    uuid=UUIDField()
    username=StringField(required=True, max_length=100)
    password=StringField(required=True, max_length=100, default="LOGGEDINWITHGOOGLE")
    picture=StringField(required=True)

    email=EmailField()

    email=EmailField()

class IP_Details(Document):

    meta = {"collection": "IP_Details"}
    IPv4=StringField(required=True, max_length=100)
    country_code=StringField(required=True, max_length=100)
    country_name=StringField(required=True, max_length=100)
    city=StringField( max_length=100)
    postal=StringField(required=True, max_length=100)
    latitude=IntField()
    longitude=IntField()
    state=StringField(required=True, max_length=100)
    search_count=IntField()
    login=IntField()

   
