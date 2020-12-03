s(PEL, no_switches, primary_dir):
        _basis_angles = [((360/no_switches * i) + primary_dir)%360 for i in range(no_switches)]
        return [(math.cos(math.radians(x)),math.sin(math.radians(x))) for x in _basis_angles]
    