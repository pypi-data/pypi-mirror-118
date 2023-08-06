import json
import jsonpickle
from .DatetimeHandler import DatetimeHandler
from datetime import datetime
from unswamp import __version__

jsonpickle.handlers.registry.register(datetime, DatetimeHandler)


class SerializableObject:
    __static_init = "static_init"
    __description_property = "description"
    __checks_property = "checks"
    __indent = 4
    __replaces = {
        "py/object": "unswamp_type",
        "_description": "description"
    }
    ##################################################################################################
    # Constructor
    ##################################################################################################

    def __init__(self):
        self._unswamp_version = __version__

    ##################################################################################################
    # Methods
    ##################################################################################################
    # TODO: rename
    def to_json(self):
        json = SerializableObject.static_to_json(self)
        return json

    @staticmethod
    def from_json(json_str):
        for key in SerializableObject.__replaces:
            value = SerializableObject.__replaces[key]
            json_str = json_str.replace(value, key)

        obj = jsonpickle.decode(json_str)
        SerializableObject.call_static_init(obj)
        return obj

    @staticmethod
    # TODO: rename
    def static_to_json(obj):
        SerializableObject.call_description_property(obj)
        raw = jsonpickle.encode(obj)
        json_str = json.loads(raw)
        formatted = json.dumps(json_str, indent=SerializableObject.__indent)

        for key in SerializableObject.__replaces:
            value = SerializableObject.__replaces[key]
            formatted = formatted.replace(key, value)
        return formatted

    @staticmethod
    def call_static_init(obj):
        method = SerializableObject.__static_init
        static_init = getattr(obj, method, None)
        if static_init and callable(init):
            static_init(obj)

    @staticmethod
    def call_description_property(obj):
        if hasattr(obj, SerializableObject.__checks_property):
            checks = getattr(obj, SerializableObject.__checks_property)
            if isinstance(checks, list):
                for check in checks:
                    if hasattr(check, SerializableObject.__description_property):
                        getattr(check, SerializableObject.__description_property)

    ##################################################################################################
    # Properties
    ##################################################################################################
    @property
    def unswamp_version(self):
        return self._unswamp_version
