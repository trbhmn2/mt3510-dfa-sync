"""
Isomorphism module — three levels of DFA isomorphism testing.

1. Strict isomorphism: bijection on states only (common alphabet)
2. Weak isomorphism: bijections on states AND alphabet
3. Semi-isomorphism: bijections on states and alphabet, ignoring start/final states
"""

from .isomorphism import (
    is_isomorphic,
    is_weakly_isomorphic,
    is_semi_isomorphic,
)

__all__ = [
    "is_isomorphic",
    "is_weakly_isomorphic",
    "is_semi_isomorphic",
]
