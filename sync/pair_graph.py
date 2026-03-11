"""
Tasks (c) and (e): Synchronization via pair graph.

Algorithm:
    Theorem: A DFA is synchronizing iff for every pair of distinct states {q1, q2},
    there exists a word that maps both to a common state.

    Pair digraph Γ_A:
    - Vertices: all 2-element subsets {q1, q2} of Q, plus singletons {q, q}
      Represent vertices as frozenset({q1, q2}). Singletons: frozenset({q}).
    - Edges: {q1, q2} → {τ(q1, a), τ(q2, a)} for each letter a ∈ Σ
      (edge labelled with letter a)
    - A is synchronizing iff every pair vertex can reach some singleton vertex.

    Task (e) — finding a reset word via iterative merging:
    1. Start with Q_0 = Q (set of all states)
    2. Pick two distinct elements q1, q2 from Q_i
    3. Find shortest path in pair graph from {q1, q2} to any singleton {r}
    4. Read off the word from edge labels along the path
    5. Apply this word to ALL states in Q_i to get Q_{i+1}
    6. Repeat until |Q_i| = 1
    7. Concatenate all words to get the reset word

    Note: This does NOT produce a shortest reset word in general,
    but it does produce a valid one.
"""

from collections import deque
from typing import Dict, FrozenSet, List, Optional, Set, Tuple

import networkx as nx

from dfa.core import DFA, State, Letter


def build_pair_graph(A: DFA) -> nx.DiGraph:
    """
    Build the pair digraph Γ_A for a DFA.

    Vertices are frozensets of 1 or 2 states.
    Edges are labelled with the alphabet letter that induces them.

    Returns a NetworkX DiGraph (or MultiDiGraph if preferred).
    """
    # TODO: Implement
    pass


def is_synchronizing_pair_graph(A: DFA) -> bool:
    """
    Task (c): Test if DFA A is synchronizing using the pair graph method.

    Builds the pair digraph and checks that every pair vertex {q1, q2}
    can reach some singleton vertex {r, r}.

    Parameters:
        A — a valid DFA 5-tuple

    Returns:
        True if A is synchronizing, False otherwise.
    """
    # TODO: Implement
    pass


def reset_word_pair_graph(A: DFA) -> Optional[List[Letter]]:
    """
    Task (e): Find a reset word using the pair graph method (iterative merging).

    This method iteratively picks pairs of states, finds words to merge them
    using shortest paths in the pair graph, and applies those words to the
    remaining state set. The concatenation of all merging words is a reset word.

    Note: The resulting word is generally NOT shortest-length. See heuristic.py
    for attempts at shortening.

    Parameters:
        A — a valid DFA 5-tuple

    Returns:
        A list of letters forming a reset word, or None if A is not synchronizing.
    """
    # TODO: Implement iterative merging
    pass
