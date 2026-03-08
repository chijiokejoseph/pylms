use pyo3::prelude::*;

pub mod mods;

#[pymodule]
fn rclean(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(mods::clean_names, m)?)?;
    m.add_function(wrap_pyfunction!(mods::clean_date, m)?)?;
    m.add_function(wrap_pyfunction!(mods::clean_dates, m)?)?;
    Ok(())
}
