"""Small library to work with dependencies in Python"""

# import inspect
# from dataclasses import dataclass, field, replace
# from functools import partial
# from typing import Any, Callable, Dict, List, Optional, Type, TypeVar, Union

from .container import Container

__all__ = ['Container']

# __version__ = '0.1.0'

# FACTORY = 'factory'

# SINGLETON = 'singleton'

# TRANSIENT = 'transient'


# T = TypeVar('T')


# @dataclass
# class Parameter:
#     """Represents a name=value pair"""
#     name: str
#     value: Any


# @dataclass
# class Argument:
#     name: str
#     type: Union[Type, str]
#     default: Any


# @dataclass
# class Constructor:
#     constructor: Callable
#     kwargs: Dict[str, Argument]


# def apply(constructor: Constructor, parameters: List[Parameter]) -> Constructor:
#     kwargs_to_apply = {
#         parameter.name: parameter.value for parameter in parameters}

#     # Compute the diff between keys(kwargs_to_apply) and keys(constructor.kwargs)
#     # If all ok, pass the values from kwargs_to_apply to a partial application of
#     # constructor_callable
#     # Remove the corresponding keys from constructor.kwargs

#     constructor_callable = None
#     kwargs = None

#     return replace(
#         constructor,
#         constructor=constructor_callable,
#         kwargs=kwargs,
#     )


# class Dependency:
#     def __init__(self, name: str, constructor: Optional[Constructor] = None):
#         self.name = name
#         self._constructor = constructor

#     @property
#     def constructor(self) -> Optional[Constructor]:
#         return self._constructor

#     @constructor.setter
#     def constructor(self, v: Constructor):
#         self._constructor = v

#     def hash(self) -> int:
#         return hash(self.name)

#     def get(self, container: 'Dil') -> T:
#         if self.constructor is None:
#             raise ValueError(
#                 f'constructor for dependency={self.name} is not set')

#         dependencies = container.dependencies[self]

#         dependency_instances: List[Any] = [dependency.get(
#             container) for dependency in dependencies]

#         return self.constructor(*dependency_instances)


# class Dil:
#     def __init__(self):
#         self.dependencies: Dict[Dependency, List[Dependency]] = {}
#         self.dependency_names: Dict[str, Dependency] = {}

#     def dependency(self, dependency_type=FACTORY) -> Callable[[Callable], Dependency]:
#         def _dependency(constructor):
#             dependencies, handler = inspect_constructor(constructor)

#             self.subscribe_dependencies(
#                 dependencies, handler, constructor, dependency_type)

#             return Dependency(handler)

#         return _dependency

#     def get_instance(self, handler: str):
#         dependency = self.dependency_names[handler]

#         return dependency.get(self)

#     def subscribe_dependencies(
#         self,
#         dependencies: List[str],
#         handler: str,
#         constructor: Constructor,
#         dependency_type: str,
#         type_: Type = object,
#     ):
#         if handler in self.dependency_names:
#             dependency = self.dependency_names[handler]
#             dependency.constructor = constructor
#         else:
#             dependency = Dependency(handler, constructor)
#             self.dependency_names[handler] = dependency

#         _dependencies = [Dependency(name) for name in dependencies]

#         for _dependency in _dependencies:
#             self.dependency_names[_dependency.name] = _dependency

#         self.dependencies[dependency] = _dependencies


# def inspect_constructor(constructor):
#     args = list(inspect.signature(constructor).parameters.keys())

#     return args, constructor.__name__
