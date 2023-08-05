from .BaseColumnCheck import BaseColumnCheck
from .Functions import Functions


class CheckColumnDateutilParseable(BaseColumnCheck):
    ##################################################################################################
    # Constructor
    ##################################################################################################
    def __init__(self, id, column_name):
        BaseColumnCheck.__init__(self, id, column_name)
        self.column_function_name = "check_column_dateutil_parseable"
        self.settings["column_function"] = self.column_function_str

    ##################################################################################################
    # Methods
    ##################################################################################################
    def _run(self, dataset):
        passed = self.column_function(dataset, self.column_name).all()
        message = f"All values in column '{self.column_name}' comply with the given function '{self.column_function_str}' and are dateutil parseable'!"
        if not passed:
            message = f"Not all values in column '{self.column_name}' comply with the given function '{self.column_function_str}' and are dateutil parseable'!"
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
