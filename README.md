# MT3510 DFA Synchronization & Isomorphism

Python/NetworkX implementation of DFA synchronization detection (transition monoid, image BFS, pair graph) and DFA isomorphism testing (strict, weak, semi).

> Built by [Taner's Claw](https://github.com/trbhmn2) — AI engineering team.

## Structure

- `dfa/` — Core DFA module (representation, utilities)
- `sync/` — Part 1: Synchronization algorithms
- `iso/` — Part 2: Isomorphism algorithms
- `tests/` — Test suite
- `demo.ipynb` — Demonstration notebook

## Quick Start

```bash
pip install networkx
python -m pytest tests/
jupyter notebook demo.ipynb
```
