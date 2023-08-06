from unswamp.checks.Functions import Functions


class BaseFunctionCheck():
    ##################################################################################################
    # Constructor
    ##################################################################################################
    def __init__(self, column_function_name):
        self.column_function_name = column_function_name

    ##################################################################################################
    # Properties
    ##################################################################################################
    @property
    def column_function_name(self):
        return self._column_function_name

    @column_function_name.setter
    def column_function_name(self, value):
        self._column_function_name = value
        self._settings["column_function_name"] = value
        self._settings["column_function_str"] = self.column_function_str

    @property
    def column_function(self):
        func = Functions.lambda_functions[self.column_function_name]
        return func

    @property
    def column_function_str(self):
        func = self.column_function
        desc = Functions.get_string(func)
        return desc
