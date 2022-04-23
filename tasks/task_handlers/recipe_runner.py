import time
import datetime
from django.utils import timezone


def run_task(task_id=None, task_name=None):
    from tasks.models import TaskSet
    from asgiref.sync import async_to_sync
    from channels.layers import get_channel_layer
    from tasks.task_handlers.handlers import HANDLERS
    from recipe.models import Step

    task = TaskSet.objects.get(pk=task_id)
    task.task_status = TaskSet.STARTED
    task.started_time = timezone.now()
    task.save()
    recipe = task.recipe

    try:
        for idx, step in enumerate(recipe.steps.all()):

            print(step.step_name)

            if step.step_type == Step.WOK_STEP:
                for _idx, sub_step in enumerate(step.sub_steps.all()):
                    ret = HANDLERS.handle(sub_step)
            elif step.step_type == Step.PICKUP_STEP:
                for _idx, sub_step in enumerate(step.sub_steps.all()):
                    ret = HANDLERS.handle(sub_step)

            time.sleep(step.wait_for)
            task.current_step = idx + 1
            task.save()

    except Exception as e:
        print(e)
        async_to_sync(get_channel_layer().group_send)(f'channel_1', {
            'type': 'channel_message',
            'message': str(e),
        })


def pick_ingredient(ingredient, requester):
    pass
