# main.py
from utilities.import_csv import read_rows
from operations.matriks_feature import build_features
from operations.matriks_target import build_target
from operations.eda import eda_csv_summary
from regressions.linear_regression import LinearRegression

def main():
    	# === 1. Baca data ===
	csv_path = "IceCreamData.csv"
	rows, header = read_rows(csv_path, has_header=True)

	print("=== DATASET ===")
	print(f"Jumlah data: {len(rows)} baris")
	print(f"Kolom: {header}\n")

    	# === 2. Lakukan EDA sederhana ===
	print("=== EDA Statistik Deskriptif ===")
	summary = eda_csv_summary(csv_path, has_header=True)
	for col, stats in summary.items():
		print(f"\nKolom: {col}")
		for key, val in stats.items():
			print(f"  {key:>6}: {val:.4f}")
	print("\n")

    	# === 3. Bentuk matriks fitur dan target ===
	if header and "Revenue" in header:
		target_idx = header.index("Revenue")
	else:
		target_idx = len(rows[0]) - 1  # kolom terakhir

	X, feat_names = build_features(rows, target_index=target_idx)
	y_vec = build_target(rows, target_index=target_idx)
	y = [r[0] for r in y_vec.to_list()]

    	# === 4. Jalankan regresi linear ===
	model = LinearRegression(fit_intercept=True)
	model.fit(X, y)

	print("=== HASIL REGRESI LINEAR ===")
	if model.fit_intercept:
		print(f"Intercept : {model.coef_[0]:.6f}")
	for i, w in enumerate(model.coef_[1:], 1):
		print(f"w{i:<2}      : {w:.6f}")
	else:
		for i, w in enumerate(model.coef_, 1):
			print(f"w{i:<2}      : {w:.6f}")

	# === 5. Evaluasi metrik ===
	r2 = model.score_r2(X, y)
	r2_adj = model.score_r2_adj(X, y)
	mae = model.score_mae(X, y)
	mse = model.score_mse(X, y)
	rmse = model.score_rmse(X, y)

	print("\n=== METRIK MODEL ===")
	print(f"R²        : {r2:.6f}")
	print(f"Adj. R²   : {r2_adj:.6f}")
	print(f"MAE       : {mae:.6f}")
	print(f"MSE       : {mse:.6f}")
	print(f"RMSE      : {rmse:.6f}")

	# === 6. Contoh prediksi ===
	preds = model.predict(X)
	print("\n=== CONTOH PREDIKSI ===")
	for i in range(min(5, len(preds))):
		print(f"Data-{i+1}: aktual={y[i]:.4f}, prediksi={preds[i]:.4f}")

if __name__ == "__main__":
	main()

