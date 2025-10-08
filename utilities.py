# matriks/utilities.py

def print_matrix(matrix):
	"""
	Mencetak isi dari objek matriks.
	"""
	for row in matrix.data:
		print(row)

def find_determinant(matrix):
    """Menghitung determinan matriks 2x2."""
    if matrix.rows != 2 or matrix.cols != 2:
        raise ValueError("Saat ini hanya mendukung matriks 2x2.")
    return matrix.data[0][0] * matrix.data[1][1] - matrix.data[0][1] * matrix.data[1][0]


def is_square(matrix):
    """Cek apakah matriks berbentuk persegi."""
    return matrix.rows == matrix.cols


def is_symmetric(matrix):
    """Cek apakah matriks simetris."""
    if matrix.rows != matrix.cols:
        return False
    for i in range(matrix.rows):
        for j in range(matrix.cols):
            if matrix.data[i][j] != matrix.data[j][i]:
                return False
    return True
