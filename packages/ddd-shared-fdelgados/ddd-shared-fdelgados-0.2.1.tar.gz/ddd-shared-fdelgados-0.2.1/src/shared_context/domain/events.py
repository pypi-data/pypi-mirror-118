from datetime import datetime
from typing import List, Dict
import json
import abc


class DomainEvent(metaclass=abc.ABCMeta):
    def __init__(self):
        self._occurred_on = datetime.now()

    @abc.abstractmethod
    def event_name(self) -> str:
        raise NotImplementedError

    @property
    def occurred_on(self):
        return self._occurred_on

    def serialize(self) -> str:
        def json_converter(o):
            if isinstance(o, datetime):
                return o.__str__()

        properties = self.__sanitize_property_names()

        return json.dumps(properties, ensure_ascii=False, default=json_converter)

    def __sanitize_property_names(self) -> Dict:
        properties = {}
        for property_name, value in self.__dict__.items():
            properties[property_name.lstrip('_')] = value

        return properties

    def __str__(self) -> str:
        return self.serialize()

    def __repr__(self) -> str:
        return "DomainEvent <{}>".format(self.event_name())


class DomainEventPublisher:
    def __init__(self, event_handlers: Dict):
        self._event_handlers = event_handlers

    def publish(self, domain_events: List[DomainEvent]) -> None:
        for domain_event in domain_events:
            self._publish_event(domain_event)

    def _publish_event(self, domain_event: DomainEvent) -> None:
        domain_event_name = _classname(domain_event)

        event = self._event_handlers.get(domain_event_name)
        subscribers = event.get('subscribers')

        for subscriber in subscribers:
            subscriber_class = subscriber()
            subscriber_class.handle(domain_event)


def _classname(obj):
    cls = type(obj)
    module = cls.__module__
    name = cls.__qualname__
    if module is not None and module != "__builtin__":
        name = "{}.{}".format(module, name)

    return name
