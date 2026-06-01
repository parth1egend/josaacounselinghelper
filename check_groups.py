#!/usr/bin/env python3
"""Stage 3a: verify the course-group chip keywords cover every program, and
report exactly which programs each group catches. Iterate until coverage==100%."""
import csv, os
from groups import CHIPS

HERE = os.path.dirname(os.path.abspath(__file__))
CSV = os.path.join(HERE, "josaa_iit_2025_r6.csv")

progs = sorted({r["program"] for r in csv.DictReader(open(CSV, encoding="utf-8"))})

def matches(prog, kws):
    p = prog.lower()
    return any(k in p for k in kws)

covered = set()
print("=== programs caught per group ===")
for label, kws in CHIPS:
    hits = [p for p in progs if matches(p, kws)]
    covered.update(hits)
    print(f"\n## {label}  ({len(hits)})")
    for p in hits:
        print("   -", p)

uncovered = [p for p in progs if p not in covered]
print("\n=== COVERAGE ===")
print(f"total distinct programs: {len(progs)}")
print(f"covered by >=1 group:    {len(covered)}")
print(f"UNCOVERED ({len(uncovered)}):")
for p in uncovered:
    print("   !!", p)

# specifically: AI / Data Science group must catch everything containing ai-ish words
ai_words = ["artificial", "data science", "data analytics", " ai", "(ai"]
ai_expected = {p for p in progs if any(w in p.lower() for w in ai_words)}
ai_group = next(kws for l, kws in CHIPS if l.startswith("AI"))
ai_got = {p for p in progs if matches(p, ai_group)}
print("\n=== AI/Data Science completeness ===")
print("expected (any AI/data word):", len(ai_expected))
print("caught by chip:            ", len(ai_got & ai_expected))
miss = ai_expected - ai_got
print("AI-related MISSED by chip:", len(miss))
for p in sorted(miss):
    print("   MISS:", p)
