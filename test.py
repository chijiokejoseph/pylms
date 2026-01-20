import polars as pl
from datetime import datetime
import numpy as np

from pylms.constants import DATE_FMT
from pylms.data import datamap

df = pl.DataFrame(
    {
        "a": [1, 2, 3, 4, 5],
    }
)

df = (
    df.lazy()
    .with_columns(pl.lit(2).alias("b"))
    .with_columns((pl.col("a") * pl.col("b")).alias("c"))
    .with_columns(
        pl.col("c").median().alias("median"),
        pl.col("c").mean().alias("mean"),
        pl.lit("10/12/2025").alias("date"),
    )
    .collect()
)


@np.vectorize
def convert(value: str) -> datetime:
    return datetime.strptime(value, DATE_FMT)


print(df)
print("\n")

parts = df[0:3]
print(parts)
print("\n")

parts = parts.to_arrow()

for row in parts.to_pylist():
    for col in parts.column_names:
        val = row[col]
        print(f"{col}: {val}")
    print()

val = df["a"][0]
print(f"{val = }\n")

# date = df["date"].to_numpy()
# date: np.ndarray = convert(date)
# date = np.array(date, dtype=np.datetime64)
# df = df.with_columns(pl.Series("date", date, dtype=pl.Datetime))

df = datamap(df, "date", convert, np.datetime64, pl.Datetime())

print(df)
