from .base.SerializableObject import SerializableObject
from .base.MetaDataObject import MetaDataObject
from .CheckRun import CheckRun


class CheckSuite(SerializableObject, MetaDataObject):
    ##################################################################################################
    # Constructor
    ##################################################################################################
    def __init__(self, suite_id, checks=None, meta_data=None):
        SerializableObject.__init__(self)
        MetaDataObject.__init__(self, meta_data)
        self.id = suite_id
        if checks is None:
            checks = []
        self.checks = checks

    ##################################################################################################
    # Methods
    ##################################################################################################
    def add_check(self, check):
        self.checks.append(check)

    def run(self, dataset, run_id=None):
        run = CheckRun(run_id)
        run.run(dataset, self)
        return run

    ##################################################################################################
    # Properties
    ##################################################################################################
    id = None
    checks = []
