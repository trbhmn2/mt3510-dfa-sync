"""
Synchronization module — three methods for detecting synchronizing DFAs
and finding reset words.

Methods:
    1. Transition monoid BFS (Task a)
    2. Image BFS (Tasks b, d)
    3. Pair graph (Tasks c, e)
    4. Heuristic shortening (Task f)
"""

from .monoid import is_synchronizing_monoid
from .images import is_synchronizing_images, shortest_reset_word_images
from .pair_graph import is_synchronizing_pair_graph, reset_word_pair_graph
from .heuristic import shorten_reset_word

__all__ = [
    "is_synchronizing_monoid",
    "is_synchronizing_images",
    "shortest_reset_word_images",
    "is_synchronizing_pair_graph",
    "reset_word_pair_graph",
    "shorten_reset_word",
]
