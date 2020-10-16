from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

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
        return getGame(request, index1)
    elif (request.method == 'DELETE'):
        return delete(request, index1)
    else:
        return HttpResponse(status = 404)

def getGame(request, index1):
    statusCode = 200
    result = "Gauta kategorija " + str(index1)
    return HttpResponse (result, status = statusCode)

def getList(request):
    statusCode = 200
    result = "Kategorijos : A, B, C, D"
    return HttpResponse (result, status = statusCode)

def create(request):
    statusCode = 201
    result = "Sukurta nauja kategorija"
    return HttpResponse (result, status = statusCode)

def update(request, index1):
    statusCode = 200
    result = "Kategorija " + str(index1) + " redaguota"
    return HttpResponse(result, status = statusCode)

def delete(request, index1):
    statusCode = 200
    result = "Kategorija " + str(index1) + " istrinta"
    return HttpResponse(result, status = statusCode)