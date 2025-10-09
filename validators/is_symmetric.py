# matriks/validators/is_symmetric.py

def is_symmetric(matrix):
    """
    Mengecek apakah sebuah matriks simetris.
    Syarat:
      1. Matriks harus persegi (jumlah baris == jumlah kolom).
      2. Elemen [i][j] harus sama dengan elemen [j][i].
    """
    # 1. Periksa apakah matriks persegi
    if matrix.rows != matrix.cols:
        return False

    # 2. Bandingkan elemen (i, j) dengan (j, i)
    for i in range(matrix.rows):
        for j in range(matrix.cols):
            if matrix.data[i][j] != matrix.data[j][i]:
                return False

    # 3. Jika semua sesuai
    return True
