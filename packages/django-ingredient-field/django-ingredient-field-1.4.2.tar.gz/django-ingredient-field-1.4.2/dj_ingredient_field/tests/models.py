from dj_ingredient_field import IngredientField, MeasurementUnitField
from django.db import models 

class TestModel(models.Model):
    ingredient = IngredientField()

class TestModel2(models.Model):
    unit = MeasurementUnitField()
    