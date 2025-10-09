# matriks/exporters/csv_exporter.py
# ---------------------------------------------------------------------
""" Fungsi: export_to_json(matriks, nama_file)
1.  Ubah data `matriks` menjadi format yang dapat dipahami JSON (misalnya, list of lists).
2.  Konversi data tersebut ke string JSON.
3.  Buka file dengan nama `nama_file` dalam mode tulis.
4.  Tuliskan data JSON ke dalam file.
5.  Tampilkan pesan sukses
"""
# matriks/exporters/csv_exporter.py
import csv

def export_to_csv(matriks, nama_file):
    """Mengekspor data matriks ke file CSV."""
    
    # Langkah 1 & 2: Buka file dan buat objek writer CSV.
    with open(nama_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        
        # Langkah 3: Tuliskan setiap baris data dari 'matriks' ke dalam file.
        writer.writerows(matriks.data)
    
    # Langkah 4: Tampilkan pesan sukses.
    print(f"Matriks berhasil diekspor ke {nama_file}")
