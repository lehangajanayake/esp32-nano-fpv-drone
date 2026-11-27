# Building the shield schematic with the KiCad MCP

A brief for a local Claude session with the KiCad MCP connected, working in a clone of this repo. The source of truth is [shield-pcb-requirements.md](shield-pcb-requirements.md); this file only says the order of work and what to export.

## 1. Project

1. Create the KiCad project `shield` in `hardware/shield/` (files `shield.kicad_pro`, `shield.kicad_sch`, `shield.kicad_pcb`).
2. Use KiCad's standard libraries where a symbol and footprint exist. Put anything missing (XIAO ESP32-S3, LSM6DS3TR-C if absent, battery and motor pad footprints, net tie) in `lib/symbols/shield.kicad_sym` and `lib/footprints/shield.pretty`, added as project libraries with `${KIPRJMOD}` paths.

## 2. Schematic

1. Place every part in section 8.1 and the non-assembled parts in section 8.2, with the reference designators exactly as in the requirements (U1, U2, Q1 to Q5, D1 to D4, R1 to R14, C1 to C12, LED1, J1, J2, J3, BAT1, MOT1 to MOT4, NT1, TP1 to TP5).
2. Wire them with **net labels named exactly as in section 5** (`VBAT_P`, `PGND`, `GND`, `MOT1_N`, `SPI_SCK`, and so on), following sections 4.1 to 4.7 and the socket table in 5.1. Use labels rather than long wires so the sheet stays readable.
3. Lay the sheet out in the blocks of section 7: battery input and protection, motor drivers x 4, XIAO sockets, XIAO power, IMU + LDO, battery sense, status LED, test points and holes. Add a text note per block naming its `SH-`/`XD-` requirement.
4. Fill a `LCSC` field on every assembled part from section 8.1. Mark J1, J2, BAT1, MOT1 to MOT4, NT1, TP1 to TP5 as excluded from BOM and position files.
5. Put no-connect flags on XIAO pin 12 (3V3) and U1 pins 9, 10, 11.
6. Run ERC and fix everything, or note why a warning is accepted.

## 3. Exports for review (commit these)

Run from `hardware/shield/`:

```sh
kicad-cli sch export pdf     -o exports/shield-schematic.pdf      shield.kicad_sch
kicad-cli sch export netlist --format kicadxml -o exports/shield.net.xml shield.kicad_sch
kicad-cli sch export bom     -o exports/shield-bom.csv            shield.kicad_sch
kicad-cli sch erc            -o exports/shield-erc.rpt            shield.kicad_sch
```

Then write `exports/shield-netlist.md`: a readable table made from the exported net list, one row per net, listing each `ref.pin (pin name)` on it, sorted as in section 5. That is the version to read through.

## 4. Check against the requirements

Compare `exports/shield-netlist.md` with section 5 net by net and list every difference (missing pin, extra pin, renamed net). Fix the schematic, not the table, unless the requirement itself is wrong; in that case, update the requirements doc in the same commit and say why.

## 5. Then the PCB

Only after the net list has been reviewed: board outline, design rules and net classes (sections 2.1, 3.2, 6.1), placement (6.3), routing, DRC, and the 1:1 paper check in SH-O10.
