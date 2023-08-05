from .BaseColumnCheck import BaseColumnCheck


class CheckColumnIsNull(BaseColumnCheck):
    ##################################################################################################
    # Constructor
    ##################################################################################################
    def __init__(self, id, column_name):
        BaseColumnCheck.__init__(self, id, column_name)

    ##################################################################################################
    # Methods
    ##################################################################################################
    def _run(self, dataset):
        passed = dataset[self.column_name].isna().all()
        message = f"All values in column '{self.column_name}' are null!"
        if not passed:
            message = f"Not all values in column '{self.column_name}' are null!"
        return passed, message
