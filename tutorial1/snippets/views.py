from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser

from snippets.models import Snippet
from snippets.serializers import SnippetSerializer


@csrf_exempt
def snippet_detail(request, pk=None):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        try:
            if pk:
                snippet = Snippet.objects.get(pk=pk)
                serializer = SnippetSerializer(snippet)
                return JsonResponse(serializer.data, safe=False, status=200)
            else:
                snippets = Snippet.objects.all()
                serializer = SnippetSerializer(snippets, many=True)
                return JsonResponse(serializer.data, safe=False, status=200)
        except Exception as e:
            return JsonResponse({"message": str(e)}, status=400)

    elif request.method == 'POST':
        try:
            data = JSONParser().parse(request)
            if data is None:
                return JsonResponse({"message": "no data in the request"}, status=400)
            serializer = SnippetSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data, status=201)
            return JsonResponse(serializer.errors, status=422)

        except Exception as e:
            return JsonResponse({"message": str(e)}, status=400)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        snippet = Snippet.objects.get(pk=pk)

        if not snippet:
            return JsonResponse(serializer.errors, status=400)

        serializer = SnippetSerializer(snippet, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=200)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        # return a simple message
        # return JsonResponse({"message": "delete method not implemented", "id": pk }, status=400)

        snippet = Snippet.objects.get(pk=pk)
        if not snippet:
            return JsonResponse(serializer.errors, status=422)
        snippet.delete()
        return HttpResponse(status=204)
