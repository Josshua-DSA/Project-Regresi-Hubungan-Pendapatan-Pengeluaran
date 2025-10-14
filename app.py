from flask import Flask, request, jsonify
from flask_cors import CORS

from matrix import Matrix
from utilities.import_csv import read_rows
from operations.matriks_feature import build_features
from operations.matriks_target import build_target
from operations.eda import eda_csv_summary
from regression.linear_regression import LinearRegression

app = Flask(__name__)
CORS(app)  # izinkan semua origin saat dev
CORS(app, resources={r"/*": {"origins": "*"}})

CSV_PATH = "IceCreamData.csv"  # dataset berada di root repo

# ------------------------- Helpers (tanpa NumPy) -------------------------

def _as_float(s):
    try:
        return float(s)
    except Exception:
        return None

def _get_regression_data(rows, feature_idx, target_idx):
    """
    Ambil titik data untuk scatter: [{temp: ..., revenue: ...}, ...]
    """
    out = []
    for r in rows:
        fx = _as_float(r[feature_idx])
        fy = _as_float(r[target_idx])
        if fx is None or fy is None:
            continue
        out.append({"temp": fx, "revenue": fy})
    return out

def _prepare_regression_line(model: LinearRegression, data_points, num_points: int = 50):
    """
    Buat data garis regresi halus (x, yhat) di rentang min..max feature.
    Tanpa NumPy.
    """
    if not data_points:
        return []

    xs = [d["temp"] for d in data_points]
    x_min, x_max = min(xs), max(xs)
    if num_points < 2 or x_min == x_max:
        # fallback: satu titik saja
        X_line = Matrix([[x_min]])
        y_line = model.predict(X_line)
        return [{"x": x_min, "y": y_line[0]}]

    step = (x_max - x_min) / (num_points - 1)
    grid = [[x_min + i * step] for i in range(num_points)]
    X_line = Matrix(grid)
    y_line = model.predict(X_line)  # -> list[float]
    return [{"x": grid[i][0], "y": y_line[i]} for i in range(num_points)]

def _histogram(values, bins=5):
    """
    Histogram sederhana tanpa NumPy.
    Return: {"labels": [...], "counts": [...]}
    """
    values = [v for v in values if isinstance(v, (int, float))]
    if not values:
        return {"labels": ["Empty"], "counts": [0]}
    vmin, vmax = min(values), max(values)
    if bins < 1:
        bins = 1
    if vmin == vmax:
        # semua nilai sama -> satu bin
        return {"labels": [f"{vmin:.0f}-{vmax:.0f}"], "counts": [len(values)]}

    width = (vmax - vmin) / bins
    counts = [0] * bins
    for v in values:
        idx = int((v - vmin) / width)
        if idx == bins:  # case v == vmax
            idx = bins - 1
        counts[idx] += 1

    labels = []
    for i in range(bins):
        left = vmin + i * width
        right = left + width
        labels.append(f"{left:.0f}-{right:.0f}")
    return {"labels": labels, "counts": counts}

# ------------------------- Endpoints -------------------------

@app.get("/")
def home():
    return jsonify({"message": "Linear Regression Backend is running!"})

@app.get("/dashboard-data")
def get_dashboard_data():
    """
    Gabungkan:
      - data scatter (Temperature vs Revenue)
      - garis regresi
      - histogram Temperature & Revenue
      - ringkasan EDA
      - metrik model (R², adj R², MAE, MSE, RMSE)
    """
    try:
        # Param optional
        target_col = request.args.get("target", "Revenue")
        fit_intercept = request.args.get("fit_intercept", "true").lower() == "true"

        # 1) Baca data
        rows, header = read_rows(CSV_PATH, has_header=True)
        if not rows or not header:
            return jsonify({"error": "CSV kosong atau header tidak ditemukan."}), 400

        # 2) Tentukan index target dan feature (asumsi 1 fitur: kolom pertama ≠ target)
        if target_col in header:
            target_idx = header.index(target_col)
        else:
            target_idx = len(header) - 1  # default terakhir

        feature_candidates = [i for i in range(len(header)) if i != target_idx]
        if not feature_candidates:
            return jsonify({"error": "Tidak ada kolom fitur selain target."}), 400
        feature_idx = feature_candidates[0]  # ambil fitur pertama (Temperature)

        # 3) Build X & y
        X, feat_names = build_features(rows, target_index=target_idx)
        y_vec = build_target(rows, target_index=target_idx)
        y = [r[0] for r in y_vec.to_list()]  # Matrix -> list

        # 4) Fit model
        model = LinearRegression(fit_intercept=fit_intercept).fit(X, y)

        # 5) Data untuk visual
        regression_data = _get_regression_data(rows, feature_idx, target_idx)
        line_data = _prepare_regression_line(model, regression_data, num_points=50)

        temp_values = []
        revenue_values = []
        for r in rows:
            fx = _as_float(r[feature_idx])
            fy = _as_float(r[target_idx])
            if fx is not None:
                temp_values.append(fx)
            if fy is not None:
                revenue_values.append(fy)

        temp_hist = _histogram(temp_values, bins=5)
        revenue_hist = _histogram(revenue_values, bins=5)

        # 6) EDA ringkas
        eda_summary = eda_csv_summary(CSV_PATH, has_header=True)
        stats_temp_key = header[feature_idx]
        stats_temp = eda_summary.get(stats_temp_key, {})

        # 7) Metrik
        metrics = {
            "r2": model.score_r2(X, y),
            "r2_adj": model.score_r2_adj(X, y),
            "mae": model.score_mae(X, y),
            "mse": model.score_mse(X, y),
            "rmse": model.score_rmse(X, y),
        }

        return jsonify({
            "regression_data": regression_data,
            "line_data": line_data,
            "metrics": metrics,
            "stats_temp": stats_temp,
            "histogram_temp": temp_hist,
            "histogram_revenue": revenue_hist
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Endpoint lama: diarahkan agar pakai dashboard-data saja
@app.post("/fit")
def fit_model():
    return jsonify({"error": "Use /dashboard-data endpoint instead."}), 405

@app.get("/eda")
def get_eda():
    return jsonify({"error": "Use /dashboard-data endpoint instead."}), 405

if __name__ == "__main__":
    # Jalankan Flask dev server
    app.run(debug=True, host="0.0.0.0", port=8000)
