'''
This is the object that represents:
- SQL TINYINT/BOOLEAN
- Python bool
'''

from ._ValueType import _ValueType

class Bool(_ValueType):
    SQL_TYPE = 'BOOLEAN'
    PYTHON_TYPE = bool

    def __init__(self, **options) -> None:
        self.options = self._get_options(options)