from collections import OrderedDict
from logging import getLogger as get_logger, Logger
from typing import Callable, MutableMapping, Mapping, Text, Type, Any

from taskflow.atom import Atom
from taskflow.flow import Flow
from taskflow.patterns.graph_flow import Flow as GraphFLow, TargetedFlow
from taskflow.patterns.linear_flow import Flow as LinearFlow
from taskflow.patterns.unordered_flow import Flow as UnorderedFlow

from .context import Context


class Geyser(object):
    atom_classes: MutableMapping[Text, Type[Atom]] = OrderedDict()
    flow_classes: Mapping[Text, Type[Flow]] = OrderedDict((
        ('linear', LinearFlow),
        ('unordered', UnorderedFlow),
        ('graph', GraphFLow),
        ('targeted_graph', TargetedFlow),
    ))

    logger: Logger = get_logger(f"geyser.geyser.Geyser")

    @classmethod
    def task(cls) -> Callable[[Type[Atom]], Type[Atom]]:
        def wrapper(atom: Type[Atom]) -> Type[Atom]:
            reference = f'{atom.__module__}.{atom.__name__}'
            if issubclass(atom, Atom):
                cls.atom_classes[reference] = atom
            else:
                cls.logger.error(f'Type "{reference}" is NOT subclass of taskflow.atom.Atom')
            return atom

        return wrapper

    @classmethod
    def execute(cls, profile: Mapping[Text, Any]):
        context = Context()
