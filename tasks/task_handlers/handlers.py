from typing import Optional

from tasks.task_handlers.sub_step_handler import AbstractHandler


class HeaterHandler(AbstractHandler):
    from recipe.models import SubStep

    def __init__(self):
        super(HeaterHandler, self).__init__()
        self.operation = 0

    def handle(self, request: SubStep) -> Optional[dict]:
        print('HEATER_HANDLER')
        from recipe.step_forms import StepFormType
        data = self.merge_dictionary(request.get_parameter())
        if request.name == StepFormType.HEATER_FORM:
            self.ws.send('{"type": "channel_message", "message": "Heater Handler Triggered"}')
            return data
        else:
            return super().handle(request)


class ValveHandler(AbstractHandler):
    from recipe.models import SubStep

    def __init__(self):
        super(ValveHandler, self).__init__()
        self.operation = 1

    def handle(self, request: SubStep) -> Optional[dict]:
        print('VALVE_HANDLER')
        from asgiref.sync import async_to_sync
        from channels.layers import get_channel_layer
        from recipe.step_forms import StepFormType

        data = self.merge_dictionary(request.get_parameter())
        if request.name == StepFormType.VALVE_FORM:
            self.ws.send('{"type": "channel_message", "message": "Valve Handler Triggered"}')
            return data
        else:
            return super().handle(request)


class MixerHandler(AbstractHandler):
    from recipe.models import SubStep

    def __init__(self):
        super(MixerHandler, self).__init__()
        self.operation = 2

    def handle(self, request: SubStep) -> Optional[dict]:
        print('VALVE_HANDLER')
        from asgiref.sync import async_to_sync
        from channels.layers import get_channel_layer
        from recipe.step_forms import StepFormType

        data = self.merge_dictionary(request.get_parameter())
        if request.name == StepFormType.MIXER_FORM:
            self.ws.send('{"type": "channel_message", "message": "Mixer Handler Triggered"}')
            return data
        else:
            return super().handle(request)


class PickupIngredientHandler(AbstractHandler):
    from recipe.models import SubStep

    def __init__(self):
        super(PickupIngredientHandler, self).__init__()
        self.operation = 3

    def handle(self, request: SubStep) -> Optional[dict]:
        print('VALVE_HANDLER')
        from recipe.step_forms import StepFormType

        data = self.merge_dictionary(request.get_parameter())
        if request.name == StepFormType.PICKUP_INGREDIENT:
            self.ws.send('{"type": "channel_message", "message": "Pickup Handler Triggered"}')
            return data
        else:
            return super().handle(request)


HANDLERS = HeaterHandler()
__mixer = MixerHandler()
__valve = ValveHandler()
__pickup = PickupIngredientHandler()

HANDLERS.set_next(__mixer).set_next(__valve).set_next(__pickup)
