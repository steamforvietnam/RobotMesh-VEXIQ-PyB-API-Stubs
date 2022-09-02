"""Documentation Decorators."""


from collections.abc import Sequence
from typing import Any


__all__: Sequence[str] = 'add_doc', 'robotmesh_doc', 'vexcode_doc'


# pylint: disable=too-few-public-methods


class add_doc:   # noqa: N801
    """Add documentation."""

    def __init__(self, doc_str: str = '', /):
        """Initialize decorator with docstring."""
        self.doc_str: str = doc_str

    def __call__(self, member: Any, /):
        """Add documentation."""
        member.__doc__ += self.doc_str
        return member


class robotmesh_doc(add_doc):   # noqa: N801
    """Add Robot Mesh Python B documentation."""

    def __init__(self, doc_str: str = '', /):
        """Initialize decorator with docstring."""
        super().__init__(f'\n\nROBOT MESH PYTHON B:\n{doc_str}\n')


class vexcode_doc(add_doc):   # noqa: N801
    """Add VEXcode Python documentation."""

    def __init__(self, doc_str: str = '', /):
        """Initialize decorator with docstring."""
        super().__init__(f'\n\nVEXCODE PYTHON:\n{doc_str}\n')