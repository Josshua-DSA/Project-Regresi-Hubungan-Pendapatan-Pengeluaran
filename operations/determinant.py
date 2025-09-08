Python
#matriks/operations/determinant

def find_determinant(matrix):
    if matrix.rows != 2 or matrix.cols != 2:
        raise ValueError("Saat ini hanya mendukung matriks 2x2.")
    return matrix.data[0][0] * matrix.data[1][1] - matrix.data[0][1] * matrix.data[1][0]
