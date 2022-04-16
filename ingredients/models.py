from django.db import models

# Create your models here.
from cnc_kitchen_lite.core_model import id_generator, DocumentModel


def upload_ingredient_image(instance, filename):
    return f"images/ingredients/{id_generator()}{filename}"


class Ingredient(DocumentModel):
    GRAM = 'GRAM'
    KILOGRAM = 'KILOGRAM'
    TABLE_SPOON = 'TABLE_SPOON'
    TEA_SPOON = 'TEA_SPOON'
    MILLILITER = 'MILLILITER'
    UNIT = (
        (GRAM, 'GRAM'),
        (KILOGRAM, 'KILOGRAM'),
        (TABLE_SPOON, 'TABLE_SPOON'),
        (MILLILITER, 'MILLILITER'),
    )

    SOLID = 'SOLID'
    GRANULAR = 'GRANULAR'
    LIQUID = 'LIQUID'

    TYPE = (
        (SOLID, 'SOLID'),
        (GRANULAR, 'GRANULAR'),
        (LIQUID, 'LIQUID'),
    )

    ingredient_name = models.CharField(null=True, blank=True, max_length=400)
    stock_count = models.DecimalField(
        max_digits=19, decimal_places=2, null=True, blank=True)
    image_path = models.ImageField(
        upload_to=upload_ingredient_image, null=True, blank=True)
    type = models.CharField(max_length=200, null=True,
                            choices=TYPE, default=None)
    unit = models.CharField(max_length=200, null=True,
                            choices=UNIT, default=None)
    invoked_count = models.IntegerField(default=0, null=True, blank=True)

    def __str__(self):
        return f'{self.ingredient_name} {self.id}'


class Coordinates(DocumentModel):
    INGREDIENT = 'INGREDIENT'
    DUMPER = 'DUMPER'
    PICKER = 'PICKER'
    PLATE = 'PLATE'

    TYPE = (
        (INGREDIENT, 'INGREDIENT'),
        (DUMPER, 'DUMPER'),
        (PICKER, 'PICKER'),
        (PLATE, 'PLATE'),
    )

    type = models.CharField(max_length=200, null=True, choices=TYPE, default=None)
    name = models.CharField(max_length=200, default=None)
    coordinate_x = models.IntegerField(default=0, null=True, blank=True, )
    coordinate_y = models.IntegerField(default=0, null=True, blank=True, )
    ordinal = models.IntegerField(default=0)
    primary = models.ForeignKey('self', on_delete=models.SET_NULL, default=None, blank=True, null=True,
                                related_name="children", )
    ingredient = models.ForeignKey(Ingredient, on_delete=models.SET_NULL, default=None, null=True, blank=True,
                                   related_name="ingredient_map", )

    def __str__(self):
        name = f'{self.name}'
        if self.ingredient is not None:
            name = f'{name} {self.ingredient.ingredient_name}'
        else:
            name = f'{name} not mapped'
        return name
