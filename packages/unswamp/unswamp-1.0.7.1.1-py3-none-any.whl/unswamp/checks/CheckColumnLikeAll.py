from .base.BaseCheck import BaseCheck
from .base.BaseColumnCheck import BaseColumnCheck
from .base.BaseFunctionCheck import BaseFunctionCheck
from .Functions import Functions


class CheckColumnLikeAll(BaseCheck, BaseColumnCheck, BaseFunctionCheck):
    ##################################################################################################
    # Constructor
    ##################################################################################################
    def __init__(self, id, column_name, column_like, match=True, check_meta_data=None):
        column_function_name = "check_column_match_regex"
        if not match:
            column_function_name = "check_column_not_match_regex"

        BaseCheck.__init__(self, id, check_meta_data)
        BaseColumnCheck.__init__(self, column_name)
        BaseFunctionCheck.__init__(self, column_function_name)

        self.column_like = column_like
        self.column_regex = Functions.like_2_regex(self.column_like)
        self.match = match

    ##################################################################################################
    # Methods
    ##################################################################################################

    def _run(self, dataset):
        passed = self.column_function(
            dataset, self.column_name, self.column_regex).all()
        match_message = "match"
        if self.match == False:
            match_message = "don't match"
        message = f"All values in column '{self.column_name}' {match_message} the given regex pattern '{self.column_regex}'!"
        if not passed:
            message = f"Not all values in column '{self.column_name}' {match_message} the given regex pattern '{self.column_regex}'!"
        return passed, message

    ##################################################################################################
    # Properties
    ##################################################################################################
    @property
    def column_regex(self):
        return self._column_regex

    @column_regex.setter
    def column_regex(self, value):
        self._column_regex = value
        self._settings["column_regex"] = value

    @property
    def column_like(self):
        return self._column_like

    @column_like.setter
    def column_like(self, value):
        self._column_like = value
        self._settings["column_like"] = value

    @property
    def match(self):
        return self._match

    @match.setter
    def match(self, value):
        self._match = value
        self._settings["match"] = value
