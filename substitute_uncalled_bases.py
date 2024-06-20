from Bio import AlignIO
import argparse
import sys
from typing import List, Dict


def main():
    parser = argparse.ArgumentParser(
        description="This script changes unassigned nucleotides (N) from one sequence in an alignment and substitutes them by the nucleotides from another sequence. This is useful if two sequences are highly similar but one has a lot of uncalled bases. The assumption is that the true state of these uncalled bases is also highly similar to the other sequence."
    )

    parser.add_argument(
        "-a", "--alignment", type=str, help="Alignment file path."
    )

    parser.add_argument(
        "-s",
        "--source",
        type=str,
        required=True,
        help="Fasta ID of source sequence.",
    )

    parser.add_argument(
        "-d",
        "--destination",
        type=str,
        required=True,
        help="Fasta ID of destination sequence (The sequence you want to change).",
    )

    args = parser.parse_args()

    # The next 6 lines are just for input handling
    # If neither -a nor data from stdin is given throw an error
    if args.alignment is None and sys.stdin.isatty():
        parser.error("Either -a/--alignment or stdin must be provided")

    if args.alignment:
        alignment = AlignIO.read(args.alignment, "fasta")
    else:
        # Read from stdin
        alignment = AlignIO.read(sys.stdin, "fasta")
    
    source = args.source
    destination = args.destination

    def store_alignments(alignment):
        """Stores source and destination sequences in a dict for easier retrieval."""
        aligned_sequences = {}
        for record in alignment:
            if record.id not in [destination, source]:
                continue
            aligned_sequences[record.id] = record.seq

        return aligned_sequences

    def find_n(seq: str) -> List[int]:
        """Finds the position of all uncalled bases in the destination sequence."""
        pos_n = []
        for i, nuc in enumerate(seq, start=0):
            if nuc in ["N", "n"]:
                pos_n.append(i)
        return pos_n

    def find_nucs(seq: str, pos_n: List[int]) -> Dict[int, str]:
        """At each position of an uncalled base in the destination sequence, this function finds the corresponding nucleotide in the source sequence."""
        nucs = {}
        for i, nuc in enumerate(seq, start=0):
            if i in pos_n:
                nucs[i] = nuc
        return nucs

    def fix_destination_seq(seq: str, nucs: Dict[int, str]) -> str:
        """Creates a new sequence with the substitutions from the source sequence in place of the uncalled bases in the destination sequence."""
        fixed_seq = []
        for i, nuc in enumerate(seq, start=0):
            if i in nucs:
                fixed_seq.append(nucs[i])
            else:
                fixed_seq.append(nuc)

        return "".join(fixed_seq)

    def sanity_check(destination_seq: str, source_seq: str) -> None:
        """A simple check that prints out  warning if the source sequence contains more uncalled bases than the destination sequence. Usually you want to fix a sequence with many uncalled bases using a sequence with fewer uncalled bases."""
        n_source_n = source_seq.upper().count("N")
        n_dest_n = destination_seq.upper().count("N")

        # If the source seq has more uncalled bases than the destination seq
        if n_source_n > n_dest_n:
            print(
                f"WARNING: Your source sequence contains more uncalled bases than your destination sequence. No. of uncalled bases in source sequence: {n_source_n} and in destination sequence: {n_dest_n}. Did you mix up up your source and destination ids?",
                file=sys.stderr,
            )
        return

    aligned_sequences = store_alignments(alignment)
    destination_seq = aligned_sequences[destination]
    pos_n = find_n(destination_seq)
    source_seq = aligned_sequences[source]
    sanity_check(destination_seq, source_seq)
    nucs = find_nucs(source_seq, pos_n)
    fixed_seq = fix_destination_seq(destination_seq, nucs)
    print(f">{destination}")
    print(fixed_seq, end="")


# grep -o 'n' | wc -l

if __name__ == "__main__":
    main()
