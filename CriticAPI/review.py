from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import connection
from CriticAPI import universal

@csrf_exempt
def API1(request, index1):
    if (request.method == 'GET'):
        return getList(request, index1)
    elif (request.method == 'POST'):
        return create(request, index1)   
    else:
        return HttpResponse(status = 404)


@csrf_exempt
def API2(request, index1, index2):
    if (request.method == 'PUT'):
        return update(request, index1, index2)
    elif (request.method == 'GET'):
        return getReview(request, index1, index2)
    elif (request.method == 'DELETE'):
        return delete(request, index1, index2) 
    else:
        return HttpResponse(status = 404)

def getReview(request, index1, index2):
    statusCode = 200
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM public.review WHERE game_id = %s AND id = %s", [index1, index2])
        row = universal.dictfetchall(cursor)
    result = universal.dumpJson(row)  
    return HttpResponse (result, status = statusCode, content_type = "application/json")

def getList(request, index1):
    statusCode = 200
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM public.review WHERE game_id = %s", [index1])
        row = universal.dictfetchall(cursor)
    result = universal.dumpJson(row)   
    return HttpResponse (result, status = statusCode, content_type = "application/json")

def create(request, index1):
    input = universal.getText(request.body)
    if input == False:
        return HttpResponse ("ErrorA", status = 400)
    if "content" not in input:
        return HttpResponse ("ErrorB", status = 400)  
    statusCode = 201
    with connection.cursor() as cursor:
        cursor.execute("INSERT INTO public.review(game_id, user_id, content) VALUES (%s, %s, %s) RETURNING id, content", [index1, input["user_id"], input["content"]])
        returnedId = universal.dictfetchall(cursor)
    result = universal.dumpJson(returnedId)
    return HttpResponse (result, status = statusCode, content_type = "application/json")

def update(request, index1, index2):
    input = universal.getText(request.body)
    if input == False:
        return HttpResponse ("Error", status = 400)
    if "content" not in input:
        return HttpResponse ("Error", status = 400)      
    statusCode = 200
    with connection.cursor() as cursor:
        cursor.execute("UPDATE public.review SET content = %s WHERE id = %s", [input["content"], index2])
    result = "Zaidimas atnaujintas"
    return HttpResponse(result, status = statusCode)

def delete(request, index1, index2):
    statusCode = 200
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM public.review WHERE id = %s", [index2])        
    return HttpResponse(status = statusCode)