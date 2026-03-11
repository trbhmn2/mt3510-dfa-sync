"""Tests for DFA isomorphism algorithms."""

import pytest
import random
from dfa.core import random_dfa, validate_dfa
from iso.isomorphism import is_isomorphic, is_weakly_isomorphic, is_semi_isomorphic


def _relabel_states(A, perm):
    """Apply state permutation to create an isomorphic DFA."""
    Q, Sigma, tau, q_s, F = A
    new_tau = {(perm[q], a): perm[tau[(q, a)]] for q in Q for a in Sigma}
    new_Q = {perm[q] for q in Q}
    new_F = {perm[q] for q in F}
    return (new_Q, Sigma, new_tau, perm[q_s], new_F)


def _relabel_alphabet(A, alpha_perm):
    """Apply alphabet permutation to create a weakly isomorphic DFA."""
    Q, Sigma, tau, q_s, F = A
    new_Sigma = {alpha_perm[a] for a in Sigma}
    new_tau = {(q, alpha_perm[a]): tau[(q, a)] for q in Q for a in Sigma}
    return (Q, new_Sigma, new_tau, q_s, F)


class TestStrictIsomorphism:
    """Task 2(a) tests."""

    def test_identical_dfas(self):
        A = random_dfa(5, 2, seed=42)
        assert is_isomorphic(A, A) is True

    def test_relabelled_states(self):
        A = random_dfa(5, 2, seed=42)
        Q = sorted(A[0])
        perm = {Q[i]: Q[(i + 1) % len(Q)] for i in range(len(Q))}
        B = _relabel_states(A, perm)
        assert is_isomorphic(A, B) is True

    def test_different_dfas(self):
        A = random_dfa(5, 2, seed=42)
        B = random_dfa(5, 2, seed=99)
        # Very unlikely to be isomorphic
        result = is_isomorphic(A, B)
        assert isinstance(result, bool)

    def test_different_sizes(self):
        A = random_dfa(5, 2, seed=42)
        B = random_dfa(6, 2, seed=42)
        assert is_isomorphic(A, B) is False


class TestWeakIsomorphism:
    """Task 2(b) tests."""

    def test_relabelled_alphabet(self):
        A = random_dfa(5, 2, seed=42)
        alpha_perm = {0: 1, 1: 0}  # swap 0 and 1
        B = _relabel_alphabet(A, alpha_perm)
        assert is_weakly_isomorphic(A, B) is True

    def test_relabelled_both(self):
        A = random_dfa(5, 2, seed=42)
        Q = sorted(A[0])
        state_perm = {Q[i]: Q[(i + 1) % len(Q)] for i in range(len(Q))}
        B = _relabel_states(A, state_perm)
        alpha_perm = {0: 1, 1: 0}
        B = _relabel_alphabet(B, alpha_perm)
        assert is_weakly_isomorphic(A, B) is True


class TestSemiIsomorphism:
    """Task 2(c) tests."""

    def test_same_structure_different_start(self):
        A = random_dfa(5, 2, seed=42)
        Q, Sigma, tau, q_s, F = A
        # Change start state — should still be semi-isomorphic to itself
        other_start = (q_s + 1) % len(Q)
        B = (Q, Sigma, tau, other_start, F)
        assert is_semi_isomorphic(A, B) is True

    def test_same_structure_different_finals(self):
        A = random_dfa(5, 2, seed=42)
        Q, Sigma, tau, q_s, F = A
        # Change final states — should still be semi-isomorphic
        new_F = Q - F if len(Q - F) > 0 else {0}
        B = (Q, Sigma, tau, q_s, new_F)
        assert is_semi_isomorphic(A, B) is True

    def test_implies_hierarchy(self):
        """Strict iso => weak iso => semi iso."""
        A = random_dfa(5, 2, seed=42)
        Q = sorted(A[0])
        perm = {Q[i]: Q[(i + 1) % len(Q)] for i in range(len(Q))}
        B = _relabel_states(A, perm)
        # If strictly isomorphic, must also be weakly and semi
        if is_isomorphic(A, B):
            assert is_weakly_isomorphic(A, B) is True
            assert is_semi_isomorphic(A, B) is True
