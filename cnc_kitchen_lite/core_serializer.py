from rest_framework.fields import CharField
from django.contrib.auth.models import User, Group
from rest_framework import serializers

from cnc_kitchen_lite.core_model import DocumentModel


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']


class DocumentModelSerializer(serializers.ModelSerializer):
    creator_name = serializers.StringRelatedField(source='creator', read_only=True)
    editor_name = serializers.StringRelatedField(source='editor', read_only=True)
    creator_obj = UserSerializer(read_only=True)
    editor_obj = UserSerializer(read_only=True)
    document_code = CharField(read_only=True)
    document_status = CharField(read_only=True)

    # def save(self, **kwargs):

    class Meta:
        model = DocumentModel
        fields = ('creator_obj', 'editor_obj')
        abstract = True
