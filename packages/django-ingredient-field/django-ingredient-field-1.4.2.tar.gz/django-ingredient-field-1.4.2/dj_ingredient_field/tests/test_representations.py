from django import test
from dj_ingredient_field import Ingredient, MeasurementUnit, UnitType, InvalidConversionException
from django.test import TestCase
from .utils import TestCaseWithUtils

# Create your tests here.
class IngredientTests(TestCase):

    def test_same_name_equals(self):
        ing = Ingredient("a")
        ing2 = Ingredient("a")

        self.assertEqual(ing,ing2, "Ingredients with the same name are not equal")

    def test_differnet_name_not_equals(self):
        ing = Ingredient("a")
        ing2 = Ingredient("b")

        self.assertNotEqual(ing,ing2, "Ingredients with different name are equal")
    
    def test_str(self):
        self.assertEqual(
            "a",
            str(Ingredient("a")),
            "Ingredient did not convert to string properly"
        )

class MeasurementUnitTests(TestCaseWithUtils):
    
    def test_invalid_conversion_invalid_type(self):
        self.assertConversionRaisesException(MeasurementUnit("testA","t",1,UnitType.MASS,True),1,MeasurementUnit("testB","t",1,UnitType.QUANTITY,True),InvalidConversionException)
    
    def test_invalid_conversion_different_base(self):
        self.assertConversionRaisesException(MeasurementUnit("testA","t",1,UnitType.MASS,True),1,MeasurementUnit("testB","t",1,UnitType.MASS,True),InvalidConversionException)
    
    def test_invalid_conversion_invalid_target_unit(self):
        self.assertConversionRaisesException(MeasurementUnit("testA","t",1,UnitType.MASS),1,MeasurementUnit("testB","t",1," "),InvalidConversionException)
    
    def test_equal_quantity_unit(self):
        self.assertEqual(MeasurementUnit("testA","t",1,UnitType.QUANTITY),MeasurementUnit("testA","t",1,UnitType.QUANTITY))
    
    def test_equal_mass_unit(self):
        self.assertEqual(MeasurementUnit("testA","t",1,UnitType.MASS),MeasurementUnit("testA","t",1,UnitType.MASS))
    
    def test_invalid_equal_volume_unit(self):
        self.assertEqual(MeasurementUnit("testA","t",1,UnitType.VOLUME),MeasurementUnit("testA","t",1,UnitType.VOLUME))
    
    def test_unequal_volume_quantity_unit(self):
        self.assertNotEqual(MeasurementUnit("testA","t",1,UnitType.VOLUME),MeasurementUnit("testA","t",1,UnitType.QUANTITY))
    

    def test_convert_1_unit_to_1_unit(self):
        self.assertConvertsTo(MeasurementUnit("test","t", None, UnitType.QUANTITY), 1, MeasurementUnit("test2","t2", None, UnitType.QUANTITY), 1, places=3)
    
    def test_convert_kg_to_m3_water(self):
        self.assertConvertsTo(MeasurementUnit("test","t", 1, UnitType.MASS), 1, MeasurementUnit("test2","t2", 1, UnitType.VOLUME), 1e-3, density=997, places=3)
    
    def test_convert_kg_to_l_water(self):
        self.assertConvertsTo(MeasurementUnit("test","t", 1, UnitType.MASS), 1, MeasurementUnit("test2","t2", 1e-3, UnitType.VOLUME), 1, density=997, places=2)

    def test_convert_m3_to_kg_water(self):
        self.assertConvertsTo(MeasurementUnit("test","t", 1, UnitType.VOLUME), 1, MeasurementUnit("test2","t2", 1, UnitType.MASS), 997, density=997, places=3)

    def test_create_base_unit_with_no_type_raises(self):
        self.assertRaises(ValueError, lambda: MeasurementUnit('a','', 1, None))
    
    def test_to_base_unit(self):
        unit = MeasurementUnit("test","t", 1e-1, UnitType.MASS)
        self.assertAlmostEqual(1e-1,unit.get_base_unit_amount(1))

    def test_convert_g_to_kg(self):
        self.assertConvertsTo(MeasurementUnit("test","t", 1e-3, UnitType.MASS),1,MeasurementUnit("test2","t2", 1, UnitType.MASS),1e-3)

    def test_convert_g_to_g(self):
        self.assertConvertsTo(MeasurementUnit("test","t", 1e-3, UnitType.MASS),1,MeasurementUnit("test2","t2", 1e-3, UnitType.MASS),1)

    def test_convert_mg_to_g(self):
        self.assertConvertsTo(MeasurementUnit("test","t", 1e-6, UnitType.MASS),1,MeasurementUnit("test2","t2", 1e-3, UnitType.MASS),1e-3)

    def test_convert_g_to_mg(self):
        self.assertConvertsTo(MeasurementUnit("test","t", 1e-3, UnitType.MASS),1,MeasurementUnit("test2","t2", 1e-6, UnitType.MASS),1e3)

    def test_to_base_unit(self):
        unit = MeasurementUnit("test","t", 1e-1, UnitType.VOLUME)
        self.assertAlmostEqual(1e-1,unit.get_base_unit_amount(1))

    def test_convert_milm3_to_m3(self):
        self.assertConvertsTo(MeasurementUnit("test","t", 1e-3, UnitType.VOLUME),1,MeasurementUnit("test2","t2", 1, UnitType.VOLUME),1e-3)

    def test_convert_milm3_to_milm3(self):
        self.assertConvertsTo(MeasurementUnit("test","t", 1e-3, UnitType.VOLUME),1,MeasurementUnit("test2","t2", 1e-3, UnitType.VOLUME),1)

    def test_convert_microm3_to_milm3(self):
        self.assertConvertsTo(MeasurementUnit("test","t", 1e-6, UnitType.VOLUME),1,MeasurementUnit("test2","t2", 1e-3, UnitType.VOLUME),1e-3)

    def test_convert_milm3_to_microm3(self):
        self.assertConvertsTo(MeasurementUnit("test","t", 1e-3, UnitType.VOLUME),1,MeasurementUnit("test2","t2", 1e-6, UnitType.VOLUME),1e3)
