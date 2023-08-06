import inspect
import re
from datetime import datetime
from dateutil.parser import parse


class Functions:
    lambda_functions = {
        "check_column_equal": lambda dataset, col, val: dataset[col] == val,
        "check_column_not_equal": lambda dataset, col, val: dataset[col] != val,
        "check_column_lower_than": lambda dataset, col, val: dataset[col] < val,
        "check_column_greater_than": lambda dataset, col, val: dataset[col] > val,
        "check_column_lower_equal_than": lambda dataset, col, val: dataset[col] <= val,
        "check_column_greater_equal_than": lambda dataset, col, val: dataset[col] >= val,
        "check_column_between": lambda dataset, col, vals: dataset[col].apply(lambda x: x > vals[0] and x < vals[1]),
        "check_column_in_set": lambda dataset, col, vals: dataset[col].apply(lambda x: x in vals),
        "check_column_not_in_set": lambda dataset, col, vals: dataset[col].apply(lambda x: x not in vals),
        "check_column_length_between": lambda dataset, col, vals: dataset[col].apply(lambda x: len(str(x)) >= vals[0] and len(str(x)) <= vals[1]),
        "check_column_length_equal": lambda dataset, col, val: dataset[col].apply(lambda x: len(str(x)) == val),
        "check_column_match_regex": lambda dataset, col, rgx: dataset[col].apply(lambda x: True if re.fullmatch(rgx, str(x)) else False),
        "check_column_not_match_regex": lambda dataset, col, rgx: dataset[col].apply(lambda x: False if re.fullmatch(rgx, str(x)) else True),
        "check_column_match_strftime_format": lambda dataset, col, format: dataset[col].apply(lambda x: Functions.str_2_datetime(str(x), format)),
        "check_column_dateutil_parseable": lambda dataset, col: dataset[col].apply(lambda x: Functions.str_datetime_parseable(str(x))),
    }

    @staticmethod
    def get_string(function):
        desc = inspect.getsource(function)
        desc = desc.strip()
        return desc

    @staticmethod
    def like_2_regex(like):
        # TODO: Match pattern in between %text%text%
        # TODO: Replace all regex chars
        # https://codereview.stackexchange.com/questions/36861/convert-sql-like-to-regex/36864
        # bcd → ^bcd$
        # %bcd → ^.*?bcd$
        # bcd% → ^bcd.*?$
        # %bcd% → ^.*?bcd.*?$
        regex_chars = ["^", ".", "*", "?", "$"]
        regex = ""
        regex_start = "^"
        regex_end = "$"
        if like.startswith("%"):
            regex_start = "^.*?"
            like = like[1:]
        if like.endswith("%"):
            regex_end = ".*?$"
            like = like[:-1]

        for char in regex_chars:
            like = like.replace(char, f"[{char}]")
        regex = f"{regex_start}{like}{regex_end}"
        return regex

    @staticmethod
    def str_2_datetime(date_text, strftime):
        # https://stackoverflow.com/questions/16870663/how-do-i-validate-a-date-string-format-in-python/16870699
        try:
            datetime.strptime(date_text, strftime)
            return True
        except ValueError:
            return False

    @staticmethod
    def str_datetime_parseable(date_text):
        # https://stackoverflow.com/questions/16870663/how-do-i-validate-a-date-string-format-in-python/16870699
        try:
            parse(date_text)
            return True
        except ValueError:
            return False
