from .BaseColumnCheck import BaseColumnCheck
from .Functions import Functions


class CheckColumnMatchStrftime(BaseColumnCheck):
    ##################################################################################################
    # Constructor
    ##################################################################################################
    def __init__(self, id, column_name, datetime_format):
        BaseColumnCheck.__init__(self, id, column_name)
        self.datetime_format = datetime_format
        self.settings["datetime_format"] = self.datetime_format
        
        self.column_function = Functions.check_column_match_strftime_format
        self.settings["column_function"] = self.column_function_str

    ##################################################################################################
    # Methods
    ##################################################################################################
    def _run(self, dataset):
        passed = self._column_function(dataset, self.column_name, self.datetime_format).all()
        message = f"All values in column '{self.column_name}' comply with the given function '{self.column_function_str}' for datetime format '{self.datetime_format}'!"
        if not passed:
            message = f"Not all values in column '{self.column_name}' comply with the given function '{self.column_function_str}' for datetime format '{self.datetime_format}'!"
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

    @property
    def datetime_format(self):
        return self._datetime_format

    @datetime_format.setter
    def datetime_format(self, value):
        self._datetime_format = value
