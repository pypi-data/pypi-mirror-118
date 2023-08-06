from ..base.BaseCheck import BaseCheck
from ..base.BaseColumnCheck import BaseColumnCheck
from ..base.BaseValueCheck import BaseValueCheck
from ..base.BaseFunctionCheck import BaseFunctionCheck


class CheckColumnFunctionAll(BaseCheck, BaseColumnCheck, BaseValueCheck, BaseFunctionCheck):
    ##################################################################################################
    # Constructor
    ##################################################################################################
    def __init__(self, check_id, column_name, column_value, function_name, meta_data=None):
        BaseCheck.__init__(self, check_id, meta_data)
        BaseColumnCheck.__init__(self, column_name)
        BaseValueCheck.__init__(self, column_value)
        BaseFunctionCheck.__init__(self, function_name)

    ##################################################################################################
    # Methods
    ##################################################################################################

    def _run(self, dataset):
        passed = self.function(dataset, self.column_name, self.column_value).all()
        message = f"All values in column '{self.column_name}' comply with the given function '{self.function_str}' for value '{self.column_value}'!"
        if not passed:
            message = f"Not all values in column '{self.column_name}' comply with the given function '{self.function_str}' for value '{self.column_value}'!"
        return passed, message
