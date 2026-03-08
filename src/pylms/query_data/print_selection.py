"""Print utility for displaying student selections."""


def print_selection(selections: list[tuple[int, str]], per_line: int = 3) -> None:
    """Print selected students in table format.

    Args:
        selections (list[tuple[int, str]]): List of (serial, name) tuples to display.
        per_line (int): Number of entries to display per line. Defaults to 3.
    """
    if len(selections) == 0:
        print("\nNo students selected.\n")
        return

    # Calculate dynamic column widths based on data
    max_serial = max(serial for serial, _ in selections)
    serial_width = len(str(max_serial))
    
    max_name_len = max(len(name) for _, name in selections)
    name_width = max(max_name_len, 20)

    # Print header
    print(f"\n{'=' * 80}")
    print(f"Selected Students ({len(selections)} total)")
    print(f"{'=' * 80}\n")

    # Print students in rows
    for i in range(0, len(selections), per_line):
        line_items = selections[i : (i + per_line)]
        formatted = [f"{serial:{serial_width}d}. {name:{name_width}s}" for serial, name in line_items]
        print("  ".join(formatted))

    # Print footer
    print(f"\n{'=' * 80}\n")
