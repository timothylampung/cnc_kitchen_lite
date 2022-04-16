from rest_framework import generics
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from recipe.models import Recipe
from tasks.api.serializer import TaskSetSerializer
from tasks.models import TaskSet


@permission_classes((AllowAny,))
class AddRecipeToTaskSet(generics.RetrieveAPIView):
    queryset = TaskSet.objects.all()
    serializer_class = TaskSetSerializer

    def get(self, request, *args, **kwargs):
        recipe_id = request.GET.get('recipe_id')
        task_name = request.GET.get('task_name')
        recipe = Recipe.objects.get(pk=recipe_id)
        task_set, _ = TaskSet.objects.get_or_create(
            recipe=recipe,
            task_name=task_name
        )
        ser = TaskSetSerializer(instance=task_set)
        return Response(ser.data)