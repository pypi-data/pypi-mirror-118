from ..base.BaseCheck import BaseCheck
from ..base.BaseColumnCheck import BaseColumnCheck


class CheckColumnIsUnique(BaseCheck, BaseColumnCheck):
    ##################################################################################################
    # Constructor
    ##################################################################################################
    def __init__(self, check_id, column_name, meta_data=None):
        BaseCheck.__init__(self, check_id, meta_data)
        BaseColumnCheck.__init__(self, column_name)

    ##################################################################################################
    # Methods
    ##################################################################################################
    def _run(self, dataset):
        passed = dataset[self.column_name].is_unique
        message = f"All values in column '{self.column_name}' are unique!"
        if not passed:
            message = f"Not all values in column '{self.column_name}' are unique!"
        return passed, message
