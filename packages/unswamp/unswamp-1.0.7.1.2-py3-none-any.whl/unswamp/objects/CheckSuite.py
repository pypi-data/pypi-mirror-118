from unswamp.objects.base.SerializableObject import SerializableObject
from unswamp.objects.base.MetaDataObject import MetaDataObject
from unswamp.objects.CheckRun import CheckRun


class CheckSuite(SerializableObject, MetaDataObject):
    ##################################################################################################
    # Constructor
    ##################################################################################################
    def __init__(self, name, checks=None, meta_data=None):
        SerializableObject.__init__(self)
        MetaDataObject.__init__(self, meta_data)
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
    def version(self):
        return self._version

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
