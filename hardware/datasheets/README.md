# Datasheets

Official datasheets and schematics for the parts in [shield/bom/shield-bom.csv](../shield/bom/shield-bom.csv) and the XIAO boards the shield is built around. Downloaded 2026-11-26. Where the manufacturer's site blocked downloads, the LCSC copy for the exact LCSC part number (or a distributor copy of the maker's own document) is used and the table says so.

## Shield parts

| Part | BOM ref(s) | LCSC # | File | Source URL |
| --- | --- | --- | --- | --- |
| LSM6DS3TR-C IMU (ST) | U1 | C967633 | [ics/lsm6ds3tr-c-datasheet.pdf](ics/lsm6ds3tr-c-datasheet.pdf) | https://www.st.com/resource/en/datasheet/lsm6ds3tr-c.pdf |
| LSM6DS3TR-C application note AN5130 (ST) | U1 | C967633 | [ics/lsm6ds3tr-c-an5130-application-note.pdf](ics/lsm6ds3tr-c-an5130-application-note.pdf) | https://www.st.com/resource/en/application_note/an5130-lsm6ds3trc-alwayson-3d-accelerometer-and-3d-gyroscope-stmicroelectronics.pdf |
| ME6211C33M5G-N LDO (Microne), no longer used: replaced by XC6206 (decision D2) | — | C82942 | [ics/me6211-ldo-datasheet.pdf](ics/me6211-ldo-datasheet.pdf) | LCSC copy: https://datasheet.lcsc.com/datasheet/pdf/d15331d096a848ac81a26b001a32d4e3.pdf?productCode=C82942 |
| XC6206P332MR LDO (Torex) | U2 | C5446 | [ics/xc6206-ldo-datasheet.pdf](ics/xc6206-ldo-datasheet.pdf) | https://product.torexsemi.com/system/files/series/xc6206.pdf |
| SGM6029 buck regulator (SG Micro), on the XIAO ESP32-S3 itself, not on the shield | (XIAO U3) | — | [ics/sgm6029-buck-datasheet.pdf](ics/sgm6029-buck-datasheet.pdf) | https://www.sg-micro.com/product/SGM6029 |
| AO3400A N-MOSFET (Alpha & Omega) | Q1, Q2, Q3, Q4 | C20917 | [discretes/ao3400a-nmos-datasheet.pdf](discretes/ao3400a-nmos-datasheet.pdf) | https://www.aosmd.com/res/datasheets/AO3400A.pdf |
| DMP2008UFG-7 P-MOSFET (Diodes Inc) | Q5 | C461052 | [discretes/dmp2008ufg-pmos-datasheet.pdf](discretes/dmp2008ufg-pmos-datasheet.pdf) | https://www.diodes.com/assets/Datasheets/DMP2008UFG.pdf |
| SS34 Schottky, SMA (MDD Microdiode) | D1, D2, D3, D4 | C8678 | [discretes/ss34-mdd-schottky-datasheet.pdf](discretes/ss34-mdd-schottky-datasheet.pdf) | LCSC copy: https://datasheet.lcsc.com/datasheet/pdf/dfa1ff67dea875d0135103ba9ada713a.pdf?productCode=C8678 |
| 0402WGF thick film resistors, 100R / 100k / 10k / 1k / 22R (UNI-ROYAL); one series datasheet covers all five | R1-R4 / R5-R10 / R11, R12 / R13 / R14 | C25076, C25741, C25744, C11702, C25092 | [passives/uniroyal-0402wgf-thick-film-resistor-datasheet.pdf](passives/uniroyal-0402wgf-thick-film-resistor-datasheet.pdf) | LCSC copy: https://datasheet.lcsc.com/datasheet/pdf/0a975aaa49b7c97f38a963127be4a823.pdf?productCode=C25076 |
| Samsung CL-series MLCC catalog: CL05B104KO5NNNC 100nF, CL10A106KP8NNNC 10uF, CL21A226MAQNNNE 22uF; one catalog covers all three | C1-C5 / C6, C7 / C8-C12 | C1525, C19702, C45783 | [passives/samsung-cl-series-mlcc-datasheet.pdf](passives/samsung-cl-series-mlcc-datasheet.pdf) | LCSC copy: https://datasheet.lcsc.com/datasheet/pdf/02336ea48ea44ca18c72517dd3cb7b47.pdf?productCode=C1525 |
| KT-0603R red 0603 LED (Hubei KENTO) | LED1 | C2286 | not stored, link only | JLC copy: https://jlcpcb.com/api/file/downloadByFileSystemAccessId/8763907065070653440 |

## Boards and modules

| Part | BOM ref(s) | LCSC # | File | Source URL |
| --- | --- | --- | --- | --- |
| ESP32-S3 SoC datasheet (Espressif) | XIAO module | - | [ics/esp32-s3-datasheet.pdf](ics/esp32-s3-datasheet.pdf) | https://documentation.espressif.com/esp32-s3_datasheet_en.pdf |
| XIAO ESP32S3 schematic v1.2 (Seeed) | XIAO module | - | [boards/xiao-esp32s3/xiao-esp32s3-schematic-v1.2.pdf](boards/xiao-esp32s3/xiao-esp32s3-schematic-v1.2.pdf) | https://files.seeedstudio.com/wiki/SeeedStudio-XIAO-ESP32S3/res/XIAO_ESP32S3_SCH_v1.2.pdf |
| XIAO ESP32S3 schematic v1.4, current on the wiki (Seeed) | XIAO module | - | [boards/xiao-esp32s3/xiao-esp32s3-schematic-v1.4.pdf](boards/xiao-esp32s3/xiao-esp32s3-schematic-v1.4.pdf) | https://files.seeedstudio.com/wiki/SeeedStudio-XIAO-ESP32S3/new-res/202003751_XIAO%20ESP32S3_v1.4_SCH_260226.pdf.pdf |
| XIAO ESP32S3 Sense schematic v1.51 (Seeed) | XIAO module | - | [boards/xiao-esp32s3/xiao-esp32s3-sense-schematic-v1.51.pdf](boards/xiao-esp32s3/xiao-esp32s3-sense-schematic-v1.51.pdf) | https://files.seeedstudio.com/wiki/SeeedStudio-XIAO-ESP32S3/new-res/202003753_XIAO%20ESP32S3%20Sense_V1.51_SCH_260611.pdf |
| XIAO ESP32S3 Sense expansion board schematic v1.0 (Seeed) | XIAO module | - | [boards/xiao-esp32s3/xiao-esp32s3-sense-expansion-board-schematic-v1.0.pdf](boards/xiao-esp32s3/xiao-esp32s3-sense-expansion-board-schematic-v1.0.pdf) | https://files.seeedstudio.com/wiki/SeeedStudio-XIAO-ESP32S3/res/XIAO_ESP32S3_ExpBoard_v1.0_SCH.pdf |
| XIAO ESP32S3 Sense expansion board schematic v1.2, current on the wiki (Seeed) | XIAO module | - | [boards/xiao-esp32s3/xiao-esp32s3-sense-expansion-board-schematic-v1.2.pdf](boards/xiao-esp32s3/xiao-esp32s3-sense-expansion-board-schematic-v1.2.pdf) | https://files.seeedstudio.com/wiki/SeeedStudio-XIAO-ESP32S3/res/XIAO_ESP32S3_Exp_Board_v1.2_SCH_PDF_260810.pdf |
| XIAO ESP32S3 Sense pinout, front (Seeed) | XIAO module | - | [boards/xiao-esp32s3/xiao-esp32s3-sense-pinout-front.png](boards/xiao-esp32s3/xiao-esp32s3-sense-pinout-front.png) | https://files.seeedstudio.com/wiki/SeeedStudio-XIAO-ESP32S3/img/XIAO_ESP32-S3_Sense_front_pinout.png |
| XIAO ESP32S3 Sense pinout, back (Seeed) | XIAO module | - | [boards/xiao-esp32s3/xiao-esp32s3-sense-pinout-back.png](boards/xiao-esp32s3/xiao-esp32s3-sense-pinout-back.png) | https://files.seeedstudio.com/wiki/SeeedStudio-XIAO-ESP32S3/img/XIAO_ESP32-S3_Sense_back_pinout.png |
| XIAO ESP32S3 Sense pinout sheet (Seeed) | XIAO module | - | [boards/xiao-esp32s3/xiao-esp32s3-sense-pinout.xlsx](boards/xiao-esp32s3/xiao-esp32s3-sense-pinout.xlsx) | https://files.seeedstudio.com/wiki/SeeedStudio-XIAO-ESP32S3/res/XIAO_ESP32S3_Sense_Pinout.xlsx |
| XIAO nRF52840 schematic, 2026-08 revision (Seeed) | Alternative MCU | - | [boards/xiao-nrf52840/xiao-nrf52840-schematic-260828.pdf](boards/xiao-nrf52840/xiao-nrf52840-schematic-260828.pdf) | https://files.seeedstudio.com/wiki/XIAO-BLE/Res/260828_XIAO_nRF52840.pdf |
| XIAO nRF52840 schematic + PCB, v1.1 (Seeed) | Alternative MCU | - | [boards/xiao-nrf52840/xiao-nrf52840-sch-pcb.pdf](boards/xiao-nrf52840/xiao-nrf52840-sch-pcb.pdf) | https://files.seeedstudio.com/wiki/XIAO-BLE/Seeed_Studio_XIAO_nRF52840_PDF.pdf |
| XIAO nRF52840 Sense pinout, front (Seeed) | Alternative MCU | - | [boards/xiao-nrf52840/xiao-nrf52840-sense-pinout-front.png](boards/xiao-nrf52840/xiao-nrf52840-sense-pinout-front.png) | https://files.seeedstudio.com/wiki/XIAO-BLE/XIAO_nRF52840_Sense_front_pinout.png |
| XIAO nRF52840 Sense pinout, back (Seeed) | Alternative MCU | - | [boards/xiao-nrf52840/xiao-nrf52840-sense-pinout-back.png](boards/xiao-nrf52840/xiao-nrf52840-sense-pinout-back.png) | https://files.seeedstudio.com/wiki/XIAO-BLE/XIAO_nRF52840_Sense_back_pinout.png |
| XIAO nRF52840 Sense pinout sheet (Seeed) | Alternative MCU | - | [boards/xiao-nrf52840/xiao-nrf52840-sense-pinout.xlsx](boards/xiao-nrf52840/xiao-nrf52840-sense-pinout.xlsx) | https://files.seeedstudio.com/wiki/XIAO-BLE/XIAO-nRF52840-Senese-pinout_sheet.xlsx |

## Not downloaded / notes

- **ESP32-S3 Technical Reference Manual**: 15.2 MB, over the ~15 MB limit, so not stored. Get it from https://documentation.espressif.com/esp32-s3_technical_reference_manual_en.pdf.
- **Seeed XIAO ESP32-S3 Series datasheet**: 29.7 MB, skipped. https://files.seeedstudio.com/wiki/XIAO/Seeed_Studio_XIAO_ESP32-S3_Series_Datasheet-26.11.3.pdf
- **onsemi SS34**: onsemi's datasheet URL now redirects to a "not found" page, so only the MDD datasheet for the actual LCSC part (C8678) is stored.
- **KENTO red LED (C2286)**: replaced the green Everlight 19-217/GHC (C72043) on 2026-11-27 because the green's ~3 V forward voltage leaves almost nothing across R13 at 3.3 V. Key figures (from JLC's listing): Vf 1.8–2.4 V, 20 mA max, 615–630 nm.
- **ME6211, SS34, resistors and MLCCs**: these come from LCSC because the makers (Microne, MDD, UNI-ROYAL, Samsung) don't offer a stable direct link. The Samsung file is the general CL-series catalog; look up each part number in it.
- The non-Sense XIAO nRF52840 pinout images and the KiCad/Eagle source zips on the Seeed wiki were not downloaded.
- The XIAO ESP32S3 schematic and expansion board come in both the older revisions that were asked for (v1.2 / v1.0) and the current wiki revisions (v1.4 / v1.2). Check which revision your board is before reading pin details.
