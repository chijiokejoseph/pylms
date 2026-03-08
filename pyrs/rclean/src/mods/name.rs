use std::borrow::Cow;

use polars::prelude::*;
use pyo3::{exceptions::PyException, prelude::*};

use pyo3_polars::PySeries;
use rlib::{ARABIC_APOSTROPHE, COMMA_DELIM, SPACE_DELIM, title};

#[pyfunction]
pub fn clean_names(names: &Bound<'_, PyAny>) -> PyResult<Py<PyAny>> {
    let py = names.py();
    let names = names.extract::<PySeries>()?;
    let names_series = &names.0;
    let closure = |name: &str| {
        let name = name.trim();
        let delim = if name.contains(COMMA_DELIM) {
            COMMA_DELIM
        } else {
            SPACE_DELIM
        };
        let name_parts = name
            .split(delim)
            .map(|s| title(s.trim()))
            .collect::<Vec<_>>();
        let new_name = name_parts.join(COMMA_DELIM);

        let new_name = if let Some(loc) = new_name.find(ARABIC_APOSTROPHE) {
            let sub = &new_name[loc..loc + 1];
            new_name.replace(sub, &sub.to_lowercase())
        } else {
            new_name
        };
        Cow::Owned(new_name)
    };

    let names_array = names_series
        .str()
        .map_err(|err| PyErr::new::<PyException, _>(err.to_string()))?
        .apply(|val| val.map(closure));
    let names_series = names_array.into_series();
    // .into_pyobject(py)?;

    Ok(PySeries(names_series).into_pyobject(py)?.into())
}
