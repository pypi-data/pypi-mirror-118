from ..base.BaseCheck import BaseCheck
from ..base.BaseColumnCheck import BaseColumnCheck
from ..base.BaseFunctionCheck import BaseFunctionCheck


class CheckColumnRegexAll(BaseCheck, BaseColumnCheck, BaseFunctionCheck):
    ##################################################################################################
    # Constructor
    ##################################################################################################
    def __init__(self, check_id, column_name, regex, match=True, meta_data=None):
        function_name = "check_column_match_regex"
        if not match:
            function_name = "check_column_not_match_regex"

        BaseCheck.__init__(self, check_id, meta_data)
        BaseColumnCheck.__init__(self, column_name)
        BaseFunctionCheck.__init__(self, function_name)
        
        self.regex = regex
        self.match = match

    ##################################################################################################
    # Methods
    ##################################################################################################

    def _run(self, dataset):
        passed = self.function(dataset, self.column_name, self.regex).all()
        match_message = "match"
        if self.match == False:
            match_message = "don't match"
        message = f"All values in column '{self.column_name}' {match_message} the given regex pattern '{self.regex}'!"
        if not passed:
            message = f"Not all values in column '{self.column_name}' {match_message} the given regex pattern '{self.regex}'!"
        return passed, message

    ##################################################################################################
    # Properties
    ##################################################################################################
    regex = None
    match = True
