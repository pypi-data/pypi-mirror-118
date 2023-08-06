'''
This is the object that represents:
- SQL INT
- Python int
'''

from ._ValueType import _ValueType

class Int(_ValueType):
    SQL_TYPE = 'INTEGER'
    PYTHON_TYPE = int

    def __init__(self, **options) -> None:
        self.options = self._get_options(options)

    def _get_options(self, options:tuple):
        options_string = ''
        if 'NOT_NULL' in options and options['NOT_NULL']:
            options_string += 'NOT NULL '
        if 'AUTO_INCREMENT' in options and options['AUTO_INCREMENT']:
            options_string += 'AUTO_INCREMENT '
        if 'PRIMARY_KEY' in options and options['PRIMARY_KEY']:
            options_string += 'PRIMARY KEY '
        return options_string.strip()