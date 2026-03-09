use std::error::Error;

use pyo3::{exceptions::PyException, prelude::*};

mod mods;


fn error(e: Box<dyn Error>) -> PyErr {
    PyErr::new::<PyException, _>(e.to_string())
}


#[pymodule]
pub fn rmpath(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(mods::rm_path, m)?)?;
    Ok(())
}