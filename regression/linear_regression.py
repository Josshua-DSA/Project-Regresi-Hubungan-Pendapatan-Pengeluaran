# regressions/linear_regression.py
from typing import Iterable, List, Optional
from matrix import Matrix
from operations.transpose import transpose
from operations.perkalian import multiply
from operations.inverse import inverse
from regression.metrics import mae as _mae, mse as _mse, rmse as _rmse, r2_adjusted as _r2_adj

class LinearRegression:
	"""β = (XᵀX)⁻¹ Xᵀ y, opsi intercept otomatis."""
	def __init__(self, fit_intercept: bool = True):
		self.fit_intercept = fit_intercept
		self.coef_: Optional[List[float]] = None

	def _add_intercept(self, X: Matrix) -> Matrix:
		data = [[1.0] + row for row in X.to_list()]
		return Matrix(data)

	def fit(self, X: Matrix, y_vec: Matrix) -> "LinearRegression":
		# pastikan y_vec adalah Matrix
		if isinstance(y_vec, list):
			y_vec = Matrix([[float(v)] for v in y_vec])

		X_ = self._add_intercept(X) if self.fit_intercept else X
		Xt  = transpose(X_)
		XtX = multiply(Xt, X_)
		XtX_inv = inverse(XtX)
		Xty = multiply(Xt, y_vec)
		beta = multiply(XtX_inv, Xty)     # (p x 1)
		self.coef_ = [row[0] for row in beta.to_list()]
		return self

	def predict(self, X: Matrix) -> List[float]:
		if self.coef_ is None:
			raise RuntimeError("Model belum di-fit.")
		X_ = self._add_intercept(X) if self.fit_intercept else X
		beta = Matrix([[b] for b in self.coef_])
		yhat = multiply(X_, beta).to_list()
		return [row[0] for row in yhat]

	def score_r2(self, X: Matrix, y: Iterable[float]) -> float:
		y_true = [float(v) for v in y]
		y_pred = self.predict(X)
		mu = sum(y_true)/len(y_true)
		ss_res = sum((a-b)**2 for a,b in zip(y_true, y_pred))
		ss_tot = sum((a-mu)**2 for a in y_true)
		return 1.0 - (ss_res/ss_tot if ss_tot else 0.0)

	def score_mae(self, X: Matrix, y: Iterable[float]) -> float:
		y_true = [float(v) for v in y]
		y_pred = self.predict(X)
		return _mae(y_true, y_pred)

	def score_mse(self, X: Matrix, y: Iterable[float]) -> float:
		y_true = [float(v) for v in y]
		y_pred = self.predict(X)
		return _mse(y_true, y_pred)

	def score_rmse(self, X: Matrix, y: Iterable[float]) -> float:
		y_true = [float(v) for v in y]
		y_pred = self.predict(X)
		return _rmse(y_true, y_pred)

	def score_r2_adj(self, X: Matrix, y: Iterable[float]) -> float:
		"""
		Adjusted R^2 menggunakan n = jumlah sampel, p = jumlah fitur (tanpa intercept).
		"""
		y_true = [float(v) for v in y]
		y_pred = self.predict(X)
		n, p = X.shape  # p = jumlah kolom fitur asli (intercept tidak dihitung)
		return _r2_adj(y_true, y_pred, n=n, p=p)
