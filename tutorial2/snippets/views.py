from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from snippets.models import Snippet
from snippets.serializers import SnippetSerializer


@api_view(['GET', 'POST'])
def snippet_list(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        try:
            snippets = Snippet.objects.all()
            serializer = SnippetSerializer(snippets, many=True)
            return Response(
                {
                    'message': 'snippets retrieved successfully',
                    'data': serializer.data
                },
                status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {
                    'message': str(e)
                },
                status.HTTP_400_BAD_REQUEST
            )

    elif request.method == 'POST':
        try:
            serializer = SnippetSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {
                        'message': 'snippet created successfully',
                        'data': serializer.data
                    },
                    status.HTTP_200_OK
                )
            else:
                return Response(
                    {
                        'message': serializer.errors
                    },
                    status.HTTP_422_UNPROCESSABLE_ENTITY
                )
        except Exception as e:
            print('exception is', e)
            return Response(
                {
                    'message': str(e)
                },
                status.HTTP_400_BAD_REQUEST
            )


@api_view(['GET', 'PUT', 'DELETE'])
def snippet_detail(request, pk):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        snippet = Snippet.objects.get(pk=pk)
    except Snippet.DoesNotExist:
        return Response(
            {
                'message': 'snippet does not exist'
            },
            status.HTTP_404_NOT_FOUND
        )

    if request.method == 'GET':
        try:
            serializer = SnippetSerializer(snippet)
            return Response(
                {
                    'message': 'snippet retrieved successfully',
                    'data': serializer.data
                },
                status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {
                    'message': str(e)
                },
                status.HTTP_400_BAD_REQUEST
            )

    elif request.method == 'PUT':
        try:
            serializer = SnippetSerializer(
                snippet,
                data=request.data,
                partial=True
            )
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {
                        'message': 'snippet updated successfully',
                        'data': serializer.data
                    },
                    status.HTTP_200_OK
                )
            else:
                return Response(
                    {
                        'message': serializer.errors
                    },
                    status.HTTP_422_UNPROCESSABLE_ENTITY
                )
        except Exception as e:
            return Response(
                {
                    'message': str(e)
                },
                status.HTTP_400_BAD_REQUEST
            )

    elif request.method == 'DELETE':
        try:
            snippet.delete()
            return Response(
                {
                    'message': 'snippet deleted successfully'
                },
                status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {
                    'message': str(e)
                },
                status.HTTP_400_BAD_REQUEST
            )
