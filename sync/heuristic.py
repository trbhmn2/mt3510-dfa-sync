"""
Task (f): Heuristic shortening of reset words from the pair graph method.

The pair graph method (Task e) produces valid reset words, but they can be
much longer than the shortest reset word (Task d). This module provides
heuristic methods to shorten them.

Possible heuristic approaches:
    1. Greedy trimming: try removing each letter from the word and check if
       the result is still a reset word.
    2. Sliding window: try replacing subsequences with shorter alternatives.
    3. Suffix trimming: the final suffix might be longer than needed.
    4. Pair selection heuristic: in the iterative merging, choosing which
       pair to merge first can affect total word length. Try merging pairs
       that are "closest" in the pair graph first.
    5. Word compression: look for repeated subwords that can be simplified.

The analysis of why a heuristic works (or doesn't) is as important as the
implementation itself.
"""

from typing import List, Optional, Callable

from dfa.core import DFA, Letter, is_synchronizing_word


def shorten_reset_word(
    A: DFA,
    word: List[Letter],
    method: str = "greedy",
) -> List[Letter]:
    """
    Task (f): Attempt to heuristically shorten a reset word.

    Parameters:
        A      — a valid DFA 5-tuple
        word   — a valid reset word for A
        method — shortening strategy: "greedy", "window", or "suffix"

    Returns:
        A (possibly shorter) reset word for A. Guaranteed to still be valid.
    """
    if method == "greedy":
        return _greedy_shorten(A, word)
    elif method == "window":
        return _window_shorten(A, word)
    elif method == "suffix":
        return _suffix_shorten(A, word)
    else:
        return _greedy_shorten(A, word)


def _greedy_shorten(A: DFA, word: List[Letter]) -> List[Letter]:
    """
    Greedy trimming: repeatedly scan the word and try removing each letter.
    If removing it still yields a valid reset word, keep the removal.
    Repeat until no more removals are possible.
    """
    current = list(word)
    changed = True
    while changed:
        changed = False
        i = 0
        while i < len(current):
            candidate = current[:i] + current[i + 1:]
            if is_synchronizing_word(A, candidate):
                current = candidate
                changed = True
                # Don't increment i — next letter is now at position i
            else:
                i += 1
    return current


def _window_shorten(A: DFA, word: List[Letter]) -> List[Letter]:
    """
    Sliding window: try removing windows of increasing size.
    Start with size 2, then 3, etc.
    """
    current = list(word)
    for window_size in range(2, len(current)):
        i = 0
        while i + window_size <= len(current):
            candidate = current[:i] + current[i + window_size:]
            if is_synchronizing_word(A, candidate):
                current = candidate
                # Restart from beginning with this window size
                i = 0
            else:
                i += 1
    # Also do single-letter greedy pass
    return _greedy_shorten(A, current)


def _suffix_shorten(A: DFA, word: List[Letter]) -> List[Letter]:
    """
    Suffix trimming: try cutting off letters from the end.
    Find the shortest prefix that is still a reset word.
    """
    current = list(word)
    # Binary search for shortest valid prefix
    lo, hi = 1, len(current)
    while lo < hi:
        mid = (lo + hi) // 2
        if is_synchronizing_word(A, current[:mid]):
            hi = mid
        else:
            lo = mid + 1
    current = current[:lo]
    # Then do greedy pass
    return _greedy_shorten(A, current)


def compare_reset_words(
    A: DFA,
    word_images: Optional[List[Letter]],
    word_pair_graph: Optional[List[Letter]],
) -> dict:
    """
    Task (f): Compare reset words obtained from image BFS (Task d) and
    pair graph (Task e).

    Returns a dict with:
        - 'len_images': length of shortest reset word (from image BFS)
        - 'len_pair_graph': length of pair graph reset word
        - 'len_shortened': length after heuristic shortening of pair graph word
        - 'ratio': len_pair_graph / len_images
        - 'ratio_shortened': len_shortened / len_images
        - 'cerny_bound': (n-1)^2 where n = |Q|
    """
    n = len(A[0])
    cerny_bound = (n - 1) ** 2

    result = {
        'cerny_bound': cerny_bound,
        'n_states': n,
    }

    if word_images is not None:
        result['len_images'] = len(word_images)
    else:
        result['len_images'] = None

    if word_pair_graph is not None:
        result['len_pair_graph'] = len(word_pair_graph)
        shortened = shorten_reset_word(A, word_pair_graph)
        result['len_shortened'] = len(shortened)
        result['shortened_word'] = shortened
    else:
        result['len_pair_graph'] = None
        result['len_shortened'] = None
        result['shortened_word'] = None

    # Compute ratios (only if both are available and images length > 0)
    if result['len_images'] and result['len_pair_graph']:
        result['ratio'] = result['len_pair_graph'] / result['len_images']
        result['ratio_shortened'] = result['len_shortened'] / result['len_images']
    else:
        result['ratio'] = None
        result['ratio_shortened'] = None

    return result
