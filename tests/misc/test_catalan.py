from permuta.misc import catalan


CATALAN_NUMBERS = [1,
                   1,
                   2,
                   5,
                  14,
                  42,
                 132,
                 429,
                1430,
                4862,
               16796,
               58786,
              208012,
              742900,
             2674440,
             9694845,
            35357670,
           129644790,
           477638700,
          1767263190,
          6564120420,
         24466267020,
         91482563640,
        343059613650,
       1289904147324,
       4861946401452,
      18367353072152,
      69533550916004,
     263747951750360,
    1002242216651368,
    3814986502092304]  # Such funny indentation


def test_first_few_catalan():
    for index, number in enumerate(CATALAN_NUMBERS):
        assert catalan(index) == number
