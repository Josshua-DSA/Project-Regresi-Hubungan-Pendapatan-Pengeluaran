from flask import Flask, request, jsonify
from flask_cors import CORS 
from operations.matriks_feature import build_features
from operations.matriks_target import build_target
from operations.eda import eda_csv_summary
from regression.linear_regression import LinearRegression
import numpy as np
from utilities.import_csv import read_rows 

app = Flask(__name__)
# Izinkan semua origin (untuk development)
CORS(app) 
CSV_PATH = "IceCreamData.csv"

# =================================================================
# FUNGSI DUMMY (Anda harus mengganti ini dengan logika Python/Pandas nyata)
# =================================================================

def _get_regression_data(rows, header):
    """
    Mengambil titik data mentah untuk scatter plot (Temp vs Revenue).
    Asumsi: Kolom pertama adalah 'Temperature', kolom terakhir adalah 'Revenue'.
    """
    data = []
    # Kunci untuk frontend (harus temp dan revenue)
    feature_name = "temp" 
    target_name = "revenue"
    
    # Indeks
    temp_idx = 0
    rev_idx = len(rows[0]) - 1

    for row in rows:
        try:
            temp = float(row[temp_idx])
            rev = float(row[rev_idx])
            data.append({feature_name: temp, target_name: rev})
        except ValueError:
            # Lewati baris yang tidak valid
            continue
    return data

def _prepare_regression_line(model, data_points):
    """
    Menghasilkan data untuk garis regresi (prediksi)
    """
    temps = np.array([d['temp'] for d in data_points]).reshape(-1, 1)
    
    # Membuat 50 titik untuk garis yang halus
    min_temp = temps.min()
    max_temp = temps.max()
    x_range = np.linspace(min_temp, max_temp, 50).reshape(-1, 1)
    
    y_line = model.predict(x_range)
    
    line_data = [{'x': x_range[i][0], 'y': y_line[i]} for i in range(len(y_line))]
    return line_data

def _get_histogram_data(rows, target_idx, col_name, bins=5):
    """
    Membuat data histogram untuk variabel tertentu.
    """
    col_idx = 0 
    
    if col_name == 'Revenue':
        col_idx = target_idx 
        
    try:
        # PENTING: Membersihkan data dari header atau string non-numerik
        values = [float(row[col_idx]) for row in rows if str(row[col_idx]).replace('.', '', 1).isdigit()]
    except IndexError:
        return {"labels": ["Error"], "counts": [0]}
        
    if not values:
        return {"labels": ["Empty"], "counts": [0]}

    # Menghitung bins
    hist, edges = np.histogram(values, bins=bins)
    
    # Format label bin
    labels = []
    for i in range(len(edges) - 1):
        labels.append(f"{edges[i]:.0f}-{edges[i+1]:.0f}")
        
    return {"labels": labels, "counts": hist.tolist()}

# =================================================================
# ENDPOINTS UTAMA
# =================================================================

@app.route("/")
def home():
    return jsonify({"message": "Linear Regression Backend is running!"})

@app.route("/dashboard-data", methods=["GET"])
def get_dashboard_data():
    """
    ENDPOINT BARU: Menggabungkan data model, metrik, regresi, dan EDA.
    """
    try:
        # 1. PARAMETER DAN SETUP
        target_col = request.args.get("target", "Revenue")
        fit_intercept = request.args.get("fit_intercept", "true").lower() == "true"
        
        # 2. BACA DATA
        rows, header = read_rows(CSV_PATH, has_header=True)
        
        if header and target_col in header:
            target_idx = header.index(target_col)
        else:
            target_idx = len(rows[0]) - 1 

        # 3. FIT MODEL
        X, feat_names = build_features(rows, target_index=target_idx)
        y_vec = build_target(rows, target_index=target_idx)
        
        # PERBAIKAN KRITIS: Menggunakan .tolist()
        y = [r[0] for r in y_vec.tolist()] 

        model = LinearRegression(fit_intercept=fit_intercept).fit(X, y)

        # 4. AMBIL DATA VISUALISASI
        regression_data = _get_regression_data(rows, header)
        line_data = _prepare_regression_line(model, regression_data)
        
        # Asumsi kolom pertama (idx 0) adalah 'Temperature'
        temp_hist = _get_histogram_data(rows, target_idx, "Temperature", bins=5)
        revenue_hist = _get_histogram_data(rows, target_idx, "Revenue", bins=5)

        # 5. KUMPULKAN HASIL EDA DAN METRIK
        eda_summary = eda_csv_summary(CSV_PATH, has_header=True)
        
        # Mengambil statistik dari kolom pertama (Temperature) sebagai statistik EDA utama
        stats_temp = eda_summary[header[0]] 

        metrics = {
            "r2": model.score_r2(X, y),
            "r2_adj": model.score_r2_adj(X, y),
            "mae": model.score_mae(X, y),
            "mse": model.score_mse(X, y),
            "rmse": model.score_rmse(X, y),
        }

        # 6. RETURN GABUNGAN JSON
        result = {
            "regression_data": regression_data,
            "line_data": line_data,
            "metrics": metrics,
            "stats_temp": stats_temp, 
            "histogram_temp": temp_hist,
            "histogram_revenue": revenue_hist
        }
        return jsonify(result)
        
    except Exception as e:
        # Menangani error seperti file CSV tidak ditemukan atau error matriks
        return jsonify({"error": str(e)}), 500

# Endpoint lama tidak dipakai lagi, tetapi dipertahankan agar app.py tetap jalan.
@app.route("/fit", methods=["POST"])
def fit_model():
     return jsonify({"error": "Use /dashboard-data endpoint instead."}), 405
@app.route("/eda", methods=["GET"])
def get_eda():
    return jsonify({"error": "Use /dashboard-data endpoint instead."}), 405

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8000)