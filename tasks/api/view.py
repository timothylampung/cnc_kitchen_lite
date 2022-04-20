from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from rest_framework import generics
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.core import management
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
        async_to_sync(get_channel_layer().group_send)(f'channel_1', {
            'type': 'channel_message',
            'message': 'Jobs added!',
        })

        return Response(ser.data)


@permission_classes((AllowAny,))
class QuickAddRecipeToTaskQueue(generics.RetrieveAPIView):
    queryset = TaskSet.objects.all()
    serializer_class = TaskSetSerializer

    def get(self, request, *args, **kwargs):
        recipe_id = request.GET.get('recipe_id')
        task_name = request.GET.get('task_name')
        module_id = request.GET.get('module_id')

        management.call_command('add_recipe_to_queue', (recipe_id, task_name, module_id))
        ser = TaskSetSerializer({"message": "Success!"})
        return Response(ser.data)


@permission_classes((AllowAny,))
class RunSetOnModule(generics.RetrieveAPIView):
    queryset = TaskSet.objects.all()
    serializer_class = TaskSetSerializer

    def get(self, request, *args, **kwargs):
        recipe_id = request.GET.get('module_id')
        task_name = request.GET.get('task_name')
        management.call_command('start_worker', ('stir_fry', 'sjames'))
        ser = TaskSetSerializer({"message": "Success!"})
        return Response(ser.data)
