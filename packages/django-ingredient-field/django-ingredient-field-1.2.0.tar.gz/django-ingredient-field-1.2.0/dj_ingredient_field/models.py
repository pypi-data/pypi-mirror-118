from dj_ingredient_field import IngredientField, MeasurementUnitField
from django.db import models

class MyModel(models.Model):
    ingredient = IngredientField()
    unit = MeasurementUnitField()
    amount = models.FloatField()

    