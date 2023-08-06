

class InvalidConversionException(Exception):
    def __init__(self, unit_from, unit_to, reason, *args) -> None:
        self.unit_from = unit_from
        self.unit_to = unit_to
        self.message = reason
        super().__init__(self,*args)

    def __str__(self) -> str:
        return 'Invalid conversion: {unit_from} -> {unit_to}: {reason}'.format(unit_from=self.unit_from,
            unit_to=self.unit_to, 
            reason=self.message)

class ParseError(Exception):
    pass