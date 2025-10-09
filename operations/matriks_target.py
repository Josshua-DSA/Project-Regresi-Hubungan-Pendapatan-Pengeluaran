# operations/matriks_target.py
from typing import Iterable, Optional, List
from matrix import Matrix

def build_target(rows: Iterable[Iterable[float]],target_index: Optional[int] = None) -> Matrix:
	"""Ambil satu kolom target sebagai vektor (m x 1)."""
	rows = [list(map(float, r)) for r in rows]
	if not rows:
		raise ValueError("No data rows.")
	n_cols = len(rows[0])
	if target_index is None:
		target_index = n_cols - 1
	y = [[r[target_index]] for r in rows]
	return Matrix(y)
