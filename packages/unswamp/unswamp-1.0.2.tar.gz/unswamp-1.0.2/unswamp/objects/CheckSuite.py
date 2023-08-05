from .CheckRun import CheckRun


class CheckSuite:
    ##################################################################################################
    # Constructor
    ##################################################################################################
    def __init__(self, name, dataset, checks=None):
        self.name = name
        self.dataset = dataset
        if checks is None:
            self.checks = []
        else:
            self.checks = checks

    ##################################################################################################
    # Methods
    ##################################################################################################
    def add_check(self, check):
        self.checks.append(check)

    def run(self):
        run = CheckRun()
        run.run(self.dataset, self.checks)
        return run

    ##################################################################################################
    # Properties
    ##################################################################################################
    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def dataset(self):
        return self._dataset

    @dataset.setter
    def dataset(self, value):
        self._dataset = value

    @property
    def checks(self):
        return self._checks

    @checks.setter
    def checks(self, value):
        self._checks = value
