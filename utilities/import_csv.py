# utilities/import_csv.py
import csv
from typing import List, Tuple, Optional

def read_rows(path: str, has_header: bool = True) -> Tuple[List[List[float]], Optional[List[str]]]:
    with open(path, newline="") as f:
        rdr = csv.reader(f)
        header = next(rdr, None) if has_header else None
        rows = [[float(v) for v in row] for row in rdr if row]
    return rows, header
