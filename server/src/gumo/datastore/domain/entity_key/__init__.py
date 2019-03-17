import dataclasses
from typing import List
from typing import Union


@dataclasses.dataclass(frozen=True)
class KeyPair:
    kind: str
    name: str


class RootKey:
    _root = None

    @classmethod
    def get_instance(cls):
        if cls._root:
            return cls._root
        cls._root = cls()
        return cls._root

    def parent(self):
        return self

    def pairs(self):
        return []

    def flat_pairs(self):
        return []

    def kind(self):
        return 'Root'

    def name(self):
        return 'root'

    def __repr__(self):
        return "RootKey(kind='Root', name='root')"


@dataclasses.dataclass(frozen=True)
class EntityKey:
    _pairs: List[KeyPair]

    def __post_init__(self):
        if len(self._pairs) == 0:
            raise ValueError('EntityKey#pairs must have at least one element.')

    def parent(self):
        if len(self._pairs) == 1:
            return RootKey.get_instance()

        return EntityKey(self._pairs[0:-1])

    def pairs(self):
        return self._pairs

    def flat_pairs(self):
        flat_pairs = []
        for pair in self.pairs():
            flat_pairs.append(pair.kind)
            flat_pairs.append(pair.name)

        return flat_pairs

    def kind(self):
        return self._pairs[-1].kind

    def name(self):
        return self._pairs[-1].name


class EntityKeyFactory:
    def __init__(self):
        pass

    def build_from_pairs(self, pairs: List[Union[tuple, dict]]) -> EntityKey:
        _pairs = []
        for pair in pairs:
            if isinstance(pair, dict):
                key_pair = KeyPair(pair.get('kind'), pair.get('name'))
            elif isinstance(pair, tuple) or isinstance(pair, list):
                key_pair = KeyPair(pair[0], pair[1])
            else:
                raise ValueError(f'Unknown object type: {type(pair)}, got: {pair}')
            _pairs.append(key_pair)

        return EntityKey(_pairs)