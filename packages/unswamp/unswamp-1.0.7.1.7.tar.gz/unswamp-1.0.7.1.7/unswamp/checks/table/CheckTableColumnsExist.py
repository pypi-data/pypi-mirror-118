from ..base.BaseCheck import BaseCheck


class CheckTableColumnsExist(BaseCheck):
    ##################################################################################################
    # Constructor
    ##################################################################################################
    def __init__(self, check_id, table_columns, check_meta_data=None):
        BaseCheck.__init__(self, check_id, check_meta_data, "table")
        self.table_columns = table_columns

    ##################################################################################################
    # Methods
    ##################################################################################################
    def _run(self, dataset):
        df_cols = set(dataset.columns)
        diff = list(set(self.table_columns).difference(df_cols))
        passed = len(diff) == 0
        message = f"All provided columns '{self.table_columns}' exist in dataset!"
        if not passed:
            message = f"The following column(s) are missing in the dataset '{diff}'!"
        return passed, message

    ##################################################################################################
    # Properties
    ##################################################################################################
    table_columns = []
