#!/usr/bin/env python3
"""Stage 1: Convert IIT_ALL.txt (raw JoSAA export) into a clean canonical CSV database.

Output: josaa_iit_2025_r6.csv  — proper RFC-4180 CSV, no trailing whitespace,
typed ranks, plus derived columns (degree, duration, dual flag) for the website.
"""
import csv, re, os

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "IIT_ALL.txt")
OUT = os.path.join(HERE, "josaa_iit_2025_r6.csv")

def clean(s):
    return re.sub(r"\s+", " ", s).strip()

def last_paren_group(s):
    """Return (content, start_index) of the last balanced top-level (...) group, else ('', -1)."""
    s = s.rstrip()
    if not s.endswith(")"):
        return "", -1
    depth = 0
    for i in range(len(s) - 1, -1, -1):
        if s[i] == ")":
            depth += 1
        elif s[i] == "(":
            depth -= 1
            if depth == 0:
                return s[i + 1:-1], i
    return "", -1

def classify_degree(deg):
    """Return (duration_years, degree_type, is_dual)."""
    dur = 0
    m = re.match(r"\s*(\d+)\s*Years", deg)
    if m:
        dur = int(m.group(1))
    d = deg.lower()
    # a program is dual/integrated if it confers a master's component or is flagged dual
    dual = any(k in d for k in (
        "dual degree", "integrated", "and mba", "m.tech", "master of technology",
        "master of science", "+ m"))
    if "mba" in d:
        dtype = "B.Tech + MBA"
    elif "bachelor of architecture" in d:
        dtype, dual = "B.Arch", False
    elif dual:
        if "master of science" in d or ("bachelor of science" in d and "ms" in d):
            dtype = "Dual Degree (BS-MS)"
        else:
            dtype = "Dual Degree (B.Tech-M.Tech)"
    elif "bachelor of technology" in d:
        dtype = "B.Tech"
    elif "bachelor of science" in d:
        dtype = "B.S."
    else:
        dtype = deg
    return dur, dtype, dual

rows = []
with open(SRC, encoding="utf-8") as f:
    header = next(f)
    for ln, line in enumerate(f, start=2):
        if not line.strip():
            continue
        parts = line.rstrip("\n").split("\t")
        if len(parts) != 7:
            raise SystemExit(f"Line {ln}: expected 7 fields, got {len(parts)}")
        inst, prog, quota, seat, gender, opr, clr = [clean(p) for p in parts]
        deg, idx = last_paren_group(prog)
        core = clean(prog[:idx]) if idx > 0 else prog
        dur, dtype, dual = classify_degree(deg)
        rows.append({
            "institute": inst,
            "institute_short": inst.replace("Indian Institute of Technology", "IIT"),
            "program": prog,
            "program_core": core,
            "quota": quota,
            "seat_type": seat,
            "gender": "Female-only" if "Female" in gender else "Gender-Neutral",
            "opening_rank": int(opr),
            "closing_rank": int(clr),
            "degree": deg,
            "duration_years": dur,
            "degree_type": dtype,
            "is_dual": "yes" if dual else "no",
        })

fields = ["institute", "institute_short", "program", "program_core", "quota",
          "seat_type", "gender", "opening_rank", "closing_rank",
          "degree", "duration_years", "degree_type", "is_dual"]

with open(OUT, "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=fields, quoting=csv.QUOTE_MINIMAL)
    w.writeheader()
    w.writerows(rows)

print(f"Wrote {OUT}  ({len(rows)} rows)")
print("degree_type counts:")
from collections import Counter
for k, v in Counter(r["degree_type"] for r in rows).most_common():
    print(f"  {v:4d}  {k}")
print("dual counts:", Counter(r["is_dual"] for r in rows))
print("duration counts:", Counter(r["duration_years"] for r in rows))
