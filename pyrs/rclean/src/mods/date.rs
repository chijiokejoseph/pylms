use chrono::prelude::*;
use polars::prelude::*;
use pyo3::{IntoPyObjectExt, exceptions::PyException, prelude::*};
use pyo3_polars::PySeries;

#[derive(FromPyObject)]
pub enum DateInput {
    #[pyo3(transparent, annotation = "str")]
    Str(String),
    #[pyo3(transparent, annotation = "datetime.date")]
    Date(NaiveDateTime),
}

#[pyfunction]
pub fn clean_date(input: DateInput, format: &str, day_first: bool) -> String {
    match input {
        DateInput::Date(val) => val.format(format).to_string(),
        DateInput::Str(val) => {
            let fmt = if day_first { "%d/%m/%Y" } else { "%m/%d/%Y" };
            let parsed = NaiveDateTime::parse_from_str(&val, fmt);
            parsed.unwrap().format(format).to_string()
        }
    }
}

#[pyfunction]
pub fn clean_dates(
    series: &Bound<'_, PyAny>,
    format: &str,
    day_first: bool,
) -> PyResult<Py<PyAny>> {
    let py = series.py();
    let series = series.extract::<PySeries>()?;
    let s = series.0;
    let s = s
        .str()
        .map_err(|e| PyErr::new::<PyException, _>(e.to_string()))?
        .into_iter()
        .map(|val| val.map(|val| clean_date(DateInput::Str(val.to_string()), format, day_first)))
        .collect::<StringChunked>()
        .into_series();
    let s = PySeries(s);
    s.into_py_any(py)
}
