'''
This represents a record/row in a table
It is mostly used as a parameter or attribute in
pythonmysequel.Table and pythonmysequel.Connection
'''

from .Table import Table
from .values import *
from .values import _ValueType

class Row:
    def __init__(self,
                table:Table, **values) -> None:
        self.table = table
        self.values = values

        self._check_value_type()

    def _check_value_type(self):
        '''Make sure row values conform to table columns'''
        table_value = self.table.values
        for key, value, column_name in zip(self.values.keys(), self.values.values(), self.values):
            python_value_type = table_value[key].PYTHON_TYPE
            inputted_value_type = type(value)

            if inputted_value_type !=  python_value_type:
                raise ValueError(f'Incorrect value type {inputted_value_type} for column "{column_name}" {python_value_type}')


    def _add_value(self, value:dict[str: _ValueType]):
        '''Add column data'''
        for k, v in value.items():
            self.values[k] = v
    
    def __str__(self) -> str:
        return str(self.values)