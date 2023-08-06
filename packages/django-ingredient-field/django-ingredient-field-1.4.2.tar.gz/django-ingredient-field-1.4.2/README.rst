=======================
django-ingredient-field
=======================

Quick start
-----------

1. Add "dj_ingredient_field" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'dj_ingredient_field',
    ]

2. To use lazy loaded widgets include this module in your urlpatterns::

    urlpatterns = [
        path('cooking/', include('dj_ingredient_field.urls')),
        ...
    ]

3. That's it!

Usage
-----

Simply add the fields you need to your model::

   from dj_ingredient_field import IngredientField, MeasurementUnitField

   class MyModel(models.Model):
      ingredient = IngredientField()
      unit = MeasurementUnitField()

The fields map to Ingredient and MeasurementUnit classes::

   from dj_ingredient_field import IngredientName, Ingredient, MeasurementUnit, INGREDIENT_UNITS

   model.ingredient = Ingredient(IngredientName.I_ARUGULA)
   model.unit = MeasurementUnit(**INGREDIENT_UNITS["Killogram"])

All the available ingredients can be found in the ``IngredientName`` enum

Ingredients and units can be customized, see 'Settings'

Documentation 
-------------
https://django-ingredient-field.readthedocs.io/en/latest
