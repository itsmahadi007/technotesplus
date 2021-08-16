from rest_framework import serializers
from web.models import Notes, SharedNotes


class NotesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notes
        fields = "__all__"


class SharedNotesSerializer(serializers.ModelSerializer):
    class Meta:
        model = SharedNotes
        fields = "__all__"
