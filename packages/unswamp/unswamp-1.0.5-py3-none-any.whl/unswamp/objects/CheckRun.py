from .base.SerializableObject import SerializableObject


class CheckRun(SerializableObject):
    ##################################################################################################
    # Constructor
    ##################################################################################################
    def __init__(self):
        SerializableObject.__init__(self)
        self._results = []

    ##################################################################################################
    # Methods
    ##################################################################################################
    def run(self, dataset, checks):
        self._results = []
        for check in checks:
            result = check.run(dataset)
            self._results.append(result)

    ##################################################################################################
    # Properties
    ##################################################################################################
    @property
    def results(self):
        return self._results

    @property
    def start(self):
        starts = (result.start for result in self.results)
        start = min(starts)
        return start

    @property
    def end(self):
        ends = (result.end for result in self.results)
        end = min(ends)
        return end

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
