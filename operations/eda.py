# operations/eda.py
from __future__ import annotations
from typing import Dict, List, Optional
import math
from utilities.import_csv import read_rows

# ------------------ Statistik Dasar ------------------ #
def _mean(arr: List[float]) -> float:
	return sum(arr) / len(arr) if arr else float("nan")

def _variance(arr: List[float], sample: bool = True) -> float:
	if len(arr) < 2:
		return float("nan")
	mean_val = _mean(arr)
	denom = len(arr) - 1 if sample else len(arr)
	return sum((x - mean_val) ** 2 for x in arr) / denom

def _std(arr: List[float], sample: bool = True) -> float:
	var = _variance(arr, sample)
	return math.sqrt(var) if not math.isnan(var) else float("nan")

def _percentile(arr: List[float], p: float) -> float:
	"""Menghitung persentil (0–100) tanpa numpy."""
	if not arr:
		return float("nan")
	sorted_arr = sorted(arr)
	k = (len(sorted_arr) - 1) * (p / 100.0)
	f = math.floor(k)
	c = math.ceil(k)
	if f == c:
		return sorted_arr[int(k)]
	return sorted_arr[f] * (c - k) + sorted_arr[c] * (k - f)

# ------------------ Fungsi Utama ------------------ #
def eda_csv_summary(csv_path: str,has_header: bool = True) -> Dict[str, Dict[str, float]]:
	"""Membaca file CSV dan menghitung statistik dasar:
	Mean, Std, Min, Q1, Median(Q2), Q3, Max, Count
	untuk setiap kolom numerik."""
	rows, header = read_rows(csv_path, has_header=has_header)
	if not rows:
		raise ValueError("CSV tidak memiliki data.")

	n_cols = len(rows[0])
	col_names = header if header else [f"col_{i+1}" for i in range(n_cols)]

	# pisahkan kolom ke bentuk list per kolom
	columns = {col_names[j]: [float(r[j]) for r in rows] for j in range(n_cols)}

	summary: Dict[str, Dict[str, float]] = {}
	for col, values in columns.items():
		stats = {
			"count": len(values),
			"mean": _mean(values),
			"std": _std(values, sample=True),
			"min": min(values),
			"q1": _percentile(values, 25),
			"q2": _percentile(values, 50),  # median
			"q3": _percentile(values, 75),
			"max": max(values),}
		summary[col] = stats

	return summary
