#matriks/matrix.py

# matrix.py
from __future__ import annotations
from typing import Iterable, List, Tuple

class Matrix:
	"""Kelas matriks ringan untuk pembelajaran (tanpa NumPy)."""
	def __init__(self, data: Iterable[Iterable[float]]):
		self._m: List[List[float]] = [list(row) for row in data]
		if not self._m or not self._m[0]:
			raise ValueError("Matrix cannot be empty.")
		n = len(self._m[0])
		if any(len(r) != n for r in self._m):
			raise ValueError("All rows must have the same length.")

	@property
	def shape(self) -> Tuple[int, int]:
		return len(self._m), len(self._m[0])

	def to_list(self) -> List[List[float]]:
		return [row[:] for row in self._m]

	@staticmethod
	def eye(n: int) -> "Matrix":
		return Matrix([[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)])

	def __repr__(self) -> str:
		return f"Matrix({self._m})"

