
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.views import APIView
from snippets.models import Snippet
from snippets.serializers import SnippetSerializer


class SnippetList(APIView):
    """
    List all snippets, or create a new snippet.
    """

    def get(self, request, format=None):
        try:
            snippets = Snippet.objects.all()
            serializer = SnippetSerializer(snippets, many=True)
            return Response(
                {
                    'message': 'snippets retrieved successfully',
                    'data': serializer.data
                },
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {
                    'message': str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def post(self, request, format=None):
        try:
            serializer = SnippetSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {
                        'message': 'snippet created successfully',
                        'data': serializer.data
                    },
                    status=status.HTTP_201_CREATED
                )
            else:
                return Response(
                    {
                        'message': serializer.errors,
                    },
                    status=status.HTTP_422_UNPROCESSABLE_ENTITY
                )
        except Exception as e:
            return Response(
                {
                    'message': str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class SnippetDetail(APIView):
    """
    Retrieve, update or delete a snippet instance.
    """

    def get_object(self, pk):
        try:
            return Snippet.objects.get(pk=pk)
        except Snippet.DoesNotExist:
            raise NotFound(
                detail='snippet not found',
                code=status.HTTP_404_NOT_FOUND
            )

    def get(self, request, pk, format=None):
        try:
            snippet = self.get_object(pk)
            serializer = SnippetSerializer(snippet)
            return Response(
                {
                    'message': 'snippet retrieved successfully',
                    'data': serializer.data
                },
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {
                    'message': str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def put(self, request, pk, format=None):
        try:
            snippet = self.get_object(pk)
            serializer = SnippetSerializer(snippet, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {
                        'message': 'snippet updated successfully',
                        'data': serializer.data
                    },
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {
                        'message': serializer.errors,
                    },
                    status=status.HTTP_422_UNPROCESSABLE_ENTITY
                )
        except Exception as e:
            return Response(
                {
                    'message': str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def patch(self, request, pk, format=None):
        try:
            snippet = self.get_object(pk)
            serializer = SnippetSerializer(
                snippet, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {
                        'message': 'snippet updated successfully',
                        'data': serializer.data
                    },
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {
                        'message': serializer.errors,
                    },
                    status=status.HTTP_422_UNPROCESSABLE_ENTITY
                )
        except Exception as e:
            return Response(
                {
                    'message': str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def delete(self, request, pk, format=None):
        try:
            snippet = self.get_object(pk)
            snippet.delete()
            return Response(
                {
                    'message': 'snippet deleted successfully',
                },
                status=status.HTTP_204_NO_CONTENT
            )
        except Exception as e:
            return Response(
                {
                    'message': str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
