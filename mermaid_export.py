def wisdom_unit_to_mermaid(wu):
    # wu: WisdomUnit
    lines = [
        "graph TD",
        f'    T["T: {wu.t.statement if wu.t else ""}"]',
        f'    Tplus["T+: {wu.t_plus.statement if wu.t_plus else ""}"]',
        f'    Tminus["T-: {wu.t_minus.statement if wu.t_minus else ""}"]',
        f'    A["A: {wu.a.statement if wu.a else ""}"]',
        f'    Aplus["A+: {wu.a_plus.statement if wu.a_plus else ""}"]',
        f'    Aminus["A-: {wu.a_minus.statement if wu.a_minus else ""}"]',
        "    T --> Tplus",
        "    T --> Tminus",
        "    T --vs--> A",
        "    A --> Aplus",
        "    A --> Aminus",
    ]
    return "\n".join(lines)

def wheel_to_mermaid(wheel):
    # wheel: Wheel
    lines = ["graph TD"]
    for idx, wu in enumerate(wheel.wisdom_units):
        prefix = f"WU{idx}_"
        # Nodes
        lines.append(f'    {prefix}T["T: {wu.t.statement if wu.t else ""}"]')
        lines.append(f'    {prefix}Tplus["T+: {wu.t_plus.statement if wu.t_plus else ""}"]')
        lines.append(f'    {prefix}Tminus["T-: {wu.t_minus.statement if wu.t_minus else ""}"]')
        lines.append(f'    {prefix}A["A: {wu.a.statement if wu.a else ""}"]')
        lines.append(f'    {prefix}Aplus["A+: {wu.a_plus.statement if wu.a_plus else ""}"]')
        lines.append(f'    {prefix}Aminus["A-: {wu.a_minus.statement if wu.a_minus else ""}"]')
        # Edges
        lines.append(f"    {prefix}T --> {prefix}Tplus")
        lines.append(f"    {prefix}T --> {prefix}Tminus")
        lines.append(f"    {prefix}T --vs--> {prefix}A")
        lines.append(f"    {prefix}A --> {prefix}Aplus")
        lines.append(f"    {prefix}A --> {prefix}Aminus")
        # Optionally, connect wisdom units in a cycle
        if idx < len(wheel.wisdom_units) - 1:
            next_prefix = f"WU{idx+1}_"
            lines.append(f"    {prefix}A --> {next_prefix}T")
    # Close the cycle
    if len(wheel.wisdom_units) > 1:
        lines.append(f"    WU{len(wheel.wisdom_units)-1}_A --> WU0_T")
    return "\n".join(lines)