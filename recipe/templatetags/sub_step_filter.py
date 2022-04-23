import json

from django.db.models import Q
from django import template

from ingredients.models import Ingredient
from recipe.models import SubStep
from recipe.step_forms import StepFormType

register = template.Library()


@register.simple_tag()
def parameters_to_pills(sub_step: SubStep):
    ret = []
    try:
        data = json.loads(sub_step.parameters)
        for _key, _value in data.items():
            ret.append({'key': _key, 'value': _value})
        return ret
    except Exception:
        return []


@register.simple_tag()
def get_ingredient_image(sub_step: SubStep):
    try:
        data = json.loads(sub_step.parameters)
        ingredient = Ingredient.objects.get(pk=int(data['ingredient']))
        return ingredient.image_path.url
    except Exception:
        return ''
