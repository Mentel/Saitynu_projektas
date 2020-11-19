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
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM public.game")
        row = universal.dictfetchall(cursor)
    result = row
    return HttpResponse (result, status = statusCode)

def getGame(request, index1):
    statusCode = 200
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM public.game WHERE id = %s", [index1])
        row = universal.dictfetchall(cursor)
    result = row    
    return HttpResponse (result, status = statusCode)

def getCategoryList(request, index1):
    statusCode = 200
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM public.game WHERE category_id = %s", [index1])
        row = universal.dictfetchall(cursor)
    result = row 
    return HttpResponse (result, status = statusCode)

def create(request):
    input = universal.getText(request.body)
    if input == False:
        return HttpResponse ("Error", status = 400)
    if "name" not in input:
        return HttpResponse ("Error", status = 400)  
    statusCode = 201
    with connection.cursor() as cursor:
        cursor.execute("INSERT INTO public.game(category_id, name, price, description) VALUES (%s, %s, %s, %s) RETURNING id, name", [input["category_id"], input["name"], input["price"], input["description"]])
        returnedId = universal.dictfetchall(cursor)
    result = universal.dumpJson(returnedId)
    return HttpResponse (result, status = statusCode, content_type = "application/json")

def update(request, index1):
    input = universal.getText(request.body)
    if input == False:
        return HttpResponse ("Error", status = 400)
    if "name" not in input:
        return HttpResponse ("Error", status = 400)      
    statusCode = 200
    with connection.cursor() as cursor:
        cursor.execute("UPDATE public.game SET name = %s, price = %s, description = %s WHERE id = %s", [input["name"], input["price"], input["description"], index1])
    result = "Zaidimas atnaujintas"
    return HttpResponse(result, status = statusCode)

def delete(request, index1):
    statusCode = 200
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM public.review WHERE game_id = %s", [index1])
        row = universal.dictfetchall(cursor)
        if len(row) >= 1:
            return HttpResponse("Sis zaidimas turi apzvalgu.", status = 409)
        cursor.execute("DELETE FROM public.game WHERE id = %s", [index1])        
    return HttpResponse(status = statusCode)