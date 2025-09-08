# matriks/validators/is_identity.py

def is_identity(matrix):
    """
    Mengecek apakah sebuah matriks adalah matriks identitas.
    Syarat:
      1. Matriks harus persegi (jumlah baris == jumlah kolom).
      2. Elemen diagonal harus 1.
      3. Elemen non-diagonal harus 0.
    """
    # 1. Periksa apakah matriks persegi
    if matrix.rows != matrix.cols:
        return False

    # 2. Periksa setiap elemen
    for i in range(matrix.rows):
        for j in range(matrix.cols):
            if i == j:  # diagonal
                if matrix.data[i][j] != 1:
                    return False
            else:  # non-diagonal
                if matrix.data[i][j] != 0:
                    return False

    # 3. Semua sesuai
    return True
