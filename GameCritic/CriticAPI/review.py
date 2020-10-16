from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def API1(request, index1, index2):
    if (request.method == 'GET'):
        return getList(request, index1, index2)
    elif (request.method == 'POST'):
        return create(request, index1, index2)
    else:
        return HttpResponse(status = 404)


@csrf_exempt
def API2(request, index1, index2, index3):
    if (request.method == 'PUT'):
        return update(request, index1, index2, index3)
    elif (request.method == 'GET'):
        return getReview(request, index1, index2, index3)
    elif (request.method == 'DELETE'):
        return delete(request, index1, index2, index3)
    else:
        return HttpResponse(status = 404)

def getReview(request, index1, index2, index3):
    statusCode = 200
    result = "Gautas kategorijos " + str(index1) + " zaidimo " + str(index2) + " ivertinimas " + str(index3)
    return HttpResponse (result, status = statusCode)

def getList(request, index1, index2):
    statusCode = 200
    result = "Visi kategorijos " + str(index1) + " zaidimo " + str(index2) +" ivertinimai : 7/10, 8/10, 5/10, 10/10"
    return HttpResponse (result, status = statusCode)

def create(request, index1, index2):
    statusCode = 201
    result = "Ikeltas naujas kategorijos " + str(index1) + " zaidimo " + str(index2) + " ivertinimas"
    return HttpResponse (result, status = statusCode)

def update(request, index1, index2, index3):
    statusCode = 200
    result = "Kategorijos " + str(index1) + " zaidimo " + str(index2) + " ivertinimas " + str(index3) + " redaguotas"
    return HttpResponse(result, status = statusCode)

def delete(request, index1, index2, index3):
    statusCode = 200
    result = "Kategorijos " + str(index1) + " zaidimo " + str(index2) + " ivertinimas " + str(index3) + " istrintas"
    return HttpResponse(result, status = statusCode)