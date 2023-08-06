class BaseValueCheck():
    ##################################################################################################
    # Constructor
    ##################################################################################################
    def __init__(self, column_value):
        self.column_value = column_value

    ##################################################################################################
    # Properties
    ##################################################################################################
    @property
    def column_value(self):
        return self._column_value

    @column_value.setter
    def column_value(self, value):
        self._column_value = value
        self._settings["column_value"] = value
