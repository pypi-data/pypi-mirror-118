class BaseFunctionArgumentsCheck():
    ##################################################################################################
    # Constructor
    ##################################################################################################
    def __init__(self, check_function_arguments=None):
        if check_function_arguments is None:
            check_function_arguments = {}
        self.check_function_arguments = check_function_arguments

    ##################################################################################################
    # Properties
    ##################################################################################################
    @property
    def check_function_arguments(self):
        return self._check_function_arguments

    @check_function_arguments.setter
    def check_function_arguments(self, value):
        self._check_function_arguments = value
        self._settings["check_function_arguments"] = value
