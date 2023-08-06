'''
This is the object that represents:
- SQL VARCHAR
- Python str
'''

from ._ValueType import _ValueType

class String(_ValueType):
    PYTHON_TYPE = str

    def __init__(self, column_limit:int = 255, **options) -> None:     
        self.SQL_TYPE = f'VARCHAR({column_limit})'   
        self.column_limit = column_limit
        self.options = self._get_options(options)