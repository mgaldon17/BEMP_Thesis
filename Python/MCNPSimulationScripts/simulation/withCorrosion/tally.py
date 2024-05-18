from typing import List

class Tally:
    """Class to represent a tally."""

    def __init__(self, number: int, list_vals: List[float], list_errors: List[float]):
        """Initialize a Tally instance."""
        self._number = number
        self._list_vals = list_vals
        self._list_errors = list_errors

    @property
    def number(self) -> int:
        """Get the number of the tally."""
        return self._number

    @property
    def list_vals(self) -> List[float]:
        """Get the list of values of the tally."""
        return self._list_vals

    @list_vals.setter
    def list_vals(self, val: float):
        """Add a value to the list of values of the tally."""
        self._list_vals.append(val)

    @property
    def list_errors(self) -> List[float]:
        """Get the list of errors of the tally."""
        return self._list_errors

    @list_errors.setter
    def list_errors(self, rel_error: float):
        """Add an error to the list of errors of the tally."""
        self._list_errors.append(rel_error)