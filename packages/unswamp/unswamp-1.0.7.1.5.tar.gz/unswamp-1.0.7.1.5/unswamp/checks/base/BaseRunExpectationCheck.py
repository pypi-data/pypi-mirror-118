class BaseRunExpectationCheck():
    ##################################################################################################
    # Constructor
    ##################################################################################################
    def __init__(self, check_run_expectation):
        self.check_run_expectation = check_run_expectation

    ##################################################################################################
    # Properties
    ##################################################################################################
    @property
    def check_run_expectation(self):
        return self._check_run_expectation

    @check_run_expectation.setter
    def check_run_expectation(self, value):
        self._check_run_expectation = value
        self._settings["check_run_expectation"] = value
