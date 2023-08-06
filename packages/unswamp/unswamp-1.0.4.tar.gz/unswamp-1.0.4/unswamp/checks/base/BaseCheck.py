import logging as log
from datetime import datetime

from unswamp.objects import CheckResult


class BaseCheck:
    _settings = {}
    ##################################################################################################
    # Constructor
    ##################################################################################################
    def __init__(self, id):
        self.id = id

    ##################################################################################################
    # Methods
    ##################################################################################################
    def run(self, dataset):
        start = datetime.now()
        log.debug(f"start run check '{self.check}' with id '{self.id}'")
        passed, message = self._run(dataset)
        end = datetime.now()
        result = CheckResult(
            self.id, self.check, self.settings, start, end, passed, message
        )
        log.debug(result)
        log.debug(f"stop run check '{self.check}' with id '{self.id}'")
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
    def check(self):
        check = self.__class__.__name__
        return check

    @property
    def settings(self):
        return self._settings
