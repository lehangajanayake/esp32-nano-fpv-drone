#!/usr/bin/env python3
"""Generate shield.kicad_sch (and the project symbol/footprint libraries) from
the net list in docs/shield-pcb-requirements.md, sections 4, 5 and 8.

Used once to capture the schematic; after that, edit shield.kicad_sch in KiCad
and do not re-run this (it would overwrite manual edits). The schematic has since
moved on (motor channels in a sub-sheet, D5 replaced by the J3 BAT+ wire pad).

Every pin is wired with a short wire stub and a local net label, so the sheet
stays readable and the net names are exactly those of section 5.

Usage:  python3 scripts/gen_schematic.py   (from hardware/shield/)
"""
import os
import re
import uuid as _uuid

KICAD = "/Applications/KiCad/KiCad.app/Contents/SharedSupport"
SYMDIR = os.path.join(KICAD, "symbols")
HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.dirname(HERE)
PROJECT = "shield"

_ns = _uuid.UUID("6f1c2a52-3b7e-4d11-9a0e-5f2d7c8b9e01")


def uid(*key):
    """Deterministic UUID, so re-running gives a stable diff."""
    return str(_uuid.uuid5(_ns, "/".join(str(k) for k in key)))


ROOT_UUID = uid("root")

# ---------------------------------------------------------------- library io


def extract_block(text, start):
    d = 0
    for j in range(start, len(text)):
        c = text[j]
        if c == "(":
            d += 1
        elif c == ")":
            d -= 1
            if d == 0:
                return text[start:j + 1]
    raise ValueError("unbalanced")


def lib_symbol(libfile, name):
    t = open(os.path.join(SYMDIR, libfile)).read()
    i = t.find('\n\t(symbol "%s"' % name)
    if i < 0:
        raise KeyError(name)
    return extract_block(t, i + 2)


def props(block):
    """Top-level property blocks of a symbol block (depth 2)."""
    out = []
    i = 0
    while True:
        i = block.find("(property ", i)
        if i < 0:
            break
        b = extract_block(block, i)
        out.append(b)
        i += len(b)
    return out


def flatten(libfile, name):
    """Return (body, pins) for a symbol, resolving one level of `extends`."""
    b = lib_symbol(libfile, name)
    m = re.search(r'\(extends "([^"]+)"\)', b)
    if m:
        parent = m.group(1)
        pb = lib_symbol(libfile, parent)
        child_props = props(b)
        # drop parent props, add child props
        for p in props(pb):
            pb = pb.replace(p, "", 1)
        pb = pb.replace('(symbol "%s"' % parent, '(symbol "%s"' % name, 1)
        pb = pb.replace('(symbol "%s_' % parent, '(symbol "%s_' % name)
        # insert child props after the header lines (before first sub-symbol)
        k = pb.find('(symbol "%s_' % name)
        pb = pb[:k] + "\n\t\t".join(child_props) + "\n\t\t" + pb[k:]
        b = pb
    return b


def pins_of(block):
    pins = {}
    for m in re.finditer(
        r'\(pin (\w+) (\w+)\s*\(at ([-\d.]+) ([-\d.]+) (\d+)\)\s*\(length ([\d.]+)\)'
        r'(.*?)\(number "([^"]*)"',
        block, re.S):
        typ, _, x, y, rot, _, _, num = m.groups()
        pins[num] = (float(x), float(y), int(rot), typ)
    return pins


def set_prop(block, key, value):
    return re.sub(r'\(property "%s" "[^"]*"' % re.escape(key),
                  '(property "%s" "%s"' % (key, value), block, count=1)


def rename(block, old, new):
    block = block.replace('(symbol "%s"' % old, '(symbol "%s"' % new, 1)
    return block.replace('(symbol "%s_' % old, '(symbol "%s_' % new)


# ------------------------------------------------- project library symbols

def make_project_symbols():
    dmp = rename(lib_symbol("Transistor_FET.kicad_sym", "DMP3013SFV"),
                 "DMP3013SFV", "DMP2008UFG")
    dmp = set_prop(dmp, "Value", "DMP2008UFG")
    dmp = set_prop(dmp, "Datasheet", "https://www.diodes.com/assets/Datasheets/DMP2008UFG.pdf")
    dmp = set_prop(dmp, "Description",
                   "-14A Id, -20V Vds, +/-8V Vgs, P-Channel MOSFET, PowerDI3333-8. "
                   "Pins 5-8 and the exposed pad are drain; the KiCad footprint merges them into pad 5")
    imu = rename(lib_symbol("Sensor_Motion.kicad_sym", "LSM6DS3"), "LSM6DS3", "LSM6DS3TR-C")
    imu = set_prop(imu, "Value", "LSM6DS3TR-C")
    imu = set_prop(imu, "Datasheet", "https://www.st.com/resource/en/datasheet/lsm6ds3tr-c.pdf")
    imu = set_prop(imu, "Description",
                   "iNEMO 6DoF IMU, 3D accelerometer and 3D gyroscope, SPI/I2C, LGA-14 2.5x3mm "
                   "(same pinout as LSM6DS3)")
    lib = ("(kicad_symbol_lib\n\t(version 20251024)\n\t(generator \"kicad_symbol_editor\")\n"
           "\t(generator_version \"10.0\")\n\t" + dmp + "\n\t" + imu + "\n)\n")
    os.makedirs(os.path.join(PROJ, "lib/symbols"), exist_ok=True)
    open(os.path.join(PROJ, "lib/symbols/shield.kicad_sym"), "w").write(lib)
    return {"shield:DMP2008UFG": dmp, "shield:LSM6DS3TR-C": imu}


# ------------------------------------------------------- project footprints

def fp_pads(name, descr, pad_w, pad_h, gap, hole_d, hole_dy, hole_xs, labels):
    pitch = pad_w + gap
    lines = [
        '(footprint "%s"' % name,
        '\t(version 20241229)', '\t(generator "pcbnew")', '\t(generator_version "10.0")',
        '\t(layer "F.Cu")',
        '\t(descr "%s")' % descr,
        '\t(attr smd exclude_from_pos_files exclude_from_bom)',
        '\t(property "Reference" "REF**" (at 0 %.2f 0) (layer "F.SilkS") (effects (font (size 1 1) (thickness 0.15))))' % (-pad_h / 2 - 1.2),
        '\t(property "Value" "%s" (at 0 %.2f 0) (layer "F.Fab") (effects (font (size 1 1) (thickness 0.15))))' % (name, pad_h / 2 + hole_dy + 1.5),
    ]
    for i, lab in enumerate(labels):
        x = (i - (len(labels) - 1) / 2) * pitch
        lines.append('\t(pad "%d" smd rect (at %.3f 0) (size %.2f %.2f) (layers "F.Cu" "F.Paste" "F.Mask"))'
                     % (i + 1, x, pad_w, pad_h))
        lines.append('\t(fp_text user "%s" (at %.3f %.2f 0) (layer "F.SilkS") (effects (font (size 0.8 0.8) (thickness 0.15))))'
                     % (lab, x, -pad_h / 2 - 1.2 + 0.0 if False else -pad_h / 2 - 0.6 - 0.4))
    for hx in hole_xs:
        lines.append('\t(pad "" np_thru_hole circle (at %.3f %.2f) (size %.2f %.2f) (drill %.2f) (layers "*.Cu" "*.Mask"))'
                     % (hx * pitch, hole_dy, hole_d, hole_d, hole_d))
    w = len(labels) * pitch / 2 + 0.5
    lines.append('\t(fp_rect (start %.2f %.2f) (end %.2f %.2f) (stroke (width 0.05) (type solid)) (fill no) (layer "F.CrtYd"))'
                 % (-w, -pad_h / 2 - 0.5, w, hole_dy + hole_d / 2 + 0.5))
    lines.append(')')
    return "\n".join(lines) + "\n"


def make_footprints():
    d = os.path.join(PROJ, "lib/footprints/shield.pretty")
    os.makedirs(d, exist_ok=True)
    open(os.path.join(d, "BAT_Pads_3x4mm.kicad_mod"), "w").write(fp_pads(
        "BAT_Pads_3x4mm",
        "1S battery pigtail pads, 3.0x4.0 mm, 3 mm gap, 2x 1.5 mm strain-relief holes 3 mm forward (SH 4.1)",
        3.0, 4.0, 3.0, 1.5, -(2.0 + 3.0), [-0.5, 0.5], ["+", "-"]))
    open(os.path.join(d, "Motor_Pads_2x3mm.kicad_mod"), "w").write(fp_pads(
        "Motor_Pads_2x3mm",
        "Brushed motor lead pads, 2.0x3.0 mm, 2.5 mm gap, 1x 1.2 mm strain-relief hole (SH 4.2)",
        2.0, 3.0, 2.5, 1.2, -(1.5 + 1.6), [0.0], ["+", "-"]))


# ------------------------------------------------------------------ the parts

R0402 = "Resistor_SMD:R_0402_1005Metric"
C0402 = "Capacitor_SMD:C_0402_1005Metric"
C0603 = "Capacitor_SMD:C_0603_1608Metric"
C0805 = "Capacitor_SMD:C_0805_2012Metric"

LIBS = {
    "Device:R": ("Device.kicad_sym", "R"),
    "Device:C": ("Device.kicad_sym", "C"),
    "Device:LED": ("Device.kicad_sym", "LED"),
    "Device:D_Schottky": ("Device.kicad_sym", "D_Schottky"),
    "Device:NetTie_2": ("Device.kicad_sym", "NetTie_2"),
    "Transistor_FET:AO3400A": ("Transistor_FET.kicad_sym", "AO3400A"),
    "Regulator_Linear:ME6211C33M5": ("Regulator_Linear.kicad_sym", "ME6211C33M5"),
    "Connector_Generic:Conn_01x07": ("Connector_Generic.kicad_sym", "Conn_01x07"),
    "Connector_Generic:Conn_01x02": ("Connector_Generic.kicad_sym", "Conn_01x02"),
    "Connector:TestPoint": ("Connector.kicad_sym", "TestPoint"),
    "Mechanical:MountingHole": ("Mechanical.kicad_sym", "MountingHole"),
    "power:PWR_FLAG": ("power.kicad_sym", "PWR_FLAG"),
}

parts = []  # dicts


def part(ref, lib, value, fp, pos, nets, lcsc=None, assembled=True, nc=(), rot=0):
    parts.append(dict(ref=ref, lib=lib, value=value, fp=fp, pos=pos, nets=nets,
                      lcsc=lcsc, assembled=assembled, nc=set(nc), rot=rot))


def R(ref, value, lcsc, pos, n1, n2):
    part(ref, "Device:R", value, R0402, pos, {"1": n1, "2": n2}, lcsc)


def C(ref, value, fp, lcsc, pos, n1, n2):
    part(ref, "Device:C", value, fp, pos, {"1": n1, "2": n2}, lcsc)


texts = []  # (text, x, y, size)
BLOCKS = []  # (title, x1, y1, x2, y2)

# 1. Battery input and reverse polarity protection ------------------------
BLOCKS.append(("Battery input and reverse polarity protection\n"
               "SH 4.1 / XD-S13, S14, S19, S20. 1S only (Q5 Vgs max +/-8 V). "
               "PGND and GND join only at NT1 (D6, XD-S17)", 15, 20, 135, 105))
part("BAT1", "Connector_Generic:Conn_01x02", "BAT 1S", "shield:BAT_Pads_3x4mm", (27.94, 50.8),
     {"1": "BAT_IN", "2": "PGND"}, assembled=False)
part("Q5", "shield:DMP2008UFG", "DMP2008UFG-7", "Package_SON:Diodes_PowerDI3333-8", (63.5, 50.8),
     {"1": "VBAT_P", "2": "VBAT_P", "3": "VBAT_P", "4": "Q5_G", "5": "BAT_IN"}, "C461052", rot=90)
R("R12", "10k 1%", "C25744", (63.5, 78.74), "Q5_G", "PGND")
C("C8", "22uF 25V X5R", C0805, "C45783", (88.9, 50.8), "VBAT_P", "PGND")
C("C9", "22uF 25V X5R", C0805, "C45783", (111.76, 50.8), "VBAT_P", "PGND")
part("NT1", "Device:NetTie_2", "NetTie_2", "NetTie:NetTie-2_SMD_Pad2.0mm", (33.02, 86.36),
     {"1": "PGND", "2": "GND"}, assembled=False)
part("#FLG01", "power:PWR_FLAG", "PWR_FLAG", "", (91.44, 86.36), {"1": "VBAT_P"}, assembled=False)
part("#FLG02", "power:PWR_FLAG", "PWR_FLAG", "", (104.14, 86.36), {"1": "PGND"}, assembled=False)
part("#FLG03", "power:PWR_FLAG", "PWR_FLAG", "", (116.84, 86.36), {"1": "GND"}, assembled=False)

# 2. Motor drivers x4 -------------------------------------------------------
BLOCKS.append(("Motor drivers x4\nSH 4.2 / XD-S6 to S10. Rn gate 100R, R(n+4) 100k pull-down at the gate, "
               "Dn flyback beside the motor pads. M1 RR CW, M2 FR CCW, M3 RL CCW, M4 FL CW (6.4)",
               145, 20, 405, 120))
for n in range(1, 5):
    x0 = 152.4 + (n - 1) * 63.5
    R("R%d" % n, "100R 1%", "C25076", (x0 + 2.54, 78.74), "PWM%d" % n, "GATE%d" % n)
    R("R%d" % (n + 4), "100k 1%", "C25741", (x0 + 15.24, 96.52), "GATE%d" % n, "PGND")
    part("Q%d" % n, "Transistor_FET:AO3400A", "AO3400A", "Package_TO_SOT_SMD:SOT-23",
         (x0 + 27.94, 81.28), {"1": "GATE%d" % n, "2": "PGND", "3": "MOT%d_N" % n}, "C20917")
    part("D%d" % n, "Device:D_Schottky", "SS34", "Diode_SMD:D_SMA", (x0 + 30.48, 50.8),
         {"1": "VBAT_P", "2": "MOT%d_N" % n}, "C8678", rot=270)
    part("MOT%d" % n, "Connector_Generic:Conn_01x02", "MOTOR M%d" % n, "shield:Motor_Pads_2x3mm",
         (x0 + 55.88, 50.8), {"1": "VBAT_P", "2": "MOT%d_N" % n}, assembled=False)
C("C10", "22uF 25V X5R", C0805, "C45783", (152.4 + 3 * 63.5 + 2.54, 40.64), "VBAT_P", "PGND")
C("C11", "22uF 25V X5R", C0805, "C45783", (152.4 + 1 * 63.5 + 2.54, 40.64), "VBAT_P", "PGND")
texts.append(("C10 at the M4 (front left) driver,\nC11 at the M2 (front right) driver", 152.4 + 2.54, 30.0))

# 3. XIAO sockets -----------------------------------------------------------
BLOCKS.append(("XIAO ESP32-S3 Sense sockets (hand-soldered, not assembled)\n"
               "SH 5.1 / XD-S1. J1 = XIAO pins 1-7, J2 = XIAO pins 14 down to 8 (pin 1 of both at the rear)",
               15, 125, 135, 200))
part("J1", "Connector_Generic:Conn_01x07", "XIAO 1-7 (D0-D6)",
     "Connector_PinSocket_2.54mm:PinSocket_1x07_P2.54mm_Vertical", (45.72, 162.56),
     {"1": "PWM1", "2": "PWM2", "3": "PWM3", "4": "PWM4", "5": "VBAT_SENSE", "6": "IMU_INT1",
      "7": "IMU_CS"}, assembled=False)
part("J2", "Connector_Generic:Conn_01x07", "XIAO 14-8 (5V,GND,3V3,D10-D7)",
     "Connector_PinSocket_2.54mm:PinSocket_1x07_P2.54mm_Vertical", (101.6, 162.56),
     {"1": "XIAO_5V", "2": "GND", "4": "SPI_MOSI", "5": "SPI_MISO", "6": "SPI_SCK",
      "7": "LED_STAT"}, assembled=False, nc=["3"])
texts.append(("J1: 1 D0/GPIO1  2 D1/GPIO2  3 D2/GPIO3  4 D3/GPIO4\n"
              "    5 D4/GPIO5 (ADC)  6 D5/GPIO6  7 D6/GPIO43", 20.32, 185.0))
texts.append(("J2: 1 5V(pin14)  2 GND(13)  3 3V3(12) NC, never tied to +3V3_IMU\n"
              "    4 D10/GPIO9  5 D9/GPIO8  6 D8/GPIO7  7 D7/GPIO44", 20.32, 193.0))

# 4. XIAO power ---------------------------------------------------------------
BLOCKS.append(("XIAO power\nSH 4.3, D1 / XD-S15. Battery feeds XIAO 5V through D5; "
               "USB 5V cannot back-feed VBAT_P", 145, 125, 255, 200))
part("D5", "Device:D_Schottky", "SS34", "Diode_SMD:D_SMA", (172.72, 152.4),
     {"1": "XIAO_5V", "2": "VBAT_P"}, "C8678")
C("C12", "22uF 25V X5R", C0805, "C45783", (203.2, 162.56), "XIAO_5V", "GND")
C("C4", "100nF 16V X7R", C0402, "C1525", (220.98, 162.56), "XIAO_5V", "GND")

# 5. IMU + LDO ----------------------------------------------------------------
BLOCKS.append(("IMU and its LDO\nSH 4.4 / XD-S11, S12, S18, S22. 4-wire SPI. C1/C2 within 1 mm of "
               "VDD/VDDIO. R11 holds CS high during XIAO boot", 15, 205, 255, 285))
part("U2", "Regulator_Linear:ME6211C33M5", "ME6211C33M5G-N", "Package_TO_SOT_SMD:SOT-23-5",
     (53.34, 241.3), {"1": "VBAT_P", "2": "GND", "3": "VBAT_P", "5": "+3V3_IMU"}, "C82942")
C("C6", "10uF 10V X5R", C0603, "C19702", (25.4, 254.0), "VBAT_P", "GND")
C("C5", "100nF 16V X7R", C0402, "C1525", (33.02, 266.7), "VBAT_P", "GND")
C("C7", "10uF 10V X5R", C0603, "C19702", (81.28, 254.0), "+3V3_IMU", "GND")
part("U1", "shield:LSM6DS3TR-C", "LSM6DS3TR-C", "Package_LGA:LGA-14_3x2.5mm_P0.5mm_LayoutBorder3x4y",
     (157.48, 246.38),
     {"1": "SPI_MISO", "2": "GND", "3": "GND", "4": "IMU_INT1", "5": "+3V3_IMU", "6": "GND",
      "7": "GND", "8": "+3V3_IMU", "12": "IMU_CS", "13": "SPI_SCK", "14": "SPI_MOSI"},
     "C967633", nc=["9", "10", "11"])
C("C1", "100nF 16V X7R", C0402, "C1525", (198.12, 236.22), "+3V3_IMU", "GND")
C("C2", "100nF 16V X7R", C0402, "C1525", (223.52, 236.22), "+3V3_IMU", "GND")
R("R11", "10k 1%", "C25744", (106.68, 241.3), "+3V3_IMU", "IMU_CS")
texts.append(("C1 at U1 pin 8 (VDD), C2 at U1 pin 5 (VDDIO)", 190.5, 215.9))

# 6. Battery sense ------------------------------------------------------------
BLOCKS.append(("Battery sense\nSH 4.5 / XD-S16. VBAT/2 to XIAO D4", 265, 125, 330, 200))
R("R9", "100k 1%", "C25741", (281.94, 147.32), "VBAT_P", "VBAT_SENSE")
R("R10", "100k 1%", "C25741", (281.94, 190.5), "VBAT_SENSE", "GND")
C("C3", "100nF 16V X7R", C0402, "C1525", (309.88, 190.5), "VBAT_SENSE", "GND")

# 7. Status LED -----------------------------------------------------------------
BLOCKS.append(("Status LED\nSH 4.6 / XD-S25. Active high from D7", 340, 125, 405, 200))
R("R13", "1k 1%", "C11702", (360.68, 152.4), "LED_STAT", "LED_A")
part("LED1", "Device:LED", "Green", "LED_SMD:LED_0603_1608Metric", (360.68, 180.34),
     {"1": "GND", "2": "LED_A"}, "C72043", rot=90)

# 8. Test points and mounting holes -------------------------------------------
BLOCKS.append(("Test points and mounting holes\nSH 4.7, SH-O5. 1.0 mm top pads; 4x M2 NPTH",
               265, 205, 405, 285))
for i, net in enumerate(["VBAT_P", "+3V3_IMU", "GND", "XIAO_5V", "IMU_INT1"]):
    part("TP%d" % (i + 1), "Connector:TestPoint", "TP_" + net.replace("+", ""),
         "TestPoint:TestPoint_Pad_D1.0mm", (280.67 + i * 25.4, 228.6), {"1": net}, assembled=False)
for i in range(4):
    part("H%d" % (i + 1), "Mechanical:MountingHole", "M2", "MountingHole:MountingHole_2.2mm_M2",
         (283.21 + i * 25.4, 246.38), {}, assembled=False)


# Reference/Value text offsets (dx, dy_ref, dy_val) where the default overlaps
TEXT_POS = {"Q5": (-5.08, -8.89, -6.35), "U2": (-5.08, -8.89, -6.35), "D5": (-2.54, -5.08, 3.81),
            "J1": (-2.54, 11.43, 13.97), "J2": (-2.54, 11.43, 13.97), "LED1": (5.08, -1.27, 1.27)}
for n in range(1, 5):
    TEXT_POS["Q%d" % n] = (6.35, -1.27, 1.27)
    TEXT_POS["D%d" % n] = (-10.16, -1.27, 1.27)
    TEXT_POS["MOT%d" % n] = (5.08, -1.27, 1.27)
TEXT_POS["BAT1"] = (5.08, -1.27, 1.27)


# ------------------------------------------------------------------- writing

def snap(v):
    return round(v / 1.27) * 1.27


def rot_vec(x, y, rot):
    # symbol rotation (counter-clockwise in lib coords, Y up)
    if rot == 0:
        return x, y
    if rot == 90:
        return -y, x
    if rot == 180:
        return -x, -y
    if rot == 270:
        return y, -x
    raise ValueError(rot)


DIRS = {0: (1, 0), 90: (0, 1), 180: (-1, 0), 270: (0, -1)}


def fmt(v):
    s = ("%.4f" % v).rstrip("0").rstrip(".")
    return "0" if s in ("-0", "") else s


def font(size=1.27):
    return "(effects (font (size %s %s)))" % (fmt(size), fmt(size))


def prop(key, val, x, y, hide=False, ang=0):
    return ('\t\t(property "%s" "%s"\n\t\t\t(at %s %s %d)\n%s\t\t\t(show_name no)\n'
            '\t\t\t(do_not_autoplace no)\n\t\t\t(effects (font (size 1.27 1.27))%s)\n\t\t)\n'
            % (key, val, fmt(x), fmt(y), ang, "\t\t\t(hide yes)\n" if hide else "",
               "" if True else ""))


def main():
    proj_syms = make_project_symbols()
    make_footprints()

    lib_bodies = {}
    pin_tables = {}
    for p in parts:
        lid = p["lib"]
        if lid in lib_bodies:
            continue
        if lid in proj_syms:
            body = proj_syms[lid]
            name = lid.split(":")[1]
        else:
            f, name = LIBS[lid]
            body = flatten(f, name)
        pin_tables[lid] = pins_of(body)
        body = body.replace('(symbol "%s"' % name, '(symbol "%s"' % lid, 1)
        lib_bodies[lid] = body

    out = []
    out.append('(kicad_sch\n\t(version 20260101)\n\t(generator "eeschema")\n\t(generator_version "10.0")\n'
               '\t(uuid "%s")\n\t(paper "A3")\n' % ROOT_UUID)
    out.append('\t(title_block\n\t\t(title "XIAO FPV shield")\n\t\t(date "2026-11-26")\n\t\t(rev "0.1")\n'
               '\t\t(comment 1 "Source of truth: docs/shield-pcb-requirements.md")\n'
               '\t\t(comment 2 "Nets wired by label; names as in requirements section 5")\n\t)\n')
    out.append("\t(lib_symbols\n")
    for lid, body in lib_bodies.items():
        out.append("\t\t" + body.replace("\n", "\n\t") + "\n")
    out.append("\t)\n")

    used_pts = {}  # point -> net, to catch collisions
    netmap = {}    # (ref,pin) -> net, for self-check
    for p in parts:
        lid = p["lib"]
        px, py = p["pos"]
        ref = p["ref"]
        is_flag = ref.startswith("#")
        pins = pin_tables[lid]
        su = uid("sym", ref)
        in_bom = "yes" if p["assembled"] else "no"
        out.append('\t(symbol\n\t\t(lib_id "%s")\n\t\t(at %s %s %d)\n\t\t(unit 1)\n\t\t(body_style 1)\n'
                   '\t\t(exclude_from_sim no)\n\t\t(in_bom %s)\n\t\t(on_board %s)\n'
                   '\t\t(in_pos_files %s)\n\t\t(dnp no)\n\t\t(uuid "%s")\n'
                   % (lid, fmt(px), fmt(py), p["rot"], "no" if is_flag else in_bom,
                      "no" if is_flag else "yes", "no" if is_flag else in_bom, su))
        # property placement: to the right of the body
        tdx, tdr, tdv = TEXT_POS.get(ref, (3.81, -1.27, 1.27))
        out.append(prop("Reference", ref, px + tdx, py + tdr, hide=is_flag, ang=p["rot"] % 180))
        out.append(prop("Value", p["value"], px + tdx, py + tdv, hide=is_flag, ang=p["rot"] % 180))
        out.append(prop("Footprint", p["fp"], px, py, hide=True))
        out.append(prop("Datasheet", "", px, py, hide=True))
        out.append(prop("Description", "", px, py, hide=True))
        if p["lcsc"]:
            out.append(prop("LCSC", p["lcsc"], px, py, hide=True))
        for num in pins:
            out.append('\t\t(pin "%s"\n\t\t\t(uuid "%s")\n\t\t)\n' % (num, uid("pin", ref, num)))
        out.append('\t\t(instances\n\t\t\t(project "%s"\n\t\t\t\t(path "/%s"\n\t\t\t\t\t(reference "%s")\n'
                   '\t\t\t\t\t(unit 1)\n\t\t\t\t)\n\t\t\t)\n\t\t)\n\t)\n' % (PROJECT, ROOT_UUID, ref))

        # wiring
        done = {}
        for num, (lx, ly, lrot, typ) in pins.items():
            net = p["nets"].get(num)
            rx, ry = rot_vec(lx, ly, p["rot"])
            ax, ay = px + rx, py - ry  # schematic Y is down
            key = (round(ax, 3), round(ay, 3))
            if num in p["nc"]:
                out.append('\t(no_connect\n\t\t(at %s %s)\n\t\t(uuid "%s")\n\t)\n'
                           % (fmt(ax), fmt(ay), uid("nc", ref, num)))
                continue
            if net is None:
                if typ != "no_connect":
                    raise SystemExit("unassigned pin %s.%s" % (ref, num))
                continue
            netmap[(ref, num)] = net
            if key in done:
                if done[key] != net:
                    raise SystemExit("stacked pins with different nets at %s.%s" % (ref, num))
                continue
            done[key] = net
            # outward direction = opposite to the pin's direction, after rotation
            dx, dy = DIRS[(lrot + p["rot"]) % 360]
            ox, oy = -dx, dy  # lib -> sch flips Y; outward = -dir
            L = 2.54
            ex, ey = ax + ox * L, ay + oy * L
            ekey = (round(ex, 3), round(ey, 3))
            if ekey in used_pts and used_pts[ekey] != net:
                raise SystemExit("label collision at %s for %s.%s" % (ekey, ref, num))
            used_pts[ekey] = net
            out.append('\t(wire\n\t\t(pts\n\t\t\t(xy %s %s) (xy %s %s)\n\t\t)\n'
                       '\t\t(stroke\n\t\t\t(width 0)\n\t\t\t(type default)\n\t\t)\n\t\t(uuid "%s")\n\t)\n'
                       % (fmt(ax), fmt(ay), fmt(ex), fmt(ey), uid("w", ref, num)))
            ang, just = {(1, 0): (0, "left"), (-1, 0): (180, "right"),
                         (0, -1): (90, "left"), (0, 1): (270, "right")}[(ox, oy)]
            out.append('\t(label "%s"\n\t\t(at %s %s %d)\n\t\t(effects\n\t\t\t(font\n\t\t\t\t(size 1.27 1.27)\n'
                       '\t\t\t)\n\t\t\t(justify %s bottom)\n\t\t)\n\t\t(uuid "%s")\n\t)\n'
                       % (net, fmt(ex), fmt(ey), ang, just, uid("l", ref, num)))

    for title, x1, y1, x2, y2 in BLOCKS:
        out.append('\t(rectangle\n\t\t(start %s %s)\n\t\t(end %s %s)\n\t\t(stroke\n\t\t\t(width 0.2)\n'
                   '\t\t\t(type dash)\n\t\t)\n\t\t(fill\n\t\t\t(type none)\n\t\t)\n\t\t(uuid "%s")\n\t)\n'
                   % (x1, y1, x2, y2, uid("rect", title)))
        out.append('\t(text "%s"\n\t\t(exclude_from_sim no)\n\t\t(at %s %s 0)\n\t\t(effects\n\t\t\t(font\n'
                   '\t\t\t\t(size 1.27 1.27)\n\t\t\t)\n\t\t\t(justify left top)\n\t\t)\n\t\t(uuid "%s")\n\t)\n'
                   % (title.replace('"', "'").replace("\n", "\\n"), x1 + 1.27, y1 + 1.27, uid("t", title)))
    for t, x, y in texts:
        out.append('\t(text "%s"\n\t\t(exclude_from_sim no)\n\t\t(at %s %s 0)\n\t\t(effects\n\t\t\t(font\n'
                   '\t\t\t\t(size 1.27 1.27)\n\t\t\t)\n\t\t\t(justify left top)\n\t\t)\n\t\t(uuid "%s")\n\t)\n'
                   % (t.replace("\n", "\\n"), fmt(x), fmt(y), uid("tx", t)))

    out.append('\t(sheet_instances\n\t\t(path "/"\n\t\t\t(page "1")\n\t\t)\n\t)\n\t(embedded_fonts no)\n)\n')
    open(os.path.join(PROJ, "shield.kicad_sch"), "w").write("".join(out))
    print("wrote shield.kicad_sch: %d symbols, %d pin-net assignments" % (len(parts), len(netmap)))


if __name__ == "__main__":
    main()
