# operations/perkalian.py
from matrix import Matrix

def multiply(A: Matrix, B: Matrix) -> Matrix:
	r1, c1 = A.shape
	r2, c2 = B.shape
	if c1 != r2:
		raise ValueError(f"Shape mismatch: {A.shape} x {B.shape}")
	# cache kolom B untuk efisiensi
	cols = list(zip(*B._m))
	out = [[sum(a*b for a, b in zip(row, col)) for col in cols] for row in A._m]
	return Matrix(out)
