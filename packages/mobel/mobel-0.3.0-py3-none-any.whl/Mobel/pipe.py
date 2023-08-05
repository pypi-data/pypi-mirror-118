from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Optional, TypeVar, TypedDict, overload


@dataclass
class DecoratorDefinition:
    decorator: Callable[..., Callable]
    arguments: Optional[List[str]] = None
    mapping: Optional[Dict[str, str]] = None


F = TypeVar("F", bound=Callable)


def mapArguments(decoratorDefinition: DecoratorDefinition, kwargs: Dict[str, Any]):
    if decoratorDefinition.arguments is None:
        return {}

    callArguments = {}
    mapping = {}
    if decoratorDefinition.mapping is not None:
        mapping = decoratorDefinition.mapping

    for key, value in kwargs.items():
        mapped_key = key
        if key in mapping:
            mapped_key = mapping[key]
        if mapped_key in decoratorDefinition.arguments:
            callArguments[mapped_key] = value

    return callArguments


def pipeDecorators(decoratorDefinitions: List[DecoratorDefinition]) -> Callable[..., Callable]:
    @overload
    def decoratorOrFactory(f: None, **kwargs) -> Callable[[F], F]: ...

    @overload
    def decoratorOrFactory(f: F) -> F: ...

    def decoratorOrFactory(f=None, /, **kwargs):
        if f is not None:
            result_f = f
            for decoratorDefinition in decoratorDefinitions:
                result_f = decoratorDefinition.decorator(result_f)
            return result_f

        decorators: List[Callable[[F], F]] = []

        for decoratorDefinition in decoratorDefinitions:
            decoratorFactory = decoratorDefinition.decorator
            mappedArguments = mapArguments(decoratorDefinition, kwargs)
            if len(mappedArguments) == 0:
                decorators.append(decoratorFactory)
            else:
                decorators.append(
                    decoratorFactory(**mappedArguments)
                )

        def decorator(f: F) -> F:
            result_f = f
            for decorator in decorators:
                result_f = decorator(result_f)
            return result_f

        return decorator

    return decoratorOrFactory
