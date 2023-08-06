import logging as log
from datetime import datetime

from unswamp.objects import CheckResult


class BaseCheck:
    _settings = {}
    ##################################################################################################
    # Constructor
    ##################################################################################################

    def __init__(self, id, check_meta_data=None):
        self.id = id
        if check_meta_data is None:
            check_meta_data = {}
        self.check_meta_data = check_meta_data

    ##################################################################################################
    # Methods
    ##################################################################################################
    def run(self, dataset):
        start = datetime.now()
        log.debug(f"start run check '{self.check_name}' with id '{self.id}'")
        passed, message = self._run(dataset)
        passed = bool(passed)
        end = datetime.now()
        result = CheckResult(self, start, end, passed, message)
        log.debug(result)
        log.debug(f"stop run check '{self.check_name}' with id '{self.id}'")
        return result

    ##################################################################################################
    # Properties
    ##################################################################################################
    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    @property
    def check_name(self):
        check_name = self.__class__.__name__
        return check_name

    @property
    def check_meta_data(self):
        return self._check_meta_data

    @check_meta_data.setter
    def check_meta_data(self, value):
        self._check_meta_data = value
        self._settings["check_meta_data"] = value

    @property
    def settings(self):
        return self._settings
