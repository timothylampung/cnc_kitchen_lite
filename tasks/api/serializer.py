from rest_framework import serializers

from cnc_kitchen_lite.core_serializer import DocumentModelSerializer
from module.models import Module
from recipe.models import Recipe
from tasks.models import TaskSet


class ModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = '__all__'


class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = '__all__'


class TaskSetSerializer(DocumentModelSerializer):
    recipe = RecipeSerializer(many=False)
    module = ModuleSerializer(many=False)

    class Meta:
        model = TaskSet
        fields = '__all__'
