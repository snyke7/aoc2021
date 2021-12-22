import attr
import typing


@attr.s(auto_attribs=True, frozen=True)
class Cuboid:
    x_min: int
    x_max: int
    y_min: int
    y_max: int
    z_min: int
    z_max: int

    def get_overlap(self, other) -> typing.Optional['Cuboid']:
        i_xmin = max(self.x_min, other.x_min)
        i_xmax = min(self.x_max, other.x_max)
        if i_xmin > i_xmax:
            return None
        i_ymin = max(self.y_min, other.y_min)
        i_ymax = min(self.y_max, other.y_max)
        if i_ymin > i_ymax:
            return None
        i_zmin = max(self.z_min, other.z_min)
        i_zmax = min(self.z_max, other.z_max)
        if i_zmin > i_zmax:
            return None
        return Cuboid(i_xmin, i_xmax, i_ymin, i_ymax, i_zmin, i_zmax)

    def contains(self, other):
        return self.get_overlap(other) == other

    def carve_out(self, other) -> typing.List['Cuboid']:  # assumes other is contained in self
        result = []
        if self.x_min < other.x_min:
            result.append(Cuboid(self.x_min, other.x_min - 1, self.y_min, self.y_max, self.z_min, self.z_max))
        if other.x_max < self.x_max:
            result.append(Cuboid(other.x_max + 1, self.x_max, self.y_min, self.y_max, self.z_min, self.z_max))
        if self.y_min < other.y_min:
            result.append(Cuboid(other.x_min, other.x_max, self.y_min, other.y_min - 1, self.z_min, self.z_max))
        if other.y_max < self.y_max:
            result.append(Cuboid(other.x_min, other.x_max, other.y_max + 1, self.y_max, self.z_min, self.z_max))
        if self.z_min < other.z_min:
            result.append(Cuboid(other.x_min, other.x_max, other.y_min, other.y_max, self.z_min, other.z_min - 1))
        if other.z_max < self.z_max:
            result.append(Cuboid(other.x_min, other.x_max, other.y_min, other.y_max, other.z_max + 1, self.z_max))
        return result

    def get_size(self):
        return (self.x_max + 1 - self.x_min) * (self.y_max + 1 - self.y_min) * (self.z_max + 1 - self.z_min)


def parse_cuboid_cmd(line):
    left, right = tuple(line.split(' '))
    cmd = left == 'on'
    xrange, yrange, zrange = tuple((tuple(map(int, rng[2:].split('..'))) for rng in right.split(',')))
    return cmd, Cuboid(
        *xrange,
        *yrange,
        *zrange
    )


def get_overlap_dict(disjoint_set: typing.Iterable[Cuboid], cuboid: Cuboid) -> typing.Dict[Cuboid, Cuboid]:
    intersects = {}
    for cub in disjoint_set:
        intersect = cub.get_overlap(cuboid)
        if intersect is not None:
            intersects[cub] = intersect
    return intersects


def get_disjoint_additions(disjoint_set: typing.Iterable[Cuboid], to_add: Cuboid) -> typing.List[Cuboid]:
    intersects = list(get_overlap_dict(disjoint_set, to_add).values())
    if not intersects:
        return [to_add]
    else:
        to_add_parts = to_add.carve_out(intersects[0])
        return [cub for part in to_add_parts for cub in get_disjoint_additions(intersects[1:], part)]


def execute_cmds(cuboid_cmds) -> typing.Set[Cuboid]:  # a set of disjoint cuboids covering the region
    result = set()
    for cmd, region in cuboid_cmds:
        if cmd:
            result.update(get_disjoint_additions(result, region))
        else:
            intersects = get_overlap_dict(result, region)  # first remove all regions which have overlap
            result.difference_update(intersects.keys())
            # now add these regions back, with the disabled region carved out
            result.update([
                part
                for intersect in intersects.keys()
                for part in intersect.carve_out(region.get_overlap(intersect))
            ])
    return result


def get_size(cuboids: typing.Iterable[Cuboid]) -> int:
    return sum((cuboid.get_size() for cuboid in cuboids))


def get_solution():
    with open('input/day22_input.txt') as f:
        lines = f.readlines()
    lines1 = '''on x=-20..26,y=-36..17,z=-47..7
on x=-20..33,y=-21..23,z=-26..28
on x=-22..28,y=-29..23,z=-38..16
on x=-46..7,y=-6..46,z=-50..-1
on x=-49..1,y=-3..46,z=-24..28
on x=2..47,y=-22..22,z=-23..27
on x=-27..23,y=-28..26,z=-21..29
on x=-39..5,y=-6..47,z=-3..44
on x=-30..21,y=-8..43,z=-13..34
on x=-22..26,y=-27..20,z=-29..19
off x=-48..-32,y=26..41,z=-47..-37
on x=-12..35,y=6..50,z=-50..-2
off x=-48..-32,y=-32..-16,z=-15..-5
on x=-18..26,y=-33..15,z=-7..46
off x=-40..-22,y=-38..-28,z=23..41
on x=-16..35,y=-41..10,z=-47..6
off x=-32..-23,y=11..30,z=-14..3
on x=-49..-5,y=-3..45,z=-29..18
off x=18..30,y=-20..-8,z=-3..13
on x=-41..9,y=-7..43,z=-33..15
on x=-54112..-39298,y=-85059..-49293,z=-27449..7877
on x=967..23432,y=45373..81175,z=27513..53682'''.splitlines()
    lines2 = '''on x=10..12,y=10..12,z=10..12
on x=11..13,y=11..13,z=11..13
off x=9..11,y=9..11,z=9..11
on x=10..10,y=10..10,z=10..10'''.splitlines()
    init_region = Cuboid(-50, 50, -50, 50, -50, 50)
    cmds = [parse_cuboid_cmd(line.strip()) for line in lines]
    init_cmds = [cmd for cmd in cmds if init_region.contains(cmd[1])]
    init_area = execute_cmds(init_cmds)
    print(get_size(init_area))
    total_area = execute_cmds(cmds)
    print(get_size(total_area))
