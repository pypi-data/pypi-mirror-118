from datetime import datetime

from unswamp.objects import CheckResult
from ..Functions import Functions
from ..Descriptions import Descriptions


class BaseCheck:
    ##################################################################################################
    # Constructor
    ##################################################################################################

    def __init__(self, check_id, meta_data=None, level="column"):
        self.id = check_id
        if meta_data is None:
            meta_data = {}
        self.meta_data = meta_data
        self.level = level
        self.description = None
        self.name = self.__class__.__name__

    ##################################################################################################
    # Methods
    ##################################################################################################

    def run(self, dataset):
        start = datetime.now()
        passed, message = self._run(dataset)
        passed = bool(passed)
        end = datetime.now()
        result = CheckResult(self, start, end, passed, message)
        return result

    ##################################################################################################
    # Properties
    ##################################################################################################
    id = None
    meta_data = {}
    level = "column"
    name = None

    ##################################################################################################
    # ReadOnly Properties
    ##################################################################################################
    @property
    def description(self):
        self.description = Descriptions.get_check_description(self.name, self.__dict__)


    @description.setter
    def description(self, value):
        self._description = value
