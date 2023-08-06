from ..base.BaseCheck import BaseCheck
from ..base.BaseFunctionCheck import BaseFunctionCheck
from ..base.BaseRunExpectationCheck import BaseRunExpectationCheck
from ..base.BaseFunctionArgumentsCheck import BaseFunctionArgumentsCheck


class CheckCustomFunction(BaseCheck, BaseFunctionCheck, BaseRunExpectationCheck, BaseFunctionArgumentsCheck):
    ##################################################################################################
    # Constructor
    ##################################################################################################
    def __init__(self, check_id, function_name, expectation, function_arguments=None, meta_data=None):
        BaseCheck.__init__(self, check_id, meta_data, level="custom")
        BaseFunctionCheck.__init__(self, function_name)
        BaseRunExpectationCheck.__init__(self, expectation)
        BaseFunctionArgumentsCheck.__init__(self, function_arguments)

    ##################################################################################################
    # Methods
    ##################################################################################################
    def _run(self, dataset):
        passed = self.function(dataset, self.function_arguments) == self.expectation
        message = f"All values in column meet the custom function expectation!"
        if not passed:
            message = f"Not all values in column meet the custom function expectation!"
        return passed, message
