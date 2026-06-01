"""Canonical course-group definitions, shared by the coverage checker and the site builder.
Each group = (label, [keyword alternatives]). Matching is case-insensitive substring
on the FULL program name, so a single group catches every variant (4-yr / 5-yr / dual /
specialisation / abbreviation) whose name contains any keyword."""

CHIPS = [
    ("Computer Science",          ["computer science", "(cse)", " cse "]),
    ("AI / Data Science",         ["artificial intelligence", "data science", "data analytics",
                                   "data engineering"]),
    ("Maths & Computing",         ["mathematics and computing", "mathematics & computing",
                                   "mathematics and scientific", "statistics", "bs in mathematics"]),
    ("Electrical",                ["electrical", "(eee)", "(power"]),
    ("Electronics / ECE / VLSI",  ["electronics", "communication", "vlsi", "microelectronics",
                                   "integrated circuit"]),
    ("Mechanical",                ["mechanical", "mechatronics", "manufacturing"]),
    ("Civil / Infrastructure",    ["civil", "infrastructure", "structural", "geotechnical"]),
    ("Chemical",                  ["chemical", "industrial chemistry", "pharmaceutical"]),
    ("Aerospace / Space",         ["aerospace", "space science"]),
    ("Materials / Metallurgy",    ["material", "metallurg", "ceramic", "mineral"]),
    ("Physics",                   ["physics", "physical science"]),
    ("Chemistry",                 ["chemistry", "chemical sciences", "chemical science",
                                   "bs in chemical"]),
    ("Mathematics (pure)",        ["mathematics"]),
    ("Bio / Biomedical",          ["bio", "biomedical", "biotech"]),
    ("Earth / Geo / Ocean",       ["geo", "earth", "ocean", "naval", "petroleum", "mining"]),
    ("Economics",                 ["economic"]),
    ("Architecture / Design",     ["architecture", "design"]),
    ("Engg. Science / Computational", ["engineering science", "engineering design",
                                       "computational", "general engineering"]),
    ("Production / Industrial",   ["production", "industrial"]),
    ("Agriculture / Food",        ["agricultur", "food"]),
    ("Instrumentation",           ["instrumentation"]),
    ("Environmental",             ["environment"]),
    ("Textile",                   ["textile"]),
    ("Interdisciplinary",         ["interdisciplinary"]),
    ("Energy",                    ["energy"]),
]
