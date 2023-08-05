from .BaseColumnValueCheck import BaseColumnValueCheck


class CheckColumnAllSame(BaseColumnValueCheck):
    ##################################################################################################
    # Constructor
    ##################################################################################################
    def __init__(self, id, column_name, column_value=None):
        BaseColumnValueCheck.__init__(self, id, column_name, column_value)

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
