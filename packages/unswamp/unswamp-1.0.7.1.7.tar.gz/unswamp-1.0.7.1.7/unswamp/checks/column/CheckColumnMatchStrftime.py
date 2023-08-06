from ..base.BaseCheck import BaseCheck
from ..base.BaseColumnCheck import BaseColumnCheck
from ..base.BaseFunctionCheck import BaseFunctionCheck


class CheckColumnMatchStrftime(BaseCheck, BaseColumnCheck, BaseFunctionCheck):
    ##################################################################################################
    # Constructor
    ##################################################################################################
    def __init__(self, check_id, column_name, datetime_format, meta_data=None):
        function_name = "check_column_match_strftime_format"

        BaseCheck.__init__(self, check_id, meta_data)
        BaseColumnCheck.__init__(self, column_name)
        BaseFunctionCheck.__init__(self, function_name)
        
        self.datetime_format = datetime_format

    ##################################################################################################
    # Methods
    ##################################################################################################
    def _run(self, dataset):
        passed = self.function(dataset, self.column_name, self.datetime_format).all()
        message = f"All values in column '{self.column_name}' comply with the given function '{self.function_str}' for datetime format '{self.datetime_format}'!"
        if not passed:
            message = f"Not all values in column '{self.column_name}' comply with the given function '{self.function_str}' for datetime format '{self.datetime_format}'!"
        return passed, message

    ##################################################################################################
    # Properties
    ##################################################################################################
    datetime_format = None
