from .BaseColumnCheck import BaseColumnCheck


class CheckColumnIsUnique(BaseColumnCheck):
    ##################################################################################################
    # Constructor
    ##################################################################################################
    def __init__(self, id, column_name):
        BaseColumnCheck.__init__(self, id, column_name)

    ##################################################################################################
    # Methods
    ##################################################################################################
    def _run(self, dataset):
        passed = dataset[self.column_name].is_unique
        message = f"All values in column '{self.column_name}' are unique!"
        if not passed:
            message = f"Not all values in column '{self.column_name}' are unique!"
        return passed, message
