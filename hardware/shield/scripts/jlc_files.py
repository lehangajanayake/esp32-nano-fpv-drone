"""Turn KiCad's BOM and position exports into JLCPCB's BOM/CPL formats.

Usage (from hardware/shield):
  python3 scripts/jlc_files.py production
Reads production/bom-raw.csv and production/pos-raw.csv (exported by the KiCad MCP or
kicad-cli), writes production/shield-bom-jlc.csv and production/shield-cpl-jlc.csv.
JLC's 0 degrees differs from KiCad's for some packages; ROTATION_FIX adds the offset
(SOT-23 is 180 out, PowerDI3333 270, seen in JLC's preview 2026-11-28). Still check every
part's orientation in JLC's placement preview.
"""
import csv
import re
import sys
from pathlib import Path

HAND_SOLDERED = {"J1", "J2"}  # XIAO sockets, fitted by hand
ROTATION_FIX = {"Q1": 180, "Q2": 180, "Q3": 180, "Q4": 180, "U2": 180, "Q5": 270}


def expand(designators):
    """'C1-C5,C7' -> ['C1', 'C2', 'C3', 'C4', 'C5', 'C7'] (JLC wants every ref listed)."""
    refs = []
    for part in designators.split(","):
        m = re.fullmatch(r"([A-Z]+)(\d+)-[A-Z]*(\d+)", part)
        if m:
            refs += [f"{m[1]}{i}" for i in range(int(m[2]), int(m[3]) + 1)]
        else:
            refs.append(part)
    return refs


def main(out):
    out = Path(out)
    with open(out / "bom-raw.csv", newline="") as f:
        bom = list(csv.DictReader(f))
    with open(out / "shield-bom-jlc.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["Comment", "Designator", "Footprint", "LCSC Part #"])
        for r in bom:
            w.writerow([r["Comment"], ",".join(expand(r["Designator"])), r["Footprint"].split(":")[-1],
                        r["LCSC Part #"]])
    bom_refs = set()
    for r in bom:
        bom_refs.update(expand(r["Designator"]))

    with open(out / "pos-raw.csv", newline="") as f:
        pos = [r for r in csv.DictReader(f) if r["Ref"] not in HAND_SOLDERED]
    missing = bom_refs - {r["Ref"] for r in pos}
    assert not missing, f"in BOM but not placed: {missing}"
    with open(out / "shield-cpl-jlc.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["Designator", "Mid X", "Mid Y", "Layer", "Rotation"])
        for r in pos:
            assert r["Ref"] in bom_refs, f"placed but not in BOM: {r['Ref']}"
            w.writerow([r["Ref"], f"{float(r['PosX']):.3f}mm", f"{float(r['PosY']):.3f}mm",
                        r["Side"].capitalize(), f"{(float(r['Rot']) + ROTATION_FIX.get(r['Ref'], 0)) % 360:g}"])
    print(f"{len(bom)} BOM lines, {len(pos)} placements")


if __name__ == "__main__":
    main(sys.argv[1])
