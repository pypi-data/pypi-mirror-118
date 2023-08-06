from ..base.BaseCheck import BaseCheck
from ..base.BaseColumnCheck import BaseColumnCheck


class CheckColumnIsNull(BaseCheck, BaseColumnCheck):
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
        passed = dataset[self.column_name].isna().all()
        message = f"All values in column '{self.column_name}' are null!"
        if not passed:
            message = f"Not all values in column '{self.column_name}' are null!"
        return passed, message
