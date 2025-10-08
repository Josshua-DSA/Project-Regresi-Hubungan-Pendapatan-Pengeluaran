# regressions/metrics.py
from __future__ import annotations
from typing import Iterable
import math

def mae(y_true: Iterable[float], y_pred: Iterable[float]) -> float:
	y = [float(v) for v in y_true]
	yhat = [float(v) for v in y_pred]
	if len(y) != len(yhat) or len(y) == 0:
		raise ValueError("mae: y_true dan y_pred harus sama panjang dan tidak kosong.")
	return sum(abs(a - b) for a, b in zip(y, yhat)) / len(y)

def mse(y_true: Iterable[float], y_pred: Iterable[float]) -> float:
	y = [float(v) for v in y_true]
	yhat = [float(v) for v in y_pred]
	if len(y) != len(yhat) or len(y) == 0:
		raise ValueError("mse: y_true dan y_pred harus sama panjang dan tidak kosong.")
	return sum((a - b) ** 2 for a, b in zip(y, yhat)) / len(y)

def rmse(y_true: Iterable[float], y_pred: Iterable[float]) -> float:
	return math.sqrt(mse(y_true, y_pred))

def r2(y_true: Iterable[float], y_pred: Iterable[float]) -> float:
	y = [float(v) for v in y_true]
	yhat = [float(v) for v in y_pred]
	if len(y) != len(yhat) or len(y) == 0:
		raise ValueError("r2: y_true dan y_pred harus sama panjang dan tidak kosong.")
	y_mean = sum(y) / len(y)
	ss_res = sum((a - b) ** 2 for a, b in zip(y, yhat))
	ss_tot = sum((a - y_mean) ** 2 for a in y)
	return 1.0 - (ss_res / ss_tot if ss_tot != 0 else 0.0)

def r2_adjusted(y_true: Iterable[float], y_pred: Iterable[float], n: int, p: int) -> float:
    """
    Adjusted R^2 = 1 - (1 - R^2) * (n - 1) / (n - p - 1)
    n = jumlah sampel, p = jumlah parameter bebas (tidak termasuk intercept).
    """
	if n <= p + 1:
 		# tak terdefinisi; kembalikan NaN agar tidak menyesatkan
		return float("nan")
	r2_val = r2(y_true, y_pred)
	return 1.0 - (1.0 - r2_val) * (n - 1) / (n - p - 1)
