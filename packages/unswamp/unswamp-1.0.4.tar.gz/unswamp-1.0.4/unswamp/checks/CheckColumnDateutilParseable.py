from .base.BaseCheck import BaseCheck
from .base.BaseColumnCheck import BaseColumnCheck
from .base.BaseFunctionCheck import BaseFunctionCheck


class CheckColumnDateutilParseable(BaseCheck, BaseColumnCheck, BaseFunctionCheck):
    ##################################################################################################
    # Constructor
    ##################################################################################################
    def __init__(self, id, column_name):
        column_function_name = "check_column_dateutil_parseable"
        BaseCheck.__init__(self, id)
        BaseColumnCheck.__init__(self, column_name)
        BaseFunctionCheck.__init__(self, column_function_name)

    ##################################################################################################
    # Methods
    ##################################################################################################
    def _run(self, dataset):
        passed = self.column_function(dataset, self.column_name).all()
        message = f"All values in column '{self.column_name}' comply with the given function '{self.column_function_str}' and are dateutil parseable'!"
        if not passed:
            message = f"Not all values in column '{self.column_name}' comply with the given function '{self.column_function_str}' and are dateutil parseable'!"
        return passed, message
