# -*- coding: utf-8 -*-

import json
from typing import List, TypeVar, Type, Dict, Any

from typing_extensions import Protocol

from log import get_logger

logger = get_logger(__name__)

T_DICTIONARY_BASED = TypeVar("T_DICTIONARY_BASED", bound="DictionaryBased")
T_JSON_MODEL = TypeVar("T_JSON_MODEL", bound="JsonModel")


class DictionaryBased(Protocol):

    @classmethod
    def from_dict(cls: Type[T_DICTIONARY_BASED], d: Dict[str, Any]) -> T_DICTIONARY_BASED:
        raise NotImplementedError()

    def to_dict(self) -> Dict[str, Any]:
        raise NotImplementedError()


class JsonModel(DictionaryBased):

    @classmethod
    def from_dict(cls: Type[T_DICTIONARY_BASED], d: Dict[str, Any]) -> T_DICTIONARY_BASED:
        raise NotImplementedError()

    def to_dict(self) -> Dict[str, Any]:
        raise NotImplementedError()

    @classmethod
    def deserialize(cls: Type[T_JSON_MODEL], bytez: bytes) -> T_JSON_MODEL:
        data = json.loads(bytez)
        return cls.from_dict(data)

    def serialize(self) -> bytes:
        data = self.to_dict()
        return json.dumps(data, indent=2).encode("utf-8")


class ClassificationRequest(JsonModel):

    def __init__(self, texts: List[str]):
        super().__init__()
        self.texts = texts

    @classmethod
    def from_dict(cls: Type['ClassificationRequest'], d) -> 'ClassificationRequest':
        return cls(texts=d["texts"])

    def to_dict(self):
        return {"texts": self.texts}
