# Menggunakan base image Python resmi
FROM python:3.12-slim

# Menetapkan direktori kerja di dalam container
WORKDIR /app

# Menyalin file dependencies dan menginstalnya
# Kita salin requirements.txt terlebih dahulu untuk memanfaatkan caching Docker
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Menyalin seluruh sisa kode proyek ke direktori kerja
COPY . .

# Mengatur environment variable untuk aplikasi Flask/Web
# Ganti port 8080 jika app.py menggunakan port lain
ENV PORT=8000
EXPOSE 8000

# Mendefinisikan perintah yang akan dijalankan saat container di-launch
CMD ["python", "app.py"]
