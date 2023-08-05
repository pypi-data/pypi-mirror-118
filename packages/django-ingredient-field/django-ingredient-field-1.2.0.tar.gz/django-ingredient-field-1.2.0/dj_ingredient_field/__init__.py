__version__ = "1.2.0"

from .enums import UnitType, IngredientName
from .exceptions import InvalidConversionException
from .settings import INGREDIENT_UNITS, VOLUME_BASE_UNIT, MASS_BASE_UNIT, EMPTY_UNIT, INGREDIENT_NAMES
from django.db import models
from numbers import Number 
from typing import Any
import math 


class Ingredient():
    format_string="{name}"

    def __init__(self, name) -> None:
        self.name = str(name)

    def __str__(self):
        return str(self.name)
        
    def __repr__(self) -> str:
        return self.__str__()

    def __eq__(self, o: object) -> bool:
        return isinstance(o, Ingredient) and o.name == self.name

class MeasurementUnit():
    """
        A class containing logic for cooking measurement units which have a 'base' unit.
    """
    base_volume_unit=None
    base_mass_unit=None

    def __init__(self, name : str, symbol : str, conversion_rate : Number, unit_type : UnitType, is_base_unit=False) -> None:
        """ 
        Creates a new MeasurementUnit instance

        :param str name: The full name of the unit, e.g.: Millilitre, Litre, Gram
        :param str symbol: The shorthand for the name of the unit, e.g.: ml, L, g
        :param base_unit: The 'base_unit', if None, then this is unit itself is a base for other units
        :type base_unit: MeasurementUnit or None
        :param bool is_base_unit: Whether this unit is a base_unit
        :param Number conversion_rate: The conversion rate from the base unit (i.e. fraction of the base unit)
        """
        self.name = str(name)
        self.conversion_rate = conversion_rate
        self.symbol = symbol
        self.unit_type = unit_type

        if not self.unit_type:
            raise ValueError("unit_type must be provided")
            
        self.base_unit = None
        if self.unit_type == UnitType.VOLUME and not is_base_unit:
            self.base_unit = MeasurementUnit.base_volume_unit if MeasurementUnit.base_volume_unit else MeasurementUnit(**VOLUME_BASE_UNIT)
            MeasurementUnit.base_volume_unit = self.base_unit
        if self.unit_type == UnitType.MASS and not is_base_unit:
            self.base_unit = MeasurementUnit.base_mass_unit if MeasurementUnit.base_mass_unit  else MeasurementUnit(**MASS_BASE_UNIT)
            MeasurementUnit.base_mass_unit = self.base_unit

    def __str__(self):
        return str(self.name)
    
    def __repr__(self) -> str:
        return self.__str__()

    def __eq__(self, o: object) -> bool:
        return isinstance(o, MeasurementUnit) and self.name == o.name and math.isclose(self.conversion_rate,o.conversion_rate) and self.symbol == o.symbol and self.base_unit == o.base_unit and self.unit_type == o.unit_type

    def get_base_unit_amount(self, amount) -> Number:
        """ 
        Returns the equivalent base unit
        """
        return amount * self.conversion_rate

    def convert_to(self, amount, o : 'MeasurementUnit', density=1.0) -> Number:

        # calculate the conversion rate between mass volume units
        cross_conversion_rate = 1.0
        if o.unit_type != self.unit_type:
            if o.unit_type == UnitType.VOLUME:
                cross_conversion_rate = 1.0 / density
            elif o.unit_type == UnitType.MASS:
                cross_conversion_rate = density
            else:
                raise ValueError("The unit_type {} cannot be a target of unit conversion".format(o.unit_type))
        elif o.base_unit != self.base_unit or not self.base_unit or not o.base_unit:
            # If the unit type is the same but the base unit is different
            raise InvalidConversionException(self,o,"different base_units: {this_base} != {other_base}".format(
                this_base=o.base_unit,
                other_base=o.base_unit)) 
            
        # the ratio of this conversion rate to the other gives 
        # the new conversion rate relative to base unit
        return cross_conversion_rate * (self.conversion_rate / o.conversion_rate) * amount

class IngredientField(models.CharField):
    """
    An ingredient field for Django models 
    which provides over 3500 cooking ingredients

    Dataset from https://dominikschmidt.xyz/simplified-recipes-1M/
    """
    description = "A cooking ingredient"

    def __init__(self, *args, **kwargs):
        
        kwargs['choices'] = INGREDIENT_NAMES
        kwargs['max_length'] = 50 # a bit of leeway (current max chars is 39)

        super().__init__(*args, **kwargs)

    def clean(self, value, model_instance):
        """
            Validates the string representation, since validate checks against the choice list,
            and generates clean python object
        """
        str_value = str(value) 
        self.validate(str_value, model_instance)
        self.run_validators(str_value)
        value = self.to_python(value)
        return value

    def deconstruct(self):
        """
        Removes choices and max_length keywords as these 
        are not to be user editable
        """
        name, path, args, kwargs = super().deconstruct()
        del kwargs['choices']
        del kwargs['max_length']

        return name, path, args, kwargs 

    def from_db_value(self, value, expression, connection):
        if value is None:
            return value
        else:
            return Ingredient(value)
            
    def to_python(self, value: Any) -> Any:
        if isinstance(value, Ingredient):
            return value
        elif value is None:
            return value
        else:
            return Ingredient(value)

    def get_prep_value(self, value : Ingredient):
        return str(value)


class MeasurementUnitField(models.CharField):
    """
    A field for picking measurement options for an ingredient
    """
    description = "A cooking measurement unit"
    units = [(key,key) for key in INGREDIENT_UNITS.keys()]

    def __init__(self, *args, **kwargs):

        kwargs['choices'] = MeasurementUnitField.units
        kwargs['max_length'] = max([len(x) for x,y in MeasurementUnitField.units])

        super().__init__(*args, **kwargs)

    def clean(self, value, model_instance):
        """
            Validates the string representation, since validate checks against the choice list,
            and generates clean python object
        """
        str_value = str(value)
        value = self.to_python(value)
        self.validate(str_value, model_instance)
        self.run_validators(str_value)

        return value

    def deconstruct(self):
        """
        Removes choices and max_length keywords as these 
        are not to be user editable
        """
        name, path, args, kwargs = super().deconstruct()
        del kwargs['choices']
        del kwargs['max_length']

        return name, path, args, kwargs 

    def get_setting_for_unit_name_or_default(self, value):
        valid_unit = INGREDIENT_UNITS.get(value, None)
        if not valid_unit:
            valid_unit = EMPTY_UNIT.copy()
            valid_unit['name'] = value
        return valid_unit

    def from_db_value(self, value, expression, connection):
        if value is None:
            return value
        else:
            return MeasurementUnit(**self.get_setting_for_unit_name_or_default(value))
            
    def to_python(self, value: Any) -> Any:
        if isinstance(value, MeasurementUnit):
            return value
        elif value is None:
            return value
        else:
            return MeasurementUnit(**self.get_setting_for_unit_name_or_default(value))

    def get_prep_value(self, value : MeasurementUnit):
        return str(value)