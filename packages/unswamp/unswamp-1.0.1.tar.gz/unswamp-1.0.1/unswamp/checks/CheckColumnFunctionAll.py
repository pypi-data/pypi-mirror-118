from .BaseColumnValueCheck import BaseColumnValueCheck
from .Functions import Functions


class CheckColumnFunctionAll(BaseColumnValueCheck):
    ##################################################################################################
    # Constructor
    ##################################################################################################
    def __init__(self, id, column_name, column_value, column_function):
        BaseColumnValueCheck.__init__(self, id, column_name, column_value)
        self.column_function = column_function
        self.settings["column_function"] = self.column_function_str

    ##################################################################################################
    # Methods
    ##################################################################################################
    def _run(self, dataset):
        passed = self._column_function(
            dataset, self.column_name, self.column_value
        ).all()
        message = f"All values in column '{self.column_name}' comply with the given function '{self.column_function_str}' for value '{self.column_value}'!"
        if not passed:
            message = f"Not all values in column '{self.column_name}' comply with the given function '{self.column_function_str}' for value '{self.column_value}'!"
        return passed, message

    ##################################################################################################
    # Properties
    ##################################################################################################
    @property
    def column_function(self):
        return self._column_function

    @column_function.setter
    def column_function(self, value):
        self._column_function = value

    @property
    def column_function_str(self):
        desc = Functions.get_string(self.column_function)
        return desc
