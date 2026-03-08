"""Unit tests for print_selection function."""

import unittest

from .print_selection import print_selection


class TestPrintSelection(unittest.TestCase):
    """Test cases for print_selection function."""

    def test_print_empty_selection(self) -> None:
        """Test printing empty selection list."""
        print("\n--- Test: Empty Selection ---")
        selections: list[tuple[int, str]] = []
        print_selection(selections)

    def test_print_single_student(self) -> None:
        """Test printing single student."""
        print("\n--- Test: Single Student ---")
        selections: list[tuple[int, str]] = [(1, "John Doe")]
        print_selection(selections)

    def test_print_three_students(self) -> None:
        """Test printing three students (one line)."""
        print("\n--- Test: Three Students ---")
        selections: list[tuple[int, str]] = [
            (1, "Alice Johnson"),
            (2, "Bob Smith"),
            (3, "Charlie Brown"),
        ]
        print_selection(selections)

    def test_print_multiple_lines(self) -> None:
        """Test printing students across multiple lines."""
        print("\n--- Test: Multiple Lines (10 students) ---")
        selections: list[tuple[int, str]] = [
            (1, "Alice Johnson"),
            (2, "Bob Smith"),
            (3, "Charlie Brown"),
            (4, "Diana Prince"),
            (5, "Edward Norton"),
            (6, "Fiona Apple"),
            (7, "George Washington"),
            (8, "Hannah Montana"),
            (9, "Isaac Newton"),
            (10, "Julia Roberts"),
        ]
        print_selection(selections)

    def test_print_large_serials(self) -> None:
        """Test printing with large serial numbers."""
        print("\n--- Test: Large Serial Numbers ---")
        selections: list[tuple[int, str]] = [
            (100, "Student One Hundred"),
            (200, "Student Two Hundred"),
            (300, "Student Three Hundred"),
        ]
        print_selection(selections)

    def test_print_long_names(self) -> None:
        """Test printing with very long names."""
        print("\n--- Test: Long Names ---")
        selections: list[tuple[int, str]] = [
            (1, "Alexander Hamilton-Montgomery III"),
            (2, "Elizabeth Victoria Anastasia Windsor"),
            (3, "Muhammad Ali ibn Abdullah al-Rashid"),
        ]
        print_selection(selections)

    def test_print_custom_per_line(self) -> None:
        """Test printing with custom per_line parameter."""
        print("\n--- Test: Custom Per Line (2 per line) ---")
        selections: list[tuple[int, str]] = [
            (1, "Alice Johnson"),
            (2, "Bob Smith"),
            (3, "Charlie Brown"),
            (4, "Diana Prince"),
            (5, "Edward Norton"),
            (6, "Fiona Apple"),
        ]
        print_selection(selections, per_line=2)

    def test_print_mixed_data(self) -> None:
        """Test printing with mixed serial numbers and name lengths."""
        print("\n--- Test: Mixed Data (15 students) ---")
        selections: list[tuple[int, str]] = [
            (1, "Ada Lovelace"),
            (5, "Grace Hopper"),
            (12, "Alan Turing"),
            (23, "Margaret Hamilton"),
            (34, "Dennis Ritchie"),
            (45, "Linus Torvalds"),
            (56, "Guido van Rossum"),
            (67, "Bjarne Stroustrup"),
            (78, "James Gosling"),
            (89, "Tim Berners-Lee"),
            (100, "Donald Knuth"),
            (111, "Edsger Dijkstra"),
            (122, "John von Neumann"),
            (133, "Claude Shannon"),
            (144, "Alonzo Church"),
        ]
        print_selection(selections)


if __name__ == "__main__":
    unittest.main()
