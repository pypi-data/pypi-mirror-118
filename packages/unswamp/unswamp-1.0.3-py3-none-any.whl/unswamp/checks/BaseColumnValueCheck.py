from .BaseColumnCheck import BaseColumnCheck

class BaseColumnValueCheck(BaseColumnCheck):
    ##################################################################################################
    # Constructor
    ##################################################################################################
    def __init__(self, id, column_name, column_value):
        BaseColumnCheck.__init__(self, id, column_name)
        self.column_value = column_value
        self._settings["column_value"] = column_value

    ##################################################################################################
    # Properties
    ##################################################################################################
    @property
    def column_value(self):
        return self._column_value

    @column_value.setter
    def column_value(self, value):
        self._column_value = value
