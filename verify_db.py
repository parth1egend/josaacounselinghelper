#!/usr/bin/env python3
"""Stage 2: verify josaa_iit_2025_r6.csv is fully consistent with IIT_ALL.txt.
Runs several independent checks; exits non-zero on any failure."""
import csv, re, os, sys
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
TXT = os.path.join(HERE, "IIT_ALL.txt")
CSV = os.path.join(HERE, "josaa_iit_2025_r6.csv")

def clean(s):
    return re.sub(r"\s+", " ", s).strip()

# ---- load raw source as canonical 7-tuples ----
src = []
with open(TXT, encoding="utf-8") as f:
    next(f)
    for line in f:
        if not line.strip():
            continue
        p = [clean(x) for x in line.rstrip("\n").split("\t")]
        assert len(p) == 7, p
        inst, prog, quota, seat, gender, opr, clr = p
        g = "Female-only" if "Female" in gender else "Gender-Neutral"
        src.append((inst, prog, quota, seat, g, int(opr), int(clr)))

# ---- load CSV ----
with open(CSV, encoding="utf-8") as f:
    db = list(csv.DictReader(f))

fails = 0
def check(name, cond, extra=""):
    global fails
    print(f"[{'PASS' if cond else 'FAIL'}] {name}" + (f"  {extra}" if extra else ""))
    if not cond:
        fails += 1

# CHECK 1: row count
check("row count 600", len(src) == 600 and len(db) == 600, f"src={len(src)} db={len(db)}")

# CHECK 2: exact 7-tuple multiset equality (method A: Counter of tuples)
db_tuples = Counter(
    (r["institute"], r["program"], r["quota"], r["seat_type"], r["gender"],
     int(r["opening_rank"]), int(r["closing_rank"])) for r in db)
src_tuples = Counter(src)
check("7-tuple multisets identical (method A)", db_tuples == src_tuples,
      f"missing={len(src_tuples-db_tuples)} extra={len(db_tuples-src_tuples)}")
for t in list((src_tuples - db_tuples).elements())[:5]:
    print("    MISSING from CSV:", t)
for t in list((db_tuples - src_tuples).elements())[:5]:
    print("    EXTRA in CSV:", t)

# CHECK 3 (method B, independent): sorted joined-string lists must match
def keyA(t): return "||".join(map(str, t))
src_lines = sorted(keyA(t) for t in src)
db_lines = sorted(keyA((r["institute"], r["program"], r["quota"], r["seat_type"],
                        r["gender"], int(r["opening_rank"]), int(r["closing_rank"]))) for r in db)
check("sorted line lists identical (method B)", src_lines == db_lines)

# CHECK 4: distinct programs preserved
check("distinct programs preserved",
      {t[1] for t in src} == {r["program"] for r in db},
      f"src={len({t[1] for t in src})} db={len({r['program'] for r in db})}")

# CHECK 5: distinct institutes preserved (and == 23)
insts = {r["institute"] for r in db}
check("distinct institutes == 23", insts == {t[0] for t in src} and len(insts) == 23,
      f"n={len(insts)}")

# CHECK 6: rank integrity
check("all opening<=closing, ranks positive ints",
      all(0 < int(r["opening_rank"]) <= int(r["closing_rank"]) for r in db))

# CHECK 7: derived columns sanity
check("duration_years in {4,5}", all(r["duration_years"] in ("4", "5") for r in db))
check("degree_type non-empty", all(r["degree_type"].strip() for r in db))
check("is_dual in {yes,no}", all(r["is_dual"] in ("yes", "no") for r in db))
# every dual program must be 5-year; no 4-year program may be dual
check("dual => 5-year (and 4-year => not dual)",
      all((r["is_dual"] == "no") for r in db if r["duration_years"] == "4") and
      all((r["duration_years"] == "5") for r in db if r["is_dual"] == "yes"))

# CHECK 8: institute_short is a faithful rename
check("institute_short maps cleanly",
      all(r["institute_short"] == r["institute"].replace("Indian Institute of Technology", "IIT")
          for r in db))

# CHECK 9: program_core is a prefix of program (nothing fabricated)
check("program_core is substring-prefix of program",
      all(r["program"].startswith(r["program_core"]) for r in db))

# CHECK 10: gender/seat/quota domains
check("gender domain", set(r["gender"] for r in db) <= {"Gender-Neutral", "Female-only"})
check("seat_type all OPEN", all(r["seat_type"] == "OPEN" for r in db))
check("quota all AI", all(r["quota"] == "AI" for r in db))

print(f"\n=== {('ALL CHECKS PASSED' if fails==0 else str(fails)+' CHECK(S) FAILED')} ===")
sys.exit(1 if fails else 0)
