'''
This class represents a table in the database
It is mostly used as a parameter for pythonmysequel.Connection methods
'''

from pythonmysequel.values import _ValueType

class Table:
    def __init__(self,
                table_name:str, **values:_ValueType) -> None:
        self.table_name = table_name
        self.values = values
        self.primary_key = None
        self._has_primary_key()

    def _has_primary_key(self) -> bool:
        '''Returns whether or not there is a primary key column (bool)'''
        for key, value in self.values.items():
            if 'PRIMARY KEY' in value.options:
                self.primary_key = key
                return True
        return False