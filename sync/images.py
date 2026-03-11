"""
Tasks (b) and (d): Synchronization via image BFS.

Algorithm:
    Instead of enumerating all transformations in T_A (which can be huge),
    we enumerate only the *images* of transformations. There are at most
    2^|Q| distinct images (subsets of Q), which is often much smaller than |T_A|.

    Key insight: if t has image R ⊆ Q, then t · t_a has image {t_a(r) : r ∈ R} = t_a(R).

    BFS approach:
    - Start with Q (the image of the identity transformation)
    - For each image R, compute t_a(R) = {τ(r, a) : r ∈ R} for each a ∈ Σ
    - If any image has size 1, the DFA is synchronizing
    - Track visited images (as frozensets)

    Task (d) extension — shortest reset word via ancestors:
    - During BFS, record the parent of each image and the letter used
    - When a singleton image is found, trace back through ancestors
      to reconstruct the word (sequence of letters) that produced it
    - Since BFS explores by word length, this gives a shortest reset word
"""

from collections import deque
from typing import Dict, FrozenSet, List, Optional, Set, Tuple

from dfa.core import DFA, State, Letter


def is_synchronizing_images(A: DFA) -> bool:
    """
    Task (b): Test if DFA A is synchronizing by BFS over images of transformations.

    More efficient than monoid enumeration since |images| ≤ 2^|Q| ≪ |Q|^|Q|.

    Parameters:
        A — a valid DFA 5-tuple

    Returns:
        True if A is synchronizing, False otherwise.
    """
    # TODO: Implement BFS over images
    pass


def shortest_reset_word_images(A: DFA) -> Optional[List[Letter]]:
    """
    Task (d): Find a shortest-length synchronizing (reset) word using image BFS
    with the ancestors method.

    BFS guarantees that the first singleton image found corresponds to the
    shortest word. By tracking parent images and the letter used at each step,
    we can reconstruct the word by tracing back from the singleton to Q.

    Parameters:
        A — a valid DFA 5-tuple

    Returns:
        A list of letters forming a shortest reset word, or None if A is not synchronizing.
    """
    # TODO: Implement BFS with ancestor tracking
    pass
