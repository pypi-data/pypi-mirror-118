from ..base.BaseCheck import BaseCheck
from ..base.BaseColumnCheck import BaseColumnCheck
from ..base.BaseValueCheck import BaseValueCheck


class CheckColumnFilterNone(BaseCheck, BaseColumnCheck, BaseValueCheck):
    ##################################################################################################
    # Constructor
    ##################################################################################################
    def __init__(self, check_id, column_name, column_value, meta_data=None):
        # TODO: make different column_name and value are in this case list and not string
        # TODO: check if name & value are of the same length
        BaseCheck.__init__(self, check_id, meta_data)
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
