# XIAO Wi-Fi FPV Drone: Requirements, Budget and BOM

Nov 26, 2026 · @Lehan

## 1. Overview

A small FPV drone you fly from a phone app over Wi-Fi: the app shows live video from the drone's forward camera and works as the remote control. It is built around a plug-in Seeed XIAO ESP32-S3 Sense; a custom shield PCB with female headers takes the XIAO and carries the brushed motor drivers (the "ESC") for four 720 coreless motors, a 6-axis IMU, power from a 1S LiPo, and battery sensing. The motors solder straight to pads on the shield.

**Decided in this version:**

- **FPV over Wi-Fi:** the drone is its own Wi-Fi access point; the phone app shows the video and sends stick commands.
- XIAO ESP32-S3 Sense plugs into **female headers** on the shield (removable, no castellated soldering); its camera faces forward.
- **720 brushed coreless motors** (7 x 20 mm), soldered to pads, driven by one MOSFET each.
- **6-axis IMU** (accelerometer + gyroscope) on the shield.
- **1S LiPo** battery on a plug, so packs swap without soldering.
- **Reverse polarity protection** at the battery pads (P-channel MOSFET), so a pigtail soldered the wrong way round can't kill the board.
- **microSD card usable** (on the Sense board), sharing the SPI bus with the IMU.
- **IMU data-ready interrupt** wired to the XIAO, and a **status LED on the shield** (the XIAO's own user LED is taken by the SD card, see 3.4).

**Dropped from the pollinator plan:** pollination, flower finding, motion capture and the IR markers. **The UWB expansion header is dropped too**.

Requirement IDs use the prefix **XD-**.

## 2. Airframe and power

720 motors suit a frame of roughly 90 to 150 mm with 55 to 65 mm props; this build targets about 100 mm with 65 mm props (decided), about 60 g all-up.

A 720 motor is a 7 x 20 mm brushed coreless motor for 1S; listings give about 3 to 5 g each and around 2 A peak current. Thrust per motor isn't published consistently, so it must be measured (XD-A4).

| ID | Requirement | Target | Priority |
| --- | --- | --- | --- |
| XD-A1 | Frame: about 100 mm motor to motor along each side, 3D printed, holding the shield in the middle and a 720 motor in each arm | Frame + guards about 10 g | Must |
| XD-A2 | Motors: four 720 brushed coreless (2 clockwise, 2 anticlockwise), leads soldered to the shield's motor pads | 3.7 V, about 2 A peak each | Must |
| XD-A3 | Props: 65 mm (55 mm as a fallback if 65 mm overloads the motors) | Fit the frame with 5 mm or more tip clearance | Must |
| XD-A4 | Thrust-to-weight ratio, measured on a scale before the first flight | 2:1 or better (about 30 g per motor at 60 g all-up) | Must |
| XD-A5 | All-up weight with battery, XIAO and camera | 65 g or less | Must |
| XD-A6 | Flight time, hovering | 6 min Must, 8 min Should | Must / Should |
| XD-A7 | Prop guards (ducts or rings) for indoor flying | Survive bumping a wall at walking pace | Must |
| XD-A8 | Battery strapped to the frame (not to the shield) so a hard landing can't tear the shield off its standoffs | Velcro strap + printed tray | Should |

## 3. Shield requirements

The XIAO sits on top of the shield in two 7-pin female headers (its back and battery pads facing the shield, Sense camera board on top), so it can be pulled out for flashing, swapping or repair; the Sense camera is mounted facing forward (XD-V10).

### 3.1 Connection to the XIAO

| ID | Requirement | Target | Priority |
| --- | --- | --- | --- |
| XD-S1 | Two 1 x 7 female headers, 2.54 mm pitch, on the shield's upper (socket) side, matching the XIAO's edge pins | XIAO plugs in with no soldering on the shield side | Must |
| XD-S2 | XIAO fitted with male pin headers (bought pre-soldered, or soldered once) | Seats fully in the sockets | Must |
| XD-S3 | XIAO held against vibration | Printed clip or a dab of hot glue on the header ends | Must |
| XD-S4 | Forward-facing camera mount and clearance for the Sense camera board and the Wi-Fi antenna | Checked with a 3D model before ordering | Must |
| XD-S5 | XIAO USB-C reachable with the drone assembled | Flash and debug without removing anything | Should |

### 3.2 Brushed motor drivers (the "ESC")

| ID | Requirement | Target | Priority |
| --- | --- | --- | --- |
| XD-S6 | One low-side N-channel MOSFET per motor (AO3400A or similar) | Fully on from a 3.3 V gate; 5 A or more | Must |
| XD-S7 | 100 ohm gate resistor and 100 kohm gate pull-down on every MOSFET | Motors never twitch during boot or reset | Must |
| XD-S8 | Schottky flyback diode across each motor | Rated 2 A or more (the 720's peak), e.g. a 3 A part in SMA | Must |
| XD-S9 | Motor solder pads, 2 per motor, with a strain-relief hole for the leads | Pads about 2 x 3 mm; labelled motor number and spin direction | Must |
| XD-S10 | PWM frequency | 16 to 32 kHz from the ESP32 LEDC timers | Must |

### 3.3 IMU and power

| ID | Requirement | Target | Priority |
| --- | --- | --- | --- |
| XD-S11 | 6-axis IMU (LSM6DS3TR-C) on SPI, near the shield's centre, aligned with the board edges, away from motor traces | Gyro up to 2000 dps | Must |
| XD-S18 | IMU INT1 (data-ready) wired to XIAO pin D5 (GPIO6); the flight loop is timed from this interrupt instead of polling | One interrupt per gyro sample, no missed samples | Must |
| XD-S12 | 3.3 V LDO (XC6206P332, behind a 22 ohm / 10 uF ripple filter) for the IMU only; never tied to the XIAO's 3V3 pin | 10 uF in and out, 100 nF at the IMU | Must |
| XD-S13 | Battery solder pads only, no connector on the shield, so any pack or pigtail can be fitted later; options in section 5 | Rated 10 A peak | Must |
| XD-S19 | Reverse polarity protection right after the battery pads: a P-channel MOSFET (DMP2008UFG) in the positive lead, drain to the battery pad, source to the protected rail (VBAT\_P), gate to ground through 10 kohm. Everything else (motors, LDO, XIAO, divider, bulk caps) runs from VBAT\_P | Reversed pack draws no current and damages nothing; forward drop under 100 mV at 8 A (9.8 mohm max at 2.5 V gate drive) | Must |
| XD-S20 | Protection MOSFET sits on a copper pour on both drain and source sides to spread heat; only 1S packs are ever fitted (its gate is rated ±8 V, a 2S pack would exceed it) | Under 0.7 W at the 8 A peak, about 0.25 W at hover | Must |
| XD-S14 | Bulk capacitance on the protected rail (VBAT\_P), right after the protection MOSFET | 4 x 22 uF ceramic | Must |
| XD-S15 | XIAO power from the protected rail (VBAT\_P) into the XIAO's BAT+ pad (its own P-FET path), so it never browns out under motor load; USB 5 V reaches the battery only through the XIAO's Li-ion charger (4.2 V, about 110 mA) | Chosen from Seeed's schematic: the 5V pin has an internal Schottky, BAT+ does not (shield doc section 4.3) | Must |
| XD-S16 | Battery voltage divider (100 k / 100 k + 100 nF) from the protected rail into XIAO pin D4 (GPIO5, ADC1 channel 4); the drone's only battery gauge, as the XIAO ESP32-S3 has no battery sense of its own. ADC1 must be used because ADC2 can't be read while Wi-Fi is on, and D6/D7 have no ADC at all | ±50 mV after calibration | Must |
| XD-S17 | Motor current routed in wide copper between battery pads and MOSFETs, away from the IMU; one ground join near the battery pads | 3 mm or wider pours | Must |

### 3.4 microSD card and status LED

The Sense board's microSD slot is wired to the same SPI pins as the shield's IMU (D8 / D9 / D10) and has its own chip select on GPIO21, which isn't on the headers. GPIO21 is also the XIAO's yellow user LED (on when the pin is low). So the built-in LED lights whenever the SD card is selected, and turning the LED on would select the SD card in the middle of IMU reads. The built-in LED is therefore left as an SD activity light, and the shield gets its own status LED.

The camera (GPIO10 to 18, 38 to 40, 47, 48), the microphone (GPIO41, 42) and the PSRAM (internal to the module) use none of D0 to D10, so they don't clash with the shield.

| ID | Requirement | Target | Priority |
| --- | --- | --- | --- |
| XD-S21 | microSD card usable for logs and recordings; the Sense board's J3 pads are left joined (the factory default) so the slot stays connected | Card mounts with the IMU and camera running | Must |
| XD-S22 | IMU and SD card share the SPI bus with separate chip selects: IMU on D6 (10 kohm pull-up on the shield), SD on GPIO21. Firmware drives GPIO21 high before any SPI transfer, sets up the SD card first, and gives each device its own SPI mode and clock (SD mode 0, IMU per its datasheet, IMU 10 MHz or less) | No corrupted IMU reads with SD writes going on | Must |
| XD-S23 | Flight never waits on the SD card: logging runs in a low-priority task on the Wi-Fi core in small writes (512 bytes) that release the bus between them, and the flight loop reads the IMU's on-chip FIFO so samples taken while the card is busy aren't lost. SPI DMA buffers stay in internal RAM, not PSRAM | Flight loop timing unchanged with logging on and off | Must |
| XD-S24 | Flight log to SD: IMU, motor outputs, battery voltage, link quality | 100 Hz or more | Should |
| XD-S25 | Status LED on the shield (0603 LED + 1 kohm) on XIAO pin D7 (GPIO44), showing armed, link lost and low battery; the built-in LED stays as SD activity | Visible indoors from 3 m | Must |

### 3.5 Pin map

Every header pin is now in use; there is no spare GPIO left.

| XIAO pin | GPIO | Shield connection |
| --- | --- | --- |
| D0 to D3 | GPIO1 to 4 | Motor MOSFET gates 1 to 4 |
| D4 | GPIO5 (ADC1) | Battery voltage divider from VBAT\_P (XD-S16) |
| D5 | GPIO6 | IMU INT1, data-ready (XD-S18) |
| D6 | GPIO43 | IMU chip select (10 kohm pull-up) |
| D7 | GPIO44 | Status LED (XD-S25) |
| D8 / D9 / D10 | GPIO7 / 8 / 9 | SPI SCK / MISO / MOSI, shared by the IMU and the Sense board's microSD |
| (not on headers) | GPIO21 | microSD chip select and built-in user LED, on the Sense board |
| BAT+ pad (back) | — | XIAO power from VBAT\_P, by a short wire to shield pad J3 (XD-S15) |
| 5V | — | Test point only (USB present) |
| GND | — | Shield ground |

D6 and D7 are the ESP32-S3's UART0 pins, so firmware uses USB serial only and never starts UART0. The boot messages the chip prints on D6 just toggle the IMU chip select with no clock, which the IMU ignores.

Sources: [Seeed: Getting started with XIAO ESP32-S3 (pin list, user LED, Sense pins)](https://wiki.seeedstudio.com/xiao_esp32s3_getting_started); [Seeed: XIAO ESP32-S3 Sense microSD and J3](https://wiki.seeedstudio.com/xiao_esp32s3_sense_filesystem/); [Diodes DMP2008UFG](https://www.diodes.com/part/view/DMP2008UFG).

## 4. FPV video, control link and app

The phone app is both the screen and the remote: it shows the camera feed and sends stick commands over the drone's own Wi-Fi. Wi-Fi video has more delay than analog FPV, so this drone is for smooth, careful flying rather than racing.

### 4.1 Link and video

| ID | Requirement | Target | Priority |
| --- | --- | --- | --- |
| XD-V1 | The drone runs its own 2.4 GHz Wi-Fi access point; the phone joins it directly | No router needed | Must |
| XD-V2 | Control: the app sends roll, pitch, yaw, throttle and arm/disarm as small UDP packets | 50 Hz | Must |
| XD-V3 | Control always beats video: when the link is busy, video frames are dropped first | Control packets never queued behind video | Must |
| XD-V4 | Video: MJPEG from the onboard camera to the app | 320 x 240 to 640 x 480 at 15 fps Must, 25 fps Should | Must / Should |
| XD-V5 | Delay from camera to phone screen | Under 200 ms Must, under 120 ms Should (to be measured) | Must / Should |
| XD-V6 | Link-loss failsafe: no control packet for 0.5 s, then level out, descend slowly and disarm on touchdown | Every time, tested | Must |
| XD-V7 | Telemetry to the app: battery voltage, link quality, armed state, flight mode | 5 Hz | Must |
| XD-V8 | Range | 30 m indoors; line-of-sight outdoors with the U.FL antenna fitted | Should |
| XD-V9 | Flight control on one ESP32-S3 core, Wi-Fi and video on the other | Control loop timing unaffected by streaming | Must |
| XD-V10 | Camera faces forward, tilted up about 15 to 25 degrees, on a vibration-damped mount | Horizon level in hover | Must |

### 4.2 Flight modes

| ID | Requirement | Target | Priority |
| --- | --- | --- | --- |
| XD-F1 | Angle (self-levelling) mode: centred sticks hold the drone level | Default mode | Must |
| XD-F2 | Acro (rate) mode | Selectable in the app | Could |
| XD-F3 | Altitude hold | Needs a barometer or distance sensor, not on this board | Could |

### 4.3 The app

| ID | Requirement | Target | Priority |
| --- | --- | --- | --- |
| XD-P1 | Android app first (or one cross-platform codebase) | Runs on your phone | Must |
| XD-P2 | Two on-screen sticks over the live video | Throttle stick does not spring back to centre | Must |
| XD-P3 | Arm switch that needs a deliberate action (slide or long press) | No accidental arming | Must |
| XD-P4 | On-screen battery voltage with a low-battery warning | Warning at about 3.5 V per cell under load | Must |
| XD-P5 | Bluetooth gamepad support for real sticks | Common gamepads | Should |
| XD-P6 | Start from Espressif's open-source ESP-Drone app and control protocol, adding the video view | Saves building the control link from scratch | Should |

### 4.4 Rules for flying FPV in Australia

CASA allows recreational FPV indoors as long as the drone can't get out of the building. Flying FPV outdoors needs membership of a model aircraft association approved for FPV (flying at its approved sites) or CASA approval.

| ID | Requirement | Target | Priority |
| --- | --- | --- | --- |
| XD-L1 | FPV flights indoors only, unless flown through an approved model aircraft association or with CASA approval | Every flight | Must |
| XD-L2 | All-up weight well under 250 g | About 60 g | Must |

Sources: [CASA: Flying first person view](https://www.casa.gov.au/drones/drone-rules/flying-first-person-view); [Espressif ESP-Drone documentation](https://docs.espressif.com/projects/espressif-esp-drone/en/latest/index.html).

## 5. Battery options

**Recommended: GNB 850 mAh 1S LiHV with an A30 (or BT2.0) connector, 2 per drone.** It gives the longest flight time for its weight, and its connector carries the drone's hover current comfortably.

The connector matters as much as the cell. This drone draws about 3.7 to 4.9 A just to hover (section 6). BetaFPV rates its BT2.0 connector at 9 A continuous and PH2.0 at only 4.5 A, so a PH2.0 pack would run at or past its connector's limit the whole flight.

| Option | Capacity | Weight | Rating | Connector | Est. hover time | Price seen |
| --- | --- | --- | --- | --- | --- | --- |
| **GNB 1S LiHV 850 mAh** *(Recommended)* | 850 mAh | 17 to 18 g | 60C | A30 or PH2.0 | 8.3 to 10.5 min | about £5.20 / €6.09 each |
| GNB 1S LiHV 720 mAh | 720 mAh | 16 g | 80C | A30 | 7.2 to 9.1 min | about €6.09 each |
| GNB 1S LiHV 660 mAh | 660 mAh | 15 g | 90C | PH2.0 | 6.7 to 8.5 min | about US$4.99 each |
| BetaFPV BT2.0 1S 550 mAh | 550 mAh | 14 g | 40C | BT2.0 | 5.7 to 7.2 min | sold in 4-packs |

Flight times are my estimates for hovering at about 60 g all-up, assuming 3.5 to 4.5 g of thrust per watt and 80% usable capacity. Real flying, with climbs and turns, will cut them by roughly a fifth.

| ID | Requirement | Target | Priority |
| --- | --- | --- | --- |
| XD-B1 | 1S LiHV pack, 720 to 850 mAh, 60C or more | 16 to 18 g | Must |
| XD-B2 | Connector rated well above hover current: A30 or BT2.0, not PH2.0 | 9 A or more continuous | Must |
| XD-B3 | Matching connector on the shield's battery pigtail | Same type on every drone and every pack | Must |
| XD-B4 | Charger that supports LiHV (4.35 V) cells with the same connector | Charges at least 4 packs at once | Must |
| XD-B5 | 2 packs per drone, plus spares | 6 to 8 packs for 3 drones | Should |

Sources: [GNB 850 mAh 1S 60C LiHV, A30 (HobbyRC)](https://www.hobbyrc.co.uk/gnb-850mah-1s-60c-lihv-battery-a30-cabled); [GNB 850 mAh 1S 60C HV A30 (Rotorama)](https://www.rotorama.com/product/gnb-850mah-1s-60c-hv-a30); [GNB 720 mAh 1S HV A30 (Rotorama)](https://www.rotorama.com/product/gnb-720mah-1s-100c-hv-a30); [GNB 660 mAh 1S PH2.0 (NewBeeDrone)](https://newbeedrone.com/a/p/products/gnb-660mah-1s-3-8v-hv-90c-lipo-battery-ph-2-1); [BetaFPV BT2.0 550 mAh 1S](https://betafpv.com/collections/parts-spares/products/bt2-0-550mah-1s-battery-4pcs); [BetaFPV BT2.0 vs PH2.0 current ratings](https://betafpv.com/collections/all/products/bt2-0-260mah-1s-30c-battery-8pcs).

## 6. Power and weight budget

With the recommended 850 mAh pack the drone weighs about 60 g and hovers on roughly 4 to 5 A, which gives about 8 to 10 minutes. All figures are estimates to replace after weighing parts and a thrust test.

| Part | Approx. weight |
| --- | --- |
| XIAO ESP32-S3 + Sense camera board + antenna + microSD card | 6.3 g |
| Shield PCB with parts, female headers and XIAO pin headers | 4.6 g (protection MOSFET and LED add about 0.1 g) |
| 4 x 720 motors | 16 to 20 g (listings say 3 to 5 g each) |
| 4 x 65 mm props | 1.6 g |
| Frame + ring guards (printed) | 10 g |
| Camera mount, wiring, battery pigtail | 1.5 g |
| **Dry weight** | **about 42 g** |
| GNB 850 mAh 1S battery | 17.5 g |
| **All-up weight** | **about 60 g** |

| Load | Typical current |
| --- | --- |
| XIAO ESP32-S3 Sense, streaming camera video over Wi-Fi | about 0.2 to 0.3 A |
| IMU + regulator + status LED | about 0.01 A |
| microSD card while writing | up to about 0.1 A |
| **Electronics total** | **about 0.3 to 0.4 A (1.1 to 1.5 W)** |
| 4 x 720 motors, hovering | about 3.4 to 4.6 A |
| **Total while hovering** | **about 3.7 to 4.9 A** |
| All 4 motors at full throttle (brief) | up to about 8 A |

The electronics use only about 7 to 9% of the power; the motors decide the flight time. The full-throttle peak of about 8 A is why the battery connector must be A30 or BT2.0 (XD-B2), and why the reverse polarity MOSFET must be a low-resistance power part: at 8 A it drops under 80 mV and loses under 0.7 W, about 2% of the power, briefly.

## 7. Bill of materials

Two lists: what JLC assembles onto each shield, and what you buy and fit yourself. Part numbers marked as JLC matches come from the 14 Nov BOM check; pick the rest in JLC's library before uploading.

### 7.1 Shield PCBA (per board, assembled by JLC)

| Designator | Part | Value / type | JLC part # | Qty | Package |
| --- | --- | --- | --- | --- | --- |
| U1 | IMU | ST LSM6DS3TR-C | C967633 (matched) | 1 | LGA-14 2.5 x 3 mm |
| U2 | 3.3 V LDO | XC6206P332MR-G | C5446 (basic) | 1 | SOT-23 |
| Q1-Q4 | Motor MOSFET | AO3400A, 30 V | C20917 (matched) | 4 | SOT-23 |
| D1-D4 | Flyback diode | Schottky, 3 A 40 V (e.g. SS34) | pick in JLC library | 4 | SMA |
| R1-R4 | Gate resistor | 100 ohm | basic part | 4 | 0402 |
| R5-R8 | Gate pull-down | 100 kohm | basic part | 4 | 0402 |
| R9-R10 | Battery divider, VBAT\_P to D4 | 100 kohm | basic part | 2 | 0402 |
| R11 | IMU\_CS pull-up | 10 kohm | basic part | 1 | 0402 |
| C1-C5 | Decoupling + divider filter | 100 nF | basic part | 5 | 0402 |
| — | IMU INT1 to D5 | trace only, no parts | — | — | — |
| C6-C7 | LDO in/out | 10 uF | basic part | 2 | 0603 |
| C8-C11 | Bulk on VBAT\_P | 22 uF (25 V) | C45783 (matched) | 4 | 0805 |
| Q5 | Reverse polarity MOSFET | DMP2008UFG-7, P-ch 20 V 14 A, 9.8 mohm at -2.5 V | C461052 (extended) | 1 | PowerDI3333-8 |
| R12 | Q5 gate to ground | 10 kohm | basic part | 1 | 0402 |
| LED1 | Status LED | Red, 0603 (KENTO KT-0603R, Vf about 2 V, about 1.3 mA with R13) | C2286 (basic) | 1 | 0603 |
| R13 | LED1 series resistor | 1 kohm | basic part | 1 | 0402 |
| R14 | IMU LDO feed: ripple filter with C6, and a link you can lift to isolate the IMU branch | 22 ohm | C25092 (basic) | 1 | 0402 |
| J1-J2 | XIAO sockets | 1 x 7 female header, 2.54 mm | pick in JLC library | 2 | Through-hole |
| — | Motor pads, battery pads | copper pads only | — | — | — |

### 7.2 Bought parts (for 3 drones)

| Item | Qty | Notes |
| --- | --- | --- |
| Seeed XIAO ESP32-S3 Sense, pin headers soldered | 3 (+1 spare) | Plugs into J1-J2; keep the U.FL antenna fitted; leave J3 on the Sense board joined so the microSD works |
| microSD cards, 8 to 32 GB, Class 10 | 3 | One per drone for flight logs |
| JLC order: 5 assembled shields | 1 order | 3 drones + 1 spare + 1 bench board |
| 720 coreless motors (2 CW + 2 CCW per drone) | 16 | 12 + 4 spares; brushed motors wear out |
| 65 mm props, sets of 4 | 6 | 55 mm sets as a fallback |
| GNB 1S LiHV 850 mAh, A30 or BT2.0 | 8 | 2 per drone + 2 spares |
| Battery pigtails, matching connector | 5 | Soldered to the shield's battery pads |
| LiHV charger, multi-port, matching connector | 1 | Must charge to 4.35 V |
| Frame, prop guards and camera mount | 3 | 3D printed |
| Soldering iron + solder + flux | 1 | Required: motors and pigtails solder to pads |
| Android phone | 1 | Your own; runs the app |
| Bluetooth gamepad (optional) | 1 | Real sticks instead of on-screen ones |

## 8. Budget plan

Three drones come to about **$540 AUD**, spent in three steps so the riskiest parts are proven before the big orders. Battery prices are converted from the listings in section 5; everything else is an approximate estimate to replace with real quotes.

| Item | Qty | Approx. each (AUD) | Approx. total (AUD) |
| --- | --- | --- | --- |
| XIAO ESP32-S3 Sense with headers | 4 | $30 | $120 |
| JLC order: 5 assembled shields incl. fees and shipping (protection MOSFET and LED add about $15) | 1 | $115 | $115 |
| 720 coreless motors | 16 | $4 | $64 |
| 65 mm props, sets of 4 | 6 | $3 | $18 |
| GNB 1S LiHV 850 mAh | 8 | $11 | $88 |
| Battery pigtails | 5 | $2 | $10 |
| LiHV multi-port charger | 1 | $35 | $35 |
| Frame, guards and camera mount (filament) | 3 | $5 | $15 |
| Soldering iron, solder, flux | 1 | $50 | $50 |
| microSD cards | 3 | $8 | $24 |
| **Total** |  |  | **$539** |
| Bluetooth gamepad (optional) | 1 | $30 to $50 | not included |

### Spending in steps

| Step | When | What | Approx. (AUD) |
| --- | --- | --- | --- |
| 1. Bench kit | Week 1 | 1 XIAO, 8 motors, 2 prop sets, 2 batteries, charger, iron. Thrust test and a video-delay test on the bare XIAO before anything else | about $175 |
| 2. Boards | Week 2 | JLC shield order, 3 more XIAO boards | about $205 |
| 3. Fleet | Weeks 3 to 4 | Remaining motors, props and batteries, pigtails, frames, microSD cards | about $159 |

### Ways to cut it

- Skip the spare XIAO: saves $30.
- Reuse microSD cards you already have: saves $24.
- 6 batteries instead of 8: saves $22.
- Fly with the on-screen sticks and skip the gamepad: saves $30 to $50.
- Build 2 drones first and the third once the design works: defers about $120.

## 9. Risks, open issues and bring-up tests

The biggest unknown is whether 720 motors with 65 mm props lift a 60 g drone with enough margin; the week 1 thrust test settles it before any boards are ordered.

| Risk / open issue | Impact | Mitigation |
| --- | --- | --- |
| 720 + 65 mm props give less than 30 g thrust per motor | Sluggish or unsafe flight | Week 1 thrust test on a kitchen scale; try 55 mm props; cut weight (lighter frame, 720 mAh pack) |
| Brushed motors wear and lose thrust | Shorter flights, drift | Log flight minutes per motor; 4 spare motors; swap at the first drop in thrust |
| XIAO works loose in its sockets from vibration | Mid-air reset | Printed clip or hot glue on the header ends (XD-S3) |
| How the XIAO gets battery power (XD-S15) | Brown-outs or uncontrolled USB backfeed | Resolved from Seeed's schematic: feed BAT+ (P-FET, about 0.05 V drop) rather than the 5V pin (internal Schottky); confirm with B7 on the bench with motors running |
| Female headers add height under the shield | Camera or antenna clashes with the frame | 3D-model the stack before ordering (XD-S4) |
| Battery connector choice (A30 vs BT2.0) | Packs and pigtails don't match | Pick one type for every pack, pigtail and the charger |
| Wi-Fi video delay too long to fly by | Hard to fly FPV; crashes | Measure delay on the bare XIAO in week 1; lower resolution and JPEG quality; fly slowly in angle mode |
| Video streaming disturbs the flight control loop | Wobbles or twitches in flight | Flight control pinned to its own core at high priority (XD-V9); check loop timing with video on and off |
| Wi-Fi interference or dropouts in busy buildings | Lost control | Link-loss failsafe (XD-V6); pick a quiet Wi-Fi channel; keep the U.FL antenna fitted and clear of the battery |
| Flying FPV outdoors without approval | Breaks CASA rules | Indoors only, or join an approved model aircraft association (XD-L1) |
| SD card writes hold the shared SPI bus while the flight loop needs the IMU | Missed gyro samples; wobbles | IMU FIFO + data-ready interrupt (XD-S18, XD-S23); small low-priority writes; test B15 with logging on |
| SD card left selected (GPIO21 low) during IMU reads, e.g. by using the built-in LED as a status light | Garbage IMU data | Built-in LED reserved for SD activity; GPIO21 driven high at boot; status on the shield LED (XD-S22, XD-S25) |
| No spare GPIO left on the headers | No room for another sensor later | Future additions go over I2C on spare pads, or share the SPI bus with another chip select from a GPIO expander |
| Protection MOSFET runs hot at full throttle | Heat near the battery pads; slightly lower voltage | Low-resistance part on copper pours (XD-S20); check its temperature in B14 |

- [ ] **B1 Thrust test:** one 720 motor + 65 mm prop on a scale; 30 g or more at full throttle from a charged pack.
- [ ] **B2 Power-up:** shield on a current-limited bench supply at 3.7 V, no XIAO fitted; 3.3 V rail reads 3.2 to 3.4 V.
- [ ] **B13 Reverse polarity:** no XIAO fitted, bench supply at 4.2 V limited to 100 mA, connected backwards for 5 s; under 1 mA flows and the shield then powers up normally the right way round. Repeat once with the XIAO fitted.
- [ ] **B3 XIAO fitted:** boots from the battery; motors stay still through power-up and reset.
- [ ] **B4 USB alone:** with USB plugged in and no battery, the battery pads read at most 4.2 V (the XIAO's charger) and no motor moves; with a battery fitted, it charges at about 110 mA (the XIAO's charge LED is on). Firmware refuses to arm while USB is connected.
- [ ] **B5 IMU:** reads its ID over SPI; gyro reads near zero when still; INT1 on D5 fires at the set data rate (count interrupts for 10 s).
- [ ] **B6 Motors:** each spins the right way at 10, 50 and 100% PWM; MOSFETs stay under 80 °C after 10 s at full.
- [ ] **B14 Protection MOSFET:** all motors at full for 10 s; voltage across Q5 under 100 mV and Q5 under 80 °C.
- [ ] **B15 SD card with IMU:** SD card mounts; write a log at 100 Hz for 5 min with the camera streaming; no IMU read errors, no missed INT1 samples, log file reads back on a PC.
- [ ] **B16 Status LED:** the shield LED shows armed, link lost and low battery; the built-in LED blinks only with SD activity.
- [ ] **B7 Brown-out:** all motors at full while the supply drops to 3.0 V; the XIAO does not reset.
- [ ] **B8 Hover:** 60 s stable hover on a tether; then a full-battery hover to measure real flight time.
- [ ] **B9 Video delay:** film a stopwatch on a screen and the phone side by side; delay under 200 ms.
- [ ] **B10 Link-loss failsafe:** switch the phone's Wi-Fi off mid-hover; the drone levels, descends and disarms.
- [ ] **B11 Loop timing:** flight loop rate unchanged with video streaming on and off.
- [ ] **B12 Range:** video and control stay usable at 30 m indoors.
