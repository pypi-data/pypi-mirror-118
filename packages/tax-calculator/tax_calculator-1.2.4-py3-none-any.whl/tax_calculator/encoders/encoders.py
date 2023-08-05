import abc
import json
from typing import Any

from arrow import Arrow

from tax_calculator.IMoney import IMoney
from tax_calculator.calculators.CodiceAteco import CodiceAteco


class AbstractJSONEncoder(abc.ABC):

    @abc.abstractmethod
    def can_manage_object(self, obj) -> bool:
        pass

    @abc.abstractmethod
    def serialize_object_to_json(self, obj: any):
        pass


class ArrowEncoder(AbstractJSONEncoder):

    def can_manage_object(self, obj) -> bool:
        return isinstance(obj, Arrow)

    def serialize_object_to_json(self, obj):
        return obj.isoformat()


class CodiceAtecoEncoder(AbstractJSONEncoder):

    def can_manage_object(self, obj) -> bool:
        return isinstance(obj, CodiceAteco)

    def serialize_object_to_json(self, obj):
        return str(obj)


class MoneyEncoder(AbstractJSONEncoder):

    def can_manage_object(self, obj) -> bool:
        return isinstance(obj, IMoney)

    def serialize_object_to_json(self, obj):
        return f"{obj:.2f}"


class GenericEncoder(AbstractJSONEncoder):

    def can_manage_object(self, obj) -> bool:
        return True

    def serialize_object_to_json(self, obj):
        return str(obj)


class MultiplexerEncoder(json.JSONEncoder):
    ENCODERS = [
        ArrowEncoder(),
        CodiceAtecoEncoder(),
        MoneyEncoder(),
        # put at last
        GenericEncoder()
    ]

    def default(self, o: Any) -> Any:
        for encoder in MultiplexerEncoder.ENCODERS:
            if encoder.can_manage_object(o):
                return encoder.serialize_object_to_json(o)
        else:
            # Let the base class default method raise the TypeError
            return json.JSONEncoder.default(self, o)


