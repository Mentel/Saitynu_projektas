from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import connection
from CriticAPI import universal

@csrf_exempt
def API1(request, index1):
    if (request.method == 'GET'):
        return getCategoryList(request, index1)
    else:
        return HttpResponse(status = 404)


@csrf_exempt
def API2(request, index1):
    if (request.method == 'PUT'):
        return update(request, index1)
    elif (request.method == 'GET'):
        return getGame(request, index1)
    elif (request.method == 'DELETE'):
        return delete(request, index1)
    else:
        return HttpResponse(status = 404)

@csrf_exempt
def API3(request):
    if (request.method == 'GET'):
        return getList(request)
    elif (request.method == 'POST'):
        return create(request)        
    else:
        return HttpResponse (status = 404)

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
        cursor.execute("SELECT * FROM public.game")
        row = universal.dictfetchall(cursor)
    result = universal.dumpJson(row)  
    return HttpResponse (result, status = statusCode, content_type = "application/json")

def getGame(request, index1):
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
        cursor.execute("SELECT * FROM public.game WHERE id = %s", [index1])
        row = universal.dictfetchall(cursor)
    result = universal.dumpJson(row)      
    return HttpResponse (result, status = statusCode, content_type = "application/json")

def getCategoryList(request, index1):
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
        cursor.execute("SELECT * FROM public.game WHERE category_id = %s", [index1])
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
    if "name" not in body:
        return HttpResponse ("ErrorB", status = 400)
        
    scope = request.headers["scope"]
    scope = int(scope)
    if scope != 2:
        return HttpResponse("Not admin", content_type, 403)         
    statusCode = 201  
    with connection.cursor() as cursor:
        cursor.execute("INSERT INTO public.game(category_id, name, price, description) VALUES (%s,%s,%s,%s) RETURNING id, name", [body["category_id"], body["name"], body["price"], body["description"]])
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
    if "name" not in body:
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

    with connection.cursor() as cursor:
        cursor.execute("UPDATE public.game SET name = %s, price = %s, description = %s WHERE id = %s", [body["name"], body["price"], body["description"], index1])
    result = "Zaidimas atnaujintas"
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
        cursor.execute("SELECT * FROM public.review WHERE game_id = %s", [index1])
        row = universal.dictfetchall(cursor)
        if len(row) >= 1:
            return HttpResponse("Sis zaidimas turi apzvalgu.", status = 409)
        cursor.execute("SELECT * FROM public.game WHERE id = %s", [index1])
        row = universal.dictfetchall(cursor)
        if len(row) == 0:
            return HttpResponse("Sis zaidimas neegzistuoja.", status = 410)
        cursor.execute("DELETE FROM public.game WHERE id = %s", [index1])        
    return HttpResponse(status = statusCode)    