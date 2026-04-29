"""Low-level writers for reporting artifacts."""

from __future__ import annotations

import csv
from pathlib import Path
from typing import Any

MODE_ORDER = ("papf", "broad_access", "prompt_only")


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=tuple(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def write_markdown(path: Path, rows: list[dict[str, Any]], title: str) -> None:
    if not rows:
        path.write_text(f"# {title}\n\nNo rows.\n", encoding="utf-8")
        return
    headers = tuple(rows[0].keys())
    lines = [
        f"# {title}",
        "",
        "|" + "|".join(headers) + "|",
        "|" + "|".join("---" for _ in headers) + "|",
    ]
    for row in rows:
        lines.append("|" + "|".join(_md_cell(row[header]) for header in headers) + "|")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_bar_svg(
    path: Path,
    *,
    title: str,
    y_label: str,
    values: dict[str, float],
    value_format: str,
) -> None:
    width, height = 720, 420
    left, top, bottom = 84, 52, 78
    chart_width = width - left - 34
    chart_height = height - top - bottom
    max_value = max([1.0, *values.values()])
    bar_width = chart_width / max(1, len(values)) * 0.58
    gap = chart_width / max(1, len(values))
    colors = {"papf": "#2563eb", "broad_access": "#dc2626", "prompt_only": "#f59e0b"}
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" role="img" aria-label="{title}">',
        "<style>text{font-family:Arial,sans-serif;fill:#111827}.axis{stroke:#374151;stroke-width:1}"
        ".grid{stroke:#e5e7eb;stroke-width:1}.bar-label{font-size:13px}.tick{font-size:12px}</style>",
        f'<text x="{width / 2}" y="28" text-anchor="middle" font-size="20" font-weight="700">{title}</text>',
        f'<text x="20" y="{top + chart_height / 2}" transform="rotate(-90 20 {top + chart_height / 2})" '
        f'text-anchor="middle" font-size="13">{y_label}</text>',
        f'<line class="axis" x1="{left}" y1="{top}" x2="{left}" y2="{top + chart_height}"/>',
        f'<line class="axis" x1="{left}" y1="{top + chart_height}" x2="{left + chart_width}" '
        f'y2="{top + chart_height}"/>',
    ]
    parts.extend(_tick_svg(left, top, chart_width, chart_height, max_value, value_format))
    for index, mode in enumerate(mode for mode in MODE_ORDER if mode in values):
        parts.extend(
            _bar_svg(
                mode=mode,
                value=values[mode],
                index=index,
                left=left,
                top=top,
                gap=gap,
                bar_width=bar_width,
                chart_height=chart_height,
                max_value=max_value,
                color=colors.get(mode, "#6b7280"),
                value_format=value_format,
            )
        )
    parts.append("</svg>")
    path.write_text("\n".join(parts) + "\n", encoding="utf-8")


def _tick_svg(
    left: int,
    top: int,
    chart_width: int,
    chart_height: int,
    max_value: float,
    value_format: str,
) -> list[str]:
    parts = []
    for tick in (0, 0.25, 0.5, 0.75, 1.0):
        y = top + chart_height - (tick * chart_height)
        label = value_format.format(tick * max_value)
        parts.append(f'<line class="grid" x1="{left}" y1="{y:.1f}" x2="{left + chart_width}" y2="{y:.1f}"/>')
        parts.append(f'<text class="tick" x="{left - 8}" y="{y + 4:.1f}" text-anchor="end">{label}</text>')
    return parts


def _bar_svg(
    *,
    mode: str,
    value: float,
    index: int,
    left: int,
    top: int,
    gap: float,
    bar_width: float,
    chart_height: int,
    max_value: float,
    color: str,
    value_format: str,
) -> list[str]:
    x = left + index * gap + (gap - bar_width) / 2
    height = chart_height * (value / max_value if max_value else 0)
    y = top + chart_height - height
    return [
        f'<rect x="{x:.1f}" y="{y:.1f}" width="{bar_width:.1f}" height="{height:.1f}" fill="{color}"/>',
        f'<text class="bar-label" x="{x + bar_width / 2:.1f}" y="{y - 8:.1f}" '
        f'text-anchor="middle">{value_format.format(value)}</text>',
        f'<text class="tick" x="{x + bar_width / 2:.1f}" y="{top + chart_height + 28}" '
        f'text-anchor="middle">{mode}</text>',
    ]


def _md_cell(value: Any) -> str:
    return str(value).replace("|", "\\|")
