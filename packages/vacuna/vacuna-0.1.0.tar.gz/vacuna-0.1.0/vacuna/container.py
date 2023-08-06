from typing import Any, Callable, List, Optional, Union

FACTORY = 'FACTORY'
SINGLETON = 'SINGLETON'
RESOURCE = 'RESOURCE'


class Dependency:
    def __init__(
        self,
        name: str,
        dependencies: Optional[List['Dependency']] = None
    ):
        self.name = name
        self.dependencies = default_if_none(dependencies, list)

    def __getattr__(self, name) -> 'Dependency':
        pass

    def __getitem__(self, idx) -> 'Dependency':
        pass


class DependencyBuilder:
    def depends_on(
        self,
        *args: Dependency,
        **kwargs: Dependency
    ) -> 'DependencyBuilder':
        pass

    def build(self, fn) -> Dependency:
        pass

    __call__ = build


class Container:
    """Container"""

    def dependency(self, kind=FACTORY) -> DependencyBuilder:
        pass

    def get(self, dep: Dependency) -> List[Any]:
        pass

    def run(self, dep: Dependency):
        with self.context():
            self.get(dep)

    def context(self) -> 'Container':
        pass

    def __enter__(self) -> 'Container':
        pass

    def __exit__(self, *args: Any) -> None:
        pass


# -- utils -- #

def default_if_none(x, default):
    if x is None:
        return default()
    return x
