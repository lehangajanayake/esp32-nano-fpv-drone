"""Hand-placed power routing for the shield PCB (vias + motor/power traces).

Run with KiCad's bundled Python:
  /Applications/KiCad/KiCad.app/Contents/Frameworks/Python.framework/Versions/Current/bin/python3 \
      hardware/shield/scripts/route_power.py hardware/shield/shield.kicad_pcb

HISTORICAL: this placed the first pass of the power routing on 2026-11-27. The board was
edited afterwards (J3 feed, IMU ground via, stitching vias, autorouted signals), and a
re-run deletes every track/via on the nets it owns (including /GND and /VBAT_P), so do
not re-run it on the current board.
Coordinates are KiCad board mm (origin top-left, +Y towards the rear of the drone).
"""
import sys
import pcbnew

MM = pcbnew.FromMM
OWNED = ["/BAT_IN", "/VBAT_P", "/PGND", "/GND",
         "/Motor1/MOT_N", "/Motor2/MOT_N", "/Motor3/MOT_N", "/Motor4/MOT_N"]

# Power vias: 0.8 mm pad / 0.4 mm drill (POWER_HI / MOTOR net class).
VIAS = {
    "/BAT_IN": [(x, y) for y in (101.2, 102.1, 103.0) for x in (117.45, 118.35, 119.25)],
    "/PGND": [
        # under the BAT- pad (back) into the In1 PGND plane
        (111.6, 101.9), (112.5, 101.9), (113.4, 101.9),
        (111.6, 102.8), (112.5, 102.8), (113.4, 102.8),
        (111.6, 103.7), (113.4, 103.7),
        (117.9, 108.55),                          # C8/C9 return
        (101.4, 114.2), (101.4, 115.1),          # Q1 source
        (105.6, 116.5),                           # R5
        (100.9, 103.4), (100.9, 104.4),           # Q2 source
        (128.6, 116.2), (128.6, 117.1),           # Q3 source
        (124.4, 116.5),                           # R7
        (121.0, 104.9), (121.7, 104.4),           # Q4 source, R8
        (123.4, 107.5), (123.4, 108.4),           # C10
        (110.0, 108.6),                           # C11
    ],
    "/VBAT_P": [
        # Q5 source pour down to the In2 VBAT_P plane
        (113.4, 105.75), (112.0, 105.7), (111.2, 105.9), (110.3, 105.3),
        (109.6, 105.6), (108.05, 105.95), (110.0, 103.9),
        (101.0, 125.4), (102.0, 125.4), (101.0, 126.3),    # MOT1 +
        (124.6, 125.3), (123.9, 125.8), (124.6, 126.3),    # MOT3 +
        (128.5, 104.2), (128.5, 105.1), (127.6, 105.6),    # MOT4 +
        (105.7, 118.4), (105.7, 119.3), (105.7, 120.2),    # D1 cathode
        (105.4, 109.9), (105.4, 110.8),                    # D2 cathode
        (124.3, 118.4), (124.3, 119.3), (124.3, 120.2),    # D3 cathode
        (124.6, 109.9), (124.6, 110.8),                    # D4 cathode
        (120.25, 108.95),                                  # C10
    ],
    "/GND": [(106.9, 110.0)],                              # NT1 GND side into In1 GND
    "/Motor3/MOT_N": [
        (125.6, 121.5), (126.5, 121.5), (127.4, 121.5),    # D3 anode
        (127.75, 114.6), (128.6, 114.2), (128.7, 115.1),   # Q3 drain (right of it; D4 sits above)
    ],
}

F, B = pcbnew.F_Cu, pcbnew.B_Cu
# (net, layer, width, [points]) polylines
TRACKS = [
    # Motor 1: pad -> D1 anode -> round the left of D1 -> Q1 drain
    ("/Motor1/MOT_N", F, 1.0, [(105, 128), (105, 124.0), (103.6, 123.15)]),
    ("/Motor1/MOT_N", F, 1.0, [(103.6, 123.15), (101.3, 123.15), (101.3, 116.6),
                               (103.7, 116.6)]),
    # Motor 2: pad + Q2 drain -> down the right of R6 -> D2 anode
    ("/Motor2/MOT_N", F, 1.0, [(107, 102), (106.0, 103.0)]),
    ("/Motor2/MOT_N", F, 1.0, [(104.14, 103.0), (106.0, 103.0), (106.0, 107.9), (103.45, 107.9)]),
    # Motor 3: pad -> D3 anode; D3 anode -> back layer -> Q3 drain
    ("/Motor3/MOT_N", F, 1.0, [(128, 128), (128, 124.3), (126.4, 123.15)]),
    ("/Motor3/MOT_N", F, 1.0, [(126.4, 123.15), (126.4, 121.5)]),
    ("/Motor3/MOT_N", F, 0.8, [(125.6, 121.5), (127.4, 121.5)]),
    ("/Motor3/MOT_N", B, 0.8, [(125.6, 121.5), (127.4, 121.5)]),
    ("/Motor3/MOT_N", B, 1.2, [(126.5, 121.5), (127.0, 121.0), (127.0, 115.0), (127.75, 114.6)]),
    ("/Motor3/MOT_N", B, 0.8, [(128.6, 114.2), (127.75, 114.6), (128.7, 115.1)]),
    ("/Motor3/MOT_N", F, 0.8, [(126.5, 114.66), (127.75, 114.6), (128.6, 114.2)]),
    ("/Motor3/MOT_N", F, 0.8, [(127.75, 114.6), (128.7, 115.1)]),
    # Motor 4: pad -> Q4 drain; pad -> D4 anode
    ("/Motor4/MOT_N", F, 1.0, [(122.64, 103.0), (125, 102)]),
    ("/Motor4/MOT_N", F, 1.0, [(125, 102), (125, 106.6), (126.55, 107.9)]),
    # Motor + pads and diode cathodes to their VBAT_P vias
    ("/VBAT_P", F, 1.0, [(102, 128), (102, 125.4), (101.0, 125.4), (101.0, 126.3)]),
    ("/VBAT_P", F, 1.0, [(125, 128), (124.6, 126.3), (124.6, 125.3)]),
    ("/VBAT_P", F, 0.8, [(124.6, 125.8), (123.9, 125.8)]),
    ("/VBAT_P", F, 1.0, [(128, 102), (128.5, 104.2), (128.5, 105.1), (127.6, 105.6)]),
    ("/VBAT_P", F, 1.0, [(103.6, 119.3), (105.7, 119.3)]),
    ("/VBAT_P", F, 0.8, [(105.7, 118.4), (105.7, 120.2)]),
    ("/VBAT_P", F, 1.0, [(103.45, 111.9), (105.4, 110.8), (105.4, 109.9)]),
    ("/VBAT_P", F, 1.0, [(126.4, 119.3), (124.3, 119.3)]),
    ("/VBAT_P", F, 0.8, [(124.3, 118.4), (124.3, 120.2)]),
    ("/VBAT_P", F, 1.0, [(126.55, 111.9), (124.6, 110.8), (124.6, 109.9)]),
    # FET sources, pull-downs and caps to their PGND vias
    ("/PGND", F, 0.8, [(102.75, 115.1), (101.4, 115.1)]),
    ("/PGND", F, 0.8, [(101.4, 114.2), (101.4, 115.1)]),
    ("/PGND", F, 0.3, [(106.0, 115.51), (105.6, 116.5)]),
    ("/PGND", F, 0.6, [(102.26, 103.95), (100.9, 103.95)]),
    ("/PGND", F, 0.8, [(100.9, 103.4), (100.9, 104.4)]),
    ("/PGND", F, 0.3, [(105.01, 105.55), (105.0, 104.6), (102.7, 104.6), (102.5, 104.2)]),
    ("/PGND", F, 0.8, [(127.45, 116.6), (128.6, 116.6)]),
    ("/PGND", F, 0.8, [(128.6, 116.2), (128.6, 117.1)]),
    ("/PGND", F, 0.3, [(124.05, 115.51), (124.4, 116.5)]),
    ("/PGND", F, 0.6, [(120.76, 103.95), (121.0, 104.9)]),
    ("/PGND", F, 0.6, [(120.76, 103.95), (121.7, 104.4)]),
    ("/PGND", F, 0.3, [(120.81, 105.6), (121.0, 104.9)]),
    ("/PGND", F, 0.3, [(118.4, 104.49), (119.9, 104.49), (120.3, 104.1)]),
    ("/PGND", F, 0.8, [(122.35, 107.5), (123.4, 107.5), (123.4, 108.4)]),
    ("/PGND", F, 0.6, [(109.95, 107.5), (110.0, 108.6)]),
    ("/VBAT_P", F, 0.8, [(108.05, 105.95), (108.05, 107.5)]),
    ("/VBAT_P", F, 0.3, [(111.3, 107.3), (111.3, 108.6), (111.89, 108.6)]),
    ("/VBAT_P", F, 0.5, [(120.25, 107.5), (120.25, 108.95)]),
    # NT1 GND side up into the GND pour (back)
    ("/GND", B, 0.5, [(106.6, 102.0), (106.6, 110.0), (106.9, 110.0)]),
]


def main(path):
    board = pcbnew.LoadBoard(path)
    for t in list(board.GetTracks()):
        if t.GetNetname() in OWNED:
            board.Remove(t)
    def net(name):
        n = board.FindNet(name)
        assert n is not None, name
        return n

    for name, pts in VIAS.items():
        for x, y in pts:
            v = pcbnew.PCB_VIA(board)
            v.SetPosition(pcbnew.VECTOR2I(MM(x), MM(y)))
            v.SetWidth(MM(0.8))
            v.SetDrill(MM(0.4))
            v.SetNet(net(name))
            board.Add(v)
    for name, layer, width, pts in TRACKS:
        for (x1, y1), (x2, y2) in zip(pts, pts[1:]):
            t = pcbnew.PCB_TRACK(board)
            t.SetStart(pcbnew.VECTOR2I(MM(x1), MM(y1)))
            t.SetEnd(pcbnew.VECTOR2I(MM(x2), MM(y2)))
            t.SetWidth(MM(width))
            t.SetLayer(layer)
            t.SetNet(net(name))
            board.Add(t)
    pcbnew.ZONE_FILLER(board).Fill(board.Zones())
    board.Save(path)


if __name__ == "__main__":
    main(sys.argv[1])
