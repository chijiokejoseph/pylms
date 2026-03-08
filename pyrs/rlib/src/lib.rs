pub const COMMA_DELIM: &str = ", ";
pub const SEMI_DELIM: &str = "; ";
pub const SPACE_DELIM: &str = " ";
pub const ARABIC_APOSTROPHE: &str = "’";


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

#[cfg(test)]
mod tests {}
