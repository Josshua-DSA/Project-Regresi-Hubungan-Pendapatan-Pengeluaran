# matriks/utilities/validators.py

def is_square(matrix):
    return matrix.rows == matrix.cols


def is_symmetric(matrix):
    if matrix.rows != matrix.cols:
        return False
    for i in range(matrix.rows):
        for j in range(matrix.cols):
            if matrix.data[i][j] != matrix.data[j][i]:
                return False
    return True

