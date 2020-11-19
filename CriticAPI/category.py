from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import connection
from CriticAPI import universal

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
        return getCategory(request, index1)
    elif (request.method == 'DELETE'):
        return delete(request, index1)
    else:
        return HttpResponse(status = 404)

def getCategory(request, index1):
    statusCode = 200
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM public.category WHERE id = %s", [index1])
        row = universal.dictfetchall(cursor)
    result = universal.dumpJson(row)
    return HttpResponse (result, status = statusCode, content_type = "application/json")

def getList(request):
    statusCode = 200
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM public.category")
        row = universal.dictfetchall(cursor)
    result = universal.dumpJson(row)
    return HttpResponse (result, status = statusCode, content_type = "application/json")

def create(request):
    input = universal.getText(request.body)
    if input == False:
        return HttpResponse ("Error", status = 400)
    if "name" not in input:
        return HttpResponse ("Error", status = 400)  
    statusCode = 201
    with connection.cursor() as cursor:
        cursor.execute("INSERT INTO public.category(name) VALUES (%s) RETURNING id, name", [input["name"]])
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
        cursor.execute("UPDATE public.category SET name = %s WHERE id = %s", [input["name"], index1])
    result = "Kategorija atnaujinta"
    return HttpResponse(result, status = statusCode)

def delete(request, index1):
    statusCode = 200
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM public.game WHERE category_id = %s", [index1])
        row = universal.dictfetchall(cursor)
        if len(row) >= 1:
            return HttpResponse("Yra zaidimu sioje kategorijoje.", status = 409)
        cursor.execute("DELETE FROM public.category WHERE id = %s", [index1])        
    return HttpResponse(status = statusCode)