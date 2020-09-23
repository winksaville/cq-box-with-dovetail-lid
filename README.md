# Create a box with a dovetail lid in CadQuery

A box with dovetail lid in cadquery

# Run:

Run directly with -h to see help. If no parameters are given the
code is run with default values but no stl files are generated.
This is useful for development and is the same as running with `make p`.

```
$ ./box_with_dovetail_lid.py -h
usage: box_with_dovetail_lid.py [-h] [-b [BOX]] [-l [LID]]
                                [-st [STLTOLERANCE]] [-c [CLEARANCE]]
                                [-x [XLEN]] [-y [YLEN]] [-z [ZLEN]]
                                [-lt [LIDTHICKNESS]] [-wt [WALLTHICKNESS]]
                                [-da [DOVETAILANGLE]]

optional arguments:
  -h, --help            show this help message and exit
  -b [BOX], --box [BOX]
                        Output box stl file, default box not output
  -l [LID], --lid [LID]
                        Output lid stl file, default: list not output
  -st [STLTOLERANCE], --stlTolerance [STLTOLERANCE]
                        stl file tollerance, default: 0.001
  -c [CLEARANCE], --clearance [CLEARANCE]
                        Clearance for lid, default: 0.05
  -x [XLEN], --xLen [XLEN]
                        X length of box, default: 25
  -y [YLEN], --yLen [YLEN]
                        Y length of box, default: 25
  -z [ZLEN], --zLen [ZLEN]
                        X length of box, default: 10
  -lt [LIDTHICKNESS], --lidThickness [LIDTHICKNESS]
                        lid thickness, default: 2
  -wt [WALLTHICKNESS], --wallThickness [WALLTHICKNESS]
                        wall thickness, default: 3
  -da [DOVETAILANGLE], --dovetailAngle [DOVETAILANGLE]
                        dovetail angle, default: 55
```

# Development:

When developing using the make can be useful, see help for command:
In particular the `make e` to run under cq-editor is useful. You'll
also want to run `make f` and `make mypy` after changing code. Right
now there are no tests so `make t` isn't useful.

```
$ make
make <target>
targets:
 f|format   # Format
 e          # Run with cq-editor
 p          # Run with python
 t          # Run pytest
 mypy       # Run mypy *.py
```

