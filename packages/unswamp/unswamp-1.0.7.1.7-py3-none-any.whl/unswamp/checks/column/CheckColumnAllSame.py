from ..base.BaseCheck import BaseCheck
from ..base.BaseColumnCheck import BaseColumnCheck
from ..base.BaseValueCheck import BaseValueCheck


class CheckColumnAllSame(BaseCheck, BaseColumnCheck, BaseValueCheck):
    ##################################################################################################
    # Constructor
    ##################################################################################################
    def __init__(self, check_id, column_name, column_value=None, meta_data=None):
        BaseCheck.__init__(self, check_id, meta_data)
        BaseColumnCheck.__init__(self, column_name)
        BaseValueCheck.__init__(self, column_value)

    ##################################################################################################
    # Methods
    ##################################################################################################
    def _run(self, dataset):
        if self.column_value is None:
            passed = dataset[self.column_name].nunique() == 1
            message = f"All values in column '{self.column_name}' are the same!"
            if not passed:
                message = f"Not all values in column '{self.column_name}' are the same!"
            return passed, message
        else:
            passed = (dataset[self.column_name] == self.column_value).all()
            message = f"All values in column '{self.column_name}' have the value '{self.column_value}'!"
            if not passed:
                message = f"Not all values in column '{self.column_name}' have the value '{self.column_value}'!"
            return passed, message
