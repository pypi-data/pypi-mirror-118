import json
import jsonpickle
from .CheckRun import CheckRun


class CheckSuite:
    ##################################################################################################
    # Constructor
    ##################################################################################################
    def __init__(self, name, checks=None):
        self.name = name
        if checks is None:
            self.checks = []
        else:
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
    
    def to_json(self):
        raw_json = jsonpickle.encode(self)
        json_object = json.loads(raw_json)
        json_formatted_str = json.dumps(json_object, indent=4)
        return json_formatted_str

    @staticmethod
    def from_json(json):
        suite = jsonpickle.decode(json)
        return suite

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
