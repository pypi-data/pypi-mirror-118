from ..base.BaseCheck import BaseCheck
from ..base.BaseColumnCheck import BaseColumnCheck
from ..base.BaseFunctionCheck import BaseFunctionCheck


class CheckColumnDateutilParseable(BaseCheck, BaseColumnCheck, BaseFunctionCheck):
    ##################################################################################################
    # Constructor
    ##################################################################################################
    def __init__(self, check_id, column_name, meta_data=None):
        function_name = "check_column_dateutil_parseable"
        BaseCheck.__init__(self, check_id, meta_data)
        BaseColumnCheck.__init__(self, column_name)
        BaseFunctionCheck.__init__(self, function_name)

    ##################################################################################################
    # Methods
    ##################################################################################################
    def _run(self, dataset):
        passed = self.function(dataset, self.column_name).all()
        message = f"All values in column '{self.column_name}' comply with the given function '{self.function_str}' and are dateutil parseable'!"
        if not passed:
            message = f"Not all values in column '{self.column_name}' comply with the given function '{self.function_str}' and are dateutil parseable'!"
        return passed, message
