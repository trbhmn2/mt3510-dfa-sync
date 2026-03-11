"""
Part 2: DFA Isomorphism testing — strict, weak, and semi-isomorphism.

Three levels (descending strictness):

1. Strict isomorphism (common Σ):
   Find bijection f: Q1 → Q2 such that:
   - τ2(f(q), a) = f(τ1(q, a)) for all q ∈ Q1, a ∈ Σ
   - f(q_s1) = q_s2
   - f(F1) = F2

2. Weak isomorphism (possibly different Σ1, Σ2):
   Find bijections f: Q1 → Q2 and g: Σ1 → Σ2 such that:
   - τ2(f(q), g(a)) = f(τ1(q, a)) for all q ∈ Q1, a ∈ Σ1
   - f(q_s1) = q_s2
   - f(F1) = F2

3. Semi-isomorphism:
   Find bijections f: Q1 → Q2 and g: Σ1 → Σ2 such that:
   - τ2(f(q), g(a)) = f(τ1(q, a)) for all q ∈ Q1, a ∈ Σ1
   (start state and final states are ignored)

Efficiency considerations:
    - Quick rejections: |Q1| != |Q2|, |Σ1| != |Σ2|, degree sequences, etc.
    - For strict iso, f(q_s1) = q_s2 is forced, so BFS/DFS from start state
      can determine f entirely (since all states are reachable from q_s).
    - For weak/semi, we must also search over alphabet permutations.
    - Since m ≪ n, iterating over alphabet permutations (m!) is cheap.
    - Canonical form / colour refinement can prune the state search space.

All three share significant common code — the core check is the same,
just with different constraints on what f and g must preserve.
"""

from itertools import permutations
from typing import Any, Dict, List, Optional, Set, Tuple

from dfa.core import DFA, State, Letter


def _quick_reject(A1: DFA, A2: DFA, check_alphabet: bool = True) -> bool:
    """
    Quick rejection tests before attempting full isomorphism search.

    Returns True if A1 and A2 CANNOT be isomorphic.

    Checks:
        - |Q1| == |Q2|
        - |Σ1| == |Σ2| (if check_alphabet)
        - |F1| == |F2| (for strict/weak only — caller decides)
        - Out-degree multisets match (structural invariant)
    """
    # TODO: Implement quick rejection
    pass


def _try_state_bijection_from_start(
    A1: DFA, A2: DFA, g: Optional[Dict[Letter, Letter]] = None
) -> Optional[Dict[State, State]]:
    """
    Attempt to build a state bijection f: Q1 → Q2 by BFS from start states.

    Since all states are reachable from q_s, we can determine f entirely:
    - f(q_s1) = q_s2 (forced)
    - For each visited q with f(q) known, for each a ∈ Σ:
        f(τ1(q, a)) must equal τ2(f(q), a_mapped)
      where a_mapped = g(a) if g is given, else a.
    - If this forces a contradiction, return None.

    Parameters:
        A1, A2 — DFA 5-tuples
        g      — alphabet bijection (None = identity, i.e. strict iso)

    Returns:
        Dict mapping Q1 states to Q2 states, or None if no consistent bijection exists.
    """
    # TODO: Implement BFS bijection construction
    pass


def is_isomorphic(A1: DFA, A2: DFA) -> bool:
    """
    Task 2(a): Test if A1 and A2 are strictly isomorphic.

    Requires common alphabet Σ. Finds bijection f: Q1 → Q2 preserving
    transitions, start state, and final states.

    Since all states are reachable from q_s, the mapping f is uniquely
    determined by f(q_s1) = q_s2 — we just need to check consistency.

    Parameters:
        A1, A2 — DFA 5-tuples with the same alphabet Σ

    Returns:
        True if A1 ≅ A2 (strictly isomorphic), False otherwise.
    """
    # TODO: Implement
    pass


def is_weakly_isomorphic(A1: DFA, A2: DFA) -> bool:
    """
    Task 2(b): Test if A1 and A2 are weakly isomorphic.

    Allows different alphabets Σ1, Σ2 (must have same size).
    Finds bijections f: Q1 → Q2 and g: Σ1 → Σ2 preserving transitions,
    start state, and final states.

    Strategy: iterate over all permutations of Σ2 (since m ≪ n, m! is small),
    and for each alphabet mapping g, attempt to build f via BFS from start states.

    Parameters:
        A1, A2 — DFA 5-tuples

    Returns:
        True if A1 and A2 are weakly isomorphic, False otherwise.
    """
    # TODO: Implement
    pass


def is_semi_isomorphic(A1: DFA, A2: DFA) -> bool:
    """
    Task 2(c): Test if A1 and A2 are semi-isomorphic.

    Like weak isomorphism but ignores start state and final states.
    Only requires τ2(f(q), g(a)) = f(τ1(q, a)) for all q, a.

    Since we can't anchor f via start states, we must try mapping
    each q ∈ Q1 to each r ∈ Q2 as a potential start point for BFS.
    Combined with alphabet permutations, this gives |Q| × |Σ|! candidates.

    Efficiency: use invariants (e.g. in-degree/out-degree profiles) to
    prune candidate mappings before full BFS.

    Parameters:
        A1, A2 — DFA 5-tuples

    Returns:
        True if A1 and A2 are semi-isomorphic, False otherwise.
    """
    # TODO: Implement
    pass
