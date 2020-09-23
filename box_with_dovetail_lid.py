#!/usr/bin/env python3
import argparse
import io
import os
import sys
from math import radians, tan

import cadquery as cq  # type: ignore


class BoxWithDovetailLid:
    """
    A box with a dovetail lid
    """

    xLen: float
    yLen: float
    zLen: float
    dovetailAngle: float
    lidClearance: float

    box: cq.Workplane
    lid: cq.Workplane

    def __init__(
        self,
        xLen: float = 25,
        yLen: float = 25,
        zLen: float = 10,
        lidThickness: float = 2,
        wallThickness: float = 3,
        dovetailAngle: float = 55,
        lidClearance: float = 0.1,
    ) -> None:
        dbg(
            f"BoxWithDovetailLid.init: xLen={xLen} yLen={yLen} zLen={zLen} lidClearance={lidClearance}"
        )

        self.xLen = xLen
        self.yLen = yLen
        self.zLen = zLen
        self.wallThickness = wallThickness
        self.dovetailAngle = dovetailAngle
        self.lidClearance = lidClearance

        # Create the box
        b = (
            cq.Workplane("XY")
            .rect(xLen, yLen, centered=False)
            .extrude(zLen)
            .faces(">Z")
            .shell(-wallThickness)
        )
        # show(b)

        dtaRad = radians(90 - dovetailAngle)
        # lidX_len = ((xLen) / 2) - wallThickness
        # lidZ_len = zLen
        lidX_offset = tan(dtaRad) * lidThickness
        lidTopLen = xLen - (2 * wallThickness)
        lidBottomLen = lidTopLen + (2 * lidX_offset)

        # Create the lidCutter
        lidCutter = (
            cq.Workplane("XZ", origin=(wallThickness, 0, zLen))
            .line(-lidX_offset, -lidThickness)
            .line(lidBottomLen, 0)
            .line(-lidX_offset, lidThickness)
            .close()
            .extrude(distance=-(yLen - wallThickness))
        )
        # show(lidCutter)

        self.box = b.cut(lidCutter)

        # Create the lid
        lid = (
            cq.Workplane("XZ", origin=(0, -10, 0))
            .line(lidX_offset, lidThickness)
            .line(lidTopLen - (2 * lidClearance), 0)
            .line(lidX_offset, -lidThickness)
            .close()
            .extrude(distance=yLen - wallThickness)
        )
        # show(lid)
        self.lid = lid


if "cq_editor" in sys.modules:
    from logbook import info as _cq_log

    def show(o: object, name=None):
        # print("cq_editor.show")
        ctx = globals()
        if ctx["show_object"] is None:
            raise ValueError("ctx['show_object'] is not available")
        ctx["show_object"](o, name=name)

    def dbg(*args):
        # print("cq_editor.dbg")
        _cq_log(*args)


else:

    def show(o: object, name=None):
        if o is None:
            dbg("o=None")
        elif isinstance(o, cq.Workplane):
            for i, thing in enumerate(o.objects):
                dbg(
                    f"{name + '.objects' if (name is not None) else ''}[{i}]: valid={o.val().isValid()} {vars(thing)}"
                )
        else:
            dbg(vars(o))

    def dbg(*args):
        print(*args)


if __name__ == "__main__" or "cq_editor" in sys.modules:
    xLen: float = 25
    yLen: float = 25
    zLen: float = 10
    lidThickness: float = 2
    wallThickness: float = 3
    dovetailAngle: float = 55
    lidClearance: float = 0.05
    stlTolerance = 0.001
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-b",
        "--box",
        help="Output box stl file, default box not output",
        nargs="?",
        const="box",
        default="no-box",
    )
    parser.add_argument(
        "-l",
        "--lid",
        help="Output lid stl file, default: list not output",
        nargs="?",
        const="lid",
        default="no-lid",
    )
    parser.add_argument(
        "-st",
        "--stlTolerance",
        help=f"stl file tollerance, default: {stlTolerance}",
        nargs="?",
        type=float,
        default=stlTolerance,
    )
    parser.add_argument(
        "-c",
        "--clearance",
        help=f"Clearance for lid, default: {lidClearance}",
        nargs="?",
        type=float,
        default=lidClearance,
    )
    parser.add_argument(
        "-x",
        "--xLen",
        help=f"X length of box, default: {xLen}",
        nargs="?",
        type=float,
        default=xLen,
    )
    parser.add_argument(
        "-y",
        "--yLen",
        help=f"Y length of box, default: {yLen}",
        nargs="?",
        type=float,
        default=yLen,
    )
    parser.add_argument(
        "-z",
        "--zLen",
        help=f"X length of box, default: {zLen}",
        nargs="?",
        type=float,
        default=zLen,
    )
    parser.add_argument(
        "-lt",
        "--lidThickness",
        help=f"lid thickness, default: {lidThickness}",
        nargs="?",
        type=float,
        default=lidThickness,
    )
    parser.add_argument(
        "-wt",
        "--wallThickness",
        help=f"wall thickness, default: {wallThickness}",
        nargs="?",
        type=float,
        default=wallThickness,
    )
    parser.add_argument(
        "-da",
        "--dovetailAngle",
        help=f"dovetail angle, default: {dovetailAngle}",
        nargs="?",
        type=float,
        default=dovetailAngle,
    )

    if "cq_editor" in sys.modules:
        # TODO: How to pass parameters to an app executed by cq-ediort
        # For now we'll pass nothing
        args = parser.parse_args([])
    else:
        # Not cq_editor so parse_args will parse the command line parameters
        args = parser.parse_args()

    dbg(f"args={vars(args)}")
    # dbg(f"args.box={args.box}")
    # dbg(f"args.lid={args.lid}")
    # dbg(f"args.clearance={args.clearance}")
    xLen = args.xLen
    yLen = args.yLen
    zLen = args.zLen
    lidThickness = args.lidThickness
    wallThickness = args.wallThickness
    dovetailAngle = args.dovetailAngle
    lidClearance = args.clearance
    stlTolerance = args.stlTolerance
    boxOutStl: bool = args.box == "box"
    lidOutStl: bool = args.lid == "lid"
    # dbg(f"boxOutStl={boxOutStl}")
    # dbg(f"lidOutStl={lidOutStl}")
    # dbg(f"lidClearance={lidClearance}")

    box = BoxWithDovetailLid(
        xLen=xLen,
        yLen=yLen,
        zLen=zLen,
        lidThickness=lidThickness,
        wallThickness=wallThickness,
        dovetailAngle=dovetailAngle,
        lidClearance=lidClearance,
    )
    show(box.box, "box")
    show(box.lid, "lid")

    if boxOutStl:
        directory: str = "generated/"
        fname: str = f"box_with_dovetail-x_{box.xLen:.2f}-y_{box.yLen:.2f}-z_{box.zLen:.2f}-wall_{box.wallThickness:.2f}-angle_{box.dovetailAngle:.2f}-clearance_{box.lidClearance:.3f}-tol_{stlTolerance:.4f}.stl"
        cq.exporters.export(
            box.box, os.path.join(directory, fname), tolerance=stlTolerance
        )
        dbg(f"{fname}")

    if lidOutStl:
        directory: str = "generated/"
        fname: str = f"lid_with_dovetail-x_{box.xLen:.2f}-y_{box.yLen:.2f}-z_{box.zLen:.2f}-wall_{box.wallThickness:.2f}-angle_{box.dovetailAngle:.2f}-clearance_{box.lidClearance:.3f}-tol_{stlTolerance:.4f}.stl"
        cq.exporters.export(
            box.lid, os.path.join(directory, fname), tolerance=stlTolerance
        )
        dbg(f"{fname}")
