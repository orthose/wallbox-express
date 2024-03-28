import csv
from typing import Any, Callable, Dict, List, Tuple, TypeVar


T = TypeVar('T')


class DataFrame:
    """
    Line indexed DataFrame minimal implementation
    """

    def __init__(self):
        self.columns = list() # Ordered 
        self.headers = dict()
        self.data = list()

    def __len__(self) -> int:
        return len(self.data)

    def __getitem__(self, key: int) -> List[Any]:
        return self.data[key]

    def __setitem__(self, key: str, value: Any) -> None:
        pass

    def read_csv(self, csv_file: str, delimiter: str = ',', quotechar: str = '"') -> None:
        with open(csv_file, 'r', newline='') as f:
            reader = csv.reader(f, delimiter=delimiter, quotechar=quotechar)
            self.columns = reader.__next__()
            self.headers = {v: i for i, v in enumerate(self.columns)}
            self.data = list(reader)

    def __iter__(self) -> List[Any]:
        return self.data.__iter__()
    
    def rename(self, columns: Dict[str, str]):
        for c1, c2 in columns.items():
            if c1 in self.headers and c1 != c2:
                self.columns[self.headers[c1]] = c2 
                self.headers[c2] = self.headers.pop(c1)

    def apply_schema(self, schema: Dict[str, Callable[[Any], Any]]) -> None:
        for col, data_type in schema.items():
            for row in self.data:
                for j in range(len(row)):
                    if self.headers[col] == j:
                        row[j] = data_type(row[j])

    def group_by(self, 
                 group_cols: List[str], 
                 agg_cols: Dict[str, Callable[[T, T], T]]
                 ) -> None:
        groups = dict()

        # Convert column names to indexes
        group_idx = tuple(self.headers[col] for col in group_cols)
        agg_idx = tuple(self.headers[col] for col in agg_cols.keys())
        agg_fun = tuple(fagg for fagg in  agg_cols.values())

        for row in self.data:
            group = tuple(row[j] for j in range(len(row)) if j in group_idx)
            agg = [row[j] for j in range(len(row)) if j in agg_idx]
            if group not in groups:
                groups[group] = agg
            else:
                for j in range(len(agg)):
                    groups[group][j] = agg_fun[j](groups[group][j], agg[j])

        # Override current dataframe
        self.columns = group_cols + list(agg_cols.keys())
        self.headers = {col: j for j, col in enumerate(self.columns)}
        self.data = [list(group) + agg for group, agg in groups.items()]
