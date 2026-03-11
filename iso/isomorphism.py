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

from collections import Counter, deque
from itertools import permutations
from typing import Any, Dict, List, Optional, Set, Tuple

from dfa.core import DFA, State, Letter


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _out_degree_sequence(A: DFA) -> List[int]:
    """
    Return the sorted multiset of distinct-target out-degrees for every state.

    For each state q, count the number of *distinct* target states across
    all letters.  The sorted list of these counts is a structural invariant
    preserved by any state bijection (regardless of alphabet relabelling).
    """
    Q, Sigma, tau, _, _ = A
    degrees = []
    for q in Q:
        targets = {tau[(q, a)] for a in Sigma}
        degrees.append(len(targets))
    degrees.sort()
    return degrees


def _in_degree_sequence(A: DFA) -> List[int]:
    """
    Return the sorted multiset of in-degrees (counting multiplicity of
    incoming (state, letter) pairs) for every state.
    """
    Q, Sigma, tau, _, _ = A
    in_deg: Dict[State, int] = {q: 0 for q in Q}
    for (q, a), r in tau.items():
        in_deg[r] += 1
    result = sorted(in_deg.values())
    return result


def _quick_reject(A1: DFA, A2: DFA, check_alphabet: bool = True,
                  check_finals: bool = True) -> bool:
    """
    Quick rejection tests before attempting full isomorphism search.

    Returns True if A1 and A2 CANNOT be isomorphic.

    Checks:
        - |Q1| == |Q2|
        - |Σ1| == |Σ2| (if check_alphabet)
        - |F1| == |F2| (if check_finals, for strict/weak only)
        - In-degree multisets match
        - Distinct-target out-degree multisets match
    """
    Q1, Sigma1, tau1, q_s1, F1 = A1
    Q2, Sigma2, tau2, q_s2, F2 = A2

    if len(Q1) != len(Q2):
        return True

    if check_alphabet and len(Sigma1) != len(Sigma2):
        return True

    if check_finals and len(F1) != len(F2):
        return True

    # Structural invariants — degree sequences must match
    if _in_degree_sequence(A1) != _in_degree_sequence(A2):
        return True

    if _out_degree_sequence(A1) != _out_degree_sequence(A2):
        return True

    return False


def _try_state_bijection_from_start(
    A1: DFA, A2: DFA,
    g: Optional[Dict[Letter, Letter]] = None,
    start_q1: Optional[State] = None,
    start_q2: Optional[State] = None,
) -> Optional[Dict[State, State]]:
    """
    Attempt to build a state bijection f: Q1 → Q2 by BFS from a given
    anchor mapping start_q1 → start_q2.

    Since all states are reachable from q_s, BFS from the anchor will
    visit every state in Q1 and determine f entirely:
    - f(start_q1) = start_q2 (forced)
    - For each visited q with f(q) known, for each a ∈ Σ1:
        f(τ1(q, a)) must equal τ2(f(q), g(a))
      where g(a) = a if g is None (identity / strict iso).
    - If this forces a contradiction (a state already mapped differently),
      return None.

    After BFS, verify f covers all of Q2 (surjective ⇒ bijection since
    |Q1| = |Q2|).

    Parameters:
        A1, A2   — DFA 5-tuples
        g        — alphabet bijection Σ1 → Σ2 (None = identity)
        start_q1 — anchor state in Q1 (default: q_s1)
        start_q2 — anchor state in Q2 (default: q_s2)

    Returns:
        Dict mapping Q1 states to Q2 states, or None if no consistent
        bijection exists from this anchor.
    """
    Q1, Sigma1, tau1, q_s1, F1 = A1
    Q2, Sigma2, tau2, q_s2, F2 = A2

    if start_q1 is None:
        start_q1 = q_s1
    if start_q2 is None:
        start_q2 = q_s2

    # f: Q1 → Q2,  f_inv tracks which Q2 states are already used
    f: Dict[State, State] = {}
    used_q2: Set[State] = set()

    f[start_q1] = start_q2
    used_q2.add(start_q2)

    queue: deque = deque([start_q1])

    while queue:
        q = queue.popleft()
        fq = f[q]

        for a in Sigma1:
            # Where q goes in A1 under letter a
            target1 = tau1[(q, a)]
            # The corresponding letter in A2
            a2 = g[a] if g is not None else a
            # Where f(q) goes in A2 under the mapped letter
            target2 = tau2[(fq, a2)]

            if target1 in f:
                # Already mapped — check consistency
                if f[target1] != target2:
                    return None
            else:
                # New mapping — check target2 isn't already used
                if target2 in used_q2:
                    return None
                f[target1] = target2
                used_q2.add(target2)
                queue.append(target1)

    # Verify surjectivity (f covers all of Q2)
    if len(f) != len(Q1) or used_q2 != Q2:
        return None

    return f


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

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
    Q1, Sigma1, tau1, q_s1, F1 = A1
    Q2, Sigma2, tau2, q_s2, F2 = A2

    # Strict iso requires identical alphabets
    if Sigma1 != Sigma2:
        return False

    # Quick structural rejection
    if _quick_reject(A1, A2, check_alphabet=True, check_finals=True):
        return False

    # BFS — f is uniquely determined (identity alphabet map)
    f = _try_state_bijection_from_start(A1, A2, g=None)
    if f is None:
        return False

    # Verify final-state preservation: f(F1) == F2
    mapped_finals = {f[q] for q in F1}
    return mapped_finals == F2


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
    Q1, Sigma1, tau1, q_s1, F1 = A1
    Q2, Sigma2, tau2, q_s2, F2 = A2

    # Quick structural rejection
    if _quick_reject(A1, A2, check_alphabet=True, check_finals=True):
        return False

    sigma1_list = sorted(Sigma1, key=str)
    sigma2_list = sorted(Sigma2, key=str)

    # Try every permutation of Σ2 as a candidate alphabet bijection g
    for perm in permutations(sigma2_list):
        g = dict(zip(sigma1_list, perm))

        f = _try_state_bijection_from_start(A1, A2, g=g)
        if f is None:
            continue

        # Verify final-state preservation
        mapped_finals = {f[q] for q in F1}
        if mapped_finals == F2:
            return True

    return False


def is_semi_isomorphic(A1: DFA, A2: DFA) -> bool:
    """
    Task 2(c): Test if A1 and A2 are semi-isomorphic.

    Like weak isomorphism but ignores start state and final states.
    Only requires τ2(f(q), g(a)) = f(τ1(q, a)) for all q, a.

    Since we can't anchor f via start states, we try mapping q_s1 to
    each q2 ∈ Q2.  All states are reachable from q_s1 in A1, so BFS
    from that anchor determines f entirely.  Combined with alphabet
    permutations this gives |Q2| × m! candidates.

    Parameters:
        A1, A2 — DFA 5-tuples

    Returns:
        True if A1 and A2 are semi-isomorphic, False otherwise.
    """
    Q1, Sigma1, tau1, q_s1, F1 = A1
    Q2, Sigma2, tau2, q_s2, F2 = A2

    # Quick rejection — don't check finals (semi ignores them)
    if _quick_reject(A1, A2, check_alphabet=True, check_finals=False):
        return False

    sigma1_list = sorted(Sigma1, key=str)
    sigma2_list = sorted(Sigma2, key=str)

    # Precompute all alphabet permutations (m! — small)
    alphabet_perms = [
        dict(zip(sigma1_list, perm)) for perm in permutations(sigma2_list)
    ]

    # Try every candidate anchor q_s1 → q2, for every alphabet bijection g
    for q2 in Q2:
        for g in alphabet_perms:
            f = _try_state_bijection_from_start(
                A1, A2, g=g, start_q1=q_s1, start_q2=q2
            )
            if f is not None:
                return True

    return False
