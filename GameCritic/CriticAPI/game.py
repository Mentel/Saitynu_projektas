from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def API1(request, index1):
    if (request.method == 'GET'):
        return getCategoryList(request, index1)
    elif (request.method == 'POST'):
        return create(request, index1)
    else:
        return HttpResponse(status = 404)


@csrf_exempt
def API2(request, index1, index2):
    if (request.method == 'PUT'):
        return update(request, index1, index2)
    elif (request.method == 'GET'):
        return getGame(request, index1, index2)
    elif (request.method == 'DELETE'):
        return delete(request, index1, index2)
    else:
        return HttpResponse(status = 404)

@csrf_exempt
def API3(request):
    if (request.method == 'GET'):
        return getList(request)
    else:
        return HttpResponse (status = 404)

def getList(request):
    statusCode = 200
    result = "Visi tinklapio zaidimai: S,L,P,Q,W,V,Y,I,Z"
    return HttpResponse (result, status = statusCode) 

def getGame(request, index1, index2):
    statusCode = 200
    result = "Gautas kategorijos " + str(index1) + " zaidimas " + str(index2)
    return HttpResponse (result, status = statusCode)

def getCategoryList(request, index1):
    statusCode = 200
    result = "Kategorijos " + str(index1) + " zaidimai : W, X, Y, Z"
    return HttpResponse (result, status = statusCode)

def create(request, index1):
    statusCode = 201
    result = "Ikeltas naujas " + str(index1) + " kategorijos zaidimas"
    return HttpResponse (result, status = statusCode)

def update(request, index1, index2):
    statusCode = 200
    result = "Kategorijos " + str(index1) + " zaidimas " + str(index2) + " redaguotas"
    return HttpResponse(result, status = statusCode)

def delete(request, index1, index2):
    statusCode = 200
    result = "Kategorijos " + str(index1) + " zaidimas " + str(index2) + " istrintas"
    return HttpResponse(result, status = statusCode)