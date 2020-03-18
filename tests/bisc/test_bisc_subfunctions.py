from permuta import Perm
from permuta.bisc.bisc_subfunctions import maximal_mesh_pattern_of_occurrence


def test_maximal_mesh_pattern_of_occurrence():
    assert maximal_mesh_pattern_of_occurrence(Perm((0,)), (0,)) == set(
        [(0, 0), (0, 1), (1, 0), (1, 1)]
    )
    assert maximal_mesh_pattern_of_occurrence(Perm((0, 1)), (0,)) == set(
        [(0, 0), (0, 1), (1, 0)]
    )
    assert maximal_mesh_pattern_of_occurrence(Perm((0, 1)), (1,)) == set(
        [(0, 1), (1, 0), (1, 1)]
    )
    assert maximal_mesh_pattern_of_occurrence(Perm((1, 0)), (0,)) == set(
        [(0, 0), (0, 1), (1, 1)]
    )
    assert maximal_mesh_pattern_of_occurrence(Perm((1, 0)), (1,)) == set(
        [(0, 0), (1, 0), (1, 1)]
    )
