# operations/matriks_feature.py
from typing import Iterable, List, Optional, Tuple
from matrix import Matrix

def build_features(rows: Iterable[Iterable[float]],target_index: Optional[int] = None,feature_names: Optional[List[str]] = None) -> Tuple[Matrix, List[str]]:
	"""Dari baris numerik, kembalikan Matrix X (semua kolom kecuali target)."""
	rows = [list(map(float, r)) for r in rows]
	if not rows:
		raise ValueError("No data rows.")
	n_cols = len(rows[0])
	if target_index is None:
		target_index = n_cols - 1
	X_rows = [[r[j] for j in range(n_cols) if j != target_index] for r in rows]
	if feature_names is None:
		feature_names = [f"x{j+1}" for j in range(n_cols) if j != target_index]
	return Matrix(X_rows), feature_names
