from .base.BaseCheck import BaseCheck
from .base.BaseFunctionCheck import BaseFunctionCheck
from .base.BaseRunExpectationCheck import BaseRunExpectationCheck
from .base.BaseFunctionArgumentsCheck import BaseFunctionArgumentsCheck


class CheckColumnFunctionCustom(BaseCheck, BaseFunctionCheck, BaseRunExpectationCheck, BaseFunctionArgumentsCheck):
    ##################################################################################################
    # Constructor
    ##################################################################################################
    def __init__(self, id, column_function_name, check_run_expectation, check_function_arguments=None, check_meta_data=None):
        BaseCheck.__init__(self, id, check_meta_data)
        BaseFunctionCheck.__init__(self, column_function_name)
        BaseRunExpectationCheck.__init__(self, check_run_expectation)
        BaseFunctionArgumentsCheck.__init__(self, check_function_arguments)

    ##################################################################################################
    # Methods
    ##################################################################################################

    def _run(self, dataset):
        passed = self.column_function(dataset, self.check_function_arguments) == self.check_run_expectation
        message = f"All values in column meet the custom function expectation!"
        if not passed:
            message = f"Not all values in column meet the custom function expectation!"
        return passed, message
