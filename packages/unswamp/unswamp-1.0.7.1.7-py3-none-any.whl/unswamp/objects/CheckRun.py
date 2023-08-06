from datetime import datetime
import uuid
from .base.SerializableObject import SerializableObject


class CheckRun(SerializableObject):
    ##################################################################################################
    # Constructor
    ##################################################################################################
    def __init__(self, run_id=None):
        if run_id is None:
            run_id = str(uuid.uuid4().hex)
        self.id = run_id
        SerializableObject.__init__(self)
        self.results = []

    ##################################################################################################
    # Methods
    ##################################################################################################
    def run(self, dataset, suite):
        self.results = []
        self.suite_id = suite.id
        for check in suite.checks:
            result = check.run(dataset)
            self.results.append(result)

    ##################################################################################################
    # Properties
    ##################################################################################################
    id = None
    suite_id = None
    results = []
    start = datetime.min
    end = datetime.min

    @property
    def duration(self):
        duration = self.end - self.start
        return duration

    @property
    def pass_rate(self):
        checks = len(self.results)
        if checks == 0:
            return 0
        check_results = list(result.passed for result in self.results)
        passed = check_results.count(True)
        rate = passed / checks
        return rate

    @property
    def fail_rate(self):
        checks = len(self.results)
        if checks == 0:
            return 0
        check_results = list(result.passed for result in self.results)
        failed = check_results.count(False)
        rate = failed / checks
        return rate
