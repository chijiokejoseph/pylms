use chrono::NaiveDateTime;
use polars::prelude::*;
use pyo3::prelude::*;
use pyo3_polars::PySeries;
use rlib::DATE_FMT;


pub fn clean_single_time(time: &str) -> Result<String, String> {
    let date = match NaiveDateTime::parse_from_str(time, rlib::TIMESTAMP_DAY_FIRST) {
        Ok(val) => format!("{}", val.format(DATE_FMT)),
        Err(e1) => match NaiveDateTime::parse_from_str(time, rlib::TIMESTAMP_MONTH_FIRST) {
            Ok(val) => format!("{}", val.format(DATE_FMT)),
            Err(e2) => return Err(format!("{e1}\n{e2}")),
        },
    };

    Ok(date)
}

#[pyfunction]
pub fn clean_timestamp(time_series: PySeries) -> PyResult<PySeries> {
    let series = time_series.0;
    let values = series
        .str()
        .map_err(|e| rlib::error(e.into()))?
        .into_iter()
        .map(|entry| entry.and_then(|val| clean_single_time(val).ok()))
        .collect::<StringChunked>()
        .into_series();
    Ok(PySeries(values))
}
