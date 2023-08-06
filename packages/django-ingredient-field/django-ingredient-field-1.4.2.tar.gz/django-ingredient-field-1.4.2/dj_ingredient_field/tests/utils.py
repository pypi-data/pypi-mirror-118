from numbers import Number
from dj_ingredient_field import MeasurementUnit
from django.test import TestCase

class TestCaseWithUtils(TestCase):
    
    
    def assertConvertsTo(self, unitA : MeasurementUnit, amountA : Number, unitB : MeasurementUnit, amountB : Number, density=1.0, places=7,message="Unit converts to wrong amount of target unit"):
        """ Asserts that the first unit converts the first amount to the target amount when converting to the target unit

        :param MeasurementUnit unitA: the first unit
        :param Number amountA: the first amount
        :type MeasurementUnit unitB: the target unit
        :param Number amountB: target unit
        """
        self.assertAlmostEqual(amountB, unitA.convert_to(amountA, unitB, density), places ,msg=message)
        
    def assertConversionRaisesException(self, unitA : MeasurementUnit, amountA : Number, unitB : MeasurementUnit, exception : Exception, density=1.0,message="Conversion should raise error"):
        """ Asserts that the first unit converts the first amount to the target amount when converting to the target unit

        :param MeasurementUnit unitA: the first unit
        :param Number amountA: the first amount
        :type MeasurementUnit unitB: the target unit
        :param Number amountB: target unit
        """
        call = lambda: unitA.convert_to(amountA, unitB, density)
        self.assertRaises(exception,call)
        