Examples
========


Usage in a model
---------------- 
::

    from dj_ingredient_field import IngredientField, MeasurementUnitField
    from django.db import models

    class MyModel(models.Model):
        ingredient = IngredientField()
        unit = MeasurementUnitField()
        amount = models.FloatField()

Using the field values
----------------------
::

    from dj_ingredient_field import Ingredient, IngredientName, MeasurementUnit, INGREDIENT_UNITS

    ingredient = Ingredient(IngredientName.I_VODKA)
    unit = MeasurementUnit(**INGREDIENT_UNITS["Killogram"])
    amount = 1

    model = MyModel(ingredient= ingredient,
        unit= unit,
        amount= amount)
    model.save()

    print(ingredient)
    # VODKA
    print(unit)
    # Killogram

    unit2 = MeasurementUnit(**INGREDIENT_UNITS["Litre"])

    # Density is in kg/m^3 (997 is water)
    kg_in_L = unit.convertTo(1,unit2,density=997)
    print(kg_in_L)
    # 1.003... 

    l_in_m3 = unit2.get_base_unit_amount(1)
    print(l_in_m3)
    # 1e-3