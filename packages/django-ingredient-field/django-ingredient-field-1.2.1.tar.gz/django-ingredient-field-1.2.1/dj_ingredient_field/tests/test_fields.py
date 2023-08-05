from django.core.exceptions import ValidationError
from dj_ingredient_field import IngredientField,MeasurementUnitField, IngredientName, Ingredient, MeasurementUnit, UnitType
from django.test import TestCase

class IngredientFieldTests(TestCase):

    def test_create_test_model(self):
        from .models import TestModel

        TestModel(ingredient=Ingredient(IngredientName.I_ADOBO)).save()

        TestModel.objects.get(pk=1)

    def test_assign_retrieve_value(self):
        from .models import TestModel

        t_model = TestModel(ingredient=Ingredient(IngredientName.I_ADOBO))
        t_model.save()
        t_model.refresh_from_db()
        t_model.full_clean()

        self.assertEquals(t_model.ingredient, Ingredient(IngredientName.I_ADOBO), "Incorrect ingredient assigned")

    def test_assign_invalid_value(self):
        from .models import TestModel
        t_model = TestModel(ingredient=Ingredient('asdasd'))
        t_model.save()
        t_model.refresh_from_db()

        self.assertRaises(ValidationError,lambda: t_model.full_clean())

    def test_retrieve_value_is_type_ingredient(self):
        from .models import TestModel
        t_model = TestModel(ingredient=Ingredient(IngredientName.I_ADOBO))
        t_model.save()
        t_model.refresh_from_db()
        self.assertIsInstance(t_model.ingredient, Ingredient, "Incorrect ingredient type on retrieveal")

    def test_retrieve_value_preserves_name(self):
        from .models import TestModel
        t_model = TestModel(ingredient=Ingredient(IngredientName.I_ADOBO))
        t_model.save()
        t_model.refresh_from_db()
        self.assertEqual(t_model.ingredient.name, IngredientName.I_ADOBO, "Ingredient value is not preserved")

    def test_deconstruct_no_args(self):
        self.assertEqual(
            (None,'dj_ingredient_field.IngredientField',[],{}),
            IngredientField().deconstruct(), "deconstructed values were not empty or something went wrong")

    def test_deconstruct_test_args(self):
        self.assertEqual(
            (None,'dj_ingredient_field.IngredientField',[],{'blank': True, 'null': True}),
            IngredientField(blank=True,null=True).deconstruct(), "deconstructed values were missing or something went wrong")

    def test_deconstruct_no_max_length(self):
        _,_,_,kwargs = IngredientField().deconstruct()
        self.assertFalse('max_length' in kwargs, 'max_length was deconstructed as a kwarg')

    def test_deconstruct_no_choices(self):
        _,_,_,kwargs = IngredientField().deconstruct()
        self.assertFalse('choices' in kwargs, 'choices was deconstructed as a kwarg')

    def test_to_python_string(self):
        self.assertEqual(Ingredient(IngredientName.I_ADOBO),IngredientField().to_python(str(IngredientName.I_ADOBO)))

    def test_to_python_none(self):
        self.assertEqual(None,IngredientField().to_python(None))
    
    def test_from_db_value_none(self):
        self.assertEqual(None,IngredientField().from_db_value(None,None,None))

class MeasurementUnitFieldTests(TestCase):

    def test_create_test_model(self):
        from .models import TestModel2

        TestModel2(unit= MeasurementUnit("a","b",1,UnitType.MASS)).save()

        TestModel2.objects.get(pk=1)

    def test_assign_invalid_value(self):
        from .models import TestModel2
        t_model = TestModel2(unit=MeasurementUnit("a","b",1,UnitType.MASS))
        t_model.save()
        t_model.refresh_from_db()
        self.assertRaises(ValidationError, lambda: t_model.full_clean())

    def test_assign_valid_value(self):
        from .models import TestModel2
        t_model = TestModel2(unit=MeasurementUnit("Killogram","kg",1,UnitType.MASS))
        t_model.save()
        t_model.refresh_from_db()
        t_model.full_clean()

    def test_retrieve_value_is_type_measurement_unit(self):
        from .models import TestModel2
        t_model = TestModel2(unit=MeasurementUnit("Killogram","kg",1,UnitType.MASS))
        t_model.save()
        t_model.refresh_from_db()
        self.assertIsInstance(t_model.unit, MeasurementUnit, "Incorrect MeasurementUnit type on retrieveal")

    def test_retrieve_value_preserves_name(self):
        from .models import TestModel2
        t_model = TestModel2(unit=MeasurementUnit("Killogram","kg",1,UnitType.MASS))
        t_model.save()
        t_model.refresh_from_db()
        self.assertEqual(t_model.unit.name, "Killogram", "MeasurementUnit value is not preserved")

 
    def test_deconstruct_no_args(self):
        self.assertEqual(
            (None,'dj_ingredient_field.MeasurementUnitField',[],{}),
            MeasurementUnitField().deconstruct(), "deconstructed values were not empty or something went wrong")

    def test_deconstruct_test_args(self):
        self.assertEqual(
            (None,'dj_ingredient_field.MeasurementUnitField',[],{'blank': True, 'null': True}),
            MeasurementUnitField(blank=True,null=True).deconstruct(), "deconstructed values were missing or something went wrong")

    def test_deconstruct_no_max_length(self):
        _,_,_,kwargs = MeasurementUnitField().deconstruct()
        self.assertFalse('max_length' in kwargs, 'max_length was deconstructed as a kwarg')

    def test_deconstruct_no_choices(self):
        _,_,_,kwargs = MeasurementUnitField().deconstruct()
        self.assertFalse('choices' in kwargs, 'choices was deconstructed as a kwarg')
    
    def test_to_python_string(self):
        self.assertEqual(MeasurementUnit("Killogram","kg",1,UnitType.MASS, True),MeasurementUnitField().to_python("Killogram"))

    def test_to_python_none(self):
        self.assertEqual(None,MeasurementUnitField().to_python(None))
    
    def test_from_db_value_none(self):
        self.assertEqual(None,MeasurementUnitField().from_db_value(None,None,None))
