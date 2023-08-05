from .BaseColumnCheck import BaseColumnCheck
from .Functions import Functions


class CheckColumnRegexAll(BaseColumnCheck):
    ##################################################################################################
    # Constructor
    ##################################################################################################
    def __init__(self, id, column_name, column_regex, match = True):
        BaseColumnCheck.__init__(self, id, column_name)
        self.column_regex = column_regex
        self.settings["column_regex"] = self.column_regex
        self.match = match
        self.settings["match"] = self.match
        if match:
            self.column_function_name = "check_column_match_regex"
        else:
            self.column_function_name = "check_column_not_match_regex"

    ##################################################################################################
    # Methods
    ##################################################################################################
    def _run(self, dataset):
        passed = self.column_function(dataset, self.column_name, self.column_regex).all()
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
    def column_function_name(self):
        return self._column_function_name

    @column_function_name.setter
    def column_function_name(self, value):
        self._column_function_name = value

    @property
    def column_function(self):
        func = Functions.lambda_functions[self.column_function_name]
        return func

    @property
    def column_function_str(self):
        func = self.column_function
        desc = Functions.get_string(func)
        return desc

    @property
    def column_regex(self):
        return self._column_regex

    @column_regex.setter
    def column_regex(self, value):
        self._column_regex = value

    @property
    def match(self):
        return self._match

    @match.setter
    def match(self, value):
        self._match = value
