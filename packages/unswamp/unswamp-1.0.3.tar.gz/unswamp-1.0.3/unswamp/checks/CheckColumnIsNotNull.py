from .BaseColumnCheck import BaseColumnCheck


class CheckColumnIsNotNull(BaseColumnCheck):
    ##################################################################################################
    # Constructor
    ##################################################################################################
    def __init__(self, id, column_name):
        BaseColumnCheck.__init__(self, id, column_name)

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
