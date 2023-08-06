from unswamp.checks.general.BaseCheck import BaseCheck
from unswamp.checks.general.BaseColumnCheck import BaseColumnCheck


class CheckColumnIsNotNull(BaseCheck, BaseColumnCheck):
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
        count = dataset[self.column_name].isna().sum()
        passed = count == 0
        message = f"All values in column '{self.column_name}' are not null!"
        if not passed:
            message = (
                f"There are '{count}' non null values in column '{self.column_name}'!"
            )
        return passed, message
