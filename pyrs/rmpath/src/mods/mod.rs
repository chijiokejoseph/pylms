use pyo3::{prelude::*, types::PyString};
use std::{fs, io, path::Path};

use crate::error;

#[pyfunction]
pub fn rm_path(file: Py<PyString>) -> PyResult<()> {
    let file = file.to_string();
    let file = Path::new(&file);
    let contents = fs::read_dir(file)
        .map_err(|e| error(e.into()))?
        .collect::<Result<Vec<_>, _>>()
        .map_err(|e| error(e.into()))?;

    for content in contents.iter() {
        let path = content.path();
        if path.is_dir() {
            fs::remove_dir(path).map_err(|e| error(e.into()))?
        } else {
            fs::remove_file(path).map_err(|e| error(e.into()))?
        }
    }

    Ok(())
}

#[allow(dead_code)]
fn make(path: &Path) -> io::Result<()> {
    if path.exists() {
        return Ok(())
    }
    let parent = if path.extension().is_none() {
        path.parent().ok_or(io::Error::new(
            io::ErrorKind::InvalidFilename,
            format!("{} has no parent", path.display()),
        ))?
    } else {
        path
    };
    fs::create_dir_all(parent)?;
    if path.extension().is_none() {
        fs::OpenOptions::new()
            .create(true)
            .write(true)
            .truncate(false)
            .open(path)?;
    }
    Ok(())
}

#[allow(dead_code)]
fn rm(file: &Path) -> PyResult<()> {
    let file = Path::new(&file);
    let contents = fs::read_dir(file)
        .map_err(|e| error(e.into()))?
        .collect::<Result<Vec<_>, _>>()
        .map_err(|e| error(e.into()))?;

    for content in contents.iter() {
        let path = content.path();
        if path.is_dir() {
            fs::remove_dir(path).map_err(|e| error(e.into()))?
        } else {
            fs::remove_file(path).map_err(|e| error(e.into()))?
        }
    }

    Ok(())
}

#[cfg(test)]
mod test {
    use super::*;

    #[test]
    pub fn test_rm() {
        let data = Path::new("E:/Python/pylms/data");
        let del_path = data.join("del");
        make(&del_path).unwrap();
        for i in 1..=3 {
            let item_path = del_path.join(format!("item{i}.txt"));
            make(&item_path).unwrap();
            let dir_path = del_path.join(format!("dir{i}"));
            make(&dir_path).unwrap();
            for j in 1..=3 {
                let subitem_path = dir_path.join(format!("item{j}.csv"));
                make(&subitem_path).unwrap();
            }
        }
        rm(&del_path).unwrap()
    }
}
