# Substitute uncalled bases
This script changes unassigned nucleotides (N) from one sequence in an alignment and substitutes them by the nucleotides from another sequence. This is useful if two sequences are highly similar but one has a lot of uncalled bases. The assumption is that the true state of these uncalled bases is also highly similar to the other sequence.

```python
python substitute_uncalled_bases.py -a tests/test.aln -s few_n -d many_n
```