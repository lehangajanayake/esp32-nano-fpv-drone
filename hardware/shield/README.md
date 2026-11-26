# Shield PCB

The board the XIAO ESP32-S3 Sense plugs into (from below), carrying the four brushed motor drivers, the IMU, reverse polarity protection, battery sense and a status LED.

**Start here:** [docs/shield-pcb-requirements.md](docs/shield-pcb-requirements.md). It holds the outline, stackup, design rules, net classes, placement rules, the full net list and the BOM.

| File | Use |
| --- | --- |
| `docs/shield-pcb-requirements.md` | The requirements to build the schematic and layout from |
| `netlist.csv` | Every part pin and its net, for checking the schematic |
| `bom/shield-bom.csv` | JLC-format BOM (Comment, Designator, Footprint, LCSC Part #) |
| `lib/symbols/`, `lib/footprints/`, `lib/3dmodels/` | Project-local libraries (XIAO, custom pads, STEP models) |
| `production/` | Gerber, drill, BOM and CPL exports for an order (generated, not committed) |

## Creating the KiCad project

1. In KiCad, **File > New Project**, save it in this folder as `shield` (so you get `shield.kicad_pro`, `shield.kicad_sch`, `shield.kicad_pcb` here; untick "Create a new folder").
2. Add `lib/symbols/shield.kicad_sym` and `lib/footprints/shield.pretty` as **project** libraries using `${KIPRJMOD}` paths, so the project works from any clone.
3. Enter the design rules and net classes from sections 2.1 and 6.1 of the requirements in **Board Setup** before routing.
4. Check every item in section 11 of the requirements before freezing the schematic.
