"""
Tasks (c) and (e): Synchronization via pair graph.

Algorithm:
    Theorem: A DFA is synchronizing iff for every pair of distinct states {q1, q2},
    there exists a word that maps both to a common state.

    Pair digraph Γ_A:
    - Vertices: all 2-element subsets {q1, q2} of Q, plus singletons {q}
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

from dfa.core import DFA, State, Letter, apply_word_to_set


def build_pair_graph(A: DFA) -> nx.DiGraph:
    """
    Build the pair digraph Γ_A for a DFA.

    Vertices are frozensets of 1 or 2 states.
    Edges are labelled with the alphabet letter that induces them.

    Returns a NetworkX DiGraph. For multiple letters producing the same edge,
    only one letter is stored (first encountered); for BFS shortest path
    any single label suffices.
    """
    Q, Sigma, tau, _, _ = A
    G = nx.DiGraph()

    states = sorted(Q)

    # Add all singleton and pair vertices
    for q in states:
        G.add_node(frozenset({q}))
    for i, q1 in enumerate(states):
        for q2 in states[i + 1:]:
            G.add_node(frozenset({q1, q2}))

    # Add edges
    for node in list(G.nodes()):
        elems = sorted(node)
        for a in Sigma:
            if len(elems) == 1:
                target = frozenset({tau[(elems[0], a)]})
            else:
                target = frozenset({tau[(elems[0], a)], tau[(elems[1], a)]})
            # Only add edge if not already present (keep first letter)
            if not G.has_edge(node, target):
                G.add_edge(node, target, letter=a)

    return G


def _find_merge_word(G: nx.DiGraph, pair: FrozenSet[State], singletons: Set[FrozenSet[State]]) -> Optional[List[Letter]]:
    """
    BFS from a pair vertex to any singleton vertex in the pair graph.
    Returns the sequence of letters along the shortest path, or None if unreachable.
    """
    if pair in singletons:
        return []

    # BFS with ancestor tracking
    ancestor = {pair: None}
    queue = deque([pair])

    while queue:
        node = queue.popleft()
        for _, target, data in G.out_edges(node, data=True):
            if target not in ancestor:
                ancestor[target] = (node, data['letter'])
                if target in singletons:
                    # Trace back
                    word = []
                    current = target
                    while ancestor[current] is not None:
                        parent, letter = ancestor[current]
                        word.append(letter)
                        current = parent
                    word.reverse()
                    return word
                queue.append(target)

    return None


def is_synchronizing_pair_graph(A: DFA) -> bool:
    """
    Task (c): Test if DFA A is synchronizing using the pair graph method.

    Builds the pair digraph and checks that every pair vertex {q1, q2}
    can reach some singleton vertex {r}.

    Parameters:
        A — a valid DFA 5-tuple

    Returns:
        True if A is synchronizing, False otherwise.
    """
    Q, Sigma, tau, _, _ = A
    G = build_pair_graph(A)

    singletons = {frozenset({q}) for q in Q}

    # Check every pair (2-element) vertex can reach a singleton
    states = sorted(Q)
    for i, q1 in enumerate(states):
        for q2 in states[i + 1:]:
            pair = frozenset({q1, q2})
            # Check if any singleton is reachable
            reachable = False
            for s in singletons:
                if nx.has_path(G, pair, s):
                    reachable = True
                    break
            if not reachable:
                return False

    return True


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
    Q, Sigma, tau, _, _ = A
    G = build_pair_graph(A)

    singletons = {frozenset({q}) for q in Q}
    current_states = set(Q)
    full_word = []

    while len(current_states) > 1:
        # Pick two distinct states
        state_list = sorted(current_states)
        q1, q2 = state_list[0], state_list[1]
        pair = frozenset({q1, q2})

        merge_word = _find_merge_word(G, pair, singletons)
        if merge_word is None:
            return None  # Not synchronizing

        # Apply merge_word to ALL current states
        current_states = apply_word_to_set(A, current_states, merge_word)
        full_word.extend(merge_word)

    return full_word
