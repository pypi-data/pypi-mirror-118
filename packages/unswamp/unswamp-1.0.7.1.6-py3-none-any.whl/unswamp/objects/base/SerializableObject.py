import json
import jsonpickle
from .DatetimeHandler import DatetimeHandler
from datetime import datetime
from unswamp import __version__

jsonpickle.handlers.registry.register(datetime, DatetimeHandler)


class SerializableObject:
    _indent = 4
    _replaces = {
        "py/object": "unswamp_type"
    }
    ##################################################################################################
    # Constructor
    ##################################################################################################
    def __init__(self):
        self._version = __version__

    ##################################################################################################
    # Methods
    ##################################################################################################
    def to_json(self):
        raw = jsonpickle.encode(self)
        json_str = json.loads(raw)
        formatted = json.dumps(json_str, indent=self._indent)

        for key in self._replaces:
            value = self._replaces[key]
            formatted = formatted.replace(key, value)

        return formatted

    @staticmethod
    def from_json(json_str):
        for key in SerializableObject._replaces:
            value = SerializableObject._replaces[key]
            json_str = json_str.replace(value, key)

        obj = jsonpickle.decode(json_str)
        return obj

    ##################################################################################################
    # Properties
    ##################################################################################################
    @property
    def version(self):
        return self._version
