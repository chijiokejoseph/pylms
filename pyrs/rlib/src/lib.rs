use std::error::Error;

use pyo3::{PyErr, exceptions::PyException};

pub const COMMA_DELIM: &str = ", ";
pub const SEMI_DELIM: &str = "; ";
pub const SPACE_DELIM: &str = " ";
pub const ARABIC_APOSTROPHE: &str = "’";
pub const TIMESTAMP_MONTH_FIRST: &str = "%Y-%m-%d %H:%M:%S";
pub const TIMESTAMP_DAY_FIRST: &str = "%Y-%d-%m %H:%M:%S";
pub const DATE_FMT: &str = "%d/%m/%Y";


pub fn title(entry: &str) -> String {
    if entry.is_empty() {
        return entry.to_string();
    }
    let first = entry.chars().next().unwrap().to_uppercase().to_string();
    let rest = entry
        .chars()
        .skip(1)
        .map(|c| c.to_lowercase().to_string())
        .collect::<String>();
    first + &rest
}

pub fn error(e: Box<dyn Error>) -> PyErr {
    PyErr::new::<PyException, _>(e.to_string())
}

#[cfg(test)]
mod tests {}
