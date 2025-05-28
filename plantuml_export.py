def wisdom_unit_to_plantuml(wu):
    """
    Generate PlantUML code for a synthesis diagram from a WisdomUnit.
    """
    # Safely get statements or use empty string if missing
    def s(attr): return getattr(wu, attr).statement if getattr(wu, attr, None) else attr

    return f"""
@startuml
!define RECTANGLE class
skinparam class {{
    BackgroundColor White
    BorderColor Black
}}

RECTANGLE T as "T\\n{s('t')}"
RECTANGLE Tplus as "T+\\n{s('t_plus')}"
RECTANGLE Splus as "S+"
RECTANGLE Aplus as "A+\\n{s('a_plus')}"
RECTANGLE A as "A\\n{s('a')}"
RECTANGLE Aminus as "A-\\n{s('a_minus')}"
RECTANGLE Sminus as "S-"
RECTANGLE Tminus as "T-\\n{s('t_minus')}"

T -right-> A
T -left-> Tplus
T -down-> Tminus
A -up-> Aplus
A -down-> Aminus
Tminus -down-> Sminus
Aminus -down-> Sminus
Tplus -up-> Splus
Aplus -up-> Splus

@enduml
""".strip()

def wheel_to_plantuml(wheel):
    """
    Generate PlantUML code for a circular dialectical wheel from a Wheel object.
    Each WisdomUnit is a 'slice' in the wheel.
    """
    def safe(attr, wu, fallback=""):
        comp = getattr(wu, attr, None)
        return comp.statement if comp and hasattr(comp, "statement") else fallback or attr

    n = len(wheel.wisdom_units)
    lines = [
        "@startuml",
        "!define RECTANGLE class",
        "skinparam class {",
        "    BackgroundColor White",
        "    BorderColor Black",
        "}"
    ]

    # Create nodes for each wisdom unit
    for i, wu in enumerate(wheel.wisdom_units):
        lines.append(f'RECTANGLE T{i} as "T{i+1}\\n{safe("t", wu)}"')
        lines.append(f'RECTANGLE Tplus{i} as "T+\\n{safe("t_plus", wu)}"')
        lines.append(f'RECTANGLE Tminus{i} as "T-\\n{safe("t_minus", wu)}"')
        lines.append(f'RECTANGLE A{i} as "A{i+1}\\n{safe("a", wu)}"')
        lines.append(f'RECTANGLE Aplus{i} as "A+\\n{safe("a_plus", wu)}"')
        lines.append(f'RECTANGLE Aminus{i} as "A-\\n{safe("a_minus", wu)}"')

    # Connect each wisdom unit's thesis to the next (cycle)
    for i in range(n):
        next_i = (i + 1) % n
        lines.append(f'T{i} -right-> T{next_i}')

    # Optionally, connect each wisdom unit's internal structure
    for i in range(n):
        lines.append(f'T{i} -up-> Tplus{i}')
        lines.append(f'T{i} -down-> Tminus{i}')
        lines.append(f'T{i} -right-> A{i}')
        lines.append(f'A{i} -up-> Aplus{i}')
        lines.append(f'A{i} -down-> Aminus{i}')

    lines.append("@enduml")
    return "\n".join(lines)