from unswamp.checks.base.BaseCheck import BaseCheck
from unswamp.checks.base.BaseColumnCheck import BaseColumnCheck
from unswamp.checks.base.BaseValueCheck import BaseValueCheck
from unswamp.checks.base.BaseFunctionCheck import BaseFunctionCheck


class CheckColumnFunctionAll(BaseCheck, BaseColumnCheck, BaseValueCheck, BaseFunctionCheck):
    ##################################################################################################
    # Constructor
    ##################################################################################################
    def __init__(self, id, column_name, column_value, column_function_name, check_meta_data=None):
        BaseCheck.__init__(self, id, check_meta_data)
        BaseColumnCheck.__init__(self, column_name)
        BaseValueCheck.__init__(self, column_value)
        BaseFunctionCheck.__init__(self, column_function_name)

    ##################################################################################################
    # Methods
    ##################################################################################################

    def _run(self, dataset):
        passed = self.column_function(
            dataset, self.column_name, self.column_value).all()
        message = f"All values in column '{self.column_name}' comply with the given function '{self.column_function_str}' for value '{self.column_value}'!"
        if not passed:
            message = f"Not all values in column '{self.column_name}' comply with the given function '{self.column_function_str}' for value '{self.column_value}'!"
        return passed, message
