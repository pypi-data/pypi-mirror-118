from dataclasses import dataclass
from typing import Callable, Optional, Type, TypeVar, Union

from .common import ANNOTATION_DIR


class Annotation:

    def __new__(cls, f: Optional[Callable] = None, /, **kwargs):
        data_cls = dataclass(cls)
        annotation_instance = super(Annotation, data_cls).__new__(cls)
        if f is None:
            return annotation_instance
        try:
            data_cls(**kwargs)
        except TypeError as e:
            raise TypeError("Annotation " + str(e)[11:])
        return annotation_instance(f)

    def __call__(self, f):
        if hasattr(f, ANNOTATION_DIR):
            getattr(f, ANNOTATION_DIR)[self.__class__.__name__] = self
        else:
            setattr(f, ANNOTATION_DIR, {self.__class__.__name__: self})
        return f


def hasAnnotation(f: Union[Callable, Type], annotation: Union[str, Type[Annotation]]) -> bool:
    if not hasattr(f, ANNOTATION_DIR):
        return False
    if isinstance(annotation, str):
        return annotation in getattr(f, ANNOTATION_DIR)
    return annotation.__name__ in getattr(f, ANNOTATION_DIR)


T = TypeVar("T", bound=Annotation)


def getAnnotation(f: Union[Callable, Type], annotation: Type[T]) -> Optional[T]:
    if not hasattr(f, ANNOTATION_DIR):
        return None
    return getattr(f, ANNOTATION_DIR).get(annotation.__name__, None)
