"""
DFA core module — representation, validation, and utilities.

A DFA is represented as a 5-tuple A = (Q, Σ, τ, q_s, F) where:
    Q   — set of states
    Σ   — set (alphabet)
    τ   — dict mapping (state, letter) -> state for all (q,a) in Q×Σ
    q_s — start state (element of Q)
    F   — set of accepting/final states (subset of Q)
"""

from .core import (
    validate_dfa,
    apply_word,
    apply_letter,
    random_dfa,
    dfa_to_digraph,
    is_synchronizing_word,
)

__all__ = [
    "validate_dfa",
    "apply_word",
    "apply_letter",
    "random_dfa",
    "dfa_to_digraph",
    "is_synchronizing_word",
]
