class BaseFunctionArgumentsCheck():
    ##################################################################################################
    # Constructor
    ##################################################################################################
    def __init__(self, function_arguments=None):
        if function_arguments is None:
            function_arguments = {}
        self.function_arguments = function_arguments

    ##################################################################################################
    # Properties
    ##################################################################################################
    @property
    def function_arguments(self):
        return self._function_arguments

    @function_arguments.setter
    def function_arguments(self, value):
        self._function_arguments = value
