from django.http import HttpResponse, JsonResponse
from django.view.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from snippets.model import Snippet
from snippets.serializers import SnippetSerializer


@csrf_exempt
def snippet_list(request):
    """List all of the snippets"""
    if request.method == "GET":
        snippets = Snippet.objects.all()
        serializer = SnippetSerializer(snippets, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == "POST":
        data = JSONParser().parse(request)
        serializer = SnippetSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


@csrf_exempt
def snippet_detail(request, pk):
    """Retrieve a detail of a Snippet object"""
    try:
        snip = Snippet.objects.get(pk=pk)
    except Snippet.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == "GET":
        ser = SnippetSerializer(snip)
        return JsonResponse(ser.data, safe=False)

    elif request.method == "PUT":
        data = JSONParser().parse(request)
        ser = SnippetSerializer(snip, data=data)
        if ser.is_valid():
            ser.save()
            return JsonResponse(ser.data)
        return JsonResponse(ser.errors, status=400)

    elif request.method == "DELETE":
        snip.delete()
        return HttpResponse(status=204)
