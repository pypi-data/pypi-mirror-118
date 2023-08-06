from collections.abc import Mapping, Sequence, MutableMapping, MutableSequence
from collections import OrderedDict
from itertools import islice, chain
from typing import TypeVar


__ALL__ = ['KVSequence', 'MutableKVSequence', 'SmartKVSequence', 'MutableSmartKVSequence', ]


K = TypeVar('K')
V = TypeVar('V')

_NoDefault = object()


class _SequenceMixin:
    def __init__(self, mapping: MutableMapping[K, V]):
        self.mapping = mapping

    def __repr__(self):
        return repr(self.mapping.data.values())

    def __str__(self):
        return str(self.data.data.values())

    def _parse_index_arg(self, iterable, index):
        if isinstance(index, int):
            start, stop, step = index, index + 1, 1
        else:
            start, stop, step = index.start, index.stop, index.step or 1

        length = len(self.mapping)

        if step < 0:
            iterable = reversed(iterable)
            start, stop, step = stop, start, -step

        start = start or 0
        stop = stop or length

        start = length + start if start < 0 else start
        stop = length + stop if stop < 0 else stop

        if start > length or stop > length:
            raise IndexError(f'index out of range: {max(start, stop)} > {length}')

        return iterable, start, stop, step

    def _get_islice(self, iterable, index):
        iterable, start, stop, step = self._parse_index_arg(iterable, index)
        return islice(iterable, start, stop, step)

    def _get_sequence_iter(self, iterable, index):
        return self._get_islice(iterable, index), not isinstance(index, int)

    def __getitem__(self, index):
        iterator, is_seq = self._get_sequence_iter(self.mapping.data.values(), index)
        return list(iterator) if is_seq else next(iterator)

    def __len__(self):
        return len(self.mapping)


class _MutableSequenceMixin:
    def __setitem__(self, index, values):
        keys, is_seq = self._get_sequence_iter(self.mapping.keys(), index)
        values = [values, ] if not is_seq else values

        for key, value in zip(keys, values):
            self.mapping[key] = value

    def __delitem__(self, index):
        items, start, stop, step = self._parse_index_arg(self.mapping.items(), index)
        exclude = range(start, stop, step)

        self.mapping.data = self.mapping.Dict(
            kv for i, kv in enumerate(items) if i not in exclude
        )

    def insert(self, index, kv):
        mapping = self.mapping.data.items()
        self.mapping.data = self.mapping.Dict(
            chain(
                self._get_islice(mapping, slice(0, index, None)),
                [kv,] ,
                self._get_islice(mapping, slice(index, None, None))
            )
        )

    def reverse(self):
        self.mapping.data = self.mapping.Dict(reversed(self.mapping.data.items()))

    def __iadd__(self, other):
        return NotImplemented


class _Seq(_SequenceMixin, Sequence):
    pass


class _MutableSeq(_MutableSequenceMixin, _SequenceMixin, MutableSequence):
    pass


class _MappingMixin:
    Dict = OrderedDict
    _Seq = _Seq

    def __init__(self, *args, **kwargs):
        self.data = self.Dict(*args, **kwargs)
        self.as_sequence = self._Seq(self)

    def __repr__(self):
        return repr(self.data)

    def __str__(self):
        return str(self.data)

    def __getitem__(self, k):
        return self.data.__getitem__(k)

    def __len__(self):
        return self.data.__len__()

    def __iter__(self):
        return self.data.__iter__()

    def keys(self):
        return self.data.keys()

    def values(self):
        return self.data.values()

    def items(self):
        return self.data.items()


class _MutableMappingMixin:
    _Seq = _MutableSeq

    def __setitem__(self, k, v):
        return self.data.__setitem__(k, v)

    def __delitem__(self, k):
        return self.data.__delitem__(k)

    def __reversed__(self):
        return self.data.__reversed__()

    def reverse(self):
        self.data = self.Dict(reversed(self.data.items()))


class KVSequence(_MappingMixin, Mapping):
    pass


class MutableKVSequence(_MutableMappingMixin, _MappingMixin, MutableMapping):
    pass


class _SmartMappingMixin(_MappingMixin):
    def __getitem__(self, k):
        target = self.as_sequence if isinstance(k, (int, slice)) else self.data
        return target.__getitem__(k)

    def count(self, value):
        return self.as_sequence.count(value)

    def index(self, *args, **kwargs):
        return self.as_sequence.index(*args, **kwargs)


class _MutableSmartMappingMixin(_MutableMappingMixin):
    def __setitem__(self, k, v):
        target = self.as_sequence if isinstance(k, (int, slice)) else self.data
        return target.__setitem__(k, v)

    def __delitem__(self, k):
        target = self.as_sequence if isinstance(k, (int, slice)) else self.data
        return target.__delitem__(k)

    def pop(self, k, d=_NoDefault):
        if isinstance(k, int):
            try:
                self.as_sequence.pop(k)
            except IndexError as e:
                if d is not _NoDefault:
                    return d
                raise e
        return self.data.pop(k) if d is _NoDefault else self.data.pop(k, d)

    def insert(self, index, value):
        return self.as_sequence.insert(index, value)

    def extend(self, iterable):
        return self.as_seqeunce.extend(iterable)

    def remove(self, item):
        return self.as_sequence.remove(item)

    def append(self, index, value):
        return self.as_sequence.append(index, value)

    def __iadd__(self, other):
        other = other.as_sequence if isinstance(other, self.__class__) else other
        return self.as_sequence.__iadd__(other)


class SmartKVSequence(_SmartMappingMixin, Mapping):
    pass


class MutableSmartKVSequence(_MutableSmartMappingMixin, _SmartMappingMixin, MutableMapping):
    pass
