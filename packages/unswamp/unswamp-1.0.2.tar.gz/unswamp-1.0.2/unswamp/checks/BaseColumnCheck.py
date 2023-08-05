from .BaseCheck import BaseCheck

class BaseColumnCheck(BaseCheck):
    ##################################################################################################
    # Constructor
    ##################################################################################################
    def __init__(self, id, column_name):
        BaseCheck.__init__(self, id)
        self.column_name = column_name
        self._settings["column_name"] = column_name

    ##################################################################################################
    # Properties
    ##################################################################################################
    @property
    def column_name(self):
        return self._column_name

    @column_name.setter
    def column_name(self, value):
        self._column_name = value
