class BaseColumnCheck():
    ##################################################################################################
    # Constructor
    ##################################################################################################
    def __init__(self, column_name):
        self.column_name = column_name

    ##################################################################################################
    # Properties
    ##################################################################################################
    @property
    def column_name(self):
        return self._column_name

    @column_name.setter
    def column_name(self, value):
        self._column_name = value
        self._settings["column_name"] = value
