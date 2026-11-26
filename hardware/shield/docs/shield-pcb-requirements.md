# Shield PCB: Requirements for Schematic and Layout

Nov 26, 2026 · @Lehan · Status: **draft, ready for schematic capture**

This document turns the system spec ([docs/requirements-budget-bom.md](../../../docs/requirements-budget-bom.md), IDs `XD-`) into rules detailed enough to draw the shield in KiCad. Requirement IDs here use the prefix **SH-** and name the `XD-` requirement they come from.

The shield is a small 2-layer board. A Seeed XIAO ESP32-S3 Sense hangs **underneath** it in two female headers. The top side carries every SMD part: four brushed motor drivers, the IMU, its LDO, reverse polarity protection, bulk capacitors, the battery divider and a status LED. Motors and the battery pigtail solder to pads.

**Cheapest possible is a hard goal.** Every choice below is made to stay inside JLCPCB's cheapest options: 2 layers, standard specs, minimum quantity, one assembled side, Economic PCBA, and basic library parts wherever a basic part can do the job (each distinct extended part adds a setup fee per order).

Section 11 lists what you must still check before the schematic is frozen. Items marked **[VERIFY]** in the text are on that list.

---

## 1. Decisions this document makes

These fill gaps the system spec left open, or change it for cost. Each is easy to reverse before layout starts.

| # | Decision | Why |
| --- | --- | --- |
| D1 | **XIAO power (XD-S15):** VBAT\_P feeds the XIAO's **BAT+ pad** through a short wire to shield pad **J3**. The XIAO's 5V pin is not powered by the shield (it only goes to TP4). | Seeed's v1.51 schematic shows the 5V pin (VBUS) reaches the XIAO's SGM6029 buck through an internal Schottky (D2, LMBR4010), while BAT+ reaches it through a P-FET (Q1, LP0404N3T5G, gate held by VBUS). The original plan (an SS34 into the 5V pin) put two diode drops in series, about 0.75 V, so the ESP32 fell below its 3.0 V minimum once the battery sagged under about 3.8 V. Through BAT+ the drop is about 0.05 V and the SGM6029 (1.95 to 5.5 V in, 100% duty cycle) passes the battery straight through, so the XIAO holds about 3.3 V down to a 3.4 V battery and stays near 2.9 V at a 3.1 V punch (test B7). Trade-off: with USB plugged in, the XIAO's SGM40567 charger charges the drone battery at 4.2 V, about 110 mA (test B4 changed to match). Decided 2026-11-27. |
| D2 | **IMU LDO:** use **XC6206P332MR** (JLC basic, C5446) instead of ME6211C33 **if** ME6211 shows as an extended part on order day. | The IMU draws under 1 mA, so the XC6206's higher dropout costs nothing here, and a basic part avoids one setup fee. The footprints differ (SOT-23 vs SOT-23-5), so choose before layout. |
| D3 | **Female headers (J1, J2) are hand-soldered by you**, not assembled by JLC. | Through-hole assembly at JLC adds a fee and a second process. 14 joints take five minutes. JLC then assembles SMD on the top side only. |
| D4 | **Board 32 x 32 mm, 1.0 mm thick**, 4 x M2 mounting holes on a 26 x 26 mm square. | Leaves room for the corner motor drivers and keeps the board under about 2 g bare. JLC charges the same for 0.8 to 1.6 mm on 2-layer boards **[VERIFY in the quote]**. |
| D5 | **XIAO orientation: back side (Sense board side) faces the shield**, USB-C pointing to the rear. | The Sense expansion board then sits in the gap under the shield, the U.FL and USB-C face down and out, and the USB-C can be reached from the rear (XD-S5). This depends on which side the XIAO's male pins come out of **[VERIFY, see 3.3]**. |
| D6 | **Two grounds joined at one point:** PGND (motor and battery current) and GND (XIAO, IMU, LDO, divider), joined by a net tie at the battery negative pad. | Implements XD-S17's single ground join in a way KiCad can check. |
| D7 | Motor numbering and spin directions follow the Betaflight "props in" layout (table in 6.4). | A common convention; firmware can remap if ESP-Drone expects another order. |

---

## 2. Manufacturing target (JLCPCB, cheapest tier)

| ID | Requirement | Value | From |
| --- | --- | --- | --- |
| SH-M1 | Layers | 2 | cost |
| SH-M2 | Material, thickness | FR-4, 1.0 mm (1.6 mm acceptable if 1.0 costs more) | D4 |
| SH-M3 | Copper | 1 oz (35 µm) outer, both layers. **No 2 oz** (extra cost) | cost |
| SH-M4 | Surface finish | HASL (with lead). ENIG costs extra; only switch if JLC flags the IMU's 0.5 mm-pitch LGA | cost |
| SH-M5 | Solder mask / silkscreen | Green / white | cost |
| SH-M6 | Quantity | 5 boards (JLC minimum), 5 assembled (or 2, Economic PCBA allows assembling fewer than ordered) | XD BOM 7.2 |
| SH-M7 | Assembly | **Economic PCBA, top side only, SMD only.** No parts on the bottom except the hand-soldered through-hole headers | cost |
| SH-M8 | Order-number text | Add a silkscreen text `JLCJLCJLCJLC` on the top side in a free 8 x 1.5 mm spot, so JLC prints its order number there for free instead of in a random place | cost |
| SH-M9 | Parts | Basic library parts wherever possible. Unavoidable extended parts: IMU (LSM6DS3TR-C), protection MOSFET (DMP2008UFG). Possibly the LDO and LED (see D2, section 10) | cost |
| SH-M10 | Panel / rails | None. Single board. If JLC asks for edge rails because parts are close to the edge, add them in the order form (small fee) rather than redesigning | cost |

### 2.1 Design rules (enter these in KiCad Board Setup)

These sit just inside JLC's standard 2-layer capabilities, so nothing triggers an extra charge.

| Rule | Value used | JLC standard minimum |
| --- | --- | --- |
| Min track width | 0.15 mm | 0.127 mm |
| Min clearance | 0.15 mm | 0.127 mm |
| Signal via | 0.3 mm drill / 0.6 mm pad | 0.3 mm drill / 0.5 mm pad |
| Power via | 0.4 mm drill / 0.8 mm pad | same tier |
| Min annular ring | 0.15 mm | 0.13 mm |
| Copper to board edge | 0.4 mm | 0.3 mm |
| Min through-hole drill | 0.3 mm | 0.3 mm (smaller costs extra) |
| Silkscreen line width / text height | 0.15 mm / 1.0 mm | 0.153 mm / 0.8 mm |
| Solder mask expansion | 0.05 mm (KiCad default is fine) | — |
| Board outline | `Edge.Cuts`, 0.1 mm line, corners rounded r = 1 mm | — |

**[VERIFY]** JLC's capability page on the day; the numbers above are the long-standing standard tier.

---

## 3. Mechanical: outline, XIAO footprint and stack

### 3.1 The XIAO ESP32-S3 Sense, as it matters to the shield

| Property | Value | Source / status |
| --- | --- | --- |
| Board outline | 21.0 x 17.8 mm | Seeed wiki |
| Height with Sense expansion board | 15 mm (the Seeed figure includes the camera) | Seeed wiki |
| Pin count | 14 (2 rows of 7) | Seeed wiki, schematic |
| Pin pitch | 2.54 mm | standard |
| Row spacing (centre to centre) | 15.24 mm | **[VERIFY]** against Seeed's KiCad footprint |
| Pin 1 / 14 distance from the USB-C end edge | about 2.88 mm (pins centred on the 21 mm length) | **[VERIFY]** |
| USB-C | On the front (component) side, overhangs the USB end edge by about 1 to 1.5 mm | **[VERIFY]** |
| U.FL antenna connector | Front side, near a corner | **[VERIFY]** exact corner |
| Sense expansion board | Plugs into a 30-pin board-to-board connector (DF40C-30DP-0.4V) on the XIAO; holds the camera FPC connector and microSD slot | Seeed schematic |
| Battery pads | Back side. **BAT+ is used**: a short wire to shield pad J3 (D1). BAT− is not needed, ground comes through pin 13. **[VERIFY]** BAT+ is reachable with the Sense board fitted | D1 |

Pin order (Seeed numbering, front view, USB-C pointing up):

| Left row, top to bottom | Right row, top to bottom |
| --- | --- |
| 1 D0 (GPIO1) | 14 5V (VBUS) |
| 2 D1 (GPIO2) | 13 GND |
| 3 D2 (GPIO3) | 12 3V3 (regulator output) |
| 4 D3 (GPIO4) | 11 D10 (GPIO9, MOSI) |
| 5 D4 (GPIO5) | 10 D9 (GPIO8, MISO) |
| 6 D5 (GPIO6) | 9 D8 (GPIO7, SCK) |
| 7 D6 (GPIO43) | 8 D7 (GPIO44) |

### 3.2 Board outline and coordinates

All coordinates are in **shield top view**, in mm, origin at the **rear-left corner** of the board, **+X to the right, +Y forward** (towards the camera). KiCad's Y axis points down, so in KiCad draw forward as "up" on screen and convert; what matters is that forward is the top of the screen.

| ID | Requirement | Value | From |
| --- | --- | --- | --- |
| SH-O1 | Outline | 32.0 x 32.0 mm max, rectangle, 1 mm corner radius. May shrink once placement is done; must not grow | XD-A1, XD-A5 |
| SH-O2 | XIAO position | XIAO centred on X = 16.0. Its **USB-C end edge on the shield's rear edge (Y = 0)**, so the USB-C receptacle sticks out about 1 to 1.5 mm behind the shield. The XIAO then covers Y = 0 to 21 | XD-S5 |
| SH-O3 | Socket pad rows | X = 8.38 and X = 23.62 (16.0 ± 7.62). Pins at Y = 2.88, 5.42, 7.96, 10.50, 13.04, 15.58, 18.12 **[VERIFY with 3.1]** | XD-S1 |
| SH-O4 | Socket pads | Through-hole, 1.0 mm drill, 1.7 mm round pad (pin 1 square). Use a standard `PinSocket_1x07_P2.54mm_Vertical` footprint placed on **B.Cu** (KiCad flips and mirrors it) | XD-S1 |
| SH-O5 | Mounting holes | 4 x M2, 2.2 mm NPTH, at (3, 3), (29, 3), (3, 29), (29, 29). 4.5 mm diameter keep-out (no copper, no parts) around each on both layers | XD-A1 |
| SH-O6 | Rear-edge notch | None needed; the shield edge stops at the XIAO's edge. Keep top-side parts at least 1 mm in from the rear edge between X = 9 and X = 23 so a USB-C plug overmould never touches them | XD-S5 |
| SH-O7 | Board centre | (16, 16). The IMU goes here (SH-P1) and the frame's centre of thrust should line up with it | XD-S11 |

Rough area map (top view, forward is up):

```
 Y=32 +---------------------------------------------+
      | (H3)  M4 pads              M2 pads    (H4) |   front corners: motor 4 (FL), motor 2 (FR)
      |  Q4 D4 R4 R8                       Q2 D2 R2 R6 |
      |  C10                               C11       |   front bulk caps
 Y=21 |- - - - -  front edge of XIAO (below) - - - - |
      |  :J1:                                 :J2:   |
      |  :  :        U1 IMU at (16,16)        :  :   |   J1 / J2 = socket pad rows
      |  :  :        U2 LDO, C1-C7            :  :   |   at X = 8.38 and 23.62
      |  :  :     R9 R10 C3 (divider)         :  :   |
      |  Q3 D3                                Q1 D1  |
      | (H1)  M3 pads  LED1 BAT+ BAT- Q5 C8 C9 M1 (H2)|  rear: battery pads, protection, bulk
 Y=0  +---------------------------------------------+
      X=0            [ USB-C sticks out here ]       X=32
```

This is a starting point for placement, not a fixed layout. Which row is J1 and which is J2 depends on SH-O8.

### 3.3 Orientation and mirroring (the easy mistake)

The XIAO hangs below the shield, so the shield "sees" one side of the XIAO from above. Which side depends on which way its male pins point.

| ID | Requirement | From |
| --- | --- | --- |
| SH-O8 | **Assumed case (D5): XIAO back side (Sense board) faces the shield.** Male pins come out of the XIAO's back. In shield top view, forward up, USB-C at the rear: the **D0 to D6 row is on the left (X = 8.38)**, with D0 nearest the rear edge; the **5V to D7 row is on the right (X = 23.62)**, with 5V nearest the rear edge | XD-S1, XD-S4 |
| SH-O9 | **Other case: XIAO front side faces the shield** (pins out of the front). Then the rows swap: D0 to D6 on the right, 5V to D7 on the left, again pin 1 and 14 at the rear. Only use this if the male pins on your XIAO point out of the front | — |
| SH-O10 | Before ordering, print the copper layers 1:1 on paper, push the XIAO's pins through at the socket positions in the orientation it will fly, and check that every label lines up | — |

**[VERIFY]** Look at your pre-soldered XIAO Sense: if the pin headers' long ends come out of the same side as the Sense expansion board, use SH-O8. Also check that the Sense board fits between the two plastic header spacers, or sits above them.

### 3.4 Stack height and clearances

| ID | Requirement | Value | From |
| --- | --- | --- | --- |
| SH-H1 | Female header | Standard 1 x 7, 2.54 mm, 8.5 mm body height | XD-S1 |
| SH-H2 | Gap from shield underside to XIAO back | About 11 mm (8.5 mm socket + 2.5 mm male header spacer) | — |
| SH-H3 | Total depth below the shield top surface | About 16 mm: 1.0 shield + 8.5 socket + 2.5 spacer + 1.0 XIAO PCB + about 3.2 USB-C | XD-S4 |
| SH-H4 | Sense board in the gap | The Sense expansion board (with the camera unstuck from it) must fit in the 11 mm gap. **No parts and no copper-exposed features on the shield's bottom side inside the XIAO footprint** (X = 7.1 to 24.9, Y = 0 to 21), apart from the socket pins | XD-S4 |
| SH-H5 | Camera | The OV2640 camera on its flex is moved to a frame mount **in front of the shield's front edge (Y > 32)**, tilted up 15 to 25 degrees, so the shield doesn't block the top of its view | XD-V10 |
| SH-H6 | microSD slot | On the Sense board, facing the shield. Check the card can be pushed in from the side with the drone assembled; if not, it's only removed when the XIAO is pulled out (acceptable) | XD-S21 |
| SH-H7 | U.FL antenna | On the XIAO front, facing down. Route the antenna flex away from the battery and motor leads; no shield change needed | XD-V8 |
| SH-H8 | Top-side component height | 3 mm max (tallest is the SMA diode body, about 2.3 mm) so the frame or a printed cover can sit over it | XD-A1 |
| SH-H9 | XIAO retention | Leave room for a printed clip or hot glue at both header ends (Y < 2 and Y > 19 on the bottom side, next to the sockets) | XD-S3 |
| SH-H10 | 3D check | Export the board STEP with the XIAO model and check it in the frame CAD before ordering | XD-S4 |

---

## 4. Electrical blocks

### 4.1 Battery input and reverse polarity protection (XD-S13, S19, S20, S14)

- **BAT1**: two solder pads on the top side at the rear edge: `BAT+` (net BAT\_IN) and `BAT-` (net PGND). Each pad 3.0 x 4.0 mm, 3 mm apart, with a pair of 1.5 mm strain-relief holes (NPTH) 3 mm forward of them so the pigtail can be zip-tied or looped through. Rated for 10 A peak.
- **Q5** DMP2008UFG-7 (P-channel, PowerDI3333-8): **drain = BAT\_IN, source = VBAT\_P, gate = Q5\_G**. R12 10 kΩ from Q5\_G to PGND. Only 1S packs (gate max ±8 V).
- **C8, C9** 22 µF bulk right at Q5's source; **C10, C11** 22 µF at the front motor pairs (one near Q4, one near Q2). This keeps the 4 x 22 µF of XD-S14 but puts half of it where the front motors' current spikes happen.

### 4.2 Motor drivers x 4 (XD-S6 to S10)

For each motor n = 1 to 4:

- XIAO PWMn pin → **Rn** 100 Ω → net GATEn → **Qn** AO3400A gate (pin 1).
- **R(n+4)** 100 kΩ from GATEn to PGND, placed at the MOSFET.
- Qn source (pin 2) → PGND. Qn drain (pin 3) → net MOTn\_N.
- **Dn** SS34: anode → MOTn\_N, cathode → VBAT\_P, placed right beside the motor pads.
- **MOTn** pads: `+` = VBAT\_P, `-` = MOTn\_N. Pads 2.0 x 3.0 mm, 2.5 mm apart, plus one 1.2 mm NPTH strain-relief hole beside them. Silkscreen: motor number, `+`/`-` and a CW/CCW arrow.

### 4.3 XIAO power (XD-S15, decision D1)

- **J3** wire pad (2.0 x 2.0 mm, 1.0 mm plated hole) on VBAT\_P. A short wire (26 to 28 AWG silicone) runs from the XIAO's **BAT+** pad on its back up through J3 and is soldered on the top side.
- **C12** 22 µF and **C4** 100 nF from VBAT\_P to GND, right at J3: local decoupling for the XIAO's supply.
- XIAO pin 14 (5V) goes to **TP4** only, so you can see whether USB is present. It is never tied to VBAT\_P.
- XIAO pin 12 (3V3) is **not connected** (no-connect flag). It is never tied to the IMU rail (XD-S12).
- XIAO pin 13 (GND) → GND. It also carries the XIAO's battery current back to the net tie.

**Why BAT+ and not the 5V pin.** Inside the XIAO (Seeed schematic v1.51, page 4) the 5V pin feeds the SGM6029 buck through a Schottky (D2), and BAT+ feeds it through a P-FET (Q1) that turns off when USB is present. Going in at 5V meant two diode drops (our SS34 plus D2, about 0.75 V); BAT+ costs about 0.05 V. The SGM6029 runs from 1.95 V and switches to 100% duty cycle near its output voltage (datasheet in `hardware/datasheets/ics/`), so its output is the battery voltage minus about 0.15 V at 0.45 A (185 mΩ typical high-side switch plus the inductor).

| Battery (under load) | Old: SS34 into 5V | Now: BAT+ |
| --- | --- | --- |
| 4.1 V | 3.3 V | 3.3 V |
| 3.4 V | about 2.5 V (below the ESP32-S3's 3.0 V) | about 3.2 V |
| 3.1 V (full-throttle punch, low pack) | about 2.2 V | about 2.9 V |

**With USB plugged in:** the XIAO runs from USB (Q1 off), and its SGM40567 charger charges whatever is on BAT+, which is the drone battery through Q5. That is a proper Li-ion CC/CV charge to 4.2 V at about 110 mA, so it is safe for a 1S LiPo (a LiHV pack just stops short of full). VBAT\_P, the IMU LDO and the motor rail are live while charging, as they are any time a battery is plugged in; the gate pull-downs hold the motors off, and the firmware must refuse to arm while USB is connected. With USB and no battery, the charger's output (up to 4.2 V, about 110 mA) appears on VBAT\_P and the battery pads.

Test B7 (all motors at full while the supply drops to 3.0 V) is still the final check. If the XIAO resets there, the next step is a lower-sag pack or a buck-boost into BAT+, not a change to this path.

### 4.4 IMU and its LDO (XD-S11, S12, S18, S22)

- **U2** LDO (ME6211C33M5G-N, or XC6206P332MR per D2): input VBAT\_P, output +3V3\_IMU. ME6211: CE tied to VIN. **C6** 10 µF + **C5** 100 nF at the input, **C7** 10 µF at the output.
- **U1** LSM6DS3TR-C, 4-wire SPI:

| U1 pin | Name | Net |
| --- | --- | --- |
| 1 | SDO/SA0 | SPI\_MISO |
| 2 | SDx | GND (aux I2C unused) |
| 3 | SCx | GND (aux I2C unused) |
| 4 | INT1 | IMU\_INT1 |
| 5 | VDDIO | +3V3\_IMU |
| 6 | GND | GND |
| 7 | GND | GND |
| 8 | VDD | +3V3\_IMU |
| 9 | INT2 | not connected |
| 10 | OCS\_Aux | not connected |
| 11 | SDO\_Aux | not connected |
| 12 | CS | IMU\_CS |
| 13 | SCL/SPC | SPI\_SCK |
| 14 | SDA/SDI/SDO | SPI\_MOSI |

- **C1** 100 nF at VDD (pin 8), **C2** 100 nF at VDDIO (pin 5), both within 1 mm of the pins.
- **R11** 10 kΩ from IMU\_CS to +3V3\_IMU (IMU deselected while the XIAO boots).

**[VERIFY]** the pin table against the LSM6DS3TR-C datasheet (table "Pin description") and against the symbol you use.

### 4.5 Battery sense (XD-S16)

- **R9** 100 kΩ from VBAT\_P to VBAT\_SENSE, **R10** 100 kΩ from VBAT\_SENSE to GND, **C3** 100 nF across R10. VBAT\_SENSE → XIAO D4. At 4.35 V the ADC sees 2.18 V.

### 4.6 Status LED (XD-S25)

- XIAO D7 → net LED\_STAT → **R13** 1 kΩ → net LED\_A → **LED1** anode; LED1 cathode → GND. Active high. Place LED1 at the rear edge so it's visible from behind the drone.

### 4.7 Test points (free, no parts)

1.0 mm round top-side pads: **TP1** VBAT\_P, **TP2** +3V3\_IMU, **TP3** GND, **TP4** XIAO\_5V (live only with USB plugged in), **TP5** IMU\_INT1. They make bring-up tests B2, B5 and B14 easier.

### 4.8 Pin notes

- D2 is GPIO3, a strapping pin that only matters if the JTAG-select eFuse is burned (it isn't by default). The 100 kΩ pull-down is harmless.
- D6 / D7 are UART0. Firmware never starts UART0 (system spec 3.5).
- The Sense board's microSD chip select (GPIO21) is not on the headers; nothing on the shield touches it.

---

## 5. Complete net list

Net names are the ones to use in the schematic. This table is the design intent; the **real net list is generated from the KiCad schematic** (see [kicad-build-steps.md](kicad-build-steps.md)) and checked against this table.

| Net | Connects | Net class |
| --- | --- | --- |
| BAT\_IN | BAT1 `+`, Q5 drain (pins 5 to 8 and pad) | POWER\_HI |
| VBAT\_P | Q5 source (pins 1 to 3), C8 to C11, MOT1 to MOT4 `+`, D1 to D4 cathodes, J3, C12, C4, U2 VIN (and CE on ME6211), C5, C6, R9, TP1 | POWER\_HI (trunk), MOTOR (branches) |
| PGND | BAT1 `-`, Q1 to Q4 sources, C8 to C11, R5 to R8, R12, NT1 pin 1 | POWER\_HI |
| GND | NT1 pin 2, J2 pin 13 (XIAO GND), U1 pins 2, 3, 6, 7, U2 GND, C1 to C7, C12, R10, LED1 cathode, TP3 | SIGNAL\_GND |
| Q5\_G | Q5 gate (pin 4), R12 | SIGNAL |
| MOT1\_N to MOT4\_N | MOTn `-`, Qn drain, Dn anode | MOTOR |
| PWM1 to PWM4 | XIAO D0 to D3 (pins 1 to 4), R1 to R4 | SIGNAL |
| GATE1 to GATE4 | R1 to R4, Q1 to Q4 gates, R5 to R8 | SIGNAL |
| XIAO\_5V | XIAO pin 14 (5V, USB VBUS), TP4 | SIGNAL (probe only, no current) |
| +3V3\_IMU | U2 VOUT, C7, U1 VDD and VDDIO, C1, C2, R11, TP2 | POWER\_LO |
| VBAT\_SENSE | R9, R10, C3, XIAO D4 (pin 5) | SIGNAL |
| IMU\_INT1 | U1 pin 4, XIAO D5 (pin 6), TP5 | SIGNAL |
| IMU\_CS | U1 pin 12, R11, XIAO D6 (pin 7) | SPI |
| LED\_STAT | XIAO D7 (pin 8), R13 | SIGNAL |
| LED\_A | R13, LED1 anode | SIGNAL |
| SPI\_SCK | XIAO D8 (pin 9), U1 pin 13 | SPI |
| SPI\_MISO | XIAO D9 (pin 10), U1 pin 1 | SPI |
| SPI\_MOSI | XIAO D10 (pin 11), U1 pin 14 | SPI |
| (no connect) | XIAO pin 12 (3V3), U1 pins 9, 10, 11 | — |

### 5.1 XIAO socket pins

J1 and J2 are the two 1 x 7 sockets. J1 carries XIAO pins 1 to 7, J2 carries pins 14 down to 8 (J2 pin 1 = XIAO pin 14, so both sockets' pin 1 sit at the rear).

| Socket pin | XIAO pin | Signal | Net |
| --- | --- | --- | --- |
| J1-1 | 1 | D0 / GPIO1 | PWM1 |
| J1-2 | 2 | D1 / GPIO2 | PWM2 |
| J1-3 | 3 | D2 / GPIO3 | PWM3 |
| J1-4 | 4 | D3 / GPIO4 | PWM4 |
| J1-5 | 5 | D4 / GPIO5 (ADC1\_CH4) | VBAT\_SENSE |
| J1-6 | 6 | D5 / GPIO6 | IMU\_INT1 |
| J1-7 | 7 | D6 / GPIO43 | IMU\_CS |
| J2-1 | 14 | 5V | XIAO\_5V (TP4 only) |
| J2-2 | 13 | GND | GND |
| J2-3 | 12 | 3V3 | no connect |
| J2-4 | 11 | D10 / GPIO9 | SPI\_MOSI |
| J2-5 | 10 | D9 / GPIO8 | SPI\_MISO |
| J2-6 | 9 | D8 / GPIO7 | SPI\_SCK |
| J2-7 | 8 | D7 / GPIO44 | LED\_STAT |

A cleaner option in the schematic is one 14-pin XIAO symbol (Seeed publishes one) with the two sockets as its footprint; either way the pin-to-net mapping above must hold.

---

## 6. Layout rules

### 6.1 Net classes and copper widths

Widths are for 1 oz outer copper using IPC-2221 (external layer). The 8 A figure is a brief full-throttle peak; hover is about 4 to 5 A.

| Net class | Nets | Current | Min width | Clearance | Vias |
| --- | --- | --- | --- | --- | --- |
| POWER\_HI | BAT\_IN, VBAT\_P trunk (pads to Q5 to bulk caps to the branch points), PGND | 8 A peak, 5 A hover | **Copper pour, 4 mm or wider** (5 mm gives about 10 °C rise at 8 A, 3.5 mm about 20 °C). Where a width is forced, 3 mm absolute minimum (XD-S17) | 0.2 mm | 0.4/0.8 mm; **at least 8 vias** wherever this current changes layer (about 1 A per via) |
| MOTOR | MOT1\_N to MOT4\_N, VBAT\_P branch to each motor | 2 A peak per motor | **1.0 mm** (about 10 °C rise at 2 A); 1.5 mm where room allows | 0.2 mm | 0.4/0.8 mm, at least 3 per layer change |
| POWER\_LO | VBAT\_P branch to J3 / C12 / C4 (XIAO supply), +3V3\_IMU | 0.5 A / 0.01 A | 0.5 mm / 0.3 mm | 0.15 mm | 0.3/0.6 mm, 2 per layer change on the J3 branch |
| SPI | SPI\_SCK, SPI\_MISO, SPI\_MOSI, IMU\_CS | 10 MHz | 0.2 mm | 0.15 mm (0.3 mm to motor nets) | 0.3/0.6 mm |
| SIGNAL | PWMn, GATEn, Q5\_G, VBAT\_SENSE, IMU\_INT1, LED\_STAT, LED\_A | mA | 0.2 mm | 0.15 mm | 0.3/0.6 mm |
| SIGNAL\_GND | GND | 0.5 A | Pour; 0.5 mm min where traced | 0.15 mm | 0.3/0.6 mm |

Pads on POWER\_HI and MOTOR pours use **solid** zone connections (no thermal relief) on Q5, Q1 to Q4 sources and drains, the bulk caps and the battery and motor pads. The through-hole socket pins use **thermal reliefs** so they're easy to hand-solder.

### 6.2 Layer use

- **Top (F.Cu):** all parts; VBAT\_P pour from Q5 out to the four corners; motor branches; signal routing.
- **Bottom (B.Cu):** PGND pour around the outer ring and rear edge, under the motor drivers and battery pads; a separate GND pour under the XIAO / IMU / LDO area. Signals may cross on the bottom only where they can't on the top, and never across the PGND / GND boundary.
- **Ground join (D6):** PGND and GND meet only through **NT1**, a 2-pad net-tie footprint (KiCad `NetTie-2_SMD_Pad0.5mm` or similar, widened to 1.5 mm) placed right beside the BAT1 `-` pad. DRC then catches any accidental second join.

### 6.3 Placement rules

| ID | Rule | From |
| --- | --- | --- |
| SH-P1 | U1 (IMU) at the board centre (16, 16), its package edges parallel to the board edges, its X axis pointing forward (+Y board) **[VERIFY axis marking on the datasheet and note it in silkscreen]**. Nothing over 1 A within 5 mm of it; no motor or POWER\_HI copper on either layer under it | XD-S11 |
| SH-P2 | U2 (LDO) and C5 to C7 within 5 mm of U1, on the GND side of the board | XD-S12 |
| SH-P3 | C1 and C2 within 1 mm of U1's VDD and VDDIO pins | XD-S12 |
| SH-P4 | SPI traces from the J2 pins to U1 under 15 mm, routed together over the GND pour, never parallel to a motor trace for more than 3 mm | XD-S22 |
| SH-P5 | Each Qn, Dn, Rn, R(n+4) cluster within 6 mm of its motor pads (in the board corners outside the socket rows: X < 7 or X > 25). The loop VBAT\_P → motor pad → drain → Dn → VBAT\_P as small as possible | XD-S6, S8 |
| SH-P6 | Gate resistors Rn at the MOSFET end of the PWM trace, pull-downs R(n+4) at the MOSFET gate pin | XD-S7 |
| SH-P7 | BAT1 pads on the rear edge, Q5 within 4 mm of them, C8 and C9 within 3 mm of Q5's source. BAT1 between X = 9 and 23 must leave the USB-C plug path behind the board clear (pads are on the top side, so they don't block it) | XD-S19, S14 |
| SH-P8 | Q5 drain and source each on 30 mm² or more of copper (top), with 6 or more vias to matching bottom copper for heat spreading | XD-S20 |
| SH-P9 | J3 just outside the XIAO footprint (SH-H4), as close as possible to where the XIAO's BAT+ pad sits, so the wire is short; C12 and C4 within 2 mm of J3. Its VBAT\_P branch comes off the trunk on the GND side, away from the motor branches **[VERIFY BAT+ pad position on the XIAO]** | XD-S15 |
| SH-P10 | R9, R10, C3 near J1 pin 5, on the GND side, away from motor copper | XD-S16 |
| SH-P11 | LED1 and R13 on the rear edge, not under the battery pigtail path | XD-S25 |
| SH-P12 | Motor pads within 2 mm of the board edge, at the corner nearest their motor, clear of the mounting-hole keep-outs | XD-S9 |
| SH-P13 | All SMD parts at least 1 mm from the board edge (JLC may otherwise ask for rails) | SH-M10 |
| SH-P14 | No parts on B.Cu except J1 and J2 bodies | SH-M7 |

### 6.4 Motor positions and silkscreen

Props-in (Betaflight default). Viewed from above, forward up.

| Motor | Position | Spin | PWM pin | Pad location |
| --- | --- | --- | --- | --- |
| M1 | Rear right | CW | D0 | rear-right corner |
| M2 | Front right | CCW | D1 | front-right corner |
| M3 | Rear left | CCW | D2 | rear-left corner |
| M4 | Front left | CW | D3 | front-left corner |

Silkscreen on the top side: board name and version (`XIAO FPV SHIELD v0.1`), a forward arrow, `M1` to `M4` with spin arrows and `+`/`-` at each motor, `BAT+` / `BAT-` (large), `1S ONLY`, `USB` at the rear, test point names, and the `JLCJLCJLCJLC` placeholder.

---

## 7. Schematic structure for KiCad

One A4 sheet is enough. Suggested blocks, left to right: battery input and protection, motor drivers x 4, XIAO sockets, XIAO power, IMU + LDO, battery sense, status LED, test points and mounting holes.

- Put the JLC part number in a `LCSC` field on every assembled part (KiCad's JLC BOM export plug-ins read this field name).
- Mark J1, J2, BAT1, MOT1 to MOT4, TP1 to TP5, NT1 and H1 to H4 as **Exclude from BOM** and **Exclude from position files**, so they don't appear in the JLC assembly files.
- Assign net classes with net-class directives or the Board Setup net-class patterns (`MOT*_N`, `SPI_*`, and so on).

---

## 8. Bill of materials

Prices and basic/extended status change; **re-check every part number in JLC's library on the order day [VERIFY]**. The same list is in [bom/shield-bom.csv](../bom/shield-bom.csv) in JLC's upload format.

### 8.1 Assembled by JLC (top side, per board)

| Ref | Value | Package | JLC # | JLC type | Qty |
| --- | --- | --- | --- | --- | --- |
| U1 | LSM6DS3TR-C IMU | LGA-14 2.5 x 3 mm | C967633 | Extended | 1 |
| U2 | ME6211C33M5G-N, 3.3 V LDO (or XC6206P332MR, C5446, basic, SOT-23, per D2) | SOT-23-5 | C82942 | **[VERIFY]** | 1 |
| Q1-Q4 | AO3400A N-MOSFET 30 V 5.7 A | SOT-23 | C20917 | Basic | 4 |
| Q5 | DMP2008UFG-7 P-MOSFET 20 V 14 A | PowerDI3333-8 | C461052 | Extended | 1 |
| D1-D4 | SS34 Schottky 40 V 3 A | SMA (DO-214AC) | C8678 | Basic | 4 |
| R1-R4 | 100 Ω 1% | 0402 | C25076 | Basic | 4 |
| R5-R10 | 100 kΩ 1% | 0402 | C25741 | Basic | 6 |
| R11, R12 | 10 kΩ 1% | 0402 | C25744 | Basic | 2 |
| R13 | 1 kΩ 1% | 0402 | C11702 | Basic | 1 |
| C1-C5 | 100 nF 16 V X7R | 0402 | C1525 | Basic | 5 |
| C6, C7 | 10 µF 10 V X5R | 0603 | C19702 | Basic | 2 |
| C8-C12 | 22 µF 25 V X5R | 0805 | C45783 | Basic | 5 |
| LED1 | Green LED | 0603 | C72043 (or red C2286) | **[VERIFY]**, both believed basic | 1 |

That is **3 or 4 extended parts** (U1, Q5, and possibly U2 and LED1). Choosing XC6206 and a basic LED brings it down to 2.

### 8.2 Not assembled (you fit them)

| Ref | Item | Qty per board | Notes |
| --- | --- | --- | --- |
| J1, J2 | 1 x 7 female header, 2.54 mm, 8.5 mm tall | 2 | Hand-soldered from the top side; buy a strip and cut |
| — | Male headers on the XIAO | 2 x 7 | Come pre-soldered on the "pre-soldered" XIAO |
| — | Battery pigtail (A30 or BT2.0, 20 AWG) | 1 | Soldered to BAT1 (XD-B3) |
| J3 wire | 26 to 28 AWG silicone wire, about 15 mm | 1 | XIAO BAT+ pad to J3 (section 4.3); unsolder it to pull the XIAO |
| — | M2 screws or printed pins | 4 | For the frame |

### 8.3 Rough JLC cost (5 boards, all assembled)

| Item | Approx. USD |
| --- | --- |
| 5 x 2-layer PCB, 32 x 32 mm, standard specs | 2 to 5 |
| Economic PCBA setup + stencil | about 9 |
| Extended part fees, 2 to 4 parts at about 3 each | 6 to 12 |
| Parts for 5 boards (IMU is the largest at a few dollars each) | 20 to 30 |
| Shipping (cheapest option) | 5 to 20 |
| **Total** | **about 45 to 75** |

Rough figures from JLC's usual pricing, to be replaced by the real quote. The system budget (section 8 of the system spec) allows about 115 AUD for this order.

---

## 9. Bring-up hooks

The board supports these tests from the system spec without extra hardware: B2 (TP2 for the 3.3 V rail), B4 (USB alone: TP1 reads at most 4.2 V from the XIAO charger, TP4 about 5 V, motors stay off), B5 (TP5 for INT1), B13 (bench supply on BAT1), B14 (measure across BAT1 `+` and TP1 for Q5's drop).

---

## 10. KiCad project layout

```
hardware/
  .gitignore                 KiCad backups, caches, generated outputs
  README.md                  what lives here
  shield/
    README.md                how to open and build the shield project
    shield.kicad_pro         (to be created in KiCad)
    shield.kicad_sch         (to be created)
    shield.kicad_pcb         (to be created)
    docs/
      shield-pcb-requirements.md   this document
      kicad-build-steps.md         steps for building the schematic with the KiCad MCP
    bom/
      shield-bom.csv         JLC-format BOM (section 8.1)
    lib/
      symbols/               project symbol library (XIAO, LSM6DS3TR-C, DMP2008UFG if missing)
      footprints/            project footprint library (shield.pretty: motor pads, battery pads)
      3dmodels/              STEP models (XIAO ESP32-S3 Sense for the 3D check)
    production/              Gerbers, drill, BOM and CPL exported for each order
```

---

## 11. What you must still verify

Before the schematic is frozen:

1. **Which side the XIAO's pins come out of**, and that the Sense board fits between or above the header spacers (SH-O8, SH-O9). This decides the mirroring of the whole socket footprint.
2. **XIAO row spacing (15.24 mm) and pin 1 position (about 2.88 mm from the USB-C end)** against Seeed's KiCad footprint or dimension drawing (SH-O3).
3. **U.FL corner, USB-C overhang and the Sense board's height** in the 11 mm gap (SH-H2 to H7).
4. ~~The XIAO's regulator (SGM6029) minimum input voltage~~ **Resolved 2026-11-27:** 1.95 V minimum with 100% duty cycle, but the 5V pin has an internal Schottky, so the feed moved to BAT+ (D1, section 4.3). Still to check: **where the BAT+ pad is and that a wire reaches it with the Sense board fitted** (SH-P9).
5. **JLC basic or extended status and stock** for every part in 8.1, in particular ME6211 (decides D2) and the LED.
6. **LSM6DS3TR-C pinout and axis marking** against the datasheet (4.4, SH-P1).
7. **DMP2008UFG pinout** (source pins 1 to 3, gate 4, drain 5 to 8 and the pad) against the Diodes datasheet.
8. **JLC capabilities and price** on the order day: 1.0 mm thickness at no extra cost, HASL OK for the 0.5 mm-pitch IMU, minimum PCBA board size, whether rails are needed.
9. **Motor numbering** matches what the flight firmware expects (6.4).

After the boards arrive: the bring-up tests B2 to B16 in the system spec.

---

Sources: [Seeed: Getting started with XIAO ESP32-S3 (dimensions, pin list, 5V pin diode note, battery notes)](https://wiki.seeedstudio.com/xiao_esp32s3_getting_started); [Seeed: XIAO ESP32-S3 Sense schematic v1.51 (SGM6029 regulator, SGM40567 charger, DF40C B2B connector, header pins)](https://files.seeedstudio.com/wiki/SeeedStudio-XIAO-ESP32S3/new-res/202003753_XIAO%20ESP32S3%20Sense_V1.51_SCH_260611.pdf); [Seeed forum: powering the XIAO ESP32-S3 from the 5V pin with a diode](https://forum.seeedstudio.com/t/how-to-power-xiao-esp32s3-from-5v-vin-vbus-with-diode/281611); [Diodes DMP2008UFG](https://www.diodes.com/part/view/DMP2008UFG); [SG Micro SGM6029 (XIAO buck regulator)](https://www.sg-micro.com/product/SGM6029). Track widths from IPC-2221 (external layers, 1 oz).
