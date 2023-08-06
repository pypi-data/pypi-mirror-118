from unswamp.checks.general.BaseCheck import BaseCheck
from unswamp.checks.general.BaseColumnCheck import BaseColumnCheck
from unswamp.checks.general.BaseFunctionCheck import BaseFunctionCheck


class CheckColumnMatchStrftime(BaseCheck, BaseColumnCheck, BaseFunctionCheck):
    ##################################################################################################
    # Constructor
    ##################################################################################################
    def __init__(self, id, column_name, datetime_format, check_meta_data=None):
        column_function_name = "check_column_match_strftime_format"

        BaseCheck.__init__(self, id, check_meta_data)
        BaseColumnCheck.__init__(self, column_name)
        BaseFunctionCheck.__init__(self, column_function_name)
        
        self.datetime_format = datetime_format

    ##################################################################################################
    # Methods
    ##################################################################################################
    def _run(self, dataset):
        passed = self.column_function(dataset, self.column_name, self.datetime_format).all()
        message = f"All values in column '{self.column_name}' comply with the given function '{self.column_function_str}' for datetime format '{self.datetime_format}'!"
        if not passed:
            message = f"Not all values in column '{self.column_name}' comply with the given function '{self.column_function_str}' for datetime format '{self.datetime_format}'!"
        return passed, message

    ##################################################################################################
    # Properties
    ##################################################################################################
    @property
    def datetime_format(self):
        return self._datetime_format

    @datetime_format.setter
    def datetime_format(self, value):
        self._datetime_format = value
        self._settings["datetime_format"] = value
