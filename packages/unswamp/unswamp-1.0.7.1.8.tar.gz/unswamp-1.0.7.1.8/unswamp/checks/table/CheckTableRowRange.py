from ..base.BaseCheck import BaseCheck


class CheckTableRowRange(BaseCheck):
    ##################################################################################################
    # Constructor
    ##################################################################################################
    def __init__(self, check_id, min_rows=0, max_rows=0, meta_data=None):
        BaseCheck.__init__(self, check_id, meta_data, "table")
        self.min_rows = min_rows
        self.max_rows = max_rows

    ##################################################################################################
    # Methods
    ##################################################################################################

    def _run(self, dataset):
        rows = dataset.shape[0]
        passed = rows >= self.min_rows and rows <= self.max_rows
        message = f"Found '#{rows}' what is between '{self.min_rows}' and '{self.max_rows}'!"
        if not passed:
            message = f"Found '#{rows}' but expected where min '{self.min_rows}' and max '{self.max_rows}'!"
        return passed, message

    ##################################################################################################
    # Properties
    ##################################################################################################
    min_rows = 0
    max_rows = 0
