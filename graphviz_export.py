def wisdom_unit_to_graphviz(wu):
    """
    Generate Graphviz (DOT) code for a synthesis wheel from a WisdomUnit,
    using clusters for Thesis and Antithesis, and the updated edge structure,
    including dotted, bidirectional arrows between T+ <-> A- and A+ <-> T-.
    """
    def safe(attr, fallback=""):
        comp = getattr(wu, attr, None)
        return comp.statement if comp and hasattr(comp, "statement") else fallback or attr

    return f"""
digraph WisdomUnit {{
    layout=fdp;
    node [shape=circle, style=filled, fontname="Arial"];

    // Thesis cluster
    subgraph cluster_T {{
        label="Thesis";
        style=dashed;
        color="#B3D1FF";
        T      [label="T\\n{safe('t')}",      fillcolor="#B3D1FF"];
        Tplus  [label="T+\\n{safe('t_plus')}",    fillcolor="#D1FFD1"];
        Tminus [label="T-\\n{safe('t_minus')}",          fillcolor="#FFD1D1"];
    }}

    // Antithesis cluster
    subgraph cluster_A {{
        label="Antithesis";
        style=dashed;
        color="#FFECB3";
        A      [label="A\\n{safe('a')}",        fillcolor="#FFECB3"];
        Aplus  [label="A+\\n{safe('a_plus')}", fillcolor="#D1FFFF"];
        Aminus [label="A-\\n{safe('a_minus')}",      fillcolor="#FFD1EC"];
    }}

    // Synthesis/other nodes (not in clusters)
    Splus  [label="S+\\nWin-Win",         fillcolor="#E0E0FF"];
    Sminus [label="S-\\nLose-Lose",       fillcolor="#FFE0E0"];

    // Main cycle
    T      -> Tplus;
    T      -> Tminus;
    Tplus  -> Splus;
    Aplus  -> Splus;
    A      -> Aplus;
    A      -> Aminus;
    Aminus -> Sminus;
    Tminus -> Sminus;

    // Direct thesis-antithesis link
    T -> A [color=black, penwidth=2];

    // Dotted entanglement arrows
    Tplus -> Aminus [style=dotted, dir=both, color=gray];
    Aplus -> Tminus [style=dotted, dir=both, color=gray];
}}
""".strip()

# Suppose you have a WisdomUnit instance called wu:
dot_code = wisdom_unit_to_graphviz(wu)
with open("dialectical_wheel.dot", "w") as f:
    f.write(dot_code)
# Then render with Graphviz:
# dot -Tpng dialectical_wheel.dot -o wheel.png
