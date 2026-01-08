import math
import re
import os
from Utilities.Converter import Conversion as conv
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


def secondary(l1: float, n1: float, n2: float) -> float:
    return (l1 * (n2 ** 2)) / (n1 ** 2)

def primary(l2: float, n1: float, n2: float) -> float:
    return (l2 * (n1 ** 2)) / (n2 ** 2)

def res_freq_c(freq: float, l: float) -> float:
    if freq <= 0 or l <= 0:
        return float('inf')
    return 1 / ((2 * math.pi * freq) ** 2 * l)

def ind_react(l: float, f: float) -> float:
    return 2 * math.pi * f * l if f > 0 else 0.0

def cap_react(c: float, f: float) -> float:
    return 1 / (2 * math.pi * f * c) if (f > 0 and c > 0) else float('inf')

def tau_rc(r: float, c: float) -> float:
    return r * c

def tau_rl(l: float, r: float) -> float:
    return l / r if r != 0 else float('inf')

def bandwidth(freq: float, q: float) -> float:
    return freq / q if q != 0 else float('inf')

def q_factor_lc(l: float, c: float, r: float) -> float:
    if l <= 0 or c <= 0 or r <= 0:
        return 0.0
    f0 = 1 / (2 * math.pi * math.sqrt(l * c))
    x_l = 2 * math.pi * f0 * l
    return x_l / r


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


def print_header(width: int = 70, color: str = "74C7EC", **fields: float | str) -> str:
    parts = []
    for key, val in fields.items():
        if isinstance(val, (int, float)):
            val_str = conv.to_metric(val)
        else:
            val_str = str(val)
        parts.append(f"{key}: {val_str}")
    joined = " | ".join(parts)
    padded = f"{' ' * 2}{joined}{' ' * 2}"
    colored = rgb_text(color, padded)
    box = f"[{colored}]"
    visible_box_width = visible_len(padded) + 2
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
    label_width = width - (2 + target_box_width)
    output = f"{label:<{label_width}}{boxed}"
    print(output)
    return strip_ansi(output)


def run(tuned_freq: float, l2: float, width: int = 70) -> list[str]:
    l2_val = conv.from_metric(l2)
    n1, n2 = 1, 1
    r_val = 50
    l1_val = primary(l2_val, n1, n2)
    l1c_val = res_freq_c(tuned_freq, l1_val)
    xc1_val = cap_react(l1c_val, tuned_freq)
    tau_rc_l1 = tau_rc(r_val, l1c_val)
    tau_rl_l1 = tau_rl(l1_val, r_val)
    q_out = q_factor_lc(l1_val, l1c_val, r_val)
    bw_out = bandwidth(tuned_freq, q_out)
    lines = []
    lines.append(print_header(width=width, color='74C7EC', L1=f'{conv.to_metric(l1_val)}H'))
    lines.append(row_line("L1 Tuned Capacitance", f"{conv.to_metric(l1c_val)}F", width))
    lines.append(row_line("L/C Reactance", f"{conv.to_metric(xc1_val)}Ω", width))
    lines.append(row_line("RC Time Constant", f"{conv.to_metric(tau_rc_l1)}s", width))
    lines.append(row_line("RL Time Constant", f"{conv.to_metric(tau_rl_l1)}s", width))
    lines.append(row_line("Bandwidth (Output)", f"{conv.to_metric(bw_out)}Hz", width))
    lines.append("")  # Add an empty line for better readability
    return lines


if __name__ == "__main__":
    freqs = ['1M', '445k', '20k', '10k']
    inductor_values = [
        '1n', '2n', '4n', '5n', '8n', '10n', '20n', '40n', '50n', '80n', '100n', '200n', '400n', '800n', '500n', '1u', '2u', '4u', '5u', '8u', '10u',
        '20u', '40u', '50u', '80u', '100u', '200u', '400u', '500u', '800u', '1m', '1m', '2m', '4m', '5m', '8m', '10m'
    ]
    results = []
    for freq in freqs:
        results.append(print_header(width=50, color='F5E0DC', Frequency=f'{freq}Hz'))
        results.append("")
        for l2 in inductor_values:
            results.extend(run(tuned_freq=conv.from_metric(freq), l2=l2, width=50))

    # save results as PDF in same dir
    script_dir = os.path.dirname(os.path.abspath(__file__))
    out_path = os.path.join(script_dir, "output.pdf")

    c = canvas.Canvas(out_path, pagesize=letter)
    width, height = letter
    y = height - 50
    for line in results:
        c.drawString(40, y, line)
        y -= 15
        if y < 50:  # new page if we run out of space
            c.showPage()
            y = height - 50
    c.save()
