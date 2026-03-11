"""
DFA core utilities — validation, word application, random generation, conversion.
"""

import random as _random
from typing import Any, Dict, FrozenSet, List, Optional, Set, Tuple

import networkx as nx

# Type aliases for clarity
State = Any
Letter = Any
TransitionDict = Dict[Tuple[State, Letter], State]
DFA = Tuple[Set[State], Set[Letter], TransitionDict, State, Set[State]]


def validate_dfa(A: DFA) -> bool:
    """
    Validate that A = (Q, Σ, τ, q_s, F) is a well-formed complete DFA.

    Checks:
        - A is a 5-tuple
        - Q and Σ are non-empty sets
        - τ has an entry for every (q, a) in Q × Σ
        - All transition targets are in Q
        - q_s ∈ Q
        - F ⊆ Q

    Returns True if valid, raises ValueError with description otherwise.
    """
    if not isinstance(A, tuple) or len(A) != 5:
        raise ValueError("DFA must be a 5-tuple (Q, Σ, τ, q_s, F)")

    Q, Sigma, tau, q_s, F = A

    if not isinstance(Q, set) or len(Q) == 0:
        raise ValueError("Q must be a non-empty set")
    if not isinstance(Sigma, set) or len(Sigma) == 0:
        raise ValueError("Σ must be a non-empty set")
    if not isinstance(tau, dict):
        raise ValueError("τ must be a dict")
    if q_s not in Q:
        raise ValueError(f"Start state {q_s} not in Q")
    if not isinstance(F, set) or not F.issubset(Q):
        raise ValueError("F must be a set that is a subset of Q")

    # Check completeness: every (q, a) pair must be defined
    for q in Q:
        for a in Sigma:
            if (q, a) not in tau:
                raise ValueError(f"Transition undefined for state {q}, letter {a}")
            if tau[(q, a)] not in Q:
                raise ValueError(
                    f"Transition target {tau[(q, a)]} for ({q}, {a}) not in Q"
                )

    return True


def apply_letter(A: DFA, q: State, a: Letter) -> State:
    """Apply a single letter a to state q in DFA A, returning τ(q, a)."""
    _, _, tau, _, _ = A
    return tau[(q, a)]


def apply_word(A: DFA, q: State, word: List[Letter]) -> State:
    """
    Apply a sequence of letters (a word) to state q, returning the final state.

    Parameters:
        A    — a DFA 5-tuple
        q    — starting state
        word — list/sequence of letters from Σ

    Returns the state reached after reading all letters in order.
    """
    _, _, tau, _, _ = A
    current = q
    for a in word:
        current = tau[(current, a)]
    return current


def apply_word_to_set(A: DFA, states: Set[State], word: List[Letter]) -> Set[State]:
    """
    Apply a word to every state in a set, returning the set of resulting states.

    Useful for checking reset words: if |apply_word_to_set(A, Q, w)| == 1, w is a reset word.
    """
    return {apply_word(A, q, word) for q in states}


def is_synchronizing_word(A: DFA, word: List[Letter]) -> bool:
    """
    Check if a given word is a reset (synchronizing) word for DFA A.

    A word w is a reset word if applying w from every state in Q
    leads to a single common state.
    """
    Q = A[0]
    result_states = apply_word_to_set(A, Q, word)
    return len(result_states) == 1


def random_dfa(
    n: int, m: int = 2, num_final: Optional[int] = None, seed: Optional[int] = None
) -> DFA:
    """
    Generate a random DFA with n states and alphabet of size m.

    Each transition τ(q, a) is chosen uniformly at random from Q.
    Random DFAs are almost surely synchronizing for |Σ| >= 2 as n → ∞.

    Parameters:
        n         — number of states (Q = {0, 1, ..., n-1})
        m         — alphabet size (Σ = {0, 1, ..., m-1}), default 2
        num_final — number of accepting states (random subset), default n//3
        seed      — random seed for reproducibility

    Returns a DFA 5-tuple.
    """
    if seed is not None:
        _random.seed(seed)

    Q = set(range(n))
    Sigma = set(range(m))

    tau = {}
    for q in Q:
        for a in Sigma:
            tau[(q, a)] = _random.randint(0, n - 1)

    q_s = 0

    if num_final is None:
        num_final = max(1, n // 3)
    F = set(_random.sample(list(Q), min(num_final, n)))

    return (Q, Sigma, tau, q_s, F)


def dfa_to_digraph(A: DFA) -> nx.DiGraph:
    """
    Convert a DFA to a NetworkX DiGraph for visualization or analysis.

    Each edge (q, τ(q,a)) is labelled with the letter a.
    Multiple letters on the same edge are stored as a list.
    """
    Q, Sigma, tau, q_s, F = A
    G = nx.DiGraph()

    for q in Q:
        G.add_node(q, start=(q == q_s), accepting=(q in F))

    for (q, a), r in tau.items():
        if G.has_edge(q, r):
            G[q][r]["labels"].append(a)
        else:
            G.add_edge(q, r, labels=[a])

    return G


def non_synchronizing_dfa(n: int, m: int = 2) -> DFA:
    """
    Generate a simple non-synchronizing DFA with n states.

    Creates a DFA where each letter acts as a permutation on Q,
    ensuring no reset word exists (permutation groups can't contain
    constant maps).

    Useful for testing that sync-detection correctly returns False.
    """
    Q = set(range(n))
    Sigma = set(range(m))
    tau = {}

    # Letter 0: identity permutation
    for q in Q:
        tau[(q, 0)] = q

    # Letter 1 (and others): cyclic shift
    for a in range(1, m):
        for q in Q:
            tau[(q, a)] = (q + a) % n

    return (Q, Sigma, tau, 0, {0})
