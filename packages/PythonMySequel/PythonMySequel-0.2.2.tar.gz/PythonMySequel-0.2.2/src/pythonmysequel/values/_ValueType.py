'''
This is the base class that pythonmysequel.values.* inherit from
It contains:
- SQL value type
- Python value type
- SQL value options
'''

class _ValueType:

    def get_SQL_value(self):
        return f'{self.SQL_TYPE} {self.options}'.strip()
    
    def _get_options(self, options:tuple):
        options_string = ''
        if 'NOT_NULL' in options and options['NOT_NULL']:
            options_string += 'NOT NULL '
        return options_string.strip()