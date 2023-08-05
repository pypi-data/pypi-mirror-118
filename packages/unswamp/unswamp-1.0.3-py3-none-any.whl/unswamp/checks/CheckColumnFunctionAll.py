from .BaseColumnValueCheck import BaseColumnValueCheck
from .Functions import Functions


class CheckColumnFunctionAll(BaseColumnValueCheck):
    ##################################################################################################
    # Constructor
    ##################################################################################################
    def __init__(self, id, column_name, column_value, column_function_name):
        BaseColumnValueCheck.__init__(self, id, column_name, column_value)
        self.column_function_name = column_function_name
        self.settings["column_function_name"] = self.column_function_name

    ##################################################################################################
    # Methods
    ##################################################################################################
    def _run(self, dataset):
        passed = self.column_function(dataset, self.column_name, self.column_value).all()
        message = f"All values in column '{self.column_name}' comply with the given function '{self.column_function_str}' for value '{self.column_value}'!"
        if not passed:
            message = f"Not all values in column '{self.column_name}' comply with the given function '{self.column_function_str}' for value '{self.column_value}'!"
        return passed, message

    ##################################################################################################
    # Properties
    ##################################################################################################
    @property
    def column_function_name(self):
        return self._column_function_name

    @column_function_name.setter
    def column_function_name(self, value):
        self._column_function_name = value

    @property
    def column_function(self):
        func = Functions.lambda_functions[self.column_function_name]
        return func

    @property
    def column_function_str(self):
        func = self.column_function
        desc = Functions.get_string(func)
        return desc
