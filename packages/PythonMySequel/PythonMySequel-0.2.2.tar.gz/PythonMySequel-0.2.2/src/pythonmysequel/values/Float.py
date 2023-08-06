'''
This is the object that represents:
- SQL FLOAT
- Python float
'''

from ._ValueType import _ValueType

class Float(_ValueType):
    SQL_TYPE = 'FLOAT'
    PYTHON_TYPE = float

    def __init__(self, **options) -> None:
        self.options = self._get_options(options)