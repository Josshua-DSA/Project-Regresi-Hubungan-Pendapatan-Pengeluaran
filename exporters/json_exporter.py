#matriks/exporters/json_exporter.py
#-----------------------------------------------------------------------------------
"""
Fungsi: export_to_json(matriks, nama_file)
1. Ubah data `matriks` menjadi format yang dapat dipahami JSON (misalnya, list of
lists).
2. Konversi data tersebut ke string JSON.
3. Buka file dengan nama `nama_file` dalam mode tulis.
4. Tuliskan data JSON ke dalam file.
5. Tampilkan pesan sukses.
"""
import json

def export_to_json(matriks, nama_file):
    """Mengekspor data matriks ke file JSON."""
    
    # Langkah 3: Buka file dengan nama 'nama_file' dalam mode tulis.
    with open(nama_file, 'w') as json_file:
        # Langkah 1, 2, & 4 digabungkan: Ubah data matriks ke format JSON 
        # dan langsung tuliskan ke dalam file.
        json.dump(matriks.data, json_file, indent=4)
    
    # Langkah 5: Tampilkan pesan sukses.
    print(f"Matriks berhasil diekspor ke {nama_file}")
