from typing import TypeVar, Callable


__ALL__ = ['split_dict', 'extract_from_dict']


K = TypeVar('K')
V = TypeVar('V')


def split_dict(d: dict[K, V], criteria: Callable[[K, V], bool]) -> tuple[dict[K, V], dict[K, V]]:
    d_true, d_false = dict(), dict()
    for k, v in d.items():
        d_to_append = d_true if criteria(k, v) else d_false
        d_to_append[k] = v
    return d_true, d_false


def extract_from_dict(d: dict[K, V], criteria: Callable[[K, V], bool]) -> dict[K, V]:
    filtered_dict = dict()

    filtered_keys = [k for k, v in d.items() if criteria(k, v)]

    for k in filtered_keys:
        filtered_dict[k] = d.pop(k)

    return filtered_dict
