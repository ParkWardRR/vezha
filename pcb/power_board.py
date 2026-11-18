"""Vezha power board — netlist, generated from docs/06-power-board-schematic.md.

Run:
    cad/.venv/bin/python pcb/power_board.py

Writes `pcb/build/vezha-power.net` (KiCad netlist) and prints an ERC report.

WHY THIS IS CODE AND NOT A DRAWN SCHEMATIC
------------------------------------------
06 is already a complete, reviewed net specification with reference
designators, verified module pinouts, a Pico pin map and six passing ngspice
decks. Re-drawing it by hand would be transcription, and transcription is
where net errors come from. This file is the transcription, done once, in a
form that diffs against the document.

SCOPE OF REV A — read this before assuming the netlist is complete
------------------------------------------------------------------
**The accessory USB-C port (U4, U5, R3–R6, J6) is NOT in this netlist.**

That is 06's own position, not a shortcut taken here:

  * 06 §Reference designators: U4's and U5's support passives "are not
    enumerated here — they come from the TI datasheets' typical-application
    tables once the switching frequency and output capacitance are fixed, and
    they should be taken from the datasheet rather than invented."
  * Neither LMR38020 nor TPS2553 has a symbol in the installed KiCad
    libraries, so their pin numbering would have to be invented too. Wrong
    pin numbers on a 80 V buck is precisely the silent fault that destroys a
    board.

Everything 06 *does* fully specify is here. The accessory branch needs a
datasheet pass first; see "What is still open" at the end of 06.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

from skidl import (
    ERC, KICAD9, SKIDL, Net, Part, Pin, generate_netlist, lib_search_paths,
    reset, set_default_tool,
)

KICAD_SYMBOLS = "/Applications/KiCad/KiCad.app/Contents/SharedSupport/symbols"
BUILD = Path(__file__).parent / "build"

# The mechanical model owns the Pico mounting decision; the board must follow
# it, not restate it. 03: "pick one, it changes the height."
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "cad"))
from params import B as _B  # noqa: E402

PICO_FP = ("Module:RaspberryPi_Pico_Common_THT" if _B.PICO_MOUNT == "socketed"
           else "Module:RaspberryPi_Pico_SMD_HandSolder")

# -----------------------------------------------------------------------
# Footprints
# -----------------------------------------------------------------------
FP_R0603 = "Resistor_SMD:R_0603_1608Metric"
FP_C0603 = "Capacitor_SMD:C_0603_1608Metric"
FP_R2512 = "Resistor_SMD:R_2512_6332Metric"       # R13, the 2 mohm shunt
FP_SMA = "Diode_SMD:D_SMA"
#: INA226AIDGSR is TI's DGS = VSSOP-10, 3x3 mm, 0.5 mm pitch, no exposed pad.
#: KiCad files that land pattern under MSOP-10. Verify against the TI drawing
#: before fabrication -- the HVSSOP/-1EP variants are NOT the same part.
FP_VSSOP10 = "Package_SO:MSOP-10_3x3mm_P0.5mm"
FP_HDR = "Connector_PinHeader_2.54mm:PinHeader_1x0{n}_P2.54mm_Vertical"
FP_HDR_2X6 = "Connector_PinHeader_2.54mm:PinHeader_2x06_P2.54mm_Vertical"
FP_HDR_1X8 = "Connector_PinHeader_2.54mm:PinHeader_1x08_P2.54mm_Vertical"
FP_JST_SH4 = "Connector_JST:JST_SH_SM04B-SRSS-TB_1x04-1MP_P1.00mm_Horizontal"
#: 6-contact power-only USB-C, matching the PowerOnly_6P symbol.
#: 06 warns separately that J6's HRO 16-pin part must be checked against its
#: drawing -- that applies to the deferred accessory port, not to this one.
FP_USBC_6P = "Connector_USB:USB_C_Receptacle_GCT_USB4125-xx-x_6P_TopMnt_Horizontal"
FP_SOIC8_EP = "Package_SO:SOIC-8-1EP_3.9x4.9mm_P1.27mm_EP2.95x4.9mm_Mask2.34x2.34mm"
FP_SOT23_6 = "Package_TO_SOT_SMD:SOT-23-6"
FP_IND = "Inductor_SMD:L_7.3x7.3_H4.5"
FP_C1210 = "Capacitor_SMD:C_1210_3225Metric"
FP_C0805 = "Capacitor_SMD:C_0805_2012Metric"
#: 06 names HRO TYPE-C-31-M-12 (LCSC C165948) and warns it must be checked
#: against the drawing. KiCad ships that exact part, so this is the real
#: footprint rather than a generic 16P stand-in.
FP_USBC_16P = "Connector_USB:USB_C_Receptacle_HRO_TYPE-C-31-M-12"

# =======================================================================
# UNVERIFIED PIN MAPS — the one place to fix when the real boards arrive
# =======================================================================
# Same discipline as cad/params.py: a number nobody has confirmed lives in
# exactly one marked place, never inline.

#: U3 Pololu D42V55F5. 06 §U3: "The exact left-to-right pin order within each
#: row is still not legible at the published resolution. Take it from the
#: physical board or the STEP model, and remember Pololu's own warning that
#: EN and PG are adjacent on different rows and easy to short together."
#:
#: PROVISIONAL. Do not fabricate a carrier against this without checking it.
U3_PINS_PROVISIONAL = True
U3 = {
    "VIN_A": 1, "VIN_B": 2,
    "GND_A": 3, "GND_B": 4,
    "VOUT_A": 5, "VOUT_B": 6,
    "EN": 7,
    "PG": 8,
    "GND_C": 9, "GND_D": 10,
    "VOUT_C": 11, "VOUT_D": 12,
}

#: U4 TI LMR38020FDDAR, 8-pin HSOIC with PowerPAD (DDA).
#: CONFIRMED from the datasheet: GND=1, EN=2, BOOT=7, SW=8, and BOOT takes a
#: 100 nF cap to SW. The remaining four (VIN, FB, RT/SYNC, PG) were not
#: readable in a form I could confirm, so they are ASSUMED here.
#: Check section 6 of SNVSC40E before fabricating -- a wrong VIN pin on an
#: 80 V part is a destroyed board, not a rework.
U4_PINS_ASSUMED = True
U4 = {
    "GND": 1, "EN": 2,                      # confirmed
    "RT": 3, "FB": 4, "PG": 5, "VIN": 6,    # ASSUMED ordering
    "BOOT": 7, "SW": 8,                     # confirmed
}

#: U5 TI TPS2553DBVR, SOT-23-6 (DBV). CONFIRMED from the datasheet:
#: IN=1, GND=2, EN=3, FAULT=4, ILIM=5, OUT=6.
#: Also confirmed: the TPS2553 is the ACTIVE-HIGH enable variant (the TPS2552
#: is active low). That agrees with 06's pin map calling GP8 "EN (active
#: high)", so the part number and the pin map are consistent.
U5 = {"IN": 1, "GND": 2, "EN": 3, "FAULT": 4, "ILIM": 5, "OUT": 6}

#: U1 RotoPD Pro 1x8 header. 06 §U1 — VERIFIED from the vendor pinout artwork.
U1 = {
    "USB_DM": 1, "USB_DP": 2, "INT": 3, "SDA": 4,
    "SCL": 5, "V3V3": 6, "GND": 7, "V5V_AUX": 8,
}


def build_netlist():
    reset()
    set_default_tool(KICAD9)
    if KICAD_SYMBOLS not in lib_search_paths[KICAD9]:
        lib_search_paths[KICAD9].append(KICAD_SYMBOLS)

    # -- Nets, named exactly as 06 §Power domains names them ---------------
    gnd      = Net("GND")
    vbus_pd  = Net("VBUS_PD")     # 4.5-48 V, 5 A  — RotoPD switched output
    v5_rtr   = Net("+5V_RTR")     # 5.0 V +-3 %, 4 A to the Pi
    v5_rtr_s = Net("+5V_RTR_SH")  # between the shunt and the seam connector
    v5_aux   = Net("+5V_AUX")     # 0.4 A continuous — controller only
    vsys     = Net("VSYS")        # 4.58-4.75 V after D1
    v3v3     = Net("+3V3")        # <=300 mA from the Pico's own regulator

    n_en   = Net("U3_EN")
    n_pg   = Net("U3_PG")
    n_int  = Net("U1_INT")
    sda1, scl1 = Net("I2C1_SDA"), Net("I2C1_SCL")   # rail-critical
    sda0, scl0 = Net("I2C0_SDA"), Net("I2C0_SCL")   # reporting only
    n_ntc  = Net("NTC_SENSE")

    # =====================================================================
    # Modules
    # =====================================================================
    # U2 — Pico 2 (non-wireless). The _Debug variant exposes SWCLK/SWDIO,
    # which J7 needs. 06's pin map was cross-checked against this symbol:
    # all 19 used pins agree.
    u2 = Part("MCU_Module", "RaspberryPi_Pico_Debug", ref="U2",
              value="RaspberryPi Pico 2", footprint=PICO_FP)

    # U1 — RotoPD Pro, landed as its 1x8 2.54 mm header.
    # 06 §U1: use the header OR the Qwiic connector, not both.
    u1 = Part("Connector_Generic", "Conn_01x08", ref="U1",
              value="RotoPD Pro hdr", footprint=FP_HDR_1X8)
    # The switched VBUS output. DECIDED 2026-11-18: the 2-position screw
    # terminal is REMOVED and heavy wire is soldered to its pads, so this is
    # a 2-pad landing, not a connector. See cad/params.py B.ROTOPD_SCREW_TERMINAL.
    u1p = Part("Connector_Generic", "Conn_01x02", ref="U1P",
               value="RotoPD VBUS pads", footprint=FP_HDR.format(n=2))

    # U3 — Pololu D42V55F5 (or F5.3; 06 leaves the part number open).
    u3 = Part("Connector_Generic", "Conn_02x06_Odd_Even", ref="U3",
              value="Pololu D42V55F5", footprint=FP_HDR_2X6)

    # U6 — INA226, router rail V and I.
    u6 = Part("Sensor_Energy", "INA226", ref="U6", value="INA226AIDGSR",
              footprint=FP_VSSOP10)

    d1 = Part("Diode", "SS14", ref="D1", value="SS14", footprint=FP_SMA)

    # =====================================================================
    # Passives — values are load-bearing, see the sim decks named in 06
    # =====================================================================
    def R(ref, val, fp=FP_R0603):
        return Part("Device", "R", ref=ref, value=val, footprint=fp)

    def C(ref, val):
        return Part("Device", "C", ref=ref, value=val, footprint=FP_C0603)

    r1  = R("R1", "1.5k")    # U3 EN pull-down — SIM-01. NOT 10k, NOT 100k.
    r2  = R("R2", "10k")     # U3 PG pull-up (Pololu says 100k; 06 chooses 10k)
    r13 = R("R13", "2m", FP_R2512)   # INA226 shunt, 2512
    r14 = R("R14", "220")    # telemetry TX series
    r15 = R("R15", "220")    # telemetry RX series
    r16 = R("R16", "10k")    # NTC divider top leg

    # Encoder: pull-up, series, cap — per channel. SIM-05 fixes 100 nF.
    r7, r8, r9    = R("R7", "10k"), R("R8", "10k"), R("R9", "10k")
    r10, r11, r12 = R("R10", "1k"), R("R11", "1k"), R("R12", "1k")
    c1, c2, c3    = C("C1", "100n"), C("C2", "100n"), C("C3", "100n")

    rt1 = Part("Device", "Thermistor_NTC", ref="RT1",
               value="10k NCP18XH103F03RB", footprint=FP_R0603)

    # JP1 — 0 R jumper, DNP in Rev A. 06 §U1 caution: it is undocumented
    # whether U1 pin 6 is an input or an output, so this must not be fitted
    # until it is measured on the bench.
    jp1 = R("JP1", "0R DNP")

    # =====================================================================
    # Connectors
    # =====================================================================
    j1 = Part("Connector_Generic", "Conn_01x04", ref="J1", value="Qwiic to U1 (alt)", footprint=FP_JST_SH4)
    j2 = Part("Connector", "USB_C_Receptacle_PowerOnly_6P", ref="J2",
              value="seam out", footprint=FP_USBC_6P)
    j3 = Part("Connector_Generic", "Conn_01x03", ref="J3", value="telemetry", footprint=FP_HDR.format(n=3))
    j4 = Part("Connector_Generic", "Conn_01x04", ref="J4", value="OLED STEMMA QT", footprint=FP_JST_SH4)
    j5 = Part("Connector_Generic", "Conn_01x04", ref="J5", value="EC11 encoder", footprint=FP_HDR.format(n=4))
    j7 = Part("Connector_Generic", "Conn_01x03", ref="J7", value="SWD", footprint=FP_HDR.format(n=3))

    # =====================================================================
    # Nets — each block cites the 06 section it comes from
    # =====================================================================

    # --- 06 §Aux 5 V -> VSYS ---------------------------------------------
    # D1 is mandatory: it blocks the programming-port back-feed AND buys
    # VSYS headroom. Do NOT also short VBUS to VSYS on the Pico.
    u1[U1["V5V_AUX"]] += v5_aux
    v5_aux += d1["A"]
    d1["K"] += vsys
    vsys += u2["VSYS"]
    u1[U1["GND"]] += gnd

    # --- 06 §I2C bus allocation ------------------------------------------
    # I2C1 is rail-critical: PD control plus the current measurement the
    # shutdown decision depends on. I2C0 is reporting only.
    u2["GPIO2"] += sda1
    u2["GPIO3"] += scl1
    u1[U1["SDA"]] += sda1
    u1[U1["SCL"]] += scl1
    u6["SDA"] += sda1
    u6["SCL"] += scl1
    j1[1] += gnd
    j1[2] += v3v3
    j1[3] += sda1
    j1[4] += scl1

    u2["GPIO4"] += sda0
    u2["GPIO5"] += scl0
    j4[1] += gnd
    j4[2] += v3v3
    j4[3] += sda0
    j4[4] += scl0

    # U1 INT -> GP11
    u2["GPIO11"] += n_int
    u1[U1["INT"]] += n_int

    # JP1: +3V3 -> U1 pin 6. DNP until measured.
    v3v3 += jp1[1]
    jp1[2] += u1[U1["V3V3"]]

    # --- 06 §Rail control — U3 EN and PG ---------------------------------
    # GP6 must be a push-pull OUTPUT and never an input.
    u2["GPIO6"] += n_en
    n_en += u3[U3["EN"]], r1[1]
    r1[2] += gnd

    u2["GPIO7"] += n_pg
    n_pg += u3[U3["PG"]], r2[1]
    r2[2] += v3v3

    # --- Main power path --------------------------------------------------
    # 06 §Power domains: VBUS_PD feeds U3 VIN (and U4 VIN, deferred).
    u1p[1] += vbus_pd
    u1p[2] += gnd
    for k in ("VIN_A", "VIN_B"):
        u3[U3[k]] += vbus_pd
    for k in ("GND_A", "GND_B", "GND_C", "GND_D"):
        u3[U3[k]] += gnd
    # 03's rule: use BOTH sets of the duplicated pins for the main path.
    # This is the full router current; a single 2.54 mm contact is not the
    # place to discover its real rating.
    for k in ("VOUT_A", "VOUT_B", "VOUT_C", "VOUT_D"):
        u3[U3[k]] += v5_rtr

    # Shunt in series with the rail, INA226 across it.
    v5_rtr += r13[1]
    r13[2] += v5_rtr_s
    u6["Vin+"] += v5_rtr
    u6["Vin-"] += v5_rtr_s
    u6["Vbus"] += v5_rtr_s
    u6["VS"] += v3v3
    u6["GND"] += gnd
    u6["A0"] += gnd          # address strap — 06: pick one colliding with neither
    u6["A1"] += gnd

    # Seam out to Enclosure A. 5 V power only; nothing else crosses.
    j2["A9"] += v5_rtr_s
    j2["B9"] += v5_rtr_s
    j2["A12"] += gnd
    j2["B12"] += gnd
    j2["SH"] += gnd

    # --- 06 §NTC on U3 (RT1) ---------------------------------------------
    v3v3 += r16[1]
    r16[2] += n_ntc
    n_ntc += rt1[1], u2["GPIO28_ADC2"]
    rt1[2] += gnd

    # --- 06 §Encoder (J5) -------------------------------------------------
    # Pull-up -> contact -> series R -> cap to GND -> GPIO. SIM-05.
    enc = [
        ("A",  r7, r10, c1, "GPIO12", 1),
        ("B",  r8, r11, c2, "GPIO13", 2),
        ("SW", r9, r12, c3, "GPIO14", 3),
    ]
    for name, rpu, rs, cap, gpio, pin in enc:
        raw = Net(f"ENC_{name}_RAW")
        flt = Net(f"ENC_{name}")
        v3v3 += rpu[1]
        rpu[2] += raw
        j5[pin] += raw
        raw += rs[1]
        rs[2] += flt
        flt += cap[1], u2[gpio]
        cap[2] += gnd
    j5[4] += gnd

    # =====================================================================
    # 06 §Accessory USB-C output port (J6) -- Config A
    # =====================================================================
    # 06 leaves "Accessory port config A or B" open and says "A is the
    # recommendation ... A needs nothing; B needs the thermal measurement
    # first". Config A chosen: R3/R4 = 36k, R5 = 22.6k, limit 1.06-1.23 A.
    #
    # U4 and U5 have no KiCad symbols, so they are built here from their
    # datasheet pin tables. U5's is confirmed; U4's middle four pins are the
    # assumption flagged in U4 above.
    #
    # 06 declines to enumerate U4/U5 support passives, saying they "come from
    # the TI datasheets' typical-application tables". Those are computed below
    # from the standard buck equations at the stated operating point, NOT
    # copied from a table I cannot see. Each is marked ASSUMED.
    v5_acc = Net("+5V_ACC")
    sw_node = Net("ACC_SW")
    boot_node = Net("ACC_BOOT")
    fb_node = Net("ACC_FB")
    cc1, cc2 = Net("ACC_CC1"), Net("ACC_CC2")
    n_u4en, n_u5en, n_flt = Net("U4_EN"), Net("U5_EN"), Net("U5_FAULT")

    u4 = Part(name="LMR38020FDDAR", ref="U4", tool=SKIDL, footprint=FP_SOIC8_EP,
              value="LMR38020FDDAR",
              pins=[Pin(num=U4["GND"], name="GND", func=Pin.types.PWRIN),
                    Pin(num=U4["EN"], name="EN", func=Pin.types.INPUT),
                    Pin(num=U4["RT"], name="RT_SYNC", func=Pin.types.INPUT),
                    Pin(num=U4["FB"], name="FB", func=Pin.types.INPUT),
                    Pin(num=U4["PG"], name="PG", func=Pin.types.OPENCOLL),
                    Pin(num=U4["VIN"], name="VIN", func=Pin.types.PWRIN),
                    Pin(num=U4["BOOT"], name="BOOT", func=Pin.types.PASSIVE),
                    Pin(num=U4["SW"], name="SW", func=Pin.types.OUTPUT)])

    u5 = Part(name="TPS2553DBVR", ref="U5", tool=SKIDL, footprint=FP_SOT23_6,
              value="TPS2553DBVR",
              pins=[Pin(num=U5["IN"], name="IN", func=Pin.types.PWRIN),
                    Pin(num=U5["GND"], name="GND", func=Pin.types.PWRIN),
                    Pin(num=U5["EN"], name="EN", func=Pin.types.INPUT),
                    Pin(num=U5["FAULT"], name="FAULT", func=Pin.types.OPENCOLL),
                    Pin(num=U5["ILIM"], name="ILIM", func=Pin.types.INPUT),
                    Pin(num=U5["OUT"], name="OUT", func=Pin.types.PWROUT)])

    # Config A values, straight from 06.
    r3 = R("R3", "36k")      # CC1 Rp to +3V3 -- SIM-03
    r4 = R("R4", "36k")      # CC2 Rp to +3V3 -- SIM-03
    r5 = R("R5", "22.6k")    # R_ILIM -> 1.06/1.14/1.23 A
    r6 = R("R6", "100k")     # FAULT pull-up

    # ASSUMED support passives. Operating point: VIN up to 48 V, VOUT 5.0 V,
    # IOUT 2 A, f_sw 400 kHz.
    #   D = 5/48 = 0.104
    #   L = Vout(1-D)/(f*dI) with dI = 30% of 2 A = 0.6 A  ->  18.7 uH -> 22 uH
    #   FB divider for a 1.0 V reference: Vout = Vref(1+Rt/Rb), Rt/Rb = 4
    #                                     -> 100k / 24.9k
    l1 = Part("Device", "L", ref="L1", value="22u", footprint=FP_IND)
    c4 = Part("Device", "C", ref="C4", value="2.2u/100V", footprint=FP_C1210)
    c5 = Part("Device", "C", ref="C5", value="2.2u/100V", footprint=FP_C1210)
    c6 = Part("Device", "C", ref="C6", value="100n/100V", footprint=FP_C0603)
    c7 = Part("Device", "C", ref="C7", value="47u/16V", footprint=FP_C1210)
    c8 = Part("Device", "C", ref="C8", value="100n", footprint=FP_C0603)
    c9 = Part("Device", "C", ref="C9", value="100n", footprint=FP_C0603)  # BOOT
    r17 = R("R17", "100k")   # RT -- ASSUMED, sets ~400 kHz; check the RT table
    r18 = R("R18", "100k")   # FB top
    r19 = R("R19", "24.9k")  # FB bottom
    r20 = R("R20", "100k")   # U4 PG pull-up
    r21 = R("R21", "200")    # 06: D+/D- shorted, the BC1.2 DCP signature

    j6 = Part("Connector", "USB_C_Receptacle_USB2.0_16P", ref="J6",
              value="accessory out", footprint=FP_USBC_16P)

    # --- U4: VBUS_PD -> +5V_ACC ------------------------------------------
    # 06: "U4 is an 80 V part because VBUS reaches 48 V." A 32 V part would be
    # destroyed by an EPR contract.
    u4["VIN"] += vbus_pd
    u4["GND"] += gnd
    u4["EN"] += n_u4en
    n_u4en += u2["GPIO10"]
    u4["SW"] += sw_node
    u4["BOOT"] += boot_node
    boot_node += c9[1]
    c9[2] += sw_node
    sw_node += l1[1]
    l1[2] += v5_acc
    for c in (c4, c5, c6):
        c[1] += vbus_pd
        c[2] += gnd
    for c in (c7, c8):
        c[1] += v5_acc
        c[2] += gnd
    u4["FB"] += fb_node
    fb_node += r18[2], r19[1]
    r18[1] += v5_acc
    r19[2] += gnd
    u4["RT_SYNC"] += r17[1]
    r17[2] += gnd
    u4["PG"] += r20[1]
    r20[2] += v3v3

    # --- U5: current limit + FAULT ---------------------------------------
    u5["IN"] += v5_acc
    u5["GND"] += gnd
    u5["EN"] += n_u5en
    n_u5en += u2["GPIO8"]
    u5["FAULT"] += n_flt
    n_flt += u2["GPIO9"], r6[1]
    r6[2] += v3v3
    u5["ILIM"] += r5[1]
    r5[2] += gnd

    # --- J6 accessory receptacle ------------------------------------------
    # Power only: no VCONN, no data. 06: Rp references +3V3, not 5 V, because
    # the 5 V rail is the thing being decided and is not available pre-attach.
    for pin in ("A4", "B4", "A9", "B9"):
        j6[pin] += u5["OUT"]
    for pin in ("A1", "B1", "A12", "B12"):
        j6[pin] += gnd
    j6["SH"] += gnd
    # SBU1/SBU2 (A8/B8) deliberately left unconnected: power-only port, no
    # VCONN, no data. Note a discrepancy worth checking at layout -- 06 says
    # the HRO 16-pin part has "SBU and the SuperSpeed pairs simply absent",
    # but KiCad's generic USB2.0_16P symbol does carry SBU1/SBU2. Verify the
    # footprint against the HRO drawing, as 06 separately instructs.
    j6["A5"] += cc1
    j6["B5"] += cc2
    cc1 += r3[1], u2["GPIO26_ADC0"]
    cc2 += r4[1], u2["GPIO27_ADC1"]
    r3[2] += v3v3
    r4[2] += v3v3
    # BC1.2 DCP signature: D+ shorted to D- through R21, so a phone that
    # ignores CC still charges above 100 mA.
    dp, dm = Net("ACC_DP"), Net("ACC_DM")
    j6["A6"] += dp
    j6["B6"] += dp
    j6["A7"] += dm
    j6["B7"] += dm
    dp += r21[1]
    r21[2] += dm

    # --- 06 §Telemetry (J3) — populated, unwired in Rev A -----------------
    u2["GPIO0"] += r14[1]
    r14[2] += j3[1]          # silkscreen "TX->RX"
    u2["GPIO1"] += r15[1]
    r15[2] += j3[2]          # silkscreen "RX->TX"
    j3[3] += gnd

    # --- SWD (J7) ---------------------------------------------------------
    j7[1] += u2["SWCLK"]
    j7[2] += gnd
    j7[3] += u2["SWDIO"]

    # --- Pico rails -------------------------------------------------------
    u2["3V3"] += v3v3
    for p in u2.pins:
        if p.name in ("GND", "AGND"):
            p += gnd

    return locals()


def verify(net_file: Path) -> list[str]:
    """Assert the nets 06 singles out as consequential.

    This file is a transcription of a document, and transcription is where
    net errors come from. These checks are the guard: each one names the 06
    section it enforces, and each is stated as (ref, pin) pairs read back
    out of the generated netlist rather than out of the builder's variables.
    """
    import re

    txt = net_file.read_text()
    nets: dict[str, set[tuple[str, str]]] = {}
    for block in txt.split("(net\n")[1:]:
        m = re.search(r'\(name "([^"]+)"\)', block)
        if not m:
            continue
        nodes = set(zip(
            re.findall(r'\(ref "([^"]+)"\)', block),
            re.findall(r'\(pin "([^"]+)"\)', block),
        ))
        nets[m.group(1)] = nodes

    # (net, must-contain, why)
    expect = [
        # 06 §Rail control. GP6 is pin 9; 1.5k R1 to GND is the whole of SIM-01.
        ("U3_EN", {("U2", "9"), ("R1", "1")}, "06 Rail control: GP6 -> U3.EN + R1"),
        ("U3_PG", {("U2", "10"), ("R2", "1")}, "06 Rail control: GP7 <- U3.PG, R2 pull-up"),
        # 06 §Aux 5V -> VSYS. D1 mandatory; VSYS must NOT also see VBUS.
        # ORIENTATION IS THE POINT HERE. On the KiCad SS14 symbol pin 1 is the
        # CATHODE and pin 2 is the ANODE -- the opposite of the usual guess.
        # Cathode to VSYS, anode to the aux rail, so current flows aux->VSYS
        # and the Pico's programming port cannot back-feed U1. Reverse it and
        # the board looks fine and does nothing.
        ("VSYS", {("D1", "1"), ("U2", "39")}, "06 Aux 5V: D1 CATHODE (pin1) -> Pico VSYS"),
        ("+5V_AUX", {("U1", "8"), ("D1", "2")}, "06 Aux 5V: U1 pin8 -> D1 ANODE (pin2)"),
        # 06 §I2C allocation. Rail-critical bus carries U1 and U6, never the OLED.
        ("I2C1_SDA", {("U2", "4"), ("U1", "4"), ("U6", "4")}, "06 I2C1 rail-critical"),
        ("I2C1_SCL", {("U2", "5"), ("U1", "5"), ("U6", "5")}, "06 I2C1 rail-critical"),
        ("I2C0_SDA", {("U2", "6"), ("J4", "3")}, "06 I2C0 reporting only"),
        ("I2C0_SCL", {("U2", "7"), ("J4", "4")}, "06 I2C0 reporting only"),
        # 06 §NTC. GP28/ADC2.
        ("NTC_SENSE", {("U2", "34"), ("RT1", "1"), ("R16", "2")}, "06 NTC divider -> ADC2"),
        # 06 §Telemetry, via the 220 R series protection.
        ("U1_INT", {("U2", "15"), ("U1", "3")}, "06 pin map: GP11 <- U1 INT"),
    ]

    problems = []
    for name, must, why in expect:
        have = nets.get(name)
        if have is None:
            problems.append(f"net {name!r} missing entirely  [{why}]")
        elif not must <= have:
            problems.append(f"net {name!r} missing {sorted(must - have)}  [{why}]")

    # 03's rule, restated in 06: BOTH sets of the duplicated Pololu output
    # pins must carry the rail. A single 2.54 mm contact is not the place to
    # discover its real current rating.
    rtr = nets.get("+5V_RTR", set())
    u3_out = {p for r, p in rtr if r == "U3"}
    wanted = {str(U3[k]) for k in ("VOUT_A", "VOUT_B", "VOUT_C", "VOUT_D")}
    if not wanted <= u3_out:
        problems.append(
            f"+5V_RTR uses only U3 pins {sorted(u3_out)}; 03 requires all of "
            f"{sorted(wanted)} -- this is the full router current"
        )

    # 06 §Aux 5V: "Do not also short VBUS to VSYS on the Pico."
    if ("U2", "40") in nets.get("VSYS", set()):
        problems.append("VSYS is tied to Pico VBUS (pin 40) -- 06 forbids this; it defeats D1")

    return problems


def main() -> int:
    BUILD.mkdir(parents=True, exist_ok=True)
    build_netlist()

    print("\n--- ERC ---")
    ERC()

    out = BUILD / "vezha-power.net"
    generate_netlist(file_=str(out))

    print(f"\nNetlist written: {out}")

    problems = verify(out)
    if problems:
        print("\n!! NET CHECK FAILED against docs/06-power-board-schematic.md:")
        for p in problems:
            print(f"   - {p}")
        return 1
    print("Net check: all consequential nets from 06 verified.")
    if U3_PINS_PROVISIONAL:
        print(
            "\n!! U3 (Pololu) pin numbering is PROVISIONAL — 06 states the\n"
            "   left-to-right order is not legible at published resolution.\n"
            "   EN and PG are adjacent on different rows and easy to short.\n"
            "   Confirm against the physical board before fabricating."
        )
    print(
        "\n!! Accessory port (U4 LMR38020, U5 TPS2553, R3-R6, J6) is NOT in\n"
        "   this netlist. 06 defers its support passives to the TI datasheets\n"
        "   and neither part has a KiCad symbol installed. Rev A is the rest."
    )
    return 0


if __name__ == "__main__":
    os.environ.setdefault("KICAD_SYMBOL_DIR", KICAD_SYMBOLS)
    sys.exit(main())
