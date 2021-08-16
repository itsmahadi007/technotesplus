from django.shortcuts import render
from django.http import JsonResponse
from web.models import Notes, SharedNotes
from .serializers import NotesSerializer, SharedNotesSerializer
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from rest_framework.views import APIView

from rest_framework.permissions import IsAuthenticated


# Create your views here.

def apioverview(request):
    return JsonResponse("API is Working | Admiral ", safe=False)


class Note_gp(APIView):
    """
    List all Data, or create a new Data.
    """
    permission_classes = (IsAuthenticated,)  # permission classes

    def get(self, request):
        obj = Notes.objects.filter(user=request.user)
        serializer = NotesSerializer(obj, many=True)
        return Response(serializer.data)

    def post(self, request):
        id = request.user.id
        request.data["user"] = id
        serializer_obj = NotesSerializer(data=request.data)

        if serializer_obj.is_valid():
            serializer_obj.save()
            return Response(serializer_obj.data, status=status.HTTP_201_CREATED)
        return Response(serializer_obj.errors, status=status.HTTP_400_BAD_REQUEST)


class Shared_by_me(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        obj = SharedNotes.objects.filter(note__user=request.user)
        serializer = SharedNotesSerializer(obj, many=True)
        return Response(serializer.data)


class Shared_with_me(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        obj = SharedNotes.objects.filter(view_permit__username=request.user.username)
        serializer = SharedNotesSerializer(obj, many=True)
        return Response(serializer.data)
