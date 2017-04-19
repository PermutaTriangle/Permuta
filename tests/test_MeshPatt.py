import random
import pytest
import itertools
from permuta import Perm, MeshPatt
from permuta.MeshPatt import gen_meshpatts
from permuta.misc import DIR_EAST, DIR_NORTH, DIR_WEST, DIR_SOUTH, DIR_NONE
from permuta.misc import factorial

mesh_pattern = MeshPatt([1, 3, 2, 0], set([(0, 0), (4, 0), (2, 1), (4, 1), (2, 2), (4, 2), (3, 3), (0, 4)]))
perm1 = Perm([5, 2, 8, 6, 7, 9, 4, 3, 1, 0])  # Occurrence: E.g., [1, 3, 6, 9]
perm2 = Perm([1, 2, 8, 6, 5, 9, 4, 3, 7, 0])  # Occurrence: E.g., [1, 6, 7, 9]
perm3 = Perm([9, 8, 7, 6, 2, 5, 3, 4, 0, 1])  # Occurrence: None (avoids)
perm4 = Perm([0, 1, 2, 3, 4])  # Avoids as well
perm5 = Perm([1, 2, 4, 3, 0])  # Two occurrences
patt1 = perm4
patt2 = perm5
patt3 = Perm((2, 3, 0, 1))
shad1 = frozenset([(0, 0), (1, 0), (2, 0), (2, 1), (3, 2), (3, 3), (5, 0), (5, 1), (5, 2)])
shad2 = frozenset([(3, 3), (2, 2), (1, 1), (0, 2)])
shad3 = frozenset([(1, 3), (4, 4), (2, 1), (2, 2), (0, 4), (4, 0)])
mesh1 = MeshPatt(patt1, shad1)
mesh2 = MeshPatt(patt2, shad2)
mesh3 = MeshPatt(patt3, shad3)

def test_init():
    Perm.toggle_check()
    try:
        with pytest.raises(ValueError): MeshPatt(Perm([0, 1, 1]), ())
        with pytest.raises(ValueError): MeshPatt(Perm([1, 0, 1]), ())
        with pytest.raises(ValueError): MeshPatt(Perm([0, 0]), ())
        with pytest.raises(ValueError): MeshPatt(Perm([1]), ())
        with pytest.raises(ValueError): MeshPatt(Perm((1)), ())
        with pytest.raises(ValueError): MeshPatt(Perm(101), ())
        with pytest.raises(ValueError): MeshPatt(Perm(-234), ())
        with pytest.raises(TypeError): MeshPatt(Perm(None), ())
        with pytest.raises(TypeError): MeshPatt(Perm([0.1, 0.2, 0.3]), ())
        with pytest.raises(TypeError): MeshPatt(Perm(()), (0, 1))
        with pytest.raises(TypeError): MeshPatt(Perm((0, 1, 2)), [(1, 'a')])
        with pytest.raises(TypeError): MeshPatt(Perm((0, 1, 2)), [('a', 1)])
        with pytest.raises(ValueError): MeshPatt(Perm.random(5), [(0,), (1, 1)])
        with pytest.raises(ValueError): MeshPatt(Perm.random(5), [(0, 0, 0), (1, 1, 1)])
        with pytest.raises(ValueError): MeshPatt(Perm(()), [(0, 1), (1, 0)])
        with pytest.raises(ValueError): MeshPatt(Perm.random(3), [(0, -1), (0, 0)])
        with pytest.raises(ValueError): MeshPatt(Perm.random(10), [(0, 0), (12, 7)])
        MeshPatt(Perm(), ())
        MeshPatt(Perm([]), ())
        MeshPatt(Perm(0), ())
        MeshPatt(Perm([0]), ())
        MeshPatt(Perm([3, 0, 2, 1]), ())
        MeshPatt(Perm([3, 0, 2, 1]), [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4),
            (1, 0), (1, 1), (1, 2), (1, 3), (1, 4), (2, 0), (2, 1), (2, 2),
            (2, 3), (2, 4), (3, 0), (3, 1), (3, 2), (3, 3), (3, 4), (4, 0),
            (4, 1), (4, 2), (4, 3), (4, 4)])
        MeshPatt(Perm([3, 0, 2, 1]), [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4)])
        MeshPatt([3, 0, 2, 1], [(0, 2), (0, 3), (0, 4)])
        MeshPatt(set([3, 0, 2, 1]), [(0, 2), (0, 3), (0, 4)])
    finally:
        Perm.toggle_check()

def test_complement():
    assert MeshPatt(Perm(), []).complement() ==  MeshPatt(Perm(), [])
    assert MeshPatt(Perm(0), []).complement() == MeshPatt(Perm(0), [])
    assert MeshPatt(Perm(0), [(0, 0)]).complement() == MeshPatt(Perm(0), [(0, 1)])
    assert MeshPatt(Perm(0), [(0, 1)]).complement() == MeshPatt(Perm(0), [(0, 0)])
    assert MeshPatt(Perm(0), [(1, 0)]).complement() == MeshPatt(Perm(0), [(1, 1)])
    assert MeshPatt(Perm(0), [(1, 1)]).complement() == MeshPatt(Perm(0), [(1, 0)])
    for _ in range(20):
        mpatt = MeshPatt.random(10)
        comp = mpatt.complement()
        assert len(mpatt.pattern) == len(comp.pattern)
        assert comp.complement() == mpatt

def test_flip_horizontal():
    assert MeshPatt(Perm(), []).flip_vertical() ==  MeshPatt(Perm(), [])
    assert MeshPatt(Perm(0), [(0, 1)]).flip_horizontal() == MeshPatt(Perm(0), [(0, 0)])

def test_reverse():
    assert MeshPatt(Perm(), []).reverse() ==  MeshPatt(Perm(), [])
    assert MeshPatt(Perm(0), []).reverse() == MeshPatt(Perm(0), [])
    assert MeshPatt(Perm(0), [(0, 0)]).reverse() == MeshPatt(Perm(0), [(1, 0)])
    assert MeshPatt(Perm(0), [(0, 1)]).reverse() == MeshPatt(Perm(0), [(1, 1)])
    assert MeshPatt(Perm(0), [(1, 0)]).reverse() == MeshPatt(Perm(0), [(0, 0)])
    assert MeshPatt(Perm(0), [(1, 1)]).reverse() == MeshPatt(Perm(0), [(0, 1)])
    for _ in range(20):
        mpatt = MeshPatt.random(10)
        comp = mpatt.reverse()
        assert len(mpatt.pattern) == len(comp.pattern)
        assert comp.reverse() == mpatt

def test_flip_vertical():
    assert MeshPatt(Perm(), []).flip_vertical() ==  MeshPatt(Perm(), [])
    assert MeshPatt(Perm(0), [(0, 0)]).flip_vertical() == MeshPatt(Perm(0), [(1, 0)])

def test_inverse():
    assert MeshPatt(Perm(), []).inverse() ==  MeshPatt(Perm(), [])
    assert MeshPatt(Perm(0), []).inverse() == MeshPatt(Perm(0), [])
    assert MeshPatt(Perm(0), [(0, 0)]).inverse() == MeshPatt(Perm(0), [(0, 0)])
    assert MeshPatt(Perm(0), [(0, 1)]).inverse() == MeshPatt(Perm(0), [(1, 0)])
    assert MeshPatt(Perm(0), [(1, 0)]).inverse() == MeshPatt(Perm(0), [(0, 1)])
    assert MeshPatt(Perm(0), [(1, 1)]).inverse() == MeshPatt(Perm(0), [(1, 1)])
    for _ in range(20):
        mpatt = MeshPatt.random(10)
        comp = mpatt.inverse()
        assert len(mpatt.pattern) == len(comp.pattern)
        assert comp.inverse() == mpatt

def test_sub_mesh_pattern():
    # Empty pattern
    assert mesh1.sub_mesh_pattern(()) == MeshPatt((), ())
    # Sub mesh pattern from indices 1, 2, and 3 of mesh1
    pattern = (0, 1, 2)
    shading = set([(1, 0), (2, 1), (2, 2)])
    mesh_pattern = MeshPatt(pattern, shading)
    sub_mesh_pattern = mesh1.sub_mesh_pattern((1, 2, 3))
    assert sub_mesh_pattern == mesh_pattern
    # Sub mesh pattern from indices 0, 1, and 4 of mesh1
    pattern = (0, 1, 2)
    shading = set([(0, 0), (1, 0), (3, 0), (3, 1)])
    mesh_pattern = MeshPatt(pattern, shading)
    sub_mesh_pattern = mesh1.sub_mesh_pattern((0, 1, 4))
    assert sub_mesh_pattern == mesh_pattern
    # Sub mesh pattern from indices 3 and 4 of mesh1
    assert mesh1.sub_mesh_pattern((3, 4)) == MeshPatt((0, 1))
    # Sub mesh pattern from indices 2 and 3 of mesh1
    assert mesh1.sub_mesh_pattern((2, 3)) == MeshPatt((0, 1), set([(1, 1)]))
    # Sub mesh pattern from index 0 of mesh3
    assert mesh3.sub_mesh_pattern((0, )) == MeshPatt((0, ))
    # Sub mesh pattern from indices 0, 1, and 3 of mesh3
    assert mesh3.sub_mesh_pattern((0, 1, 3)) == MeshPatt((1, 2, 0), set([(0, 3), (1, 2), (3, 3)]))
    # Some complete sub meshes
    assert mesh1.sub_mesh_pattern(range(len(mesh1))) == mesh1
    assert mesh2.sub_mesh_pattern(range(len(mesh2))) == mesh2
    assert mesh3.sub_mesh_pattern(range(len(mesh3))) == mesh3

    mpatt = MeshPatt((0,1), [(0,0), (0,1), (1,0), (1,1)])
    assert mpatt.sub_mesh_pattern([0]) == MeshPatt((0,), [(0,0)])
    assert mpatt.sub_mesh_pattern([1]) == MeshPatt((0,))

    mpatt = MeshPatt((0,1,2), [(0,1), (1,1), (1,2), (2,1), (2,2), (3,1)])
    mpatt.sub_mesh_pattern([0, 1]) == MeshPatt((0,1), [(0,1), (1,1), (2,1)])
    mpatt.sub_mesh_pattern([0, 2]) == MeshPatt((0,1), [])

def test_flip_diagonal():
    assert MeshPatt(Perm(), []).flip_diagonal() ==  MeshPatt(Perm(), [])
    assert MeshPatt(Perm(0), [(0, 1)]).flip_diagonal() == MeshPatt(Perm(0), [(1, 0)])

def test_rotate():
    assert MeshPatt(Perm(), [])._rotate_right() == MeshPatt(Perm(), [])
    assert MeshPatt(Perm(), [])._rotate_left() == MeshPatt(Perm(), [])
    assert MeshPatt(Perm(), [])._rotate_180() == MeshPatt(Perm(), [])

    assert MeshPatt(Perm(0), [])._rotate_right() == MeshPatt(Perm(0), [])
    assert MeshPatt(Perm(0), [])._rotate_left() == MeshPatt(Perm(0), [])
    assert MeshPatt(Perm(0), [])._rotate_180() == MeshPatt(Perm(0), [])

    for _ in range(50):
        mpatt = MeshPatt.random(6)
        assert mpatt._rotate_right()._rotate_right() == mpatt._rotate_180()
        assert mpatt._rotate_left()._rotate_left() == mpatt._rotate_180()
        assert mpatt._rotate_right()._rotate_left() == mpatt
        assert mpatt._rotate_left()._rotate_right() == mpatt
        assert mpatt._rotate_180()._rotate_180() == mpatt

def test_shade():
    mpatt = MeshPatt()
    assert MeshPatt().shade((0, 0)).is_shaded((0, 0))
    assert MeshPatt().shade([(0, 0)]).is_shaded((0, 0))

    newshad = [(1, 2), (3, 3), (4, 4)]
    mesh1shaded = mesh1.shade(newshad)
    for shading in shad1:
        assert mesh1shaded.is_shaded(shading)
    for shading in newshad:
        assert mesh1shaded.is_shaded((shading))

    newshad = [(2, 2), (1, 1), (0, 2), (1, 2), (3, 3), (4, 4)]
    mesh2shaded = mesh2.shade(newshad)
    for shading in shad2:
        assert mesh2shaded.is_shaded(shading)
    for shading in newshad:
        assert mesh2shaded.is_shaded(shading)

    with pytest.raises(ValueError): mesh2.shade(())
    with pytest.raises(ValueError): mesh1.shade(())

def test_add_point():
    mpatt = MeshPatt()
    assert mpatt.add_point((0, 0)) == MeshPatt((0,))
    assert mpatt.add_point((0, 0), shade_dir=DIR_EAST) == MeshPatt((0,), [(1, 0), (1, 1)])
    assert mpatt.add_point((0, 0), shade_dir=DIR_NORTH) == MeshPatt((0,), [(0, 1), (1, 1)])
    assert mpatt.add_point((0, 0), shade_dir=DIR_WEST) == MeshPatt((0,), [(0, 0), (0, 1)])
    assert mpatt.add_point((0, 0), shade_dir=DIR_SOUTH) == MeshPatt((0,), [(0, 0), (1, 0)])

    mpatt = MeshPatt((0, 1, 2), [(1, 0), (2, 1), (3, 2)])
    assert mpatt.add_point((2, 0), shade_dir=DIR_SOUTH) == MeshPatt((1, 2, 0, 3),
            [(1, 0), (1, 1), (2, 0), (2, 2), (3, 0), (3, 2), (4, 3)])
    assert mpatt.add_point((1, 2), shade_dir=DIR_WEST) == MeshPatt((0, 2, 1, 3),
            [(1, 0), (1, 2), (1, 3), (2, 0), (3, 1), (4, 2), (4, 3)])
    assert mesh1.add_point((2, 3), shade_dir=DIR_NORTH) == MeshPatt((0, 1, 3, 2, 4, 5),
            [(0, 0), (1, 0), (2, 0), (2, 1), (2, 4), (3, 0), (3, 1), (3, 4), (4, 2), (4, 3), (4, 4), (6, 0), (6, 1), (6, 2)])

    with pytest.raises(TypeError): mpatt.add_point(('a', (0,)))
    with pytest.raises(ValueError): mpatt.add_point((2, 1))

def test_add_increase():
    mpatt = MeshPatt()
    assert mpatt.add_increase((0, 0)) == MeshPatt((0, 1))
    mpatt = MeshPatt((0, 1, 2), [(1, 0), (2, 1), (3, 2)])
    assert mpatt.add_increase((2, 0)) == MeshPatt(Perm((2, 3, 0, 1, 4)),
            [(1, 2), (5, 4), (3, 3), (2, 3), (4, 3), (1, 0), (1, 1)])
    assert mpatt.add_increase((1, 2)) == MeshPatt((0, 2, 3, 1, 4),
            [(1, 0), (2, 0), (3, 0), (4, 1), (5, 2), (5, 3), (5, 4)])

def test_add_decrease():
    mpatt = MeshPatt()
    assert mpatt.add_decrease((0, 0)) == MeshPatt((1, 0))
    mpatt = MeshPatt((0, 1, 2), [(1, 0), (2, 1), (3, 2)])
    assert mpatt.add_decrease((2, 0)) == MeshPatt(Perm((2, 3, 1, 0, 4)),
            [(1, 2), (5, 4), (3, 3), (2, 3), (4, 3), (1, 0), (1, 1)])
    assert mpatt.add_decrease((1, 2)) == MeshPatt((0, 3, 2, 1, 4),
            [(1, 0), (2, 0), (3, 0), (4, 1), (5, 2), (5, 3), (5, 4)])

def test_contained_in():
    assert Perm([0, 1, 2]).contains(MeshPatt([0, 1], set([(1, 0), (1, 1), (1, 2)])))
    assert mesh_pattern.contained_in(perm1)
    assert mesh_pattern.contained_in(perm2)
    assert not (mesh_pattern.contained_in(perm3))
    assert mesh_pattern.contained_in(perm1, perm2)
    assert not (mesh_pattern.contained_in(perm1, perm3))

def test_avoided_by():
    assert not (mesh_pattern.avoided_by(perm1))
    assert not (mesh_pattern.avoided_by(perm2))
    assert mesh_pattern.avoided_by(perm3)
    assert mesh_pattern.avoided_by(perm4)
    assert mesh_pattern.avoided_by(perm3, perm4)
    assert not (mesh_pattern.avoided_by(perm4, perm1, perm3))

def test_count_occurrences_in():
    assert mesh_pattern.count_occurrences_in(perm1) == 8
    assert mesh_pattern.count_occurrences_in(perm2) == 12
    assert mesh_pattern.count_occurrences_in(perm3) == 0
    assert mesh_pattern.count_occurrences_in(perm4) == 0
    assert mesh_pattern.count_occurrences_in(perm5) == 2

def test_is_shaded():
    mpatt = MeshPatt(Perm(), ((0, 0),))
    assert mpatt.is_shaded((0, 0))
    mpatt = MeshPatt((0, 2, 1), [(0, 0), (0, 2), (1, 1), (1, 3), (2, 0), (2, 2), (3, 1), (3, 3)])
    for (x0, y0) in itertools.combinations(range(len(mpatt) + 1), 2):
        for (x1, y1) in itertools.combinations(range(len(mpatt) + 1), 2):
            if x0 > x1 or y0 > y1:
                with pytest.raises(ValueError): mpatt.is_shaded((x0, y0), (x1, y1))
            elif x0 == x1 and y0 == y1:
                if (x0 + y0) % 2 == 0:
                    assert mpatt.is_shaded((x0, y0))
                    assert mpatt.is_shaded((x0, y0), (x1, y1))
            else:
                assert not mpatt.is_shaded((x0, y0), (x1, y1))
    with pytest.raises(ValueError): mpatt.is_shaded((4, 0))
    with pytest.raises(ValueError): mpatt.is_shaded((0, 4))
    with pytest.raises(ValueError): mpatt.is_shaded((-1, 2))
    with pytest.raises(ValueError): mpatt.is_shaded((0, 0), (0, 4))

def test_is_pointfree():
    mpatt = MeshPatt((0,1), [(0,0), (0,1), (1,0), (1,1)])
    assert not mpatt.is_pointfree((0,0), (1,1))
    assert not mpatt.is_pointfree((1,1), (2,2))
    assert not mpatt.is_pointfree((0,1), (2,2))
    assert mpatt.is_pointfree((0,1), (2,1))
    assert not mpatt.is_pointfree((0,1), (2,2))
    mpatt = MeshPatt((0,1,2), [(0,1), (1,1), (1,2), (2,1), (2,2), (3,1)])
    assert not mpatt.is_pointfree((1,1), (2,2))

def test_can_shade():
    assert not (MeshPatt().can_shade((0, 0)))
    assert MeshPatt((0,)).can_shade((0, 0)) == [0]
    assert MeshPatt((0,)).can_shade((1, 0)) == [0]
    assert not (MeshPatt((0,),[(0, 0)]).can_shade((0, 0)))
    assert not (MeshPatt((0,),[(0, 0)]).can_shade((1, 1)))
    assert not mesh_pattern.can_shade((1, 1))
    assert not mesh_pattern.can_shade((3, 2))
    assert not mesh_pattern.can_shade((1, 2))
    assert mesh_pattern.can_shade((0, 1)) == [1]
    mpatt = MeshPatt((1, 2, 0), [(2,2),(3,0),(3,2),(3,3)])
    assert list(sorted(mpatt.can_shade((1, 2)))) == [1, 2]
    assert mpatt.can_shade((3, 1)) == [0]

def test_can_simul_shade():
    assert not (MeshPatt().can_simul_shade((0, 0), (0, 0)))
    assert MeshPatt((0,)).can_simul_shade((0, 0), (0, 1)) == [0]
    assert not (MeshPatt((0, 1, 2)).can_simul_shade((2, 0), (2, 2)))
    assert not mesh1.can_simul_shade((2, 2), (3, 2))
    assert not mesh1.can_simul_shade((1, 2), (2, 2))
    assert not mesh2.can_simul_shade((3, 3), (4, 3))
    assert not mesh2.can_simul_shade((3, 4), (4, 4))
    assert not mesh1.can_simul_shade((4, 4), (4, 5))
    assert not mesh1.can_simul_shade((4, 5), (5, 5))
    assert mesh1.can_simul_shade((5, 4), (5, 5)) == [4]

    mpatt = MeshPatt((2, 3, 0, 1), [(0, 4), (1, 3), (2, 1), (2, 2), (3, 4), (4, 0), (4, 4)])
    assert mpatt.can_simul_shade((4, 1), (4, 2)) == [1]
    mpatt = MeshPatt((1, 2, 0), [(0, 2), (0, 3), (1, 1), (2, 0), (2, 1), (3, 2), (3, 3)])
    assert mpatt.can_simul_shade((2, 2), (2, 3)) == [2]
    assert not mpatt.can_simul_shade((1, 2), (2, 2))
    assert not mpatt.can_simul_shade((1, 2), (1, 3))

def test_shadable_boxes():
    assert not (MeshPatt().shadable_boxes())
    assert len(MeshPatt((0,)).shadable_boxes()[0]) == 8
    assert len(MeshPatt((0, 1)).shadable_boxes()[0]) == 8
    assert len(MeshPatt((0, 1)).shadable_boxes()[1]) == 8

def test_non_pointless_boxes():
    assert MeshPatt(Perm()).non_pointless_boxes() == set()
    assert MeshPatt((0,)).non_pointless_boxes() == set([(0, 0), (0, 1), (1, 0), (1, 1)])
    assert (MeshPatt((0, 1, 2), [(0, 0), (1, 2,), (0, 2), (2, 0), (2, 1)]).non_pointless_boxes() ==
            set([(0, 0), (0, 1), (1, 0), (1, 1), (1, 2), (2, 1), (2, 2), (2, 3), (3, 2), (3, 3)]))
    print(mesh2)
    assert (mesh2.non_pointless_boxes() == set([(0, 1), (0, 2), (1, 1), (1, 2),
        (1, 3), (2, 2), (2, 3), (2, 4), (2, 5), (3, 3), (3, 4), (3, 5), (4, 0),
        (4, 1), (4, 3), (4, 4), (5, 0), (5, 1)]))

def test_has_anchered_point():
    assert not any(MeshPatt(Perm()).has_anchored_point())
    assert all(MeshPatt(Perm(), [(0,0)]).has_anchored_point())
    assert not any(MeshPatt(Perm.random(5)).has_anchored_point())
    assert all(MeshPatt.unrank((1,2,0), 65535))
    right, top, left, bottom = MeshPatt((0, 1, 2), [(0,i) for i in range(4)]).has_anchored_point()
    assert left and not (right or top or bottom)
    right, top, left, bottom = MeshPatt((0, 1, 2), [(3,i) for i in range(4)]).has_anchored_point()
    assert right and not (left or top or bottom)
    right, top, left, bottom = MeshPatt((0, 1, 2), [(i,0) for i in range(4)]).has_anchored_point()
    assert bottom and not (left or top or right)
    right, top, left, bottom = MeshPatt((0, 1, 2), [(i,3) for i in range(4)]).has_anchored_point()
    assert top and not (left or bottom or right)

    mpatt = MeshPatt.random(5)
    leftshad = [(0,i) for i in range(len(mpatt) + 1)]
    rightshad = [(len(mpatt),i) for i in range(len(mpatt) + 1)]
    upshad = [(i,len(mpatt)) for i in range(len(mpatt) + 1)]
    bottomshad = [(i,0) for i in range(len(mpatt) + 1)]
    right, top, left, bottom = mpatt.shade(leftshad).has_anchored_point()
    assert left
    right, top, left, bottom = mpatt.shade(rightshad).has_anchored_point()
    assert right
    right, top, left, bottom = mpatt.shade(upshad).has_anchored_point()
    assert top
    right, top, left, bottom = mpatt.shade(bottomshad).has_anchored_point()
    assert bottom

def test_rank():
    assert MeshPatt(Perm((0, 1)), [(0, 1), (1, 2), (2, 1), (2, 0), (2, 2), (1, 1)]).rank() == 498
    assert MeshPatt(Perm((1, 0, 2)), [(3, 2), (0, 0), (2, 3), (1, 0), (0, 1), 
        (1, 2), (3, 3), (3, 1), (2, 0)]).rank() == 59731
    assert MeshPatt(Perm((0, 3, 2, 1)),
            [(0, 1), (4, 4), (1, 4), (2, 3), (4, 2), (4, 1), (0, 2)]).rank() == 23077382

    pattern = Perm([1,2])
    mesh = MeshPatt(pattern, set([(0,1), (0,2), (1,2), (2,0), (2,1)]))
    assert mesh.rank() == 230

    pattern = Perm([3,1,2])
    mesh = MeshPatt(pattern, set([(0,0), (0,1), (0,2), (1,0), (1,2), (2,0),
        (2,1), (2,2), (2,3), (3,0)]))
    assert mesh.rank() == 8023

    assert mesh1.rank() == 0b111000000001100000011000001000001

    for _ in range(50):
        mesh = MeshPatt.random(random.randint(0, 20))
        assert MeshPatt.unrank(mesh.pattern, mesh.rank()) == mesh

def test_unrank():
    assert MeshPatt.unrank(Perm((0, 1)), 498) == MeshPatt( Perm((0, 1)),
            frozenset({(0, 1), (1, 2), (2, 1), (2, 0), (2, 2), (1, 1)}))
    assert MeshPatt.unrank(Perm((1, 0, 2)), 59731) == MeshPatt( Perm((1, 0, 2)),
            frozenset({(3, 2), (0, 0), (2, 3), (1, 0), (0, 1), (1, 2), (3, 3), (3, 1), (2, 0)}))
    assert MeshPatt.unrank(Perm((0, 3, 2, 1)), 23077382) == MeshPatt(
            Perm((0, 3, 2, 1)),
            frozenset({(0, 1), (4, 4), (1, 4), (2, 3), (4, 2), (4, 1), (0, 2)}))

    pattern = Perm([1,2])
    mesh = MeshPatt(pattern, set([(0,1), (0,2), (1,2), (2,0), (2,1)]))
    assert MeshPatt.unrank(pattern, 230) == mesh

    pattern = Perm([3,1,2])
    mesh = MeshPatt(pattern, set([(0,0), (0,1), (0,2), (1,0), (1,2), (2,0),
        (2,1), (2,2), (2,3), (3,0)]))
    assert MeshPatt.unrank(pattern, 8023) == mesh

    assert MeshPatt.unrank(patt1, 0b111000000001100000011000001000001) ==  mesh1

    for length in range(20):
        m = MeshPatt.unrank(Perm.random(length), 0)
        assert not m.shading
    for length in range(20):
        m = MeshPatt.unrank(Perm.random(length), 2**((length + 1)**2) - 1)
        assert len(m.shading) == (length + 1)**2

    with pytest.raises(ValueError): MeshPatt.unrank([1,2,3], -1)
    with pytest.raises(ValueError): MeshPatt.unrank(Perm([1]), 16)
    with pytest.raises(ValueError): MeshPatt.unrank(Perm([1]), -1)
    with pytest.raises(TypeError): MeshPatt.unrank(Perm.random(length), 'haha')
    with pytest.raises(TypeError): MeshPatt.unrank(Perm([1]), "1")
    with pytest.raises(ValueError):
        MeshPatt.unrank(Perm.random(10), 2**((10 + 1)**2) + 1)

def test_random():
    assert MeshPatt.random(0) in set([MeshPatt(Perm(()), []), MeshPatt(Perm(()), [(0, 0)])])
    assert MeshPatt.random(1) in set(MeshPatt.unrank(Perm((0)), i) for i in range(0, 16))
    assert MeshPatt.random(2) in (
            set(MeshPatt.unrank(Perm((0, 1)), i) for i in range(0, 512))
            | set(MeshPatt.unrank(Perm((1, 0)), i) for i in range(0, 512)))
    for length in range(3, 20):
        assert len(MeshPatt.random(length)) == length

def test_len():
    assert len(mesh1) == 5
    assert len(mesh2) == 5
    assert len(mesh3) == 4
    assert len(MeshPatt()) == 0
    assert len(MeshPatt((1,))) == 1
    for _ in range(20):
        length = random.randint(0, 20)
        m = MeshPatt(Perm.random(length), random.sample([ (i,j) for i in range(length + 1) for j in range(length + 1)], k=length))
        assert len(m) == length

def test_bool():
    assert mesh1
    assert mesh2
    assert mesh3
    assert MeshPatt(Perm((1,)))
    assert MeshPatt((), set([(0,0)]))
    assert MeshPatt(Perm([0, 1, 2, 3]), ())
    assert MeshPatt(Perm([0, 1, 2, 3]), ((0, 0),))
    assert MeshPatt(Perm([0]), ())
    assert not (MeshPatt(Perm([]), ()))
    assert not (MeshPatt(Perm(), ()))

def test_eq():
    assert not (mesh1 == mesh2)
    assert not (mesh1 == mesh3)
    assert not (mesh2 == mesh1)
    assert not (mesh2 == mesh3)
    assert not (mesh3 == mesh1)
    assert not (mesh3 == mesh2)
    mesh1copy = MeshPatt(patt1, shad1)
    mesh2copy = MeshPatt(patt2, shad2)
    mesh3copy = MeshPatt(patt3, shad3)
    assert mesh1 == mesh1copy
    assert mesh2 == mesh2copy
    assert mesh3 == mesh3copy
    assert mesh1copy == mesh1copy
    assert mesh2copy == mesh2copy
    assert mesh3copy == mesh3copy

# def test_gen_meshpatts():
def gen_meshpatts():
    assert list(gen_meshpatts(0)) == [MeshPatt(), MeshPatt((), [(0, 0)])]
    assert len(list(gen_meshpatts(1))) == 2**4
    for i in range(2, 4):
        patt = Perm.random(i)
        len_i = list(gen_meshpatts(i, patt))
        assert(len(set(len_i))) == 2**((i + 1) ** 2)
        for mpatt in len_i:
            assert mpatt.pattern == patt
    len_i = list(gen_meshpatts(2))
    assert(len(set(len_i)) == (2**((2 + 1) ** 2)*factorial(2)))
    patt = tuple(Perm.random(3))
    len_i = list(gen_meshpatts(3, patt))
    assert(len(set(len_i))) == 2**((3 + 1) ** 2)

