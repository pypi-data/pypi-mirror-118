from unswamp.checks.general.BaseCheck import BaseCheck
from unswamp.checks.general.BaseColumnCheck import BaseColumnCheck


class CheckColumnIsNull(BaseCheck, BaseColumnCheck):
    ##################################################################################################
    # Constructor
    ##################################################################################################
    def __init__(self, id, column_name, check_meta_data=None):
        BaseCheck.__init__(self, id, check_meta_data)
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
