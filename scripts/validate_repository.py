"""Run lightweight, dependency-free checks on the published project files."""

from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = [
    "README.md",
    "data/P35372.fasta",
    "data/low_confidence_segments.csv",
    "data/model_comparison.csv",
    "structures/alphafold-P35372.pdb",
    "structures/swissmodel-P35372.pdb",
    "structures/8EF6-assembly1.cif.gz",
    "figures/active-complex-8EF6.png",
    "figures/model-superposition.png",
    "figures/orthosteric-pocket.png",
]

PRIVATE_EXTENSIONS = {".docx", ".pdf", ".pptx", ".pse"}


def fasta_length(path: Path) -> int:
    lines = path.read_text(encoding="utf-8").splitlines()
    return len("".join(line.strip() for line in lines if not line.startswith(">")))


def pdb_atom_count(path: Path) -> int:
    with path.open(encoding="utf-8", errors="ignore") as handle:
        return sum(line.startswith(("ATOM  ", "HETATM")) for line in handle)


def main() -> None:
    missing = [item for item in REQUIRED_FILES if not (ROOT / item).is_file()]
    assert not missing, f"Missing required files: {missing}"

    assert fasta_length(ROOT / "data/P35372.fasta") == 400, "Unexpected P35372 sequence length"

    for model in ("alphafold-P35372.pdb", "swissmodel-P35372.pdb"):
        assert pdb_atom_count(ROOT / "structures" / model) > 1000, f"Too few atoms in {model}"

    with (ROOT / "data/model_comparison.csv").open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    assert {row["model"] for row in rows} == {"AlphaFold", "SWISS-MODEL"}

    private_files = [
        path.relative_to(ROOT).as_posix()
        for path in ROOT.rglob("*")
        if path.is_file() and ".git" not in path.parts and path.suffix.lower() in PRIVATE_EXTENSIONS
    ]
    assert not private_files, f"Submission documents or working sessions found: {private_files}"

    print("Repository checks passed: sequence, structures, metrics, figures and privacy guard.")


if __name__ == "__main__":
    main()
