from .base.BaseCheck import BaseCheck
from .base.BaseColumnCheck import BaseColumnCheck
from .base.BaseValueCheck import BaseValueCheck


class CheckColumnFilterNone(BaseCheck, BaseColumnCheck, BaseValueCheck):
    ##################################################################################################
    # Constructor
    ##################################################################################################
    def __init__(self, id, column_name, column_value, check_meta_data=None):
        BaseCheck.__init__(self, id, check_meta_data)
        BaseColumnCheck.__init__(self, column_name)
        BaseValueCheck.__init__(self, column_value)

    ##################################################################################################
    # Methods
    ##################################################################################################

    def _run(self, dataset):
        where = ""
        df = dataset.copy(deep=True)
        for pos in range(len(self.column_name)):
            col = self.column_name[pos]
            val = self.column_value[pos]
            where += f"'{col}' == '{val}' &"
            df = df[df[col] == val]
        where = where[:-2]

        passed = df.shape[0] == 0
        message = f"None of the records matches the filter {where}!"
        if not passed:
            message = f"'{df.shape[0]}' of the records matches the filter {where}!"
        return passed, message
