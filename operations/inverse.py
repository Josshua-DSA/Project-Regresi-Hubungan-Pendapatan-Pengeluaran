# operations/inverse.py
from matrix import Matrix

def inverse(A: Matrix) -> Matrix:
	r, c = A.shape
	if r != c:
		raise ValueError("Inverse only defined for square matrices.")
	n = r
	aug = [row[:] + eye[:] for row, eye in zip(A._m, Matrix.eye(n)._m)]

	for col in range(n):
		# partial pivoting
		p = max(range(col, n), key=lambda i: abs(aug[i][col]))
		if abs(aug[p][col]) < 1e-12:
			raise ValueError("Matrix is singular.")
		if p != col:
			aug[col], aug[p] = aug[p], aug[col]

        	# normalisasi pivot row
		pv = aug[col][col]
		aug[col] = [v / pv for v in aug[col]]

        	# eliminasi baris lain
		for i in range(n):
			if i == col: 
				continue
			f = aug[i][col]
			if f != 0.0:
				aug[i] = [a - f*b for a, b in zip(aug[i], aug[col])]

	inv = [row[n:] for row in aug]
	return Matrix(inv)
