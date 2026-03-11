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
    # TODO: Implement heuristic shortening strategies
    pass


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
    # TODO: Implement comparison
    pass
