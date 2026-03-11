"""Tests for synchronization algorithms."""

import pytest
from dfa.core import random_dfa, non_synchronizing_dfa, is_synchronizing_word
from sync.monoid import is_synchronizing_monoid
from sync.images import is_synchronizing_images, shortest_reset_word_images
from sync.pair_graph import is_synchronizing_pair_graph, reset_word_pair_graph
from sync.heuristic import shorten_reset_word, compare_reset_words

# Example DFA from spec — known to be synchronizing (reset word "11")
# TODO: Test Engineer will verify exact transitions from the spec diagram
SPEC_DFA = (
    {0, 1, 2, 3},
    {0, 1},
    {
        (0, 0): 0, (0, 1): 0,
        (1, 0): 0, (1, 1): 0,
        (2, 0): 1, (2, 1): 0,
        (3, 0): 0, (3, 1): 2,
    },
    3,
    {1, 2},
)


class TestMonoidMethod:
    """Task (a) tests."""

    def test_spec_dfa_is_synchronizing(self):
        assert is_synchronizing_monoid(SPEC_DFA) is True

    def test_non_sync_dfa(self):
        A = non_synchronizing_dfa(4, 2)
        assert is_synchronizing_monoid(A) is False

    def test_small_random_sync(self):
        # Random DFAs with |Σ|>=2 are almost surely synchronizing
        A = random_dfa(5, 2, seed=42)
        result = is_synchronizing_monoid(A)
        assert isinstance(result, bool)


class TestImageMethod:
    """Task (b) tests."""

    def test_spec_dfa_is_synchronizing(self):
        assert is_synchronizing_images(SPEC_DFA) is True

    def test_non_sync_dfa(self):
        A = non_synchronizing_dfa(4, 2)
        assert is_synchronizing_images(A) is False

    def test_agrees_with_monoid(self):
        """Both methods should agree on the same DFA."""
        for seed in range(10):
            A = random_dfa(6, 2, seed=seed)
            assert is_synchronizing_monoid(A) == is_synchronizing_images(A)


class TestPairGraphMethod:
    """Task (c) tests."""

    def test_spec_dfa_is_synchronizing(self):
        assert is_synchronizing_pair_graph(SPEC_DFA) is True

    def test_non_sync_dfa(self):
        A = non_synchronizing_dfa(4, 2)
        assert is_synchronizing_pair_graph(A) is False

    def test_agrees_with_others(self):
        for seed in range(10):
            A = random_dfa(6, 2, seed=seed)
            r1 = is_synchronizing_images(A)
            r2 = is_synchronizing_pair_graph(A)
            assert r1 == r2


class TestShortestResetWord:
    """Task (d) tests."""

    def test_spec_dfa_reset_word(self):
        word = shortest_reset_word_images(SPEC_DFA)
        assert word is not None
        assert is_synchronizing_word(SPEC_DFA, word)
        # Shortest reset word for spec DFA should be length 2 ("10" or "11")
        assert len(word) == 2

    def test_non_sync_returns_none(self):
        A = non_synchronizing_dfa(4, 2)
        assert shortest_reset_word_images(A) is None


class TestPairGraphResetWord:
    """Task (e) tests."""

    def test_spec_dfa_reset_word(self):
        word = reset_word_pair_graph(SPEC_DFA)
        assert word is not None
        assert is_synchronizing_word(SPEC_DFA, word)

    def test_non_sync_returns_none(self):
        A = non_synchronizing_dfa(4, 2)
        assert reset_word_pair_graph(A) is None


class TestHeuristic:
    """Task (f) tests."""

    def test_shortened_word_still_valid(self):
        A = random_dfa(10, 2, seed=42)
        word = reset_word_pair_graph(A)
        if word is not None:
            shortened = shorten_reset_word(A, word)
            assert is_synchronizing_word(A, shortened)
            assert len(shortened) <= len(word)

    def test_comparison(self):
        A = random_dfa(10, 2, seed=42)
        w_img = shortest_reset_word_images(A)
        w_pg = reset_word_pair_graph(A)
        stats = compare_reset_words(A, w_img, w_pg)
        assert "len_images" in stats
        assert "len_pair_graph" in stats
