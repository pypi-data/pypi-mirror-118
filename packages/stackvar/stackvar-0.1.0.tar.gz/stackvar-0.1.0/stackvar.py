import collections
import threading
from functools import wraps
import inspect
from typing import (
    Any,
    Callable,
    Dict,
)
from pydantic.typing import ForwardRef, evaluate_forwardref


def send(**stack_variables):
    return _storage.send_variables(stack_variables)


class Variable:
    pass


class Factory(Variable):
    pass


def receive(method):
    variables_dict = get_declared_variables(method)
    if not variables_dict:
        return method
    pos_to_param  = tuple((pos, name) for name, (anno, value, pos) in variables_dict.items())
    first_pos = pos_to_param[0][0]
    last_pos = pos_to_param[-1][0]
    pos_to_param = collections.OrderedDict(pos_to_param)

    @wraps(method)
    def wrapper(*a, **kw):
        passed = set()
        if first_pos <= (len(a) - 1):
            for pos in range(first_pos, max(last_pos + 1, len(a))):
                if pos in pos_to_param:
                    passed.add(pos_to_param[pos])
        for k in kw:
            if k in passed:
                raise StackVarNameError(f'Multiple values passed for {k} parameter.')
            passed.add(k)
        non_passed = set(variables_dict) - passed
        undeclared_diff = _storage.get_undeclared_diff(non_passed)
        if not undeclared_diff:
            for k in non_passed:
                kw[k] = _storage[k]
            return method(*a, **kw)
        sent_variables = {}
        missing = []
        for k in undeclared_diff:
            anno, value, pos = variables_dict[k]
            if value == inspect._empty:
                # [(pos,name),...]
                missing.append((variables_dict[k][2], k))
                continue
            if isinstance(anno, Factory):
                value = value()
            sent_variables[k] = value
        if missing:
            # Print right order
            missing = [n for _,n in sorted(missing)]
            raise TypeError(f'{method.__name__}() missing {len(missing)} required positional stack variable'
                            f'{"s" if len(missing) > 1 else ""}: {", ".join(missing)}')
        with _storage.send_variables(sent_variables):
            for k in undeclared_diff:
                kw[k] = _storage[k]
            return method(*a, **kw)
    return wrapper


def get_declared_variables(method):
    sign = get_typed_signature(method)
    variables_dict = collections.OrderedDict()
    for pos, (param_name, param) in enumerate(sign.parameters.items()):
        if issubclass(param.annotation, Variable):
            variables_dict[param_name] = param.annotation, param.default, pos
    return variables_dict


def get_typed_signature(call: Callable[..., Any]) -> inspect.Signature:
    # From FastAPI (MIT License)
    signature = inspect.signature(call)
    globalns = getattr(call, "__globals__", {})
    typed_params = [
        inspect.Parameter(
            name=param.name,
            kind=param.kind,
            default=param.default,
            annotation=get_typed_annotation(param, globalns),
        )
        for param in signature.parameters.values()
    ]
    typed_signature = inspect.Signature(typed_params)
    return typed_signature


def get_typed_annotation(param: inspect.Parameter, globalns: Dict[str, Any]) -> Any:
    # From FastAPI (MIT License)
    annotation = param.annotation
    if isinstance(annotation, str):
        annotation = ForwardRef(annotation)
        annotation = evaluate_forwardref(annotation, globalns, globalns)
    return annotation


class StackVarNameError(NameError):
    pass


class _VariablesStorage:
    def __init__(self):
        self._thread_stacks = collections.defaultdict(list)

    def send_variables(self, variables_dict, override_dict=None):
        override_dict = override_dict or {}
        for k in variables_dict:
            assert isinstance(k, str), f'Stack variable name {k!r} must be string not {type(k)}'
        created = False
        stack = self._thread_stacks[threading.get_ident()]
        common = None
        should_override = None
        if stack:
            common = set(variables_dict) & stack[-1]
            should_override = set(k for k in common if not override_dict.get(k, False))
        if should_override:
            raise StackVarNameError('You are trying to override existing'
                                    f' stack variables:{",".join(should_override)}'
                                    '. Specify the override flag when declaring.')
        if not stack or common:
            created = True
            stack.append(dict())
        length = len(stack)
        current_vars = stack[length - 1]
        class WithCtx:
            def __enter__(self):
                current_vars.update(variables_dict)
                return variables_dict
            def __exit__(self, exc_type, exc_val, exc_tb):
                if created:
                    assert len(stack) == length, 'You must exit contexts in the correct order'
                    stack.pop()
                else:
                    for key in variables_dict:
                        del current_vars[key]
        return WithCtx()

    def __getitem__(self, key):
        current_vars = self.__contains__(key)
        if current_vars:
            return current_vars[key]
        raise StackVarNameError(f'stack variable {key!r} is not defined')

    def __contains__(self, key):
        stack = self._thread_stacks[threading.get_ident()]
        for current_vars in reversed(stack):
            if key in current_vars:
                return current_vars

    def get_undeclared_diff(self, keys):
        stack = self._thread_stacks[threading.get_ident()]
        if stack:
            diff = keys - set.union(*(set(v.keys()) for v in stack))
            return diff
        return keys

    def __setitem__(self, key, value):
        stack = self._thread_stacks[threading.get_ident()]
        current_vars = self.__contains__(key)
        if not current_vars:
            raise StackVarNameError(f'stack variable {key!r} is not defined')
        elif current_vars and current_vars is not stack[-1]:
            current_vars = stack[-1]
        current_vars[key] = value


_storage = _VariablesStorage()


class _Namespace:
    def __getattr__(self, name):
        if name in _storage:
            return _storage[name]
        raise AttributeError(f'Stack variable {name} undefined')
    def __getitem__(self, name):
        return _storage[name]
    def __contains__(self, name):
        return name in _storage


namespace = _Namespace()
