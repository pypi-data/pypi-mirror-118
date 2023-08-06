from ..Functions import Functions


class BaseFunctionCheck():
    ##################################################################################################
    # Constructor
    ##################################################################################################

    def __init__(self, function_name):
        self.function_name = function_name
        self.function_str = Functions.get_string(self.function)

    ##################################################################################################
    # Properties
    ##################################################################################################
    function_name = None
    function_str = None

    ##################################################################################################
    # ReadOnly Property
    ##################################################################################################
    @property
    def function(self):
        fx = Functions.lambda_functions[self.function_name]
        return fx
