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
    print('request method is', request.method)
    if request.method == 'GET':
        try:
            if pk:
                snippet = Snippet.objects.get(pk=pk)
                serializer = SnippetSerializer(snippet)
                response = {
                    'message': 'snippet retrieved successfully',
                    'data': serializer.data
                }
            else:
                snippets = Snippet.objects.all()
                serializer = SnippetSerializer(snippets, many=True)
                response = {
                    'message': 'snippets retrieved successfully',
                    'data': serializer.data
                }
            return JsonResponse(response, status=200)
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
                response = {
                    'message': 'snippet created successfully',
                    'data': serializer.data
                }
                return JsonResponse(response, status=200)
            else:
                return JsonResponse({'message': serializer.errors}, status=422)
        except Exception as e:
            return JsonResponse({"message": str(e)}, status=400)

    elif request.method == 'PUT':
        try:
            data = JSONParser().parse(request)
            snippet = Snippet.objects.get(pk=pk)

            serializer = SnippetSerializer(snippet, data=data)
            if serializer.is_valid():
                serializer.save()
                response = {
                    'message': 'snippet updated successfully',
                    'data': serializer.data
                }
                return JsonResponse(response, status=200)
            else:
                return JsonResponse(serializer.errors, status=400)
        except Exception as e:
            return JsonResponse({'message': str(e)}, status=400)

    elif request.method == 'DELETE':
        try:
            snippet = Snippet.objects.get(pk=pk)
            snippet.delete()
            return JsonResponse({'message': 'snippet deleted'}, status=204)
        except Exception as e:
            return JsonResponse({'message': str(e)}, status=400)
    