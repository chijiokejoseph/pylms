// use pyo3::prelude::*;

// #[pyfunction]
// fn title(entry: &str) -> String {
//     entry
//         .split(" ")
//         .map(|s| s.trim())
//         .map(|s| s[..1].to_ascii_uppercase() + &s[1..].to_ascii_lowercase())
//         .collect::<Vec<_>>()
//         .join(" ")
// }

// #[pyfunction]
// fn conv_title(names: Vec<String>) -> Vec<String> {
//     names.into_iter().map(|s| title(&s)).collect()
// }

// #[pymodule]
// fn pyrs(m: &Bound<'_, PyModule>) -> PyResult<()> {
//     m.add_function(wrap_pyfunction!(title, m)?)?;
//     m.add_function(wrap_pyfunction!(conv_title, m)?)?;
//     Ok(())
// }
