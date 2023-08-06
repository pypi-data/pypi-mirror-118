from .base.SerializableObject import SerializableObject
from .base.MetaDataObject import MetaDataObject
from .CheckRun import CheckRun


class CheckSuite(SerializableObject, MetaDataObject):
    ##################################################################################################
    # Constructor
    ##################################################################################################
    def __init__(self, suite_id, dataset_name, checks=None, meta_data=None):
        SerializableObject.__init__(self)
        MetaDataObject.__init__(self, meta_data)
        self.id = suite_id
        self.dataset_name = dataset_name
        if checks is None:
            checks = []
        self.checks = checks

    ##################################################################################################
    # Methods
    ##################################################################################################
    def add_check(self, check):
        self.checks.append(check)

    def run(self, dataset, run_name, run_id=None, meta_data=None):
        run = CheckRun(run_id, meta_data)
        run.run(dataset, self, run_name)
        return run

    ##################################################################################################
    # Properties
    ##################################################################################################
    id = None
    dataset_name = None
    checks = []
