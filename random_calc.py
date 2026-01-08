import math
import re
import numpy as np
from Utilities.Converter import Conversion as conv


# ─────────────────────────────────────────────────────────────────────────────
# Core Electrical Calculations
# ─────────────────────────────────────────────────────────────────────────────

def secondary(l1: float, n1: float, n2: float) -> float:
    return (l1 * (n2 ** 2)) / (n1 ** 2)

def primary(l2: float, n1: float, n2: float) -> float:
    return (l2 * (n1 ** 2)) / (n2 ** 2)

def res_freq_c(res: float, l: float) -> float:
    return 1 / (4 * (math.pi ** 2) * l * (res ** 2))

def ind_react(l: float, f: float) -> float:
    return 2 * math.pi * f * l

def cap_react(c: float, f: float) -> float:
    return 1 / (2 * math.pi * f * c)

def tau_rc(r: float, c: float) -> float:
    """Time constant for an RC circuit."""
    return r * c

def tau_rl(l: float, r: float) -> float:
    """Time constant for an RL circuit."""
    return l / r



# ─────────────────────────────────────────────────────────────────────────────
# Terminal Utilities
# ─────────────────────────────────────────────────────────────────────────────

ansi_escape = re.compile(r'\x1b\[[0-9;]*m')

def rgb_text(hex_color: str, text: str) -> str:
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)
    return f"\033[38;2;{r};{g};{b}m{text}\033[0m"

def visible_len(text: str) -> int:
    return len(ansi_escape.sub('', text))

def strip_ansi(text: str) -> str:
    return ansi_escape.sub('', text)


# ─────────────────────────────────────────────────────────────────────────────
# Display Helpers
# ─────────────────────────────────────────────────────────────────────────────

def print_header(width: int = 70, color: str = "74C7EC", **fields: float | str) -> str:
    from itertools import chain

    # Format all key-value fields
    parts = []
    for key, val in fields.items():
        if isinstance(val, (int, float)):
            val_str = conv.to_metric(val)
        else:
            val_str = str(val)
        parts.append(f"{key}: {val_str}")

    joined = " | ".join(parts)

    # Add 5-space padding left and right
    padded = f"{' ' * 2}{joined}{' ' * 2}"
    colored = rgb_text(color, padded)

    # Wrap in brackets
    box = f"[{colored}]"

    # Account for visual width (no ANSI)
    visible_box_width = visible_len(padded) + 2  # +2 for brackets
    padding = width - visible_box_width
    left = "─" * (padding // 2)
    right = "─" * (padding - len(left))
    output = f"{left}{box}{right}"
    print(output)
    return strip_ansi(output)


def row_line(label: str, value: str, width: int = 70, color: str = 'EBA0AC') -> str:
    target_box_width = 14
    padded = f"{value:^{target_box_width}}"
    colored = rgb_text(color, padded)
    boxed = f"[{colored}]"
    label_width = width - (2 + target_box_width)  # 2 for the brackets
    output = f"{label:<{label_width}}{boxed}"
    print(output)
    return strip_ansi(output)


def run(tuned_freq: float, l2: float, width: int = 70) -> None:
    # Constants
    l2_val = conv.from_metric(l2)
    n1, n2 = 1, 4
    r_val = 1500

    # Calculations
    l1_val = primary(l2_val, n1, n2)

    # Resonant capacitances
    l2c_val = res_freq_c(tuned_freq, l2_val)
    l1c_val = res_freq_c(tuned_freq, l1_val)

    # Reactances
    xc1_val = cap_react(l1c_val, tuned_freq)  # L1’s capacitor
    xl1_val = ind_react(l1_val, tuned_freq)   # L1’s inductor
    xc2_val = cap_react(l2c_val, tuned_freq)  # L2’s capacitor
    xl2_val = ind_react(l2_val, tuned_freq)   # L2’s inductor

    # Quality factors
    l2_q_val = r_val * math.sqrt(l2c_val / l2_val)
    l1_q_val = r_val * math.sqrt(l1c_val / l1_val)

    # Equivalent impedance
    z_val = l2_q_val * xl1_val

    # Time constants
    tau_rc_l1 = tau_rc(r_val, l1c_val)
    tau_rc_l2 = tau_rc(r_val, l2c_val)
    tau_rl_l1 = tau_rl(l1_val, r_val)
    tau_rl_l2 = tau_rl(l2_val, r_val)

    # Print header
    print_header(
        width=width,
        color='74C7EC',
        L1=f'{conv.to_metric(l1_val)}H',
        L2=f'{conv.to_metric(l2_val)}H',
        Ratio=f'{n1}:{n2}',
    )

    # L1 section
    row_line("L1 (LOW SIDE WINDING) Tuned Capacitance", f"{conv.to_metric(l1c_val)}F", width)
    row_line("Capacitive Reactance", f"{conv.to_metric(xc1_val)}Ω", width)
    row_line("Inductive Reactance", f"{conv.to_metric(xl1_val)}Ω", width)
    row_line("RC Time Constant", f"{conv.to_metric(tau_rc_l1)}s", width)
    row_line("RL Time Constant", f"{conv.to_metric(tau_rl_l1)}s", width)
    row_line(f"Q Factor [RE: {conv.to_metric(r_val)}Ω - L1]", f"{conv.to_metric(l1_q_val)}", width)
    
    print()  # spacing

    # L2 section
    row_line("L2 (HIGH SIDE WINDING) Tuned Capacitance", f"{conv.to_metric(l2c_val)}F", width)
    row_line("Capacitive Reactance", f"{conv.to_metric(xc2_val)}Ω", width)
    row_line("Inductive Reactance", f"{conv.to_metric(xl2_val)}Ω", width)
    row_line("RC Time Constant", f"{conv.to_metric(tau_rc_l2)}s", width)
    row_line("RL Time Constant", f"{conv.to_metric(tau_rl_l2)}s", width)
    row_line(f"Q Factor [RE: {conv.to_metric(r_val)}Ω - L2]", f"{conv.to_metric(l2_q_val)}", width)

    print()  # spacing

freqs = [
    '1M',
]

inductor_values = ['1n', '2n', '4n', '8n', '10n', '20n', '40n', '80n', '100n', '200n', '400n', '800n', '1u', '2u', '4u', '8u', '10u', '20u', '40u', '80u', '100u', '200u', '400u', '800u']

for freq in freqs:
    print_header(width=100, color='F5E0DC', Frequency=f'{conv.from_metric(freq)}Hz')
    print()
    for l2 in inductor_values:
        run(tuned_freq=conv.from_metric(freq), l2=conv.from_metric(l2), width=100)
