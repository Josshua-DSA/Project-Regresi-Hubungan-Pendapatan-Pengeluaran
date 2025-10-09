# operations/transpose.py
from matrix import Matrix

def transpose(A: Matrix) -> Matrix:
	r, c = A.shape
	return Matrix([[A._m[i][j] for i in range(r)] for j in range(c)])
