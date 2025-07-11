import re
from typing import Union
import math
import numpy as np

class Conversion:
    @staticmethod
    def spice(value: Union[int, float, str], precision: int = 2) -> str:
        """
        Converts numeric input (int, float, or metric string) into a clean SPICE-compatible
        string with proper metric suffixes.

        Args:
            value (int | float | str): The input value to format.
            precision (int): Decimal rounding precision before suffix.

        Returns:
            str: SPICE-compatible string like '4.7u', '22k', '1Meg'

        Raises:
            ValueError: If the input string format is invalid.
        """
        spice_prefixes = {
            -15: 'f',
            -12: 'p',
            -9:  'n',
            -6:  'u',
            -3:  'm',
            0:   '',
            3:   'k',
            6:   'Meg',
            9:   'G',
            12:  'T'
        }

        suffix_multipliers = {
            'y': 1e-24, 'z': 1e-21, 'a': 1e-18, 'f': 1e-15,
            'p': 1e-12, 'n': 1e-9,  'u': 1e-6,  'µ': 1e-6,
            'm': 1e-3,  '': 1,      'k': 1e3,   'K': 1e3,
            'M': 1e6,   'meg': 1e6, 'g': 1e9,   'G': 1e9,
            't': 1e12,  'T': 1e12,  'Meg': 1e6,
        }

        def parse_str_metric(s: str) -> float:
            s = s.strip()
            match = re.fullmatch(r'([-+]?\d*\.?\d+(?:[eE][-+]?\d+)?)([a-zA-Zµ]*)', s)
            if not match:
                raise ValueError(f"Invalid SPICE value string: '{s}'")
            num_str, suffix = match.groups()
            multiplier = suffix_multipliers.get(suffix)
            if multiplier is None:
                raise ValueError(f"Unrecognized metric suffix: '{suffix}'")
            return float(num_str) * multiplier

        # Normalize input
        if isinstance(value, str):
            value = parse_str_metric(value)
        elif isinstance(value, (int, float)):
            value = float(value)
        else:
            raise TypeError(f"Unsupported type for value: {type(value).__name__}")

        if value == 0:
            return "0"

        # Determine proper metric prefix
        exponent = int(math.floor(math.log10(abs(value)) / 3) * 3)
        exponent = max(min(exponent, 12), -15)  # Clamp to SPICE-supported
        scaled = value / (10 ** exponent)
        rounded = round(scaled, precision)

        # Clean up trailing zeros
        if math.isclose(rounded, round(rounded), abs_tol=10**-precision):
            rounded_str = str(int(round(rounded)))
        else:
            rounded_str = f"{rounded:.{precision}f}".rstrip("0").rstrip(".")

        suffix = spice_prefixes.get(exponent, f"e{exponent}")
        return f"{rounded_str}{suffix}"
    
    @staticmethod
    def from_metric(s: Union[int, float, str]) -> float:
        """
        Parses a numeric value with optional metric suffix (e.g. '1k', '4.7u') and returns its float equivalent.

        Args:
            s (int | float | str): A numeric input with or without a metric suffix.

        Returns:
            float: The parsed and scaled numeric value.

        Raises:
            ValueError: If the string format is invalid.
        """
        multipliers = {
            'y': 1e-24, 'z': 1e-21, 'a': 1e-18, 'f': 1e-15,
            'p': 1e-12, 'n': 1e-9,  'u': 1e-6,  'µ': 1e-6,
            'm': 1e-3,  '': 1,      'k': 1e3,   'K': 1e3,
            'M': 1e6,   'G': 1e9,   'T': 1e12,  'P': 1e15,
            'E': 1e18,  'Z': 1e21,  'Y': 1e24
        }

        if isinstance(s, (int, float, np.number)):
            return float(s)

        if not isinstance(s, str):
            raise TypeError(f"Unsupported type for metric parsing: {type(s).__name__}")

        s = s.strip()
        match = re.fullmatch(r'(-?\d*\.?\d+|-?\d+)([a-zA-Zµ]?)', s)
        if not match:
            raise ValueError(f"Invalid metric string: '{s}'")

        num_str, prefix = match.groups()
        multiplier = multipliers.get(prefix)
        if multiplier is None:
            raise ValueError(f"Unknown metric prefix: '{prefix}'")

        return float(num_str) * multiplier
    
    @staticmethod
    def to_metric(value: Union[int, float], precision: int = 2) -> str:
        """
        Converts a numeric value to a SPICE-friendly string with metric prefix, 
        rounded to the nearest whole number when trailing zeroes repeat.

        Args:
            value (int | float): The numeric value to convert.
            precision (int): Decimal precision before rounding to whole if applicable.

        Returns:
            str: A metric-prefixed string, like '1u', '47k', '10'

        Raises:
            TypeError: If value is not int or float.
        """
        if not isinstance(value, (int, float)):
            raise TypeError(f"Expected int or float, got {type(value).__name__}")

        if value == 0:
            return "0"

        prefixes = {
            -24: 'y', -21: 'z', -18: 'a', -15: 'f',
            -12: 'p', -9: 'n', -6: 'u', -3: 'm',
            0: '',    3: 'k',   6: 'M',   9: 'G',
            12: 'T', 15: 'P',  18: 'E',  21: 'Z', 24: 'Y'
        }

        exponent = int(math.floor(math.log10(abs(value)) / 3) * 3)
        exponent = max(min(exponent, 24), -24)  # Clamp exponent to supported range

        scaled = value / (10 ** exponent)
        rounded = round(scaled, precision)

        # If rounded is effectively an integer, format it as such
        if math.isclose(rounded, round(rounded), abs_tol=10**-precision):
            rounded_str = str(int(round(rounded)))
        else:
            rounded_str = f"{rounded:.{precision}f}".rstrip("0").rstrip(".")

        prefix = prefixes.get(exponent, '')
        return f"{rounded_str}{prefix}"