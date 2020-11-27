from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import connection, transaction, IntegrityError
from CriticAPI import universal
import jwt
import simplejson as json
from django.shortcuts import render
from django.conf import settings
from django.core import serializers
from pathlib import Path
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime, timedelta
from django.contrib.auth.hashers import make_password, check_password

@csrf_exempt
def API1(request):
    if (request.method == 'GET'):
        return getList(request)
    elif (request.method == 'POST'):
        return create(request)
    else:
        return HttpResponse(status = 404)


@csrf_exempt
def API2(request, index1):
    if (request.method == 'PUT'):
        return update(request, index1)
    elif (request.method == 'GET'):
        return getUser(request, index1)
    elif (request.method == 'DELETE'):
        return delete(request, index1)
    else:
        return HttpResponse(status = 404)

@csrf_exempt
def API3(request):  
    if (request.method == 'POST'):
        return getToken(request)
    else:
        return HttpResponse(status = 404)


def getUser(request, index1):
    statusCode = 200
    result = "bad"
    content_type = None

    if "Authorization" in request.headers:
        auth = universal.decode_token(request.headers["Authorization"])
        if auth[0] == False:
            return HttpResponse (result, content_type, 401)
    else:
        return HttpResponse (result, content_type, 401)

    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM public.user WHERE id = %s", [index1])
        row = universal.dictfetchall(cursor)
    result = universal.dumpJson(row)      
    return HttpResponse (result, status = statusCode, content_type = "application/json")

def getList(request):
    statusCode = 200
    result = "bad"
    content_type = None

    if "Authorization" in request.headers:
        auth = universal.decode_token(request.headers["Authorization"])
        if auth[0] == False:
            return HttpResponse (result, content_type, 401)
    else:
        return HttpResponse (result, content_type, 401)

    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM public.user")
        row = universal.dictfetchall(cursor)
    result = universal.dumpJson(row)  
    return HttpResponse (result, status = statusCode, content_type = "application/json")

def create(request):
    statusCode = 200
    result = "bad"
    content_type = None

    if "Authorization" in request.headers:
        auth = universal.decode_token(request.headers["Authorization"])
        if auth[0] == False:
            return HttpResponse (result, content_type, 401)
    else:
        return HttpResponse (result, content_type, 401)  

    input = universal.getText(request.body)
    body = input[1]
    if input[0] == False:
        return HttpResponse ("ErrorA", status = 400)
    if "username" not in body:
        return HttpResponse ("ErrorB", status = 400)

    scope = request.headers["scope"]
    scope = int(scope)
    if scope != 2:
        return HttpResponse("Not admin" + scope, content_type, 403)         
    statusCode = 201
    hashedPass = make_password(body["password"])  
    with connection.cursor() as cursor:
        cursor.execute("INSERT INTO public.user(username, password, role) VALUES (%s, %s, %s) RETURNING id, username", [body["username"], hashedPass, body["role"]])
        returnedId = universal.dictfetchall(cursor)
    result = universal.dumpJson(returnedId)
    return HttpResponse (result, status = statusCode, content_type = "application/json")

def update(request, index1):
    statusCode = 200
    result = "bad"
    content_type = None

    if "Authorization" in request.headers:
        auth = universal.decode_token(request.headers["Authorization"])
        if auth[0] == False:
            return HttpResponse (result, content_type, 401)
    else:
        return HttpResponse (result, content_type, 401)   

    input = universal.getText(request.body)
    body = input[1]
    if input == False:
        return HttpResponse ("ErrorA", status = 400)
    if "username" not in body:
        return HttpResponse ("ErrorB", status = 400)      
    statusCode = 200
    result = "bad"
    content_type = None

    if "Authorization" in request.headers:
        auth = universal.decode_token(request.headers["Authorization"])
        if auth[0] == False:
            return HttpResponse (result, content_type, 401)
    else:
        return HttpResponse (result, content_type, 401)   

    hashedPass = make_password(body["password"])

    with connection.cursor() as cursor:
        cursor.execute("UPDATE public.user SET username = %s, password = %s, role = %s WHERE id = %s", [body["username"], hashedPass, body["role"], index1])
    result = "Vartotojas atnaujintas"
    return HttpResponse(result, status = statusCode)

def delete(request, index1):
    statusCode = 200
    result = "bad"
    content_type = None

    if "Authorization" in request.headers:
        auth = universal.decode_token(request.headers["Authorization"])
        if auth[0] == False:
            result = "Unauthorized"
            return HttpResponse (result, content_type, 401)
    else:
        result = "No token"
        return HttpResponse (result, content_type, 401)   

    scope = request.headers["scope"]
    scope = int(scope)
    if scope != 2:
        return HttpResponse("Not admin" + scope, content_type, 403)        

    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM public.review WHERE user_id = %s", [index1])
        row = universal.dictfetchall(cursor)
        if len(row) >= 1:
            return HttpResponse("Sis vartotojas turi apzvalgu.", status = 409)
        cursor.execute("SELEcT * FROM public.user WHERE id = %s", [index1])
        row = universal.dictfetchall(cursor)
        if len(row) == 0:
            return HttpResponse("Vartotjas neegzistuoja.", status = 410)
        cursor.execute("DELETE FROM public.user WHERE id = %s", [index1])        
    return HttpResponse(status = statusCode)

def getToken(request):
    result = ""
    content_type = None
    statusCode = 200 #401
    if "client-id" in request.headers and "redirect-uri" in request.headers and "scope" in request.headers:
        if isinstance(request.headers["client-id"], str) and isinstance(request.headers["redirect-uri"], str) and isinstance(request.headers["scope"], str):
            client_id = request.headers["client-id"]
            redirect_uri = request.headers["redirect-uri"]
            scope = request.headers["scope"].split(" ")
        else:
            result = "First"
            return HttpResponse(result, content_type, 400)
    else:
        result = "Second" 
        return HttpResponse(result, content_type, 400)

    if redirect_uri != universal.getRedirect_uri():
        result = "Third"
        return HttpResponse(result, content_type, 401)

    with connection.cursor() as cursor:
        cursor.execute("SELECT username, role FROM public.user WHERE username = %s", [client_id])
        row = universal.dictfetchall(cursor)
        if len(row) == 1:
            if row[0]["username"] != client_id:
                result = "Fourth"
                return HttpResponse(result, content_type, 401)
        else:
            result = "Fifth"
            return HttpResponse(result, content_type, 401)
        role = row[0]["role"]
        user_id = row[0]["username"]
    if role == 2:
        eglibible_scopes = universal.get_admin_scopes()
    else:
        eglibible_scopes = universal.get_user_scopes()

    for s in scope:
        if s not in eglibible_scopes:
            return HttpResponse(result, content_type, 403)

    content_type = "application/json"
    token = jwt.encode({'exp': datetime.utcnow() + timedelta(minutes=60), 'id': user_id, 'scope': " ".join(scope)}, settings.SECRET_KEY, algorithm='HS256')
    result = json.dumps({'access_token': token, 'token_type': "bearer", 'expires_in': 3600})
    return HttpResponse(result, content_type, statusCode)    

