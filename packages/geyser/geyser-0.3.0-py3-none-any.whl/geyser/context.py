from collections import OrderedDict
from json import loads
from pkgutil import get_data
from typing import Mapping, Text, Any

from jsonschema import validate
from taskflow.atom import Atom


class Context(object):
    schema = loads(get_data(__package__, 'schema.json'))

    class AtomContext(OrderedDict):
        def __setitem__(self, key, value):
            assert isinstance(value, Atom)

    def __init__(self, profile: Mapping[Text, Any]):
        self.profile = profile
        validate(self.profile, self.schema)
