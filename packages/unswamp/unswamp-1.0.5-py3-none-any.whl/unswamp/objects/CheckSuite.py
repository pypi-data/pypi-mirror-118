from .base.SerializableObject import SerializableObject
from .CheckRun import CheckRun


class CheckSuite(SerializableObject):
    ##################################################################################################
    # Constructor
    ##################################################################################################
    def __init__(self, name, checks=None):
        SerializableObject.__init__(self)
        self.name = name
        if checks is None:
            checks = []
        self.checks = checks

    ##################################################################################################
    # Methods
    ##################################################################################################
    def add_check(self, check):
        self.checks.append(check)

    def run(self, dataset):
        run = CheckRun()
        run.run(dataset, self.checks)
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
    def checks(self):
        return self._checks

    @checks.setter
    def checks(self, value):
        self._checks = value
