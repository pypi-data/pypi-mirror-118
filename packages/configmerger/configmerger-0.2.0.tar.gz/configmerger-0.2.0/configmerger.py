# -*- coding: utf-8 -*-
#
# Copyright (c) 2021~2999 - Cologler <skyoflw@gmail.com>
# ----------
#
# ----------

from typing import *
import itertools
import functools

def trim_none_from_end(items: list):
    'A helper function to remove all `None` from end.'
    tl = len(items)
    if tl > 0:
        for i in range(tl):
            if items[-1-i] is not None:
                return items[:tl-i]
    return []

def get_typed_values_from_end(
        values: List[Any], types: Union[type, Tuple[type, ...]], *,
        skip_none: bool = True):
    '''
    A helper function to get values match the `types` from end,
    stop until the value is mismatch, unless it is `None`.
    '''
    rv = []
    for value in reversed(values):
        if isinstance(value, types):
            rv.append(value)
        elif value is not None or not skip_none:
            break
    rv.reverse()
    return rv

class _MergerHandlerTreeNode:
    __slots__ = ('_children', '_value')

    def __init__(self):
        self._children: dict = None
        self._value = None

    def set_handler(self, keys: Tuple[Union[type, str, int]], handler):
        if not keys:
            self._value = handler
        else:
            if self._children is None:
                self._children = {}
            node = self._children.setdefault(keys[0], _MergerHandlerTreeNode())
            node.set_handler(keys[1:], handler)

    def find_all(self, keys: Tuple[Union[str, int]], result: list) -> '_MergerHandlerTreeNode':
        if not keys:
            if self._value:
                result.append(self._value)
        elif self._children:
            key = keys[0]
            if node := self._children.get(key):
                node.find_all(keys[1:], result)
            elif node := self._children.get(type(key)):
                node.find_all(keys[1:], result)

class Merger:
    def __init__(self) -> None:
        self._keys_handlers = _MergerHandlerTreeNode()
        self._type_handlers = {}

        self.configure(object, self._merge_objects)
        self.configure(list, self._merge_lists)
        self.configure(dict, self._merge_dicts)

    def configure(self, keys: Tuple[Union[type, str, int]], handler: Union[Callable, str]):
        if isinstance(handler, str):
            name = handler
            handler = vars(MergeMethods).get(name) # prevent use method from object
            if isinstance(handler, staticmethod):
                handler = handler.__func__
            if handler is None or name[0] == '_':
                raise ValueError(f'unknown handler name: {name}')

        if not callable(handler):
            raise TypeError(f'handler must be callable or str, not {handler!r}')

        if isinstance(keys, tuple):
            self._keys_handlers.set_handler(keys, handler)
        elif isinstance(keys, type):
            self._type_handlers[keys] = handler
        else:
            raise TypeError(f'keys must be tuple or type, not {keys!r}')

    def merge(self, values: List[Any]):
        'merge multi values, latest have highest priority.'
        merge_internal = self._merge_internal
        merge_callback = functools.partial(merge_internal)
        merge_callback.keywords['merge'] = merge_callback
        return merge_callback(values, ())

    def _merge_internal(self, values: List[Any], keys: Tuple[Union[str, int]], merge):
        if not values:
            raise ValueError('you cannot merge zero items.')
        if not isinstance(keys, tuple):
            raise TypeError(f'keys must be tuple, not {keys!r}')

        trimed_values = trim_none_from_end(values)
        if not trimed_values:
            return None
        if len(trimed_values) == 1:
            return trimed_values[0]
        last_value = trimed_values[-1]

        # merge with key
        khs = []
        self._keys_handlers.find_all(keys, khs)
        if khs:
            return khs[0](trimed_values, keys, merge)

        # merge with type only
        for klass in type(last_value).__mro__:
            if mh := self._type_handlers.get(klass):
                return mh(trimed_values, keys, merge)

        raise TypeError(f'unsupported type: {type(last_value)}')

    @staticmethod
    def _merge_objects(values: List[Any], keys: Tuple[Union[str, int]], _):
        'The default merge objects method.'

        return values[-1]

    @staticmethod
    def _merge_dicts(values: List[Any], keys: Tuple[Union[str, int]], merge):
        'The default merge dicts method.'

        rv = {}
        typed_values = get_typed_values_from_end(values, dict)
        values_keys = set(itertools.chain(*typed_values))
        for k in values_keys:
            rv[k] = merge([tv.get(k) for tv in typed_values], keys + (k, ))
        return rv

    def _merge_lists(self, values: List[Any], *_):
        'The default merge lists method.'

        return list(
            itertools.chain(
                *reversed(
                    get_typed_values_from_end(values, list, skip_none=True)
                )
            )
        )

class MergeMethods:
    @staticmethod
    def _get_typed_values(values: list):
        return get_typed_values_from_end(values, type(values[-1]))

    @staticmethod
    def first(values: list, keys: tuple, merge: callable):
        assert values
        return MergeMethods._get_typed_values(values)[0]

    @staticmethod
    def last(values: list, keys: tuple, merge: callable):
        assert values and values[-1] is not None
        return values[-1]

__all__ = ['Merger', ]
