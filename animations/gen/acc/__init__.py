"""Accessory library registry.

Every module in this folder (except names starting with '_') defines ITEMS = [Item(...), ...].
    from acc import get, all_items
    hat = get('party_hat')
A module that fails to import is skipped (see errors()), so one broken file never breaks the others.
"""
import importlib
import os
import sys

_DIR = os.path.dirname(os.path.abspath(__file__))
_items = None
_errors = {}


def _load():
    global _items
    if _items is not None:
        return _items
    _items = {}
    for f in sorted(os.listdir(_DIR)):
        if not f.endswith('.py') or f.startswith('_'):
            continue
        name = f[:-3]
        try:
            mod = importlib.import_module('acc.' + name)
        except Exception as e:  # keep going: other modules still work
            _errors[name] = '%s: %s' % (type(e).__name__, e)
            continue
        for it in getattr(mod, 'ITEMS', []):
            it.module = name
            if it.name in _items:
                _errors[name + ':' + it.name] = 'duplicate item name (also in %s)' % _items[it.name].module
                continue
            _items[it.name] = it
    return _items


def get(name):
    items = _load()
    if name not in items:
        raise KeyError('no accessory %r. Known: %s' % (name, ', '.join(sorted(items))))
    return items[name]


def all_items():
    return list(_load().values())


def errors():
    _load()
    return dict(_errors)


def reload():
    global _items
    _items = None
    _errors.clear()
    for k in list(sys.modules):
        if k.startswith('acc.'):
            del sys.modules[k]
