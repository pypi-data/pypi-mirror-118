import os
from .base.DatetimeHandler import DatetimeHandler


class CheckResult:
    ##################################################################################################
    # Constructor
    ##################################################################################################
    def __init__(self, check, start, end, passed, message):
        self.check = check
        self.start = start
        self.end = end
        self.passed = passed
        self.message = message

    ##################################################################################################
    # Overrides
    ##################################################################################################
    def __str__(self):
        obj = "#" * 50 + os.linesep
        obj += f"# {self.check.id}{os.linesep}"
        obj += "#" * 50 + os.linesep
        obj += f"- passed: '{self.passed}'{os.linesep}"
        obj += f"- message: '{self.message}'{os.linesep}"
        obj += "#" * 50 + os.linesep
        obj += f"- check: '{self.check}'{os.linesep}"
        obj += f"- start: '{self.start}'{os.linesep}"
        obj += f"- end: '{self.end}'{os.linesep}"
        obj += f"- duration: '{self.duration}'{os.linesep}"
        obj += "#" * 50 + os.linesep
        obj += f"- settings:{os.linesep}"
        for key in self.check.settings:
            obj += f"    - {key}: '{self.check.settings[key]}'{os.linesep}"
        obj += "#" * 50 + os.linesep
        obj += os.linesep
        return obj

    ##################################################################################################
    # Properties
    ##################################################################################################
    @property
    def check(self):
        return self._check

    @check.setter
    def check(self, value):
        self._check = value

    @property
    def start(self):
        # TODO: is there a better version to do restore datetime after serialization
        self._start = DatetimeHandler.from_json(self._start)
        return self._start

    @start.setter
    def start(self, value):
        self._start = value

    @property
    def end(self):
        # TODO: is there a better version to do restore datetime after serialization
        self._end = DatetimeHandler.from_json(self._end)
        return self._end

    @end.setter
    def end(self, value):
        self._end = value

    @property
    def passed(self):
        return self._passed

    @passed.setter
    def passed(self, value):
        self._passed = value

    @property
    def message(self):
        return self._message

    @message.setter
    def message(self, value):
        self._message = value

    @property
    def duration(self):
        return self.end - self.start
