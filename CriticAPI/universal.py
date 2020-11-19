from django.http import QueryDict
import simplejson as json

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
        return False
    if bab == None or not isinstance(bab,dict):
        return False
    else:
        return bab
