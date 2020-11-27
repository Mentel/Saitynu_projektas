from django.http import QueryDict
import simplejson as json
import jwt
from django.conf import settings


def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

def loadJson(jsonData):
    try:
        toReturn = json.loads(jsonData)
    except ValueError as err:
        return None
    return toReturn

def dumpJson(data):
    return json.dumps(data, ensure_ascii=False).encode('utf8')

def getText(incomingData):
    data = QueryDict(incomingData) 
    if len(data) == 0:
        return False
    for x in data:
        bab = x
    bab = loadJson(bab)
    if bab == "empty":
        return [False, ""]
    elif bab == None or not isinstance(bab,dict):
        return [False, bab]
    else:
        return [True, bab]

def decode_token(auth):
    success = True
    result = ""
    token = auth.split()
    if len(token) == 2:
        if token[0] == "Bearer":
            try:
                result = jwt.decode(token[1], settings.SECRET_KEY, algorithms='HS256')
                result["scope"] = result["scope"].split()
            except jwt.exceptions.DecodeError:
                success = False
                result = "wrong_input"
            except jwt.ExpiredSignatureError:
                success = False
                result = "expired"
    else:
        success = False
        result = "wrong_input"
    return [success, result]

def getRedirect_uri():
    return "https://gamecritic.azurewebsites.net/"

def get_admin_scopes():
    return ["2"]

def get_user_scopes():
    return ["1"]