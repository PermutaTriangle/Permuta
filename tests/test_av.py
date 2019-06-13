from permuta import Av
from permuta import Perm


def test_av_perm():
    p = Perm((0,1))
    av = Av([p])
    for length in range(10):
        assert len(set(av.of_length(length))) == 1
