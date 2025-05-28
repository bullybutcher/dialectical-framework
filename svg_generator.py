import math

def svg_dialectical_wheel(slices, center_label="Core", radius=150, width=400, height=400):
    """
    slices: list of dicts, each with keys:
        - labels: list of (label, color) from center outward along the slice
    Example:
        slices = [
            {"labels": [("Clarity, relief", "yellow"), ("Family unity", "green"), ("Buy a house", "black"), ("Burden", "red")]},
            {"labels": [("Clarity, relief", "yellow"), ("Don't buy", "black"), ("Separation", "red")]},
        ]
    """
    cx, cy = width // 2, height // 2
    n = len(slices)
    angle_per = 2 * math.pi / n
    svg = [f'<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">']

    # Draw center circle and label
    svg.append(f'<circle cx="{cx}" cy="{cy}" r="{radius*0.2}" fill="#FFFF99" stroke="black" stroke-width="2"/>')
    svg.append(
        f'<text x="{cx}" y="{cy}" font-size="16" font-weight="bold" text-anchor="middle" alignment-baseline="middle">{center_label}</text>'
    )

    # Draw each slice
    for i, sl in enumerate(slices):
        start_angle = i * angle_per
        end_angle = (i + 1) * angle_per
        angle_mid = (start_angle + end_angle) / 2
        n_labels = len(sl["labels"])
        for j, (label, color) in enumerate(sl["labels"]):
            r = radius * (0.2 + 0.7 * (j+1) / n_labels)  # spread labels from center outward
            lx = cx + r * math.cos(angle_mid)
            ly = cy + r * math.sin(angle_mid)
            svg.append(
                f'<text x="{lx}" y="{ly}" font-size="14" text-anchor="middle" alignment-baseline="middle" fill="{color}">{label}</text>'
            )
        # Draw the slice sector (optional, for visual separation)
        x1 = cx + radius * math.cos(start_angle)
        y1 = cy + radius * math.sin(start_angle)
        x2 = cx + radius * math.cos(end_angle)
        y2 = cy + radius * math.sin(end_angle)
        large_arc = 1 if angle_per > math.pi else 0
        path = (
            f'M {cx},{cy} '
            f'L {x1},{y1} '
            f'A {radius},{radius} 0 {large_arc},1 {x2},{y2} '
            f'Z'
        )
        svg.append(f'<path d="{path}" fill="none" stroke="#888" stroke-width="1"/>')

    svg.append('</svg>')
    return "\n".join(svg)

# Example usage:
slices = [
    {"labels": [("Clarity, relief", "orange"), ("Family unity", "green"), ("Buy a house", "black"), ("Burden", "red")]},
    {"labels": [("Clarity, relief", "orange"), ("Don't buy", "black"), ("Separation", "red")]},
]
svg_code = svg_dialectical_wheel(slices, center_label="Clarity, relief")
with open("dialectical_wheel.svg", "w") as f:
    f.write(svg_code)
