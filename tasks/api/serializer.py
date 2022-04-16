from cnc_kitchen_lite.core_serializer import DocumentModelSerializer
from tasks.models import TaskSet


class TaskSetSerializer(DocumentModelSerializer):
    class Meta:
        model = TaskSet
        fields = '__all__'
