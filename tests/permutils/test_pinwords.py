# import pytest

from pathlib import Path

from automata.fa.dfa import DFA
from automata.fa.nfa import NFA

from permuta import Perm
from permuta.permutils.pin_words import PinWords


def test_pinwords_of_length():
    assert list(PinWords.pinwords_of_length(0)) == [""]
    assert list(PinWords.pinwords_of_length(1)) == ["1", "2", "3", "4"]
    assert list(PinWords.pinwords_of_length(2)) == [
        "1U",
        "1D",
        "1L",
        "1R",
        "11",
        "12",
        "13",
        "14",
        "2U",
        "2D",
        "2L",
        "2R",
        "21",
        "22",
        "23",
        "24",
        "3U",
        "3D",
        "3L",
        "3R",
        "31",
        "32",
        "33",
        "34",
        "4U",
        "4D",
        "4L",
        "4R",
        "41",
        "42",
        "43",
        "44",
    ]
    assert list(PinWords.pinwords_of_length(3)) == [
        "1UL",
        "1UR",
        "1U1",
        "1U2",
        "1U3",
        "1U4",
        "1DL",
        "1DR",
        "1D1",
        "1D2",
        "1D3",
        "1D4",
        "1LU",
        "1LD",
        "1L1",
        "1L2",
        "1L3",
        "1L4",
        "1RU",
        "1RD",
        "1R1",
        "1R2",
        "1R3",
        "1R4",
        "11U",
        "11D",
        "11L",
        "11R",
        "111",
        "112",
        "113",
        "114",
        "12U",
        "12D",
        "12L",
        "12R",
        "121",
        "122",
        "123",
        "124",
        "13U",
        "13D",
        "13L",
        "13R",
        "131",
        "132",
        "133",
        "134",
        "14U",
        "14D",
        "14L",
        "14R",
        "141",
        "142",
        "143",
        "144",
        "2UL",
        "2UR",
        "2U1",
        "2U2",
        "2U3",
        "2U4",
        "2DL",
        "2DR",
        "2D1",
        "2D2",
        "2D3",
        "2D4",
        "2LU",
        "2LD",
        "2L1",
        "2L2",
        "2L3",
        "2L4",
        "2RU",
        "2RD",
        "2R1",
        "2R2",
        "2R3",
        "2R4",
        "21U",
        "21D",
        "21L",
        "21R",
        "211",
        "212",
        "213",
        "214",
        "22U",
        "22D",
        "22L",
        "22R",
        "221",
        "222",
        "223",
        "224",
        "23U",
        "23D",
        "23L",
        "23R",
        "231",
        "232",
        "233",
        "234",
        "24U",
        "24D",
        "24L",
        "24R",
        "241",
        "242",
        "243",
        "244",
        "3UL",
        "3UR",
        "3U1",
        "3U2",
        "3U3",
        "3U4",
        "3DL",
        "3DR",
        "3D1",
        "3D2",
        "3D3",
        "3D4",
        "3LU",
        "3LD",
        "3L1",
        "3L2",
        "3L3",
        "3L4",
        "3RU",
        "3RD",
        "3R1",
        "3R2",
        "3R3",
        "3R4",
        "31U",
        "31D",
        "31L",
        "31R",
        "311",
        "312",
        "313",
        "314",
        "32U",
        "32D",
        "32L",
        "32R",
        "321",
        "322",
        "323",
        "324",
        "33U",
        "33D",
        "33L",
        "33R",
        "331",
        "332",
        "333",
        "334",
        "34U",
        "34D",
        "34L",
        "34R",
        "341",
        "342",
        "343",
        "344",
        "4UL",
        "4UR",
        "4U1",
        "4U2",
        "4U3",
        "4U4",
        "4DL",
        "4DR",
        "4D1",
        "4D2",
        "4D3",
        "4D4",
        "4LU",
        "4LD",
        "4L1",
        "4L2",
        "4L3",
        "4L4",
        "4RU",
        "4RD",
        "4R1",
        "4R2",
        "4R3",
        "4R4",
        "41U",
        "41D",
        "41L",
        "41R",
        "411",
        "412",
        "413",
        "414",
        "42U",
        "42D",
        "42L",
        "42R",
        "421",
        "422",
        "423",
        "424",
        "43U",
        "43D",
        "43L",
        "43R",
        "431",
        "432",
        "433",
        "434",
        "44U",
        "44D",
        "44L",
        "44R",
        "441",
        "442",
        "443",
        "444",
    ]


def test_pinword_to_perm_mapping():
    assert PinWords.pinword_to_perm_mapping(0) == {"": Perm(())}
    assert PinWords.pinword_to_perm_mapping(1) == {
        "1": Perm((0,)),
        "2": Perm((0,)),
        "3": Perm((0,)),
        "4": Perm((0,)),
    }
    assert PinWords.pinword_to_perm_mapping(2) == {
        "1U": Perm((1, 0)),
        "1D": Perm((0, 1)),
        "1L": Perm((0, 1)),
        "1R": Perm((1, 0)),
        "11": Perm((0, 1)),
        "12": Perm((1, 0)),
        "13": Perm((0, 1)),
        "14": Perm((1, 0)),
        "2U": Perm((0, 1)),
        "2D": Perm((1, 0)),
        "2L": Perm((0, 1)),
        "2R": Perm((1, 0)),
        "21": Perm((0, 1)),
        "22": Perm((1, 0)),
        "23": Perm((0, 1)),
        "24": Perm((1, 0)),
        "3U": Perm((0, 1)),
        "3D": Perm((1, 0)),
        "3L": Perm((1, 0)),
        "3R": Perm((0, 1)),
        "31": Perm((0, 1)),
        "32": Perm((1, 0)),
        "33": Perm((0, 1)),
        "34": Perm((1, 0)),
        "4U": Perm((1, 0)),
        "4D": Perm((0, 1)),
        "4L": Perm((1, 0)),
        "4R": Perm((0, 1)),
        "41": Perm((0, 1)),
        "42": Perm((1, 0)),
        "43": Perm((0, 1)),
        "44": Perm((1, 0)),
    }
    assert PinWords.pinword_to_perm_mapping(3) == {
        "1UL": Perm((1, 2, 0)),
        "1UR": Perm((2, 0, 1)),
        "1U1": Perm((1, 0, 2)),
        "1U2": Perm((2, 1, 0)),
        "1U3": Perm((0, 2, 1)),
        "1U4": Perm((2, 1, 0)),
        "1DL": Perm((1, 0, 2)),
        "1DR": Perm((0, 2, 1)),
        "1D1": Perm((0, 1, 2)),
        "1D2": Perm((2, 0, 1)),
        "1D3": Perm((0, 1, 2)),
        "1D4": Perm((1, 2, 0)),
        "1LU": Perm((0, 2, 1)),
        "1LD": Perm((1, 0, 2)),
        "1L1": Perm((0, 1, 2)),
        "1L2": Perm((2, 0, 1)),
        "1L3": Perm((0, 1, 2)),
        "1L4": Perm((1, 2, 0)),
        "1RU": Perm((1, 2, 0)),
        "1RD": Perm((2, 0, 1)),
        "1R1": Perm((1, 0, 2)),
        "1R2": Perm((2, 1, 0)),
        "1R3": Perm((0, 2, 1)),
        "1R4": Perm((2, 1, 0)),
        "11U": Perm((0, 2, 1)),
        "11D": Perm((1, 0, 2)),
        "11L": Perm((1, 0, 2)),
        "11R": Perm((0, 2, 1)),
        "111": Perm((0, 1, 2)),
        "112": Perm((2, 0, 1)),
        "113": Perm((0, 1, 2)),
        "114": Perm((1, 2, 0)),
        "12U": Perm((1, 2, 0)),
        "12D": Perm((2, 0, 1)),
        "12L": Perm((1, 2, 0)),
        "12R": Perm((2, 0, 1)),
        "121": Perm((1, 0, 2)),
        "122": Perm((2, 1, 0)),
        "123": Perm((0, 2, 1)),
        "124": Perm((2, 1, 0)),
        "13U": Perm((0, 2, 1)),
        "13D": Perm((1, 0, 2)),
        "13L": Perm((1, 0, 2)),
        "13R": Perm((0, 2, 1)),
        "131": Perm((0, 1, 2)),
        "132": Perm((2, 0, 1)),
        "133": Perm((0, 1, 2)),
        "134": Perm((1, 2, 0)),
        "14U": Perm((1, 2, 0)),
        "14D": Perm((2, 0, 1)),
        "14L": Perm((1, 2, 0)),
        "14R": Perm((2, 0, 1)),
        "141": Perm((1, 0, 2)),
        "142": Perm((2, 1, 0)),
        "143": Perm((0, 2, 1)),
        "144": Perm((2, 1, 0)),
        "2UL": Perm((1, 0, 2)),
        "2UR": Perm((0, 2, 1)),
        "2U1": Perm((0, 1, 2)),
        "2U2": Perm((2, 0, 1)),
        "2U3": Perm((0, 1, 2)),
        "2U4": Perm((1, 2, 0)),
        "2DL": Perm((1, 2, 0)),
        "2DR": Perm((2, 0, 1)),
        "2D1": Perm((1, 0, 2)),
        "2D2": Perm((2, 1, 0)),
        "2D3": Perm((0, 2, 1)),
        "2D4": Perm((2, 1, 0)),
        "2LU": Perm((0, 2, 1)),
        "2LD": Perm((1, 0, 2)),
        "2L1": Perm((0, 1, 2)),
        "2L2": Perm((2, 0, 1)),
        "2L3": Perm((0, 1, 2)),
        "2L4": Perm((1, 2, 0)),
        "2RU": Perm((1, 2, 0)),
        "2RD": Perm((2, 0, 1)),
        "2R1": Perm((1, 0, 2)),
        "2R2": Perm((2, 1, 0)),
        "2R3": Perm((0, 2, 1)),
        "2R4": Perm((2, 1, 0)),
        "21U": Perm((0, 2, 1)),
        "21D": Perm((1, 0, 2)),
        "21L": Perm((1, 0, 2)),
        "21R": Perm((0, 2, 1)),
        "211": Perm((0, 1, 2)),
        "212": Perm((2, 0, 1)),
        "213": Perm((0, 1, 2)),
        "214": Perm((1, 2, 0)),
        "22U": Perm((1, 2, 0)),
        "22D": Perm((2, 0, 1)),
        "22L": Perm((1, 2, 0)),
        "22R": Perm((2, 0, 1)),
        "221": Perm((1, 0, 2)),
        "222": Perm((2, 1, 0)),
        "223": Perm((0, 2, 1)),
        "224": Perm((2, 1, 0)),
        "23U": Perm((0, 2, 1)),
        "23D": Perm((1, 0, 2)),
        "23L": Perm((1, 0, 2)),
        "23R": Perm((0, 2, 1)),
        "231": Perm((0, 1, 2)),
        "232": Perm((2, 0, 1)),
        "233": Perm((0, 1, 2)),
        "234": Perm((1, 2, 0)),
        "24U": Perm((1, 2, 0)),
        "24D": Perm((2, 0, 1)),
        "24L": Perm((1, 2, 0)),
        "24R": Perm((2, 0, 1)),
        "241": Perm((1, 0, 2)),
        "242": Perm((2, 1, 0)),
        "243": Perm((0, 2, 1)),
        "244": Perm((2, 1, 0)),
        "3UL": Perm((1, 0, 2)),
        "3UR": Perm((0, 2, 1)),
        "3U1": Perm((0, 1, 2)),
        "3U2": Perm((2, 0, 1)),
        "3U3": Perm((0, 1, 2)),
        "3U4": Perm((1, 2, 0)),
        "3DL": Perm((1, 2, 0)),
        "3DR": Perm((2, 0, 1)),
        "3D1": Perm((1, 0, 2)),
        "3D2": Perm((2, 1, 0)),
        "3D3": Perm((0, 2, 1)),
        "3D4": Perm((2, 1, 0)),
        "3LU": Perm((1, 2, 0)),
        "3LD": Perm((2, 0, 1)),
        "3L1": Perm((1, 0, 2)),
        "3L2": Perm((2, 1, 0)),
        "3L3": Perm((0, 2, 1)),
        "3L4": Perm((2, 1, 0)),
        "3RU": Perm((0, 2, 1)),
        "3RD": Perm((1, 0, 2)),
        "3R1": Perm((0, 1, 2)),
        "3R2": Perm((2, 0, 1)),
        "3R3": Perm((0, 1, 2)),
        "3R4": Perm((1, 2, 0)),
        "31U": Perm((0, 2, 1)),
        "31D": Perm((1, 0, 2)),
        "31L": Perm((1, 0, 2)),
        "31R": Perm((0, 2, 1)),
        "311": Perm((0, 1, 2)),
        "312": Perm((2, 0, 1)),
        "313": Perm((0, 1, 2)),
        "314": Perm((1, 2, 0)),
        "32U": Perm((1, 2, 0)),
        "32D": Perm((2, 0, 1)),
        "32L": Perm((1, 2, 0)),
        "32R": Perm((2, 0, 1)),
        "321": Perm((1, 0, 2)),
        "322": Perm((2, 1, 0)),
        "323": Perm((0, 2, 1)),
        "324": Perm((2, 1, 0)),
        "33U": Perm((0, 2, 1)),
        "33D": Perm((1, 0, 2)),
        "33L": Perm((1, 0, 2)),
        "33R": Perm((0, 2, 1)),
        "331": Perm((0, 1, 2)),
        "332": Perm((2, 0, 1)),
        "333": Perm((0, 1, 2)),
        "334": Perm((1, 2, 0)),
        "34U": Perm((1, 2, 0)),
        "34D": Perm((2, 0, 1)),
        "34L": Perm((1, 2, 0)),
        "34R": Perm((2, 0, 1)),
        "341": Perm((1, 0, 2)),
        "342": Perm((2, 1, 0)),
        "343": Perm((0, 2, 1)),
        "344": Perm((2, 1, 0)),
        "4UL": Perm((1, 2, 0)),
        "4UR": Perm((2, 0, 1)),
        "4U1": Perm((1, 0, 2)),
        "4U2": Perm((2, 1, 0)),
        "4U3": Perm((0, 2, 1)),
        "4U4": Perm((2, 1, 0)),
        "4DL": Perm((1, 0, 2)),
        "4DR": Perm((0, 2, 1)),
        "4D1": Perm((0, 1, 2)),
        "4D2": Perm((2, 0, 1)),
        "4D3": Perm((0, 1, 2)),
        "4D4": Perm((1, 2, 0)),
        "4LU": Perm((1, 2, 0)),
        "4LD": Perm((2, 0, 1)),
        "4L1": Perm((1, 0, 2)),
        "4L2": Perm((2, 1, 0)),
        "4L3": Perm((0, 2, 1)),
        "4L4": Perm((2, 1, 0)),
        "4RU": Perm((0, 2, 1)),
        "4RD": Perm((1, 0, 2)),
        "4R1": Perm((0, 1, 2)),
        "4R2": Perm((2, 0, 1)),
        "4R3": Perm((0, 1, 2)),
        "4R4": Perm((1, 2, 0)),
        "41U": Perm((0, 2, 1)),
        "41D": Perm((1, 0, 2)),
        "41L": Perm((1, 0, 2)),
        "41R": Perm((0, 2, 1)),
        "411": Perm((0, 1, 2)),
        "412": Perm((2, 0, 1)),
        "413": Perm((0, 1, 2)),
        "414": Perm((1, 2, 0)),
        "42U": Perm((1, 2, 0)),
        "42D": Perm((2, 0, 1)),
        "42L": Perm((1, 2, 0)),
        "42R": Perm((2, 0, 1)),
        "421": Perm((1, 0, 2)),
        "422": Perm((2, 1, 0)),
        "423": Perm((0, 2, 1)),
        "424": Perm((2, 1, 0)),
        "43U": Perm((0, 2, 1)),
        "43D": Perm((1, 0, 2)),
        "43L": Perm((1, 0, 2)),
        "43R": Perm((0, 2, 1)),
        "431": Perm((0, 1, 2)),
        "432": Perm((2, 0, 1)),
        "433": Perm((0, 1, 2)),
        "434": Perm((1, 2, 0)),
        "44U": Perm((1, 2, 0)),
        "44D": Perm((2, 0, 1)),
        "44L": Perm((1, 2, 0)),
        "44R": Perm((2, 0, 1)),
        "441": Perm((1, 0, 2)),
        "442": Perm((2, 1, 0)),
        "443": Perm((0, 2, 1)),
        "444": Perm((2, 1, 0)),
    }


def test_perm_to_pinword_mapping():
    assert PinWords.perm_to_pinword_mapping(0) == {Perm(()): {""}}
    assert PinWords.perm_to_pinword_mapping(1) == {Perm((0,)): {"1", "2", "3", "4"}}
    assert PinWords.perm_to_pinword_mapping(2) == {
        Perm((1, 0)): {
            "4L",
            "12",
            "24",
            "3L",
            "42",
            "2D",
            "34",
            "32",
            "44",
            "1U",
            "22",
            "2R",
            "4U",
            "14",
            "1R",
            "3D",
        },
        Perm((0, 1)): {
            "43",
            "23",
            "2U",
            "4R",
            "13",
            "3U",
            "3R",
            "11",
            "41",
            "21",
            "1D",
            "1L",
            "2L",
            "31",
            "33",
            "4D",
        },
    }
    assert PinWords.perm_to_pinword_mapping(3) == {
        Perm((1, 2, 0)): {
            "4LU",
            "44U",
            "14U",
            "12L",
            "2DL",
            "1RU",
            "14L",
            "1UL",
            "3DL",
            "4R4",
            "22L",
            "214",
            "114",
            "4D4",
            "32L",
            "32U",
            "34U",
            "22U",
            "12U",
            "24U",
            "3R4",
            "34L",
            "4UL",
            "234",
            "2U4",
            "434",
            "2L4",
            "1L4",
            "2RU",
            "414",
            "44L",
            "334",
            "42L",
            "24L",
            "3LU",
            "134",
            "42U",
            "3U4",
            "1D4",
            "314",
        },
        Perm((2, 0, 1)): {
            "24R",
            "32R",
            "4UR",
            "1L2",
            "1UR",
            "42D",
            "3R2",
            "42R",
            "2U2",
            "44D",
            "4LD",
            "132",
            "2L2",
            "312",
            "22D",
            "3DR",
            "232",
            "12D",
            "34D",
            "44R",
            "12R",
            "212",
            "432",
            "14R",
            "32D",
            "4D2",
            "332",
            "24D",
            "1D2",
            "34R",
            "412",
            "4R2",
            "112",
            "14D",
            "2RD",
            "1RD",
            "22R",
            "3LD",
            "3U2",
            "2DR",
        },
        Perm((1, 0, 2)): {
            "1DL",
            "1R1",
            "2D1",
            "13D",
            "3UL",
            "11D",
            "13L",
            "31D",
            "21D",
            "2LD",
            "2R1",
            "1LD",
            "241",
            "3RD",
            "43D",
            "321",
            "221",
            "43L",
            "3L1",
            "1U1",
            "33L",
            "23L",
            "4L1",
            "421",
            "31L",
            "121",
            "41L",
            "11L",
            "23D",
            "4RD",
            "441",
            "341",
            "21L",
            "3D1",
            "33D",
            "4U1",
            "2UL",
            "141",
            "41D",
            "4DL",
        },
        Perm((2, 1, 0)): {
            "322",
            "4L4",
            "424",
            "2R2",
            "422",
            "1U4",
            "124",
            "142",
            "344",
            "122",
            "4U2",
            "4L2",
            "3L2",
            "3D4",
            "1R2",
            "1R4",
            "244",
            "324",
            "342",
            "222",
            "442",
            "242",
            "3L4",
            "224",
            "2R4",
            "1U2",
            "4U4",
            "2D2",
            "144",
            "444",
            "2D4",
            "3D2",
        },
        Perm((0, 2, 1)): {
            "2LU",
            "143",
            "4DR",
            "41R",
            "41U",
            "423",
            "1R3",
            "33R",
            "43U",
            "2UR",
            "31R",
            "1LU",
            "243",
            "21R",
            "443",
            "31U",
            "123",
            "33U",
            "4RU",
            "23R",
            "343",
            "11R",
            "13R",
            "4U3",
            "2D3",
            "1DR",
            "323",
            "43R",
            "3UR",
            "13U",
            "3L3",
            "2R3",
            "21U",
            "3RU",
            "4L3",
            "3D3",
            "11U",
            "1U3",
            "223",
            "23U",
        },
        Perm((0, 1, 2)): {
            "4D3",
            "413",
            "4D1",
            "3U3",
            "2U1",
            "233",
            "231",
            "1L3",
            "111",
            "113",
            "213",
            "313",
            "4R3",
            "411",
            "3R3",
            "1D3",
            "431",
            "3U1",
            "3R1",
            "311",
            "433",
            "211",
            "131",
            "1D1",
            "4R1",
            "2L3",
            "333",
            "2L1",
            "331",
            "2U3",
            "133",
            "1L1",
        },
    }


def test_is_strict_pinword():
    assert PinWords.is_strict_pinword("") is True
    assert PinWords.is_strict_pinword("1") is True
    assert PinWords.is_strict_pinword("2") is True
    assert PinWords.is_strict_pinword("3") is True
    assert PinWords.is_strict_pinword("4") is True
    assert PinWords.is_strict_pinword("1U") is True
    assert PinWords.is_strict_pinword("1D") is True
    assert PinWords.is_strict_pinword("1L") is True
    assert PinWords.is_strict_pinword("1R") is True
    assert PinWords.is_strict_pinword("11") is False
    assert PinWords.is_strict_pinword("12") is False
    assert PinWords.is_strict_pinword("13") is False
    assert PinWords.is_strict_pinword("14") is False
    assert PinWords.is_strict_pinword("2U") is True
    assert PinWords.is_strict_pinword("2D") is True
    assert PinWords.is_strict_pinword("2L") is True
    assert PinWords.is_strict_pinword("2R") is True
    assert PinWords.is_strict_pinword("21") is False
    assert PinWords.is_strict_pinword("22") is False
    assert PinWords.is_strict_pinword("23") is False
    assert PinWords.is_strict_pinword("24") is False
    assert PinWords.is_strict_pinword("3U") is True
    assert PinWords.is_strict_pinword("3D") is True
    assert PinWords.is_strict_pinword("3L") is True
    assert PinWords.is_strict_pinword("3R") is True
    assert PinWords.is_strict_pinword("31") is False
    assert PinWords.is_strict_pinword("32") is False
    assert PinWords.is_strict_pinword("33") is False
    assert PinWords.is_strict_pinword("34") is False
    assert PinWords.is_strict_pinword("4U") is True
    assert PinWords.is_strict_pinword("4D") is True
    assert PinWords.is_strict_pinword("4L") is True
    assert PinWords.is_strict_pinword("4R") is True
    assert PinWords.is_strict_pinword("41") is False
    assert PinWords.is_strict_pinword("42") is False
    assert PinWords.is_strict_pinword("43") is False
    assert PinWords.is_strict_pinword("44") is False
    assert PinWords.is_strict_pinword("434") is False
    assert PinWords.is_strict_pinword("2D1") is False
    assert PinWords.is_strict_pinword("3U3") is False
    assert PinWords.is_strict_pinword("34R") is False
    assert PinWords.is_strict_pinword("24D") is False
    assert PinWords.is_strict_pinword("43U") is False
    assert PinWords.is_strict_pinword("4LD") is True
    assert PinWords.is_strict_pinword("3U4") is False
    assert PinWords.is_strict_pinword("33U") is False
    assert PinWords.is_strict_pinword("34U") is False
    assert PinWords.is_strict_pinword("3L4") is False
    assert PinWords.is_strict_pinword("214") is False
    assert PinWords.is_strict_pinword("2UR") is True
    assert PinWords.is_strict_pinword("3D3D") is False
    assert PinWords.is_strict_pinword("3U3R") is False
    assert PinWords.is_strict_pinword("21UL") is False
    assert PinWords.is_strict_pinword("2RD2") is False
    assert PinWords.is_strict_pinword("4R4D") is False
    assert PinWords.is_strict_pinword("113R") is False
    assert PinWords.is_strict_pinword("2L14") is False
    assert PinWords.is_strict_pinword("33LD") is False
    assert PinWords.is_strict_pinword("44UL") is False
    assert PinWords.is_strict_pinword("224D") is False
    assert PinWords.is_strict_pinword("3D3R") is False
    assert PinWords.is_strict_pinword("3423") is False
    assert PinWords.is_strict_pinword("21RU") is False
    assert PinWords.is_strict_pinword("1ULU") is True
    assert PinWords.is_strict_pinword("411R") is False
    assert PinWords.is_strict_pinword("43L2") is False


def test_stict_pinwords_of_length():
    assert list(PinWords.strict_pinwords_of_length(0)) == [""]
    assert list(PinWords.strict_pinwords_of_length(1)) == ["1", "2", "3", "4"]
    assert list(PinWords.strict_pinwords_of_length(2)) == [
        "1U",
        "1D",
        "1L",
        "1R",
        "2U",
        "2D",
        "2L",
        "2R",
        "3U",
        "3D",
        "3L",
        "3R",
        "4U",
        "4D",
        "4L",
        "4R",
    ]
    assert list(PinWords.strict_pinwords_of_length(3)) == [
        "1UL",
        "1UR",
        "1DL",
        "1DR",
        "1LU",
        "1LD",
        "1RU",
        "1RD",
        "2UL",
        "2UR",
        "2DL",
        "2DR",
        "2LU",
        "2LD",
        "2RU",
        "2RD",
        "3UL",
        "3UR",
        "3DL",
        "3DR",
        "3LU",
        "3LD",
        "3RU",
        "3RD",
        "4UL",
        "4UR",
        "4DL",
        "4DR",
        "4LU",
        "4LD",
        "4RU",
        "4RD",
    ]
    assert list(PinWords.strict_pinwords_of_length(4)) == [
        "1ULU",
        "1ULD",
        "1URU",
        "1URD",
        "1DLU",
        "1DLD",
        "1DRU",
        "1DRD",
        "1LUL",
        "1LUR",
        "1LDL",
        "1LDR",
        "1RUL",
        "1RUR",
        "1RDL",
        "1RDR",
        "2ULU",
        "2ULD",
        "2URU",
        "2URD",
        "2DLU",
        "2DLD",
        "2DRU",
        "2DRD",
        "2LUL",
        "2LUR",
        "2LDL",
        "2LDR",
        "2RUL",
        "2RUR",
        "2RDL",
        "2RDR",
        "3ULU",
        "3ULD",
        "3URU",
        "3URD",
        "3DLU",
        "3DLD",
        "3DRU",
        "3DRD",
        "3LUL",
        "3LUR",
        "3LDL",
        "3LDR",
        "3RUL",
        "3RUR",
        "3RDL",
        "3RDR",
        "4ULU",
        "4ULD",
        "4URU",
        "4URD",
        "4DLU",
        "4DLD",
        "4DRU",
        "4DRD",
        "4LUL",
        "4LUR",
        "4LDL",
        "4LDR",
        "4RUL",
        "4RUR",
        "4RDL",
        "4RDR",
    ]
    assert list(PinWords.strict_pinwords_of_length(5)) == [
        "1ULUL",
        "1ULUR",
        "1ULDL",
        "1ULDR",
        "1URUL",
        "1URUR",
        "1URDL",
        "1URDR",
        "1DLUL",
        "1DLUR",
        "1DLDL",
        "1DLDR",
        "1DRUL",
        "1DRUR",
        "1DRDL",
        "1DRDR",
        "1LULU",
        "1LULD",
        "1LURU",
        "1LURD",
        "1LDLU",
        "1LDLD",
        "1LDRU",
        "1LDRD",
        "1RULU",
        "1RULD",
        "1RURU",
        "1RURD",
        "1RDLU",
        "1RDLD",
        "1RDRU",
        "1RDRD",
        "2ULUL",
        "2ULUR",
        "2ULDL",
        "2ULDR",
        "2URUL",
        "2URUR",
        "2URDL",
        "2URDR",
        "2DLUL",
        "2DLUR",
        "2DLDL",
        "2DLDR",
        "2DRUL",
        "2DRUR",
        "2DRDL",
        "2DRDR",
        "2LULU",
        "2LULD",
        "2LURU",
        "2LURD",
        "2LDLU",
        "2LDLD",
        "2LDRU",
        "2LDRD",
        "2RULU",
        "2RULD",
        "2RURU",
        "2RURD",
        "2RDLU",
        "2RDLD",
        "2RDRU",
        "2RDRD",
        "3ULUL",
        "3ULUR",
        "3ULDL",
        "3ULDR",
        "3URUL",
        "3URUR",
        "3URDL",
        "3URDR",
        "3DLUL",
        "3DLUR",
        "3DLDL",
        "3DLDR",
        "3DRUL",
        "3DRUR",
        "3DRDL",
        "3DRDR",
        "3LULU",
        "3LULD",
        "3LURU",
        "3LURD",
        "3LDLU",
        "3LDLD",
        "3LDRU",
        "3LDRD",
        "3RULU",
        "3RULD",
        "3RURU",
        "3RURD",
        "3RDLU",
        "3RDLD",
        "3RDRU",
        "3RDRD",
        "4ULUL",
        "4ULUR",
        "4ULDL",
        "4ULDR",
        "4URUL",
        "4URUR",
        "4URDL",
        "4URDR",
        "4DLUL",
        "4DLUR",
        "4DLDL",
        "4DLDR",
        "4DRUL",
        "4DRUR",
        "4DRDL",
        "4DRDR",
        "4LULU",
        "4LULD",
        "4LURU",
        "4LURD",
        "4LDLU",
        "4LDLD",
        "4LDRU",
        "4LDRD",
        "4RULU",
        "4RULD",
        "4RURU",
        "4RURD",
        "4RDLU",
        "4RDLD",
        "4RDRU",
        "4RDRD",
    ]


def test_perm_to_strict_pinword_mapping():
    assert PinWords.perm_to_strict_pinword_mapping(0) == {Perm(()): {""}}
    assert PinWords.perm_to_strict_pinword_mapping(1) == {
        Perm((0,)): {"3", "2", "4", "1"}
    }
    assert PinWords.perm_to_strict_pinword_mapping(2) == {
        Perm((1, 0)): {"3D", "3L", "4U", "2R", "2D", "1U", "4L", "1R"},
        Perm((0, 1)): {"2U", "2L", "3U", "4R", "1D", "4D", "1L", "3R"},
    }
    assert PinWords.perm_to_strict_pinword_mapping(3) == {
        Perm((1, 2, 0)): {"4LU", "2DL", "3DL", "1UL", "4UL", "2RU", "3LU", "1RU"},
        Perm((2, 0, 1)): {"2DR", "4LD", "4UR", "3LD", "2RD", "3DR", "1RD", "1UR"},
        Perm((1, 0, 2)): {"2UL", "2LD", "4DL", "4RD", "1DL", "3RD", "3UL", "1LD"},
        Perm((2, 1, 0)): set(),
        Perm((0, 2, 1)): {"3UR", "2LU", "4RU", "1DR", "1LU", "4DR", "3RU", "2UR"},
        Perm((0, 1, 2)): set(),
    }
    assert PinWords.perm_to_strict_pinword_mapping(4) == {
        Perm((1, 3, 2, 0)): {"1ULU", "2DLU", "4ULU", "3DLU"},
        Perm((2, 0, 3, 1)): {
            "3RUL",
            "4RDR",
            "4URU",
            "3DRU",
            "3RDR",
            "1ULD",
            "4ULD",
            "1URU",
            "3DLD",
            "1LDR",
            "2DRU",
            "1LUL",
            "2DLD",
            "4RUL",
            "2LDR",
            "2LUL",
        },
        Perm((1, 2, 0, 3)): {"4RDL", "2LDL", "1LDL", "3RDL"},
        Perm((3, 1, 2, 0)): set(),
        Perm((0, 2, 3, 1)): {"4DRU", "3URU", "1DRU", "2URU"},
        Perm((2, 3, 1, 0)): set(),
        Perm((3, 1, 0, 2)): {"2DRD", "3DRD", "1URD", "4URD"},
        Perm((2, 0, 1, 3)): {"3ULD", "2ULD", "1DLD", "4DLD"},
        Perm((3, 2, 0, 1)): set(),
        Perm((0, 3, 1, 2)): {"4RUR", "1LUR", "3RUR", "2LUR"},
        Perm((1, 0, 3, 2)): set(),
        Perm((2, 1, 0, 3)): set(),
        Perm((1, 0, 2, 3)): set(),
        Perm((0, 2, 1, 3)): set(),
        Perm((2, 1, 3, 0)): {"1RUL", "4LUL", "3LUL", "2RUL"},
        Perm((3, 0, 2, 1)): {"3LDR", "4LDR", "1RDR", "2RDR"},
        Perm((3, 2, 1, 0)): set(),
        Perm((0, 3, 2, 1)): set(),
        Perm((0, 1, 3, 2)): set(),
        Perm((1, 3, 0, 2)): {
            "4DLU",
            "4DRD",
            "4LUR",
            "4LDL",
            "1DLU",
            "3URD",
            "3LDL",
            "2RUR",
            "1RDL",
            "2ULU",
            "2URD",
            "1DRD",
            "2RDL",
            "1RUR",
            "3LUR",
            "3ULU",
        },
        Perm((0, 1, 2, 3)): set(),
        Perm((3, 0, 1, 2)): set(),
        Perm((1, 2, 3, 0)): set(),
        Perm((2, 3, 0, 1)): set(),
    }
    assert PinWords.perm_to_strict_pinword_mapping(5) == {
        Perm((3, 1, 4, 2, 0)): {"1ULUL", "2DLUL", "3DLUL", "4ULUL"},
        Perm((1, 4, 2, 0, 3)): {
            "4RURD",
            "2LDLU",
            "1URDL",
            "3RDLU",
            "1LDLU",
            "2LURD",
            "3RURD",
            "4ULUR",
            "3DLUR",
            "4URDL",
            "4RDLU",
            "1LURD",
            "2DRDL",
            "1ULUR",
            "3DRDL",
            "2DLUR",
        },
        Perm((1, 3, 2, 0, 4)): set(),
        Perm((4, 1, 3, 2, 0)): set(),
        Perm((0, 2, 4, 3, 1)): set(),
        Perm((2, 4, 3, 1, 0)): set(),
        Perm((1, 3, 0, 4, 2)): {
            "2DLDL",
            "1RURU",
            "3DLDL",
            "4LURU",
            "2RURU",
            "4ULDL",
            "1ULDL",
            "3LURU",
        },
        Perm((3, 0, 4, 2, 1)): {"1ULDR", "4ULDR", "2DLDR", "3DLDR"},
        Perm((2, 0, 3, 1, 4)): {"1LDLD", "2LDLD", "4RDLD", "3RDLD"},
        Perm((4, 2, 0, 3, 1)): {"3DRDR", "4URDR", "2DRDR", "1URDR"},
        Perm((0, 3, 1, 4, 2)): {"1LURU", "4RURU", "2LURU", "3RURU"},
        Perm((1, 2, 0, 4, 3)): set(),
        Perm((2, 3, 1, 0, 4)): set(),
        Perm((3, 1, 2, 0, 4)): set(),
        Perm((1, 2, 0, 3, 4)): set(),
        Perm((4, 1, 2, 0, 3)): set(),
        Perm((0, 2, 3, 1, 4)): set(),
        Perm((2, 3, 1, 4, 0)): set(),
        Perm((3, 4, 1, 2, 0)): set(),
        Perm((4, 0, 2, 3, 1)): set(),
        Perm((4, 3, 1, 2, 0)): set(),
        Perm((0, 4, 2, 3, 1)): set(),
        Perm((4, 2, 3, 1, 0)): set(),
        Perm((1, 0, 3, 4, 2)): set(),
        Perm((0, 3, 4, 2, 1)): set(),
        Perm((0, 1, 3, 4, 2)): set(),
        Perm((1, 3, 4, 2, 0)): set(),
        Perm((3, 4, 2, 0, 1)): set(),
        Perm((3, 4, 2, 1, 0)): set(),
        Perm((3, 2, 0, 4, 1)): {"3DRUL", "4URUL", "1URUL", "2DRUL"},
        Perm((2, 0, 4, 1, 3)): {
            "3LDLD",
            "4LDLD",
            "4URUR",
            "1URUR",
            "2DRUR",
            "1RDLD",
            "2RDLD",
            "3DRUR",
        },
        Perm((3, 1, 0, 2, 4)): set(),
        Perm((4, 3, 1, 0, 2)): set(),
        Perm((0, 4, 2, 1, 3)): set(),
        Perm((4, 2, 1, 3, 0)): set(),
        Perm((2, 0, 1, 4, 3)): set(),
        Perm((3, 2, 0, 1, 4)): set(),
        Perm((2, 0, 1, 3, 4)): set(),
        Perm((4, 2, 0, 1, 3)): set(),
        Perm((0, 3, 1, 2, 4)): set(),
        Perm((3, 1, 2, 4, 0)): set(),
        Perm((4, 0, 3, 1, 2)): set(),
        Perm((4, 3, 2, 0, 1)): set(),
        Perm((0, 4, 3, 1, 2)): set(),
        Perm((1, 0, 4, 2, 3)): set(),
        Perm((0, 1, 4, 2, 3)): set(),
        Perm((1, 4, 2, 3, 0)): set(),
        Perm((4, 2, 3, 0, 1)): set(),
        Perm((3, 1, 0, 4, 2)): set(),
        Perm((1, 0, 3, 2, 4)): set(),
        Perm((4, 1, 0, 3, 2)): set(),
        Perm((0, 2, 1, 4, 3)): set(),
        Perm((2, 1, 4, 3, 0)): set(),
        Perm((2, 1, 0, 3, 4)): set(),
        Perm((4, 2, 1, 0, 3)): set(),
        Perm((0, 3, 2, 1, 4)): set(),
        Perm((3, 2, 1, 4, 0)): set(),
        Perm((2, 4, 1, 0, 3)): {"1RURD", "3LURD", "2RURD", "4LURD"},
        Perm((3, 0, 2, 1, 4)): set(),
        Perm((2, 1, 4, 0, 3)): set(),
        Perm((1, 0, 2, 4, 3)): set(),
        Perm((2, 1, 3, 0, 4)): set(),
        Perm((1, 0, 2, 3, 4)): set(),
        Perm((4, 1, 0, 2, 3)): set(),
        Perm((0, 2, 1, 3, 4)): set(),
        Perm((2, 1, 3, 4, 0)): set(),
        Perm((3, 4, 1, 0, 2)): set(),
        Perm((4, 0, 2, 1, 3)): set(),
        Perm((0, 3, 2, 4, 1)): set(),
        Perm((0, 1, 3, 2, 4)): set(),
        Perm((1, 3, 2, 4, 0)): set(),
        Perm((3, 2, 4, 0, 1)): set(),
        Perm((3, 2, 4, 1, 0)): set(),
        Perm((1, 4, 0, 3, 2)): set(),
        Perm((4, 0, 3, 2, 1)): set(),
        Perm((4, 3, 0, 2, 1)): set(),
        Perm((0, 4, 1, 3, 2)): set(),
        Perm((2, 1, 0, 4, 3)): set(),
        Perm((3, 2, 1, 0, 4)): set(),
        Perm((4, 3, 2, 1, 0)): set(),
        Perm((0, 4, 3, 2, 1)): set(),
        Perm((1, 0, 4, 3, 2)): set(),
        Perm((0, 1, 4, 3, 2)): set(),
        Perm((1, 4, 3, 2, 0)): set(),
        Perm((2, 0, 4, 3, 1)): set(),
        Perm((1, 4, 3, 0, 2)): {"4LDLU", "3LDLU", "1RDLU", "2RDLU"},
        Perm((3, 4, 0, 2, 1)): set(),
        Perm((4, 0, 1, 3, 2)): set(),
        Perm((0, 1, 2, 4, 3)): set(),
        Perm((1, 2, 4, 3, 0)): set(),
        Perm((2, 4, 3, 0, 1)): set(),
        Perm((3, 1, 4, 0, 2)): {
            "1DLUL",
            "1LDRD",
            "3ULUL",
            "4DLUL",
            "2ULUL",
            "3RDRD",
            "4RDRD",
            "2LDRD",
        },
        Perm((1, 4, 0, 2, 3)): {"4DLUR", "2ULUR", "1DLUR", "3ULUR"},
        Perm((1, 3, 0, 2, 4)): {"2ULDL", "1DLDL", "3ULDL", "4DLDL"},
        Perm((4, 1, 3, 0, 2)): {"4LDRD", "2RDRD", "1RDRD", "3LDRD"},
        Perm((0, 2, 4, 1, 3)): {"3URUR", "2URUR", "1DRUR", "4DRUR"},
        Perm((2, 4, 1, 3, 0)): {"2RULU", "3LULU", "4LULU", "1RULU"},
        Perm((3, 0, 2, 4, 1)): {
            "4LDRU",
            "1DLDR",
            "1RULD",
            "2ULDR",
            "4DRUL",
            "2RULD",
            "1RDRU",
            "1DRUL",
            "4LULD",
            "3LDRU",
            "3LULD",
            "3ULDR",
            "3URUL",
            "4DLDR",
            "2RDRU",
            "2URUL",
        },
        Perm((1, 2, 4, 0, 3)): {"4DRDL", "1DRDL", "3URDL", "2URDL"},
        Perm((2, 4, 0, 3, 1)): {
            "4RULU",
            "2URDR",
            "4DRDR",
            "3RULU",
            "3URDR",
            "1DRDR",
            "2LULU",
            "1LULU",
        },
        Perm((3, 0, 1, 4, 2)): {"1LULD", "2LULD", "4RULD", "3RULD"},
        Perm((1, 2, 3, 0, 4)): set(),
        Perm((2, 3, 0, 4, 1)): set(),
        Perm((2, 4, 0, 1, 3)): set(),
        Perm((3, 0, 1, 2, 4)): set(),
        Perm((0, 1, 2, 3, 4)): set(),
        Perm((4, 0, 1, 2, 3)): set(),
        Perm((1, 2, 3, 4, 0)): set(),
        Perm((3, 4, 0, 1, 2)): set(),
        Perm((4, 3, 0, 1, 2)): set(),
        Perm((0, 4, 1, 2, 3)): set(),
        Perm((4, 1, 2, 3, 0)): set(),
        Perm((0, 2, 3, 4, 1)): set(),
        Perm((2, 3, 4, 0, 1)): set(),
        Perm((2, 3, 4, 1, 0)): set(),
        Perm((2, 3, 0, 1, 4)): set(),
        Perm((0, 3, 4, 1, 2)): set(),
        Perm((3, 0, 4, 1, 2)): set(),
        Perm((2, 0, 3, 4, 1)): {"1LDRU", "4RDRU", "2LDRU", "3RDRU"},
        Perm((1, 3, 4, 0, 2)): set(),
    }


def test_factor_pinword():
    assert PinWords.factor_pinword("") == []
    assert PinWords.factor_pinword("1") == ["1"]
    assert PinWords.factor_pinword("2") == ["2"]
    assert PinWords.factor_pinword("3") == ["3"]
    assert PinWords.factor_pinword("4") == ["4"]
    assert PinWords.factor_pinword("1U") == ["1U"]
    assert PinWords.factor_pinword("1D") == ["1D"]
    assert PinWords.factor_pinword("1L") == ["1L"]
    assert PinWords.factor_pinword("1R") == ["1R"]
    assert PinWords.factor_pinword("11") == ["1", "1"]
    assert PinWords.factor_pinword("12") == ["1", "2"]
    assert PinWords.factor_pinword("13") == ["1", "3"]
    assert PinWords.factor_pinword("14") == ["1", "4"]
    assert PinWords.factor_pinword("2U") == ["2U"]
    assert PinWords.factor_pinword("2D") == ["2D"]
    assert PinWords.factor_pinword("2L") == ["2L"]
    assert PinWords.factor_pinword("2R") == ["2R"]
    assert PinWords.factor_pinword("21") == ["2", "1"]
    assert PinWords.factor_pinword("22") == ["2", "2"]
    assert PinWords.factor_pinword("23") == ["2", "3"]
    assert PinWords.factor_pinword("24") == ["2", "4"]
    assert PinWords.factor_pinword("3U") == ["3U"]
    assert PinWords.factor_pinword("3D") == ["3D"]
    assert PinWords.factor_pinword("3L") == ["3L"]
    assert PinWords.factor_pinword("3R") == ["3R"]
    assert PinWords.factor_pinword("31") == ["3", "1"]
    assert PinWords.factor_pinword("32") == ["3", "2"]
    assert PinWords.factor_pinword("33") == ["3", "3"]
    assert PinWords.factor_pinword("34") == ["3", "4"]
    assert PinWords.factor_pinword("4U") == ["4U"]
    assert PinWords.factor_pinword("4D") == ["4D"]
    assert PinWords.factor_pinword("4L") == ["4L"]
    assert PinWords.factor_pinword("4R") == ["4R"]
    assert PinWords.factor_pinword("41") == ["4", "1"]
    assert PinWords.factor_pinword("42") == ["4", "2"]
    assert PinWords.factor_pinword("43") == ["4", "3"]
    assert PinWords.factor_pinword("44") == ["4", "4"]
    assert PinWords.factor_pinword("44U") == ["4", "4U"]
    assert PinWords.factor_pinword("1R4") == ["1R", "4"]
    assert PinWords.factor_pinword("3U3") == ["3U", "3"]
    assert PinWords.factor_pinword("434") == ["4", "3", "4"]
    assert PinWords.factor_pinword("114") == ["1", "1", "4"]
    assert PinWords.factor_pinword("313") == ["3", "1", "3"]
    assert PinWords.factor_pinword("3R1") == ["3R", "1"]
    assert PinWords.factor_pinword("31R") == ["3", "1R"]
    assert PinWords.factor_pinword("4D1") == ["4D", "1"]
    assert PinWords.factor_pinword("42R") == ["4", "2R"]
    assert PinWords.factor_pinword("4LU") == ["4LU"]
    assert PinWords.factor_pinword("13D") == ["1", "3D"]
    assert PinWords.factor_pinword("2U4") == ["2U", "4"]
    assert PinWords.factor_pinword("3DR") == ["3DR"]
    assert PinWords.factor_pinword("441") == ["4", "4", "1"]
    assert PinWords.factor_pinword("33U") == ["3", "3U"]
    assert PinWords.factor_pinword("331") == ["3", "3", "1"]
    assert PinWords.factor_pinword("341") == ["3", "4", "1"]
    assert PinWords.factor_pinword("132") == ["1", "3", "2"]
    assert PinWords.factor_pinword("1L1") == ["1L", "1"]
    assert PinWords.factor_pinword("311R") == ["3", "1", "1R"]
    assert PinWords.factor_pinword("244L") == ["2", "4", "4L"]
    assert PinWords.factor_pinword("14RD") == ["1", "4RD"]
    assert PinWords.factor_pinword("1R4L") == ["1R", "4L"]
    assert PinWords.factor_pinword("43R4") == ["4", "3R", "4"]
    assert PinWords.factor_pinword("41D1") == ["4", "1D", "1"]
    assert PinWords.factor_pinword("42RD") == ["4", "2RD"]
    assert PinWords.factor_pinword("3D41") == ["3D", "4", "1"]
    assert PinWords.factor_pinword("42D1") == ["4", "2D", "1"]
    assert PinWords.factor_pinword("1LD2") == ["1LD", "2"]
    assert PinWords.factor_pinword("3R1L") == ["3R", "1L"]
    assert PinWords.factor_pinword("344D") == ["3", "4", "4D"]
    assert PinWords.factor_pinword("2DL1") == ["2DL", "1"]
    assert PinWords.factor_pinword("1242") == ["1", "2", "4", "2"]
    assert PinWords.factor_pinword("3R3L") == ["3R", "3L"]
    assert PinWords.factor_pinword("1D42") == ["1D", "4", "2"]
    assert PinWords.factor_pinword("1431") == ["1", "4", "3", "1"]
    assert PinWords.factor_pinword("42U2") == ["4", "2U", "2"]
    assert PinWords.factor_pinword("2D11") == ["2D", "1", "1"]
    assert PinWords.factor_pinword("2UR2") == ["2UR", "2"]
    assert PinWords.factor_pinword("323L1") == ["3", "2", "3L", "1"]
    assert PinWords.factor_pinword("1313L") == ["1", "3", "1", "3L"]
    assert PinWords.factor_pinword("434UL") == ["4", "3", "4UL"]
    assert PinWords.factor_pinword("1UL23") == ["1UL", "2", "3"]
    assert PinWords.factor_pinword("4U31R") == ["4U", "3", "1R"]
    assert PinWords.factor_pinword("3L1RD") == ["3L", "1RD"]
    assert PinWords.factor_pinword("22LD4") == ["2", "2LD", "4"]
    assert PinWords.factor_pinword("2R412") == ["2R", "4", "1", "2"]
    assert PinWords.factor_pinword("1ULD3") == ["1ULD", "3"]
    assert PinWords.factor_pinword("42433") == ["4", "2", "4", "3", "3"]
    assert PinWords.factor_pinword("12213") == ["1", "2", "2", "1", "3"]
    assert PinWords.factor_pinword("2U3L1") == ["2U", "3L", "1"]
    assert PinWords.factor_pinword("4D31U") == ["4D", "3", "1U"]
    assert PinWords.factor_pinword("13RU2") == ["1", "3RU", "2"]
    assert PinWords.factor_pinword("33R13") == ["3", "3R", "1", "3"]
    assert PinWords.factor_pinword("2U23R") == ["2U", "2", "3R"]
    assert PinWords.factor_pinword("34ULU") == ["3", "4ULU"]
    assert PinWords.factor_pinword("333L3") == ["3", "3", "3L", "3"]
    assert PinWords.factor_pinword("24U1U") == ["2", "4U", "1U"]
    assert PinWords.factor_pinword("2R2U3") == ["2R", "2U", "3"]
    assert PinWords.factor_pinword("12U132") == ["1", "2U", "1", "3", "2"]
    assert PinWords.factor_pinword("1UR24L") == ["1UR", "2", "4L"]
    assert PinWords.factor_pinword("323R23") == ["3", "2", "3R", "2", "3"]
    assert PinWords.factor_pinword("31UL22") == ["3", "1UL", "2", "2"]
    assert PinWords.factor_pinword("44R242") == ["4", "4R", "2", "4", "2"]
    assert PinWords.factor_pinword("22D3U3") == ["2", "2D", "3U", "3"]
    assert PinWords.factor_pinword("1U4RD3") == ["1U", "4RD", "3"]
    assert PinWords.factor_pinword("1R3D13") == ["1R", "3D", "1", "3"]
    assert PinWords.factor_pinword("1D31L2") == ["1D", "3", "1L", "2"]
    assert PinWords.factor_pinword("224L3R") == ["2", "2", "4L", "3R"]
    assert PinWords.factor_pinword("31U4UL") == ["3", "1U", "4UL"]
    assert PinWords.factor_pinword("2URD32") == ["2URD", "3", "2"]
    assert PinWords.factor_pinword("1U1U23") == ["1U", "1U", "2", "3"]
    assert PinWords.factor_pinword("31L233") == ["3", "1L", "2", "3", "3"]
    assert PinWords.factor_pinword("322UL4") == ["3", "2", "2UL", "4"]
    assert PinWords.factor_pinword("2341R4") == ["2", "3", "4", "1R", "4"]
    assert PinWords.factor_pinword("4131U3") == ["4", "1", "3", "1U", "3"]
    assert PinWords.factor_pinword("3UL24D") == ["3UL", "2", "4D"]
    assert PinWords.factor_pinword("22U244") == ["2", "2U", "2", "4", "4"]
    assert PinWords.factor_pinword("24LD42") == ["2", "4LD", "4", "2"]
    assert PinWords.factor_pinword("4LU1UL3") == ["4LU", "1UL", "3"]
    assert PinWords.factor_pinword("4D33DR1") == ["4D", "3", "3DR", "1"]
    assert PinWords.factor_pinword("4UR1D24") == ["4UR", "1D", "2", "4"]
    assert PinWords.factor_pinword("1U1U4L3") == ["1U", "1U", "4L", "3"]
    assert PinWords.factor_pinword("1R12434") == ["1R", "1", "2", "4", "3", "4"]
    assert PinWords.factor_pinword("3RD4U4D") == ["3RD", "4U", "4D"]
    assert PinWords.factor_pinword("2U2D2R2") == ["2U", "2D", "2R", "2"]
    assert PinWords.factor_pinword("1D43U31") == ["1D", "4", "3U", "3", "1"]
    assert PinWords.factor_pinword("14D2U22") == ["1", "4D", "2U", "2", "2"]
    assert PinWords.factor_pinword("3421R3R") == ["3", "4", "2", "1R", "3R"]
    assert PinWords.factor_pinword("4U41D1D") == ["4U", "4", "1D", "1D"]
    assert PinWords.factor_pinword("412L113") == ["4", "1", "2L", "1", "1", "3"]
    assert PinWords.factor_pinword("1L1LU34") == ["1L", "1LU", "3", "4"]
    assert PinWords.factor_pinword("2UL332D") == ["2UL", "3", "3", "2D"]
    assert PinWords.factor_pinword("32344RU") == ["3", "2", "3", "4", "4RU"]
    assert PinWords.factor_pinword("21U4LUR") == ["2", "1U", "4LUR"]
    assert PinWords.factor_pinword("3L1LD11") == ["3L", "1LD", "1", "1"]
    assert PinWords.factor_pinword("14ULU33") == ["1", "4ULU", "3", "3"]
    assert PinWords.factor_pinword("442D2D3") == ["4", "4", "2D", "2D", "3"]
    assert PinWords.factor_pinword("4RD333R") == ["4RD", "3", "3", "3R"]


def test_sp_to_m():
    assert PinWords.sp_to_m("") == ("",)
    assert PinWords.sp_to_m("1") == ("RU", "UR")
    assert PinWords.sp_to_m("2") == ("LU", "UL")
    assert PinWords.sp_to_m("3") == ("LD", "DL")
    assert PinWords.sp_to_m("4") == ("RD", "DR")
    assert PinWords.sp_to_m("1U") == ("URU",)
    assert PinWords.sp_to_m("1D") == ("URD",)
    assert PinWords.sp_to_m("1L") == ("RUL",)
    assert PinWords.sp_to_m("1R") == ("RUR",)
    assert PinWords.sp_to_m("2U") == ("ULU",)
    assert PinWords.sp_to_m("2D") == ("ULD",)
    assert PinWords.sp_to_m("2L") == ("LUL",)
    assert PinWords.sp_to_m("2R") == ("LUR",)
    assert PinWords.sp_to_m("3U") == ("DLU",)
    assert PinWords.sp_to_m("3D") == ("DLD",)
    assert PinWords.sp_to_m("3L") == ("LDL",)
    assert PinWords.sp_to_m("3R") == ("LDR",)
    assert PinWords.sp_to_m("4U") == ("DRU",)
    assert PinWords.sp_to_m("4D") == ("DRD",)
    assert PinWords.sp_to_m("4L") == ("RDL",)
    assert PinWords.sp_to_m("4R") == ("RDR",)
    assert PinWords.sp_to_m("1UL") == ("URUL",)
    assert PinWords.sp_to_m("1UR") == ("URUR",)
    assert PinWords.sp_to_m("1DL") == ("URDL",)
    assert PinWords.sp_to_m("1DR") == ("URDR",)
    assert PinWords.sp_to_m("1LU") == ("RULU",)
    assert PinWords.sp_to_m("1LD") == ("RULD",)
    assert PinWords.sp_to_m("1RU") == ("RURU",)
    assert PinWords.sp_to_m("1RD") == ("RURD",)
    assert PinWords.sp_to_m("2UL") == ("ULUL",)
    assert PinWords.sp_to_m("2UR") == ("ULUR",)
    assert PinWords.sp_to_m("2DL") == ("ULDL",)
    assert PinWords.sp_to_m("2DR") == ("ULDR",)
    assert PinWords.sp_to_m("2LU") == ("LULU",)
    assert PinWords.sp_to_m("2LD") == ("LULD",)
    assert PinWords.sp_to_m("2RU") == ("LURU",)
    assert PinWords.sp_to_m("2RD") == ("LURD",)
    assert PinWords.sp_to_m("3UL") == ("DLUL",)
    assert PinWords.sp_to_m("3UR") == ("DLUR",)
    assert PinWords.sp_to_m("3DL") == ("DLDL",)
    assert PinWords.sp_to_m("3DR") == ("DLDR",)
    assert PinWords.sp_to_m("3LU") == ("LDLU",)
    assert PinWords.sp_to_m("3LD") == ("LDLD",)
    assert PinWords.sp_to_m("3RU") == ("LDRU",)
    assert PinWords.sp_to_m("3RD") == ("LDRD",)
    assert PinWords.sp_to_m("4UL") == ("DRUL",)
    assert PinWords.sp_to_m("4UR") == ("DRUR",)
    assert PinWords.sp_to_m("4DL") == ("DRDL",)
    assert PinWords.sp_to_m("4DR") == ("DRDR",)
    assert PinWords.sp_to_m("4LU") == ("RDLU",)
    assert PinWords.sp_to_m("4LD") == ("RDLD",)
    assert PinWords.sp_to_m("4RU") == ("RDRU",)
    assert PinWords.sp_to_m("4RD") == ("RDRD",)
    assert PinWords.sp_to_m("1LDR") == ("RULDR",)
    assert PinWords.sp_to_m("2URU") == ("ULURU",)
    assert PinWords.sp_to_m("3RDR") == ("LDRDR",)
    assert PinWords.sp_to_m("2LUL") == ("LULUL",)
    assert PinWords.sp_to_m("1DRU") == ("URDRU",)
    assert PinWords.sp_to_m("3ULD") == ("DLULD",)
    assert PinWords.sp_to_m("3RDL") == ("LDRDL",)
    assert PinWords.sp_to_m("3DRU") == ("DLDRU",)
    assert PinWords.sp_to_m("2LDR") == ("LULDR",)
    assert PinWords.sp_to_m("3DRD") == ("DLDRD",)
    assert PinWords.sp_to_m("4DRUL") == ("DRDRUL",)
    assert PinWords.sp_to_m("2LDLD") == ("LULDLD",)
    assert PinWords.sp_to_m("4DRDL") == ("DRDRDL",)
    assert PinWords.sp_to_m("1ULUL") == ("URULUL",)
    assert PinWords.sp_to_m("2LDLD") == ("LULDLD",)
    assert PinWords.sp_to_m("4DRDL") == ("DRDRDL",)
    assert PinWords.sp_to_m("3ULUL") == ("DLULUL",)
    assert PinWords.sp_to_m("4DRUR") == ("DRDRUR",)
    assert PinWords.sp_to_m("1RULU") == ("RURULU",)
    assert PinWords.sp_to_m("1RURU") == ("RURURU",)
    assert PinWords.sp_to_m("3DRULD") == ("DLDRULD",)
    assert PinWords.sp_to_m("3RDLUR") == ("LDRDLUR",)
    assert PinWords.sp_to_m("1LDLDL") == ("RULDLDL",)
    assert PinWords.sp_to_m("1LURUR") == ("RULURUR",)
    assert PinWords.sp_to_m("1RULUL") == ("RURULUL",)
    assert PinWords.sp_to_m("1DLDLD") == ("URDLDLD",)
    assert PinWords.sp_to_m("4URULU") == ("DRURULU",)
    assert PinWords.sp_to_m("3RDRDL") == ("LDRDRDL",)
    assert PinWords.sp_to_m("2ULDLU") == ("ULULDLU",)
    assert PinWords.sp_to_m("2DLURD") == ("ULDLURD",)


def test_m_to_sp():
    assert PinWords.m_to_sp("LUR") == "2R"
    assert PinWords.m_to_sp("LD") == "3"
    assert PinWords.m_to_sp("RUL") == "1L"
    assert PinWords.m_to_sp("DL") == "3"
    assert PinWords.m_to_sp("DRU") == "4U"
    assert PinWords.m_to_sp("DRDL") == "4DL"
    assert PinWords.m_to_sp("RUR") == "1R"
    assert PinWords.m_to_sp("RDL") == "4L"
    assert PinWords.m_to_sp("DLD") == "3D"
    assert PinWords.m_to_sp("URU") == "1U"
    assert PinWords.m_to_sp("RDR") == "4R"
    assert PinWords.m_to_sp("ULU") == "2U"
    assert PinWords.m_to_sp("LDL") == "3L"
    assert PinWords.m_to_sp("LDRUL") == "3RUL"
    assert PinWords.m_to_sp("ULD") == "2D"
    assert PinWords.m_to_sp("URUR") == "1UR"


def test_quadrant():
    assert PinWords.quadrant("1", 0) == "1"
    assert PinWords.quadrant("2", 0) == "2"
    assert PinWords.quadrant("3", 0) == "3"
    assert PinWords.quadrant("4", 0) == "4"
    assert PinWords.quadrant("1U", 0) == "1"
    assert PinWords.quadrant("1U", 1) == "1"
    assert PinWords.quadrant("1D", 0) == "1"
    assert PinWords.quadrant("1D", 1) == "4"
    assert PinWords.quadrant("1L", 0) == "1"
    assert PinWords.quadrant("1L", 1) == "2"
    assert PinWords.quadrant("1R", 0) == "1"
    assert PinWords.quadrant("1R", 1) == "1"
    assert PinWords.quadrant("11", 0) == "1"
    assert PinWords.quadrant("11", 1) == "1"
    assert PinWords.quadrant("12", 0) == "1"
    assert PinWords.quadrant("12", 1) == "2"
    assert PinWords.quadrant("13", 0) == "1"
    assert PinWords.quadrant("13", 1) == "3"
    assert PinWords.quadrant("14", 0) == "1"
    assert PinWords.quadrant("14", 1) == "4"
    assert PinWords.quadrant("2U", 0) == "2"
    assert PinWords.quadrant("2U", 1) == "2"
    assert PinWords.quadrant("2D", 0) == "2"
    assert PinWords.quadrant("2D", 1) == "3"
    assert PinWords.quadrant("2L", 0) == "2"
    assert PinWords.quadrant("2L", 1) == "2"
    assert PinWords.quadrant("2R", 0) == "2"
    assert PinWords.quadrant("2R", 1) == "1"
    assert PinWords.quadrant("21", 0) == "2"
    assert PinWords.quadrant("21", 1) == "1"
    assert PinWords.quadrant("22", 0) == "2"
    assert PinWords.quadrant("22", 1) == "2"
    assert PinWords.quadrant("23", 0) == "2"
    assert PinWords.quadrant("23", 1) == "3"
    assert PinWords.quadrant("24", 0) == "2"
    assert PinWords.quadrant("24", 1) == "4"
    assert PinWords.quadrant("3U", 0) == "3"
    assert PinWords.quadrant("3U", 1) == "2"
    assert PinWords.quadrant("3D", 0) == "3"
    assert PinWords.quadrant("3D", 1) == "3"
    assert PinWords.quadrant("3L", 0) == "3"
    assert PinWords.quadrant("3L", 1) == "3"
    assert PinWords.quadrant("3R", 0) == "3"
    assert PinWords.quadrant("3R", 1) == "4"
    assert PinWords.quadrant("31", 0) == "3"
    assert PinWords.quadrant("31", 1) == "1"
    assert PinWords.quadrant("32", 0) == "3"
    assert PinWords.quadrant("32", 1) == "2"
    assert PinWords.quadrant("33", 0) == "3"
    assert PinWords.quadrant("33", 1) == "3"
    assert PinWords.quadrant("34", 0) == "3"
    assert PinWords.quadrant("34", 1) == "4"
    assert PinWords.quadrant("4U", 0) == "4"
    assert PinWords.quadrant("4U", 1) == "1"
    assert PinWords.quadrant("4D", 0) == "4"
    assert PinWords.quadrant("4D", 1) == "4"
    assert PinWords.quadrant("4L", 0) == "4"
    assert PinWords.quadrant("4L", 1) == "3"
    assert PinWords.quadrant("4R", 0) == "4"
    assert PinWords.quadrant("4R", 1) == "4"
    assert PinWords.quadrant("41", 0) == "4"
    assert PinWords.quadrant("41", 1) == "1"
    assert PinWords.quadrant("42", 0) == "4"
    assert PinWords.quadrant("42", 1) == "2"
    assert PinWords.quadrant("43", 0) == "4"
    assert PinWords.quadrant("43", 1) == "3"
    assert PinWords.quadrant("44", 0) == "4"
    assert PinWords.quadrant("44", 1) == "4"
    assert PinWords.quadrant("224", 0) == "2"
    assert PinWords.quadrant("224", 1) == "2"
    assert PinWords.quadrant("224", 2) == "4"
    assert PinWords.quadrant("4UR", 0) == "4"
    assert PinWords.quadrant("4UR", 1) == "1"
    assert PinWords.quadrant("4UR", 2) == "1"
    assert PinWords.quadrant("4D4", 0) == "4"
    assert PinWords.quadrant("4D4", 1) == "4"
    assert PinWords.quadrant("4D4", 2) == "4"
    assert PinWords.quadrant("224", 0) == "2"
    assert PinWords.quadrant("224", 1) == "2"
    assert PinWords.quadrant("224", 2) == "4"
    assert PinWords.quadrant("4UR", 0) == "4"
    assert PinWords.quadrant("4UR", 1) == "1"
    assert PinWords.quadrant("4UR", 2) == "1"
    assert PinWords.quadrant("2U3L", 0) == "2"
    assert PinWords.quadrant("2U3L", 1) == "2"
    assert PinWords.quadrant("2U3L", 2) == "3"
    assert PinWords.quadrant("2U3L", 3) == "3"
    assert PinWords.quadrant("3L3D", 0) == "3"
    assert PinWords.quadrant("3L3D", 1) == "3"
    assert PinWords.quadrant("3L3D", 2) == "3"
    assert PinWords.quadrant("3L3D", 3) == "3"
    assert PinWords.quadrant("2D44", 0) == "2"
    assert PinWords.quadrant("2D44", 1) == "3"
    assert PinWords.quadrant("2D44", 2) == "4"
    assert PinWords.quadrant("2D44", 3) == "4"
    assert PinWords.quadrant("12L3", 0) == "1"
    assert PinWords.quadrant("12L3", 1) == "2"
    assert PinWords.quadrant("12L3", 2) == "2"
    assert PinWords.quadrant("12L3", 3) == "3"
    assert PinWords.quadrant("4R42", 0) == "4"
    assert PinWords.quadrant("4R42", 1) == "4"
    assert PinWords.quadrant("4R42", 2) == "4"
    assert PinWords.quadrant("4R42", 3) == "2"
    assert PinWords.quadrant("243U1", 0) == "2"
    assert PinWords.quadrant("243U1", 1) == "4"
    assert PinWords.quadrant("243U1", 2) == "3"
    assert PinWords.quadrant("243U1", 3) == "2"
    assert PinWords.quadrant("243U1", 4) == "1"
    assert PinWords.quadrant("14U4R", 0) == "1"
    assert PinWords.quadrant("14U4R", 1) == "4"
    assert PinWords.quadrant("14U4R", 2) == "1"
    assert PinWords.quadrant("14U4R", 3) == "4"
    assert PinWords.quadrant("14U4R", 4) == "4"
    assert PinWords.quadrant("224UL", 0) == "2"
    assert PinWords.quadrant("224UL", 1) == "2"
    assert PinWords.quadrant("224UL", 2) == "4"
    assert PinWords.quadrant("224UL", 3) == "1"
    assert PinWords.quadrant("224UL", 4) == "2"
    assert PinWords.quadrant("44343", 0) == "4"
    assert PinWords.quadrant("44343", 1) == "4"
    assert PinWords.quadrant("44343", 2) == "3"
    assert PinWords.quadrant("44343", 3) == "4"
    assert PinWords.quadrant("44343", 4) == "3"
    assert PinWords.quadrant("13U44", 0) == "1"
    assert PinWords.quadrant("13U44", 1) == "3"
    assert PinWords.quadrant("13U44", 2) == "2"
    assert PinWords.quadrant("13U44", 3) == "4"
    assert PinWords.quadrant("13U44", 4) == "4"
    assert PinWords.quadrant("21DL42", 0) == "2"
    assert PinWords.quadrant("21DL42", 1) == "1"
    assert PinWords.quadrant("21DL42", 2) == "4"
    assert PinWords.quadrant("21DL42", 3) == "3"
    assert PinWords.quadrant("21DL42", 4) == "4"
    assert PinWords.quadrant("21DL42", 5) == "2"
    assert PinWords.quadrant("424U3R", 0) == "4"
    assert PinWords.quadrant("424U3R", 1) == "2"
    assert PinWords.quadrant("424U3R", 2) == "4"
    assert PinWords.quadrant("424U3R", 3) == "1"
    assert PinWords.quadrant("424U3R", 4) == "3"
    assert PinWords.quadrant("424U3R", 5) == "4"
    assert PinWords.quadrant("1U343R", 0) == "1"
    assert PinWords.quadrant("1U343R", 1) == "1"
    assert PinWords.quadrant("1U343R", 2) == "3"
    assert PinWords.quadrant("1U343R", 3) == "4"
    assert PinWords.quadrant("1U343R", 4) == "3"
    assert PinWords.quadrant("1U343R", 5) == "4"
    assert PinWords.quadrant("4R2U14", 0) == "4"
    assert PinWords.quadrant("4R2U14", 1) == "4"
    assert PinWords.quadrant("4R2U14", 2) == "2"
    assert PinWords.quadrant("4R2U14", 3) == "2"
    assert PinWords.quadrant("4R2U14", 4) == "1"
    assert PinWords.quadrant("4R2U14", 5) == "4"
    assert PinWords.quadrant("4R2R11", 0) == "4"
    assert PinWords.quadrant("4R2R11", 1) == "4"
    assert PinWords.quadrant("4R2R11", 2) == "2"
    assert PinWords.quadrant("4R2R11", 3) == "1"
    assert PinWords.quadrant("4R2R11", 4) == "1"
    assert PinWords.quadrant("4R2R11", 5) == "1"


def test_pinword_occurrences_sp():
    assert list(PinWords.pinword_occurrences_sp("1", "4")) == []
    assert list(PinWords.pinword_occurrences_sp("2", "1")) == []
    assert list(PinWords.pinword_occurrences_sp("3", "1")) == []
    assert list(PinWords.pinword_occurrences_sp("4", "4")) == [0]
    assert list(PinWords.pinword_occurrences_sp("1U", "4U")) == []
    assert list(PinWords.pinword_occurrences_sp("1D", "1D")) == [0]
    assert list(PinWords.pinword_occurrences_sp("1L", "1L")) == [0]
    assert list(PinWords.pinword_occurrences_sp("1R", "1")) == [0, 1]
    assert list(PinWords.pinword_occurrences_sp("11", "1")) == [0, 1]
    assert list(PinWords.pinword_occurrences_sp("12", "2")) == [1]
    assert list(PinWords.pinword_occurrences_sp("13", "3")) == [1]
    assert list(PinWords.pinword_occurrences_sp("14", "1")) == [0]
    assert list(PinWords.pinword_occurrences_sp("2U", "2")) == [0, 1]
    assert list(PinWords.pinword_occurrences_sp("2D", "2")) == [0]
    assert list(PinWords.pinword_occurrences_sp("2L", "2L")) == [0]
    assert list(PinWords.pinword_occurrences_sp("2R", "2R")) == [0]
    assert list(PinWords.pinword_occurrences_sp("21", "2")) == [0]
    assert list(PinWords.pinword_occurrences_sp("22", "2")) == [0, 1]
    assert list(PinWords.pinword_occurrences_sp("23", "2")) == [0]
    assert list(PinWords.pinword_occurrences_sp("24", "2")) == [0]
    assert list(PinWords.pinword_occurrences_sp("3U", "3")) == [0]
    assert list(PinWords.pinword_occurrences_sp("3D", "3")) == [0, 1]
    assert list(PinWords.pinword_occurrences_sp("3L", "3")) == [0, 1]
    assert list(PinWords.pinword_occurrences_sp("3R", "4")) == [1]
    assert list(PinWords.pinword_occurrences_sp("31", "3")) == [0]
    assert list(PinWords.pinword_occurrences_sp("32", "2")) == [1]
    assert list(PinWords.pinword_occurrences_sp("33", "3")) == [0, 1]
    assert list(PinWords.pinword_occurrences_sp("34", "4")) == [1]
    assert list(PinWords.pinword_occurrences_sp("4U", "4")) == [0]
    assert list(PinWords.pinword_occurrences_sp("4D", "4")) == [0, 1]
    assert list(PinWords.pinword_occurrences_sp("4L", "4")) == [0]
    assert list(PinWords.pinword_occurrences_sp("4R", "4")) == [0, 1]
    assert list(PinWords.pinword_occurrences_sp("41", "1")) == [1]
    assert list(PinWords.pinword_occurrences_sp("42", "4")) == [0]
    assert list(PinWords.pinword_occurrences_sp("43", "4")) == [0]
    assert list(PinWords.pinword_occurrences_sp("44", "4")) == [0, 1]
    assert list(PinWords.pinword_occurrences_sp("1U1", "1")) == [0, 1, 2]
    assert list(PinWords.pinword_occurrences_sp("2RU", "1")) == [1, 2]
    assert list(PinWords.pinword_occurrences_sp("33L", "3")) == [0, 1, 2]
    assert list(PinWords.pinword_occurrences_sp("234", "3")) == [1]
    assert list(PinWords.pinword_occurrences_sp("13L", "1")) == [0]
    assert list(PinWords.pinword_occurrences_sp("2D2L", "2")) == [0, 2, 3]
    assert list(PinWords.pinword_occurrences_sp("4L2U", "2")) == [2, 3]
    assert list(PinWords.pinword_occurrences_sp("13R3", "3R")) == [1]
    assert list(PinWords.pinword_occurrences_sp("34L4", "3")) == [0, 2]
    assert list(PinWords.pinword_occurrences_sp("11L3", "1")) == [0, 1]
    assert list(PinWords.pinword_occurrences_sp("32142", "4")) == [3]
    assert list(PinWords.pinword_occurrences_sp("33311", "1")) == [3, 4]
    assert list(PinWords.pinword_occurrences_sp("134L3", "1")) == [0]
    assert list(PinWords.pinword_occurrences_sp("4R4D3", "3")) == [4]
    assert list(PinWords.pinword_occurrences_sp("3U421", "3")) == [0]
    assert list(PinWords.pinword_occurrences_sp("4ULULD", "4U")) == [0]
    assert list(PinWords.pinword_occurrences_sp("4D2U41", "2")) == [2, 3]
    assert list(PinWords.pinword_occurrences_sp("313D4D", "1")) == [1]
    assert list(PinWords.pinword_occurrences_sp("331R14", "3")) == [0, 1]
    assert list(PinWords.pinword_occurrences_sp("3LU1DL", "4L")) == [4]


def test_pinword_contains_sp():
    assert PinWords.pinword_contains_sp("1", "2") is False
    assert PinWords.pinword_contains_sp("2", "4") is False
    assert PinWords.pinword_contains_sp("3", "1") is False
    assert PinWords.pinword_contains_sp("4", "4") is True
    assert PinWords.pinword_contains_sp("1U", "4") is False
    assert PinWords.pinword_contains_sp("1D", "3") is False
    assert PinWords.pinword_contains_sp("1L", "3L") is False
    assert PinWords.pinword_contains_sp("1R", "3D") is False
    assert PinWords.pinword_contains_sp("11", "4") is False
    assert PinWords.pinword_contains_sp("12", "3") is False
    assert PinWords.pinword_contains_sp("13", "1L") is False
    assert PinWords.pinword_contains_sp("14", "3") is False
    assert PinWords.pinword_contains_sp("2U", "4") is False
    assert PinWords.pinword_contains_sp("2D", "3") is True
    assert PinWords.pinword_contains_sp("2L", "2") is True
    assert PinWords.pinword_contains_sp("2R", "2R") is True
    assert PinWords.pinword_contains_sp("21", "2L") is False
    assert PinWords.pinword_contains_sp("22", "4") is False
    assert PinWords.pinword_contains_sp("23", "2R") is False
    assert PinWords.pinword_contains_sp("24", "4R") is False
    assert PinWords.pinword_contains_sp("3U", "2") is True
    assert PinWords.pinword_contains_sp("3D", "1R") is False
    assert PinWords.pinword_contains_sp("3L", "2") is False
    assert PinWords.pinword_contains_sp("3R", "3") is True
    assert PinWords.pinword_contains_sp("31", "1D") is False
    assert PinWords.pinword_contains_sp("32", "1") is False
    assert PinWords.pinword_contains_sp("33", "2D") is False
    assert PinWords.pinword_contains_sp("34", "3") is True
    assert PinWords.pinword_contains_sp("4U", "1D") is False
    assert PinWords.pinword_contains_sp("4D", "4") is True
    assert PinWords.pinword_contains_sp("4L", "2") is False
    assert PinWords.pinword_contains_sp("4R", "1D") is False
    assert PinWords.pinword_contains_sp("41", "3") is False
    assert PinWords.pinword_contains_sp("42", "3") is False
    assert PinWords.pinword_contains_sp("43", "2") is False
    assert PinWords.pinword_contains_sp("44", "1U") is False
    assert PinWords.pinword_contains_sp("43U", "4") is True
    assert PinWords.pinword_contains_sp("213", "4DL") is False
    assert PinWords.pinword_contains_sp("4U3", "3L") is False
    assert PinWords.pinword_contains_sp("12U", "1") is True
    assert PinWords.pinword_contains_sp("421", "3DL") is False
    assert PinWords.pinword_contains_sp("42D4", "4") is True
    assert PinWords.pinword_contains_sp("43D3", "1DL") is False
    assert PinWords.pinword_contains_sp("44D3", "1") is False
    assert PinWords.pinword_contains_sp("341L", "3L") is False
    assert PinWords.pinword_contains_sp("14U2", "3UL") is False
    assert PinWords.pinword_contains_sp("4RU3D", "1ULD") is False
    assert PinWords.pinword_contains_sp("11D34", "1LDLU") is False
    assert PinWords.pinword_contains_sp("311U3", "1U") is True
    assert PinWords.pinword_contains_sp("34LDR", "3D") is True
    assert PinWords.pinword_contains_sp("12UR1", "2URD") is False
    assert PinWords.pinword_contains_sp("3L44LU", "1") is False
    assert PinWords.pinword_contains_sp("133223", "4LDR") is False
    assert PinWords.pinword_contains_sp("4D4413", "4LDRUL") is False
    assert PinWords.pinword_contains_sp("23U2L3", "1DL") is False
    assert PinWords.pinword_contains_sp("1L3UL4", "3RDL") is False


def test_pinword_occurences():
    assert list(PinWords.pinword_occurrences("1", "1")) == [(0,)]
    assert list(PinWords.pinword_occurrences("2", "1")) == []
    assert list(PinWords.pinword_occurrences("3", "4")) == []
    assert list(PinWords.pinword_occurrences("4", "2")) == []
    assert list(PinWords.pinword_occurrences("1U", "2")) == []
    assert list(PinWords.pinword_occurrences("1D", "1")) == [(0,)]
    assert list(PinWords.pinword_occurrences("1L", "2")) == [(1,)]
    assert list(PinWords.pinword_occurrences("1R", "1")) == [(0,), (1,)]
    assert list(PinWords.pinword_occurrences("11", "1")) == [(0,), (1,)]
    assert list(PinWords.pinword_occurrences("12", "1")) == [(0,)]
    assert list(PinWords.pinword_occurrences("13", "3")) == [(1,)]
    assert list(PinWords.pinword_occurrences("14", "4")) == [(1,)]
    assert list(PinWords.pinword_occurrences("2U", "2")) == [(0,), (1,)]
    assert list(PinWords.pinword_occurrences("2D", "2")) == [(0,)]
    assert list(PinWords.pinword_occurrences("2L", "2")) == [(0,), (1,)]
    assert list(PinWords.pinword_occurrences("2R", "2")) == [(0,)]
    assert list(PinWords.pinword_occurrences("21", "2")) == [(0,)]
    assert list(PinWords.pinword_occurrences("22", "2")) == [(0,), (1,)]
    assert list(PinWords.pinword_occurrences("23", "2")) == [(0,)]
    assert list(PinWords.pinword_occurrences("24", "2")) == [(0,)]
    assert list(PinWords.pinword_occurrences("3U", "2")) == [(1,)]
    assert list(PinWords.pinword_occurrences("3D", "3")) == [(0,), (1,)]
    assert list(PinWords.pinword_occurrences("3L", "3")) == [(0,), (1,)]
    assert list(PinWords.pinword_occurrences("3R", "4")) == [(1,)]
    assert list(PinWords.pinword_occurrences("31", "3")) == [(0,)]
    assert list(PinWords.pinword_occurrences("32", "2")) == [(1,)]
    assert list(PinWords.pinword_occurrences("33", "3")) == [(0,), (1,)]
    assert list(PinWords.pinword_occurrences("34", "4")) == [(1,)]
    assert list(PinWords.pinword_occurrences("4U", "4")) == [(0,)]
    assert list(PinWords.pinword_occurrences("4D", "4")) == [(0,), (1,)]
    assert list(PinWords.pinword_occurrences("4L", "3")) == [(1,)]
    assert list(PinWords.pinword_occurrences("4R", "4")) == [(0,), (1,)]
    assert list(PinWords.pinword_occurrences("41", "1")) == [(1,)]
    assert list(PinWords.pinword_occurrences("42", "4")) == [(0,)]
    assert list(PinWords.pinword_occurrences("43", "4")) == [(0,)]
    assert list(PinWords.pinword_occurrences("44", "4")) == [(0,), (1,)]
    assert list(PinWords.pinword_occurrences("2R4", "4")) == [(2,)]
    assert list(PinWords.pinword_occurrences("242", "4")) == [(1,)]
    assert list(PinWords.pinword_occurrences("23R", "2")) == [(0,)]
    assert list(PinWords.pinword_occurrences("12R", "1")) == [(0,), (2,)]
    assert list(PinWords.pinword_occurrences("4D1", "4D")) == [(0,)]
    assert list(PinWords.pinword_occurrences("4RDR", "4D")) == [(1,)]
    assert list(PinWords.pinword_occurrences("142U", "2")) == [(2,), (3,)]
    assert list(PinWords.pinword_occurrences("3U31", "1")) == [(3,)]
    assert list(PinWords.pinword_occurrences("121U", "12")) == [(0, 1)]
    assert list(PinWords.pinword_occurrences("1423", "2")) == [(2,)]
    assert list(PinWords.pinword_occurrences("41DR1", "4")) == [(0,), (2,), (3,)]
    assert list(PinWords.pinword_occurrences("211R3", "11")) == [(1, 2), (1, 3), (2, 3)]
    assert list(PinWords.pinword_occurrences("4334D", "4D")) == [(3,)]
    assert list(PinWords.pinword_occurrences("13RU2", "1")) == [(0,), (3,)]
    assert list(PinWords.pinword_occurrences("34321", "21")) == [(3, 4)]
    assert list(PinWords.pinword_occurrences("4DL44L", "3")) == [(2,), (5,)]
    assert list(PinWords.pinword_occurrences("1L1RUR", "1L1U")) == [(0, 3)]
    assert list(PinWords.pinword_occurrences("1R31L2", "1")) == [(0,), (1,), (3,)]
    assert list(PinWords.pinword_occurrences("1U13RU", "41")) == [(4, 5)]
    assert list(PinWords.pinword_occurrences("2232D2", "2")) == [(0,), (1,), (3,), (5,)]


def test_pinword_contains():
    assert PinWords.pinword_contains("1", "3") is False
    assert PinWords.pinword_contains("2", "4") is False
    assert PinWords.pinword_contains("3", "1") is False
    assert PinWords.pinword_contains("4", "2") is False
    assert PinWords.pinword_contains("1U", "21") is False
    assert PinWords.pinword_contains("1D", "1") is True
    assert PinWords.pinword_contains("1L", "2D") is False
    assert PinWords.pinword_contains("1R", "12") is False
    assert PinWords.pinword_contains("11", "1") is True
    assert PinWords.pinword_contains("12", "12") is True
    assert PinWords.pinword_contains("13", "31") is False
    assert PinWords.pinword_contains("14", "2") is False
    assert PinWords.pinword_contains("2U", "3") is False
    assert PinWords.pinword_contains("2D", "3L") is False
    assert PinWords.pinword_contains("2L", "4U") is False
    assert PinWords.pinword_contains("2R", "1L") is False
    assert PinWords.pinword_contains("21", "2D") is False
    assert PinWords.pinword_contains("22", "4L") is False
    assert PinWords.pinword_contains("23", "24") is False
    assert PinWords.pinword_contains("24", "2U") is False
    assert PinWords.pinword_contains("3U", "1") is False
    assert PinWords.pinword_contains("3D", "3") is True
    assert PinWords.pinword_contains("3L", "3D") is False
    assert PinWords.pinword_contains("3R", "2") is False
    assert PinWords.pinword_contains("31", "32") is False
    assert PinWords.pinword_contains("32", "2") is True
    assert PinWords.pinword_contains("33", "3R") is False
    assert PinWords.pinword_contains("34", "14") is False
    assert PinWords.pinword_contains("4U", "31") is False
    assert PinWords.pinword_contains("4D", "1") is False
    assert PinWords.pinword_contains("4L", "3U") is False
    assert PinWords.pinword_contains("4R", "3") is False
    assert PinWords.pinword_contains("41", "1") is True
    assert PinWords.pinword_contains("42", "3") is False
    assert PinWords.pinword_contains("43", "1") is False
    assert PinWords.pinword_contains("44", "34") is False
    assert PinWords.pinword_contains("43D", "3L") is False
    assert PinWords.pinword_contains("3R4", "22") is False
    assert PinWords.pinword_contains("213", "1") is True
    assert PinWords.pinword_contains("4D3", "3") is True
    assert PinWords.pinword_contains("111", "4RD") is False
    assert PinWords.pinword_contains("4DR2", "1L32") is False
    assert PinWords.pinword_contains("1UR3", "1") is True
    assert PinWords.pinword_contains("23L1", "4U1") is False
    assert PinWords.pinword_contains("2424", "32") is False
    assert PinWords.pinword_contains("14D2", "3") is False
    assert PinWords.pinword_contains("4ULD3", "442") is False
    assert PinWords.pinword_contains("41413", "3R1D") is False
    assert PinWords.pinword_contains("1D4D2", "4D3") is False
    assert PinWords.pinword_contains("2U1UR", "3244L") is False
    assert PinWords.pinword_contains("1RU13", "3U2L1") is False
    assert PinWords.pinword_contains("11D4R3", "241D") is False
    assert PinWords.pinword_contains("211214", "2") is True
    assert PinWords.pinword_contains("42DRD2", "341") is False
    assert PinWords.pinword_contains("2L41DR", "2") is True
    assert PinWords.pinword_contains("32D4U3", "3D") is False


def test_make_nfa_for_pinword():
    assert PinWords.make_nfa_for_pinword("1") == NFA(
        states={"2", "3", "0", "1"},
        input_symbols={"U", "D", "L", "R"},
        transitions={
            "0": {"U": {"2", "0"}, "L": {"0"}, "D": {"0"}, "R": {"0", "1"}},
            "3": {"U": {"3"}, "L": {"3"}, "D": {"3"}, "R": {"3"}},
            "1": {"U": {"3"}},
            "2": {"R": {"3"}},
        },
        initial_state="0",
        final_states={"3"},
    )
    assert PinWords.make_nfa_for_pinword("2") == NFA(
        states={"2", "3", "0", "1"},
        input_symbols={"U", "D", "L", "R"},
        transitions={
            "0": {"U": {"2", "0"}, "L": {"0", "1"}, "D": {"0"}, "R": {"0"}},
            "3": {"U": {"3"}, "L": {"3"}, "D": {"3"}, "R": {"3"}},
            "1": {"U": {"3"}},
            "2": {"L": {"3"}},
        },
        initial_state="0",
        final_states={"3"},
    )
    assert PinWords.make_nfa_for_pinword("3") == NFA(
        states={"2", "3", "0", "1"},
        input_symbols={"U", "D", "L", "R"},
        transitions={
            "0": {"U": {"0"}, "L": {"0", "1"}, "D": {"2", "0"}, "R": {"0"}},
            "3": {"U": {"3"}, "L": {"3"}, "D": {"3"}, "R": {"3"}},
            "1": {"D": {"3"}},
            "2": {"L": {"3"}},
        },
        initial_state="0",
        final_states={"3"},
    )
    assert PinWords.make_nfa_for_pinword("4") == NFA(
        states={"2", "3", "0", "1"},
        input_symbols={"U", "D", "L", "R"},
        transitions={
            "0": {"U": {"0"}, "L": {"0"}, "D": {"2", "0"}, "R": {"0", "1"}},
            "3": {"U": {"3"}, "L": {"3"}, "D": {"3"}, "R": {"3"}},
            "1": {"D": {"3"}},
            "2": {"R": {"3"}},
        },
        initial_state="0",
        final_states={"3"},
    )
    assert PinWords.make_nfa_for_pinword("1U") == NFA(
        states={"2", "3", "0", "1"},
        input_symbols={"U", "D", "L", "R"},
        transitions={
            "0": {"U": {"0", "1"}, "L": {"0"}, "D": {"0"}, "R": {"0"}},
            "1": {"R": {"2"}},
            "3": {"U": {"3"}, "L": {"3"}, "D": {"3"}, "R": {"3"}},
            "2": {"U": {"3"}},
        },
        initial_state="0",
        final_states={"3"},
    )
    assert PinWords.make_nfa_for_pinword("1D") == NFA(
        states={"2", "3", "0", "1"},
        input_symbols={"U", "D", "L", "R"},
        transitions={
            "0": {"U": {"0", "1"}, "L": {"0"}, "D": {"0"}, "R": {"0"}},
            "1": {"R": {"2"}},
            "3": {"U": {"3"}, "L": {"3"}, "D": {"3"}, "R": {"3"}},
            "2": {"D": {"3"}},
        },
        initial_state="0",
        final_states={"3"},
    )
    assert PinWords.make_nfa_for_pinword("1L") == NFA(
        states={"2", "3", "0", "1"},
        input_symbols={"U", "D", "L", "R"},
        transitions={
            "0": {"U": {"0"}, "L": {"0"}, "D": {"0"}, "R": {"0", "1"}},
            "1": {"U": {"2"}},
            "3": {"U": {"3"}, "L": {"3"}, "D": {"3"}, "R": {"3"}},
            "2": {"L": {"3"}},
        },
        initial_state="0",
        final_states={"3"},
    )
    assert PinWords.make_nfa_for_pinword("1R") == NFA(
        states={"2", "3", "0", "1"},
        input_symbols={"U", "D", "L", "R"},
        transitions={
            "0": {"U": {"0"}, "L": {"0"}, "D": {"0"}, "R": {"0", "1"}},
            "1": {"U": {"2"}},
            "3": {"U": {"3"}, "L": {"3"}, "D": {"3"}, "R": {"3"}},
            "2": {"R": {"3"}},
        },
        initial_state="0",
        final_states={"3"},
    )
    assert PinWords.make_nfa_for_pinword("11") == NFA(
        states={"6", "3", "2", "4", "5", "1", "0"},
        input_symbols={"U", "D", "L", "R"},
        transitions={
            "0": {"U": {"2", "0"}, "L": {"0"}, "D": {"0"}, "R": {"0", "1"}},
            "3": {"U": {"5", "3"}, "L": {"3"}, "D": {"3"}, "R": {"4", "3"}},
            "1": {"U": {"3"}},
            "2": {"R": {"3"}},
            "6": {"U": {"6"}, "L": {"6"}, "D": {"6"}, "R": {"6"}},
            "4": {"U": {"6"}},
            "5": {"R": {"6"}},
        },
        initial_state="0",
        final_states={"6"},
    )
    assert PinWords.make_nfa_for_pinword("12") == NFA(
        states={"6", "3", "2", "4", "5", "1", "0"},
        input_symbols={"U", "D", "L", "R"},
        transitions={
            "0": {"U": {"2", "0"}, "L": {"0"}, "D": {"0"}, "R": {"0", "1"}},
            "3": {"U": {"5", "3"}, "L": {"4", "3"}, "D": {"3"}, "R": {"3"}},
            "1": {"U": {"3"}},
            "2": {"R": {"3"}},
            "6": {"U": {"6"}, "L": {"6"}, "D": {"6"}, "R": {"6"}},
            "4": {"U": {"6"}},
            "5": {"L": {"6"}},
        },
        initial_state="0",
        final_states={"6"},
    )
    assert PinWords.make_nfa_for_pinword("13") == NFA(
        states={"6", "3", "2", "4", "5", "1", "0"},
        input_symbols={"U", "D", "L", "R"},
        transitions={
            "0": {"U": {"2", "0"}, "L": {"0"}, "D": {"0"}, "R": {"0", "1"}},
            "3": {"U": {"3"}, "L": {"4", "3"}, "D": {"5", "3"}, "R": {"3"}},
            "1": {"U": {"3"}},
            "2": {"R": {"3"}},
            "6": {"U": {"6"}, "L": {"6"}, "D": {"6"}, "R": {"6"}},
            "4": {"D": {"6"}},
            "5": {"L": {"6"}},
        },
        initial_state="0",
        final_states={"6"},
    )
    assert PinWords.make_nfa_for_pinword("14") == NFA(
        states={"6", "3", "2", "4", "5", "1", "0"},
        input_symbols={"U", "D", "L", "R"},
        transitions={
            "0": {"U": {"2", "0"}, "L": {"0"}, "D": {"0"}, "R": {"0", "1"}},
            "3": {"U": {"3"}, "L": {"3"}, "D": {"5", "3"}, "R": {"4", "3"}},
            "1": {"U": {"3"}},
            "2": {"R": {"3"}},
            "6": {"U": {"6"}, "L": {"6"}, "D": {"6"}, "R": {"6"}},
            "4": {"D": {"6"}},
            "5": {"R": {"6"}},
        },
        initial_state="0",
        final_states={"6"},
    )
    assert PinWords.make_nfa_for_pinword("2U") == NFA(
        states={"2", "3", "0", "1"},
        input_symbols={"U", "D", "L", "R"},
        transitions={
            "0": {"U": {"0", "1"}, "L": {"0"}, "D": {"0"}, "R": {"0"}},
            "1": {"L": {"2"}},
            "3": {"U": {"3"}, "L": {"3"}, "D": {"3"}, "R": {"3"}},
            "2": {"U": {"3"}},
        },
        initial_state="0",
        final_states={"3"},
    )
    assert PinWords.make_nfa_for_pinword("2D") == NFA(
        states={"2", "3", "0", "1"},
        input_symbols={"U", "D", "L", "R"},
        transitions={
            "0": {"U": {"0", "1"}, "L": {"0"}, "D": {"0"}, "R": {"0"}},
            "1": {"L": {"2"}},
            "3": {"U": {"3"}, "L": {"3"}, "D": {"3"}, "R": {"3"}},
            "2": {"D": {"3"}},
        },
        initial_state="0",
        final_states={"3"},
    )
    assert PinWords.make_nfa_for_pinword("2L") == NFA(
        states={"2", "3", "0", "1"},
        input_symbols={"U", "D", "L", "R"},
        transitions={
            "0": {"U": {"0"}, "L": {"0", "1"}, "D": {"0"}, "R": {"0"}},
            "1": {"U": {"2"}},
            "3": {"U": {"3"}, "L": {"3"}, "D": {"3"}, "R": {"3"}},
            "2": {"L": {"3"}},
        },
        initial_state="0",
        final_states={"3"},
    )
    assert PinWords.make_nfa_for_pinword("2R") == NFA(
        states={"2", "3", "0", "1"},
        input_symbols={"U", "D", "L", "R"},
        transitions={
            "0": {"U": {"0"}, "L": {"0", "1"}, "D": {"0"}, "R": {"0"}},
            "1": {"U": {"2"}},
            "3": {"U": {"3"}, "L": {"3"}, "D": {"3"}, "R": {"3"}},
            "2": {"R": {"3"}},
        },
        initial_state="0",
        final_states={"3"},
    )
    assert PinWords.make_nfa_for_pinword("21") == NFA(
        states={"6", "3", "2", "4", "5", "1", "0"},
        input_symbols={"U", "D", "L", "R"},
        transitions={
            "0": {"U": {"2", "0"}, "L": {"0", "1"}, "D": {"0"}, "R": {"0"}},
            "3": {"U": {"5", "3"}, "L": {"3"}, "D": {"3"}, "R": {"4", "3"}},
            "1": {"U": {"3"}},
            "2": {"L": {"3"}},
            "6": {"U": {"6"}, "L": {"6"}, "D": {"6"}, "R": {"6"}},
            "4": {"U": {"6"}},
            "5": {"R": {"6"}},
        },
        initial_state="0",
        final_states={"6"},
    )
    assert PinWords.make_nfa_for_pinword("22") == NFA(
        states={"6", "3", "2", "4", "5", "1", "0"},
        input_symbols={"U", "D", "L", "R"},
        transitions={
            "0": {"U": {"2", "0"}, "L": {"0", "1"}, "D": {"0"}, "R": {"0"}},
            "3": {"U": {"5", "3"}, "L": {"4", "3"}, "D": {"3"}, "R": {"3"}},
            "1": {"U": {"3"}},
            "2": {"L": {"3"}},
            "6": {"U": {"6"}, "L": {"6"}, "D": {"6"}, "R": {"6"}},
            "4": {"U": {"6"}},
            "5": {"L": {"6"}},
        },
        initial_state="0",
        final_states={"6"},
    )
    assert PinWords.make_nfa_for_pinword("23") == NFA(
        states={"6", "3", "2", "4", "5", "1", "0"},
        input_symbols={"U", "D", "L", "R"},
        transitions={
            "0": {"U": {"2", "0"}, "L": {"0", "1"}, "D": {"0"}, "R": {"0"}},
            "3": {"U": {"3"}, "L": {"4", "3"}, "D": {"5", "3"}, "R": {"3"}},
            "1": {"U": {"3"}},
            "2": {"L": {"3"}},
            "6": {"U": {"6"}, "L": {"6"}, "D": {"6"}, "R": {"6"}},
            "4": {"D": {"6"}},
            "5": {"L": {"6"}},
        },
        initial_state="0",
        final_states={"6"},
    )
    assert PinWords.make_nfa_for_pinword("24") == NFA(
        states={"6", "3", "2", "4", "5", "1", "0"},
        input_symbols={"U", "D", "L", "R"},
        transitions={
            "0": {"U": {"2", "0"}, "L": {"0", "1"}, "D": {"0"}, "R": {"0"}},
            "3": {"U": {"3"}, "L": {"3"}, "D": {"5", "3"}, "R": {"4", "3"}},
            "1": {"U": {"3"}},
            "2": {"L": {"3"}},
            "6": {"U": {"6"}, "L": {"6"}, "D": {"6"}, "R": {"6"}},
            "4": {"D": {"6"}},
            "5": {"R": {"6"}},
        },
        initial_state="0",
        final_states={"6"},
    )
    assert PinWords.make_nfa_for_pinword("3U") == NFA(
        states={"2", "3", "0", "1"},
        input_symbols={"U", "D", "L", "R"},
        transitions={
            "0": {"U": {"0"}, "L": {"0"}, "D": {"0", "1"}, "R": {"0"}},
            "1": {"L": {"2"}},
            "3": {"U": {"3"}, "L": {"3"}, "D": {"3"}, "R": {"3"}},
            "2": {"U": {"3"}},
        },
        initial_state="0",
        final_states={"3"},
    )
    assert PinWords.make_nfa_for_pinword("3D") == NFA(
        states={"2", "3", "0", "1"},
        input_symbols={"U", "D", "L", "R"},
        transitions={
            "0": {"U": {"0"}, "L": {"0"}, "D": {"0", "1"}, "R": {"0"}},
            "1": {"L": {"2"}},
            "3": {"U": {"3"}, "L": {"3"}, "D": {"3"}, "R": {"3"}},
            "2": {"D": {"3"}},
        },
        initial_state="0",
        final_states={"3"},
    )
    assert PinWords.make_nfa_for_pinword("3L") == NFA(
        states={"2", "3", "0", "1"},
        input_symbols={"U", "D", "L", "R"},
        transitions={
            "0": {"U": {"0"}, "L": {"0", "1"}, "D": {"0"}, "R": {"0"}},
            "1": {"D": {"2"}},
            "3": {"U": {"3"}, "L": {"3"}, "D": {"3"}, "R": {"3"}},
            "2": {"L": {"3"}},
        },
        initial_state="0",
        final_states={"3"},
    )
    assert PinWords.make_nfa_for_pinword("3R") == NFA(
        states={"2", "3", "0", "1"},
        input_symbols={"U", "D", "L", "R"},
        transitions={
            "0": {"U": {"0"}, "L": {"0", "1"}, "D": {"0"}, "R": {"0"}},
            "1": {"D": {"2"}},
            "3": {"U": {"3"}, "L": {"3"}, "D": {"3"}, "R": {"3"}},
            "2": {"R": {"3"}},
        },
        initial_state="0",
        final_states={"3"},
    )
    assert PinWords.make_nfa_for_pinword("31") == NFA(
        states={"6", "3", "2", "4", "5", "1", "0"},
        input_symbols={"U", "D", "L", "R"},
        transitions={
            "0": {"U": {"0"}, "L": {"0", "1"}, "D": {"2", "0"}, "R": {"0"}},
            "3": {"U": {"5", "3"}, "L": {"3"}, "D": {"3"}, "R": {"4", "3"}},
            "1": {"D": {"3"}},
            "2": {"L": {"3"}},
            "6": {"U": {"6"}, "L": {"6"}, "D": {"6"}, "R": {"6"}},
            "4": {"U": {"6"}},
            "5": {"R": {"6"}},
        },
        initial_state="0",
        final_states={"6"},
    )
    assert PinWords.make_nfa_for_pinword("32") == NFA(
        states={"6", "3", "2", "4", "5", "1", "0"},
        input_symbols={"U", "D", "L", "R"},
        transitions={
            "0": {"U": {"0"}, "L": {"0", "1"}, "D": {"2", "0"}, "R": {"0"}},
            "3": {"U": {"5", "3"}, "L": {"4", "3"}, "D": {"3"}, "R": {"3"}},
            "1": {"D": {"3"}},
            "2": {"L": {"3"}},
            "6": {"U": {"6"}, "L": {"6"}, "D": {"6"}, "R": {"6"}},
            "4": {"U": {"6"}},
            "5": {"L": {"6"}},
        },
        initial_state="0",
        final_states={"6"},
    )
    assert PinWords.make_nfa_for_pinword("33") == NFA(
        states={"6", "3", "2", "4", "5", "1", "0"},
        input_symbols={"U", "D", "L", "R"},
        transitions={
            "0": {"U": {"0"}, "L": {"0", "1"}, "D": {"2", "0"}, "R": {"0"}},
            "3": {"U": {"3"}, "L": {"4", "3"}, "D": {"5", "3"}, "R": {"3"}},
            "1": {"D": {"3"}},
            "2": {"L": {"3"}},
            "6": {"U": {"6"}, "L": {"6"}, "D": {"6"}, "R": {"6"}},
            "4": {"D": {"6"}},
            "5": {"L": {"6"}},
        },
        initial_state="0",
        final_states={"6"},
    )
    assert PinWords.make_nfa_for_pinword("34") == NFA(
        states={"6", "3", "2", "4", "5", "1", "0"},
        input_symbols={"U", "D", "L", "R"},
        transitions={
            "0": {"U": {"0"}, "L": {"0", "1"}, "D": {"2", "0"}, "R": {"0"}},
            "3": {"U": {"3"}, "L": {"3"}, "D": {"5", "3"}, "R": {"4", "3"}},
            "1": {"D": {"3"}},
            "2": {"L": {"3"}},
            "6": {"U": {"6"}, "L": {"6"}, "D": {"6"}, "R": {"6"}},
            "4": {"D": {"6"}},
            "5": {"R": {"6"}},
        },
        initial_state="0",
        final_states={"6"},
    )
    assert PinWords.make_nfa_for_pinword("4U") == NFA(
        states={"2", "3", "0", "1"},
        input_symbols={"U", "D", "L", "R"},
        transitions={
            "0": {"U": {"0"}, "L": {"0"}, "D": {"0", "1"}, "R": {"0"}},
            "1": {"R": {"2"}},
            "3": {"U": {"3"}, "L": {"3"}, "D": {"3"}, "R": {"3"}},
            "2": {"U": {"3"}},
        },
        initial_state="0",
        final_states={"3"},
    )
    assert PinWords.make_nfa_for_pinword("4D") == NFA(
        states={"2", "3", "0", "1"},
        input_symbols={"U", "D", "L", "R"},
        transitions={
            "0": {"U": {"0"}, "L": {"0"}, "D": {"0", "1"}, "R": {"0"}},
            "1": {"R": {"2"}},
            "3": {"U": {"3"}, "L": {"3"}, "D": {"3"}, "R": {"3"}},
            "2": {"D": {"3"}},
        },
        initial_state="0",
        final_states={"3"},
    )
    assert PinWords.make_nfa_for_pinword("4L") == NFA(
        states={"2", "3", "0", "1"},
        input_symbols={"U", "D", "L", "R"},
        transitions={
            "0": {"U": {"0"}, "L": {"0"}, "D": {"0"}, "R": {"0", "1"}},
            "1": {"D": {"2"}},
            "3": {"U": {"3"}, "L": {"3"}, "D": {"3"}, "R": {"3"}},
            "2": {"L": {"3"}},
        },
        initial_state="0",
        final_states={"3"},
    )
    assert PinWords.make_nfa_for_pinword("4R") == NFA(
        states={"2", "3", "0", "1"},
        input_symbols={"U", "D", "L", "R"},
        transitions={
            "0": {"U": {"0"}, "L": {"0"}, "D": {"0"}, "R": {"0", "1"}},
            "1": {"D": {"2"}},
            "3": {"U": {"3"}, "L": {"3"}, "D": {"3"}, "R": {"3"}},
            "2": {"R": {"3"}},
        },
        initial_state="0",
        final_states={"3"},
    )
    assert PinWords.make_nfa_for_pinword("41") == NFA(
        states={"6", "3", "2", "4", "5", "1", "0"},
        input_symbols={"U", "D", "L", "R"},
        transitions={
            "0": {"U": {"0"}, "L": {"0"}, "D": {"2", "0"}, "R": {"0", "1"}},
            "3": {"U": {"5", "3"}, "L": {"3"}, "D": {"3"}, "R": {"4", "3"}},
            "1": {"D": {"3"}},
            "2": {"R": {"3"}},
            "6": {"U": {"6"}, "L": {"6"}, "D": {"6"}, "R": {"6"}},
            "4": {"U": {"6"}},
            "5": {"R": {"6"}},
        },
        initial_state="0",
        final_states={"6"},
    )
    assert PinWords.make_nfa_for_pinword("42") == NFA(
        states={"6", "3", "2", "4", "5", "1", "0"},
        input_symbols={"U", "D", "L", "R"},
        transitions={
            "0": {"U": {"0"}, "L": {"0"}, "D": {"2", "0"}, "R": {"0", "1"}},
            "3": {"U": {"5", "3"}, "L": {"4", "3"}, "D": {"3"}, "R": {"3"}},
            "1": {"D": {"3"}},
            "2": {"R": {"3"}},
            "6": {"U": {"6"}, "L": {"6"}, "D": {"6"}, "R": {"6"}},
            "4": {"U": {"6"}},
            "5": {"L": {"6"}},
        },
        initial_state="0",
        final_states={"6"},
    )
    assert PinWords.make_nfa_for_pinword("43") == NFA(
        states={"6", "3", "2", "4", "5", "1", "0"},
        input_symbols={"U", "D", "L", "R"},
        transitions={
            "0": {"U": {"0"}, "L": {"0"}, "D": {"2", "0"}, "R": {"0", "1"}},
            "3": {"U": {"3"}, "L": {"4", "3"}, "D": {"5", "3"}, "R": {"3"}},
            "1": {"D": {"3"}},
            "2": {"R": {"3"}},
            "6": {"U": {"6"}, "L": {"6"}, "D": {"6"}, "R": {"6"}},
            "4": {"D": {"6"}},
            "5": {"L": {"6"}},
        },
        initial_state="0",
        final_states={"6"},
    )
    assert PinWords.make_nfa_for_pinword("44") == NFA(
        states={"6", "3", "2", "4", "5", "1", "0"},
        input_symbols={"U", "D", "L", "R"},
        transitions={
            "0": {"U": {"0"}, "L": {"0"}, "D": {"2", "0"}, "R": {"0", "1"}},
            "3": {"U": {"3"}, "L": {"3"}, "D": {"5", "3"}, "R": {"4", "3"}},
            "1": {"D": {"3"}},
            "2": {"R": {"3"}},
            "6": {"U": {"6"}, "L": {"6"}, "D": {"6"}, "R": {"6"}},
            "4": {"D": {"6"}},
            "5": {"R": {"6"}},
        },
        initial_state="0",
        final_states={"6"},
    )
    assert PinWords.make_nfa_for_pinword("1D4") == NFA(
        states={"6", "3", "2", "4", "5", "1", "0"},
        input_symbols={"U", "D", "L", "R"},
        transitions={
            "0": {"U": {"0", "1"}, "L": {"0"}, "D": {"0"}, "R": {"0"}},
            "1": {"R": {"2"}},
            "3": {"U": {"3"}, "L": {"3"}, "D": {"5", "3"}, "R": {"4", "3"}},
            "2": {"D": {"3"}},
            "6": {"U": {"6"}, "L": {"6"}, "D": {"6"}, "R": {"6"}},
            "4": {"D": {"6"}},
            "5": {"R": {"6"}},
        },
        initial_state="0",
        final_states={"6"},
    )
    assert PinWords.make_nfa_for_pinword("3R4") == NFA(
        states={"6", "3", "2", "4", "5", "1", "0"},
        input_symbols={"U", "D", "L", "R"},
        transitions={
            "0": {"U": {"0"}, "L": {"0", "1"}, "D": {"0"}, "R": {"0"}},
            "1": {"D": {"2"}},
            "3": {"U": {"3"}, "L": {"3"}, "D": {"5", "3"}, "R": {"4", "3"}},
            "2": {"R": {"3"}},
            "6": {"U": {"6"}, "L": {"6"}, "D": {"6"}, "R": {"6"}},
            "4": {"D": {"6"}},
            "5": {"R": {"6"}},
        },
        initial_state="0",
        final_states={"6"},
    )
    assert PinWords.make_nfa_for_pinword("1L4") == NFA(
        states={"6", "3", "2", "4", "5", "1", "0"},
        input_symbols={"U", "D", "L", "R"},
        transitions={
            "0": {"U": {"0"}, "L": {"0"}, "D": {"0"}, "R": {"0", "1"}},
            "1": {"U": {"2"}},
            "3": {"U": {"3"}, "L": {"3"}, "D": {"5", "3"}, "R": {"4", "3"}},
            "2": {"L": {"3"}},
            "6": {"U": {"6"}, "L": {"6"}, "D": {"6"}, "R": {"6"}},
            "4": {"D": {"6"}},
            "5": {"R": {"6"}},
        },
        initial_state="0",
        final_states={"6"},
    )
    assert PinWords.make_nfa_for_pinword("4D3") == NFA(
        states={"6", "3", "2", "4", "5", "1", "0"},
        input_symbols={"U", "D", "L", "R"},
        transitions={
            "0": {"U": {"0"}, "L": {"0"}, "D": {"0", "1"}, "R": {"0"}},
            "1": {"R": {"2"}},
            "3": {"U": {"3"}, "L": {"4", "3"}, "D": {"5", "3"}, "R": {"3"}},
            "2": {"D": {"3"}},
            "6": {"U": {"6"}, "L": {"6"}, "D": {"6"}, "R": {"6"}},
            "4": {"D": {"6"}},
            "5": {"L": {"6"}},
        },
        initial_state="0",
        final_states={"6"},
    )
    assert PinWords.make_nfa_for_pinword("413") == NFA(
        states={"6", "3", "9", "1", "0", "7", "2", "4", "5", "8"},
        input_symbols={"U", "D", "L", "R"},
        transitions={
            "0": {"U": {"0"}, "L": {"0"}, "D": {"2", "0"}, "R": {"0", "1"}},
            "3": {"U": {"5", "3"}, "L": {"3"}, "D": {"3"}, "R": {"4", "3"}},
            "1": {"D": {"3"}},
            "2": {"R": {"3"}},
            "6": {"U": {"6"}, "L": {"7", "6"}, "D": {"6", "8"}, "R": {"6"}},
            "4": {"U": {"6"}},
            "5": {"R": {"6"}},
            "9": {"U": {"9"}, "L": {"9"}, "D": {"9"}, "R": {"9"}},
            "7": {"D": {"9"}},
            "8": {"L": {"9"}},
        },
        initial_state="0",
        final_states={"9"},
    )
    assert PinWords.make_nfa_for_pinword("1111") == NFA(
        states={"6", "3", "10", "12", "9", "1", "0", "7", "2", "4", "5", "11", "8"},
        input_symbols={"U", "D", "L", "R"},
        transitions={
            "0": {"U": {"2", "0"}, "L": {"0"}, "D": {"0"}, "R": {"0", "1"}},
            "3": {"U": {"5", "3"}, "L": {"3"}, "D": {"3"}, "R": {"4", "3"}},
            "1": {"U": {"3"}},
            "2": {"R": {"3"}},
            "6": {"U": {"6", "8"}, "L": {"6"}, "D": {"6"}, "R": {"7", "6"}},
            "4": {"U": {"6"}},
            "5": {"R": {"6"}},
            "9": {"U": {"11", "9"}, "L": {"9"}, "D": {"9"}, "R": {"10", "9"}},
            "7": {"U": {"9"}},
            "8": {"R": {"9"}},
            "12": {"U": {"12"}, "L": {"12"}, "D": {"12"}, "R": {"12"}},
            "10": {"U": {"12"}},
            "11": {"R": {"12"}},
        },
        initial_state="0",
        final_states={"12"},
    )
    assert PinWords.make_nfa_for_pinword("4413") == NFA(
        states={"6", "3", "10", "12", "9", "1", "0", "7", "2", "4", "5", "11", "8"},
        input_symbols={"U", "D", "L", "R"},
        transitions={
            "0": {"U": {"0"}, "L": {"0"}, "D": {"2", "0"}, "R": {"0", "1"}},
            "3": {"U": {"3"}, "L": {"3"}, "D": {"5", "3"}, "R": {"4", "3"}},
            "1": {"D": {"3"}},
            "2": {"R": {"3"}},
            "6": {"U": {"6", "8"}, "L": {"6"}, "D": {"6"}, "R": {"7", "6"}},
            "4": {"D": {"6"}},
            "5": {"R": {"6"}},
            "9": {"U": {"9"}, "L": {"10", "9"}, "D": {"11", "9"}, "R": {"9"}},
            "7": {"U": {"9"}},
            "8": {"R": {"9"}},
            "12": {"U": {"12"}, "L": {"12"}, "D": {"12"}, "R": {"12"}},
            "10": {"D": {"12"}},
            "11": {"L": {"12"}},
        },
        initial_state="0",
        final_states={"12"},
    )
    assert PinWords.make_nfa_for_pinword("1U41") == NFA(
        states={"6", "3", "9", "1", "0", "7", "2", "4", "5", "8"},
        input_symbols={"U", "D", "L", "R"},
        transitions={
            "0": {"U": {"0", "1"}, "L": {"0"}, "D": {"0"}, "R": {"0"}},
            "1": {"R": {"2"}},
            "3": {"U": {"3"}, "L": {"3"}, "D": {"5", "3"}, "R": {"4", "3"}},
            "2": {"U": {"3"}},
            "6": {"U": {"6", "8"}, "L": {"6"}, "D": {"6"}, "R": {"7", "6"}},
            "4": {"D": {"6"}},
            "5": {"R": {"6"}},
            "9": {"U": {"9"}, "L": {"9"}, "D": {"9"}, "R": {"9"}},
            "7": {"U": {"9"}},
            "8": {"R": {"9"}},
        },
        initial_state="0",
        final_states={"9"},
    )
    assert PinWords.make_nfa_for_pinword("23R3") == NFA(
        states={"6", "3", "9", "1", "0", "7", "2", "4", "5", "8"},
        input_symbols={"U", "D", "L", "R"},
        transitions={
            "0": {"U": {"2", "0"}, "L": {"0", "1"}, "D": {"0"}, "R": {"0"}},
            "3": {"U": {"3"}, "L": {"4", "3"}, "D": {"3"}, "R": {"3"}},
            "1": {"U": {"3"}},
            "2": {"L": {"3"}},
            "4": {"D": {"5"}},
            "6": {"U": {"6"}, "L": {"7", "6"}, "D": {"6", "8"}, "R": {"6"}},
            "5": {"R": {"6"}},
            "9": {"U": {"9"}, "L": {"9"}, "D": {"9"}, "R": {"9"}},
            "7": {"D": {"9"}},
            "8": {"L": {"9"}},
        },
        initial_state="0",
        final_states={"9"},
    )
    assert PinWords.make_nfa_for_pinword("2L24") == NFA(
        states={"6", "3", "9", "1", "0", "7", "2", "4", "5", "8"},
        input_symbols={"U", "D", "L", "R"},
        transitions={
            "0": {"U": {"0"}, "L": {"0", "1"}, "D": {"0"}, "R": {"0"}},
            "1": {"U": {"2"}},
            "3": {"U": {"5", "3"}, "L": {"4", "3"}, "D": {"3"}, "R": {"3"}},
            "2": {"L": {"3"}},
            "6": {"U": {"6"}, "L": {"6"}, "D": {"6", "8"}, "R": {"7", "6"}},
            "4": {"U": {"6"}},
            "5": {"L": {"6"}},
            "9": {"U": {"9"}, "L": {"9"}, "D": {"9"}, "R": {"9"}},
            "7": {"D": {"9"}},
            "8": {"R": {"9"}},
        },
        initial_state="0",
        final_states={"9"},
    )
    assert PinWords.make_nfa_for_pinword("222D4") == NFA(
        states={"6", "3", "10", "12", "9", "1", "0", "7", "2", "4", "5", "11", "8"},
        input_symbols={"U", "D", "L", "R"},
        transitions={
            "0": {"U": {"2", "0"}, "L": {"0", "1"}, "D": {"0"}, "R": {"0"}},
            "3": {"U": {"5", "3"}, "L": {"4", "3"}, "D": {"3"}, "R": {"3"}},
            "1": {"U": {"3"}},
            "2": {"L": {"3"}},
            "6": {"U": {"7", "6"}, "L": {"6"}, "D": {"6"}, "R": {"6"}},
            "4": {"U": {"6"}},
            "5": {"L": {"6"}},
            "7": {"L": {"8"}},
            "9": {"U": {"9"}, "L": {"9"}, "D": {"11", "9"}, "R": {"10", "9"}},
            "8": {"D": {"9"}},
            "12": {"U": {"12"}, "L": {"12"}, "D": {"12"}, "R": {"12"}},
            "10": {"D": {"12"}},
            "11": {"R": {"12"}},
        },
        initial_state="0",
        final_states={"12"},
    )


def test_make_dfa_for_m():
    assert PinWords.make_dfa_for_m() == DFA(
        states={"0", "1", "2", "3"},
        input_symbols=set("ULDR"),
        transitions={
            "0": {"U": "1", "D": "1", "L": "2", "R": "2"},
            "1": {"U": "3", "D": "3", "L": "2", "R": "2"},
            "2": {"U": "1", "D": "1", "L": "3", "R": "3"},
            "3": {"U": "3", "D": "3", "L": "3", "R": "3"},
        },
        initial_state="0",
        final_states={"0", "1", "2"},
    )


def test_make_dfa_for_pinword():
    assert PinWords.make_dfa_for_pinword("1D") == DFA(
        states={"{0,2}", "{0}", "{0,1}", "{{0,1,3},{0,2,3},{0,3}}"},
        input_symbols={"R", "U", "D", "L"},
        transitions={
            "{0}": {"R": "{0}", "U": "{0,1}", "D": "{0}", "L": "{0}"},
            "{0,1}": {"R": "{0,2}", "U": "{0,1}", "D": "{0}", "L": "{0}"},
            "{0,2}": {
                "R": "{0}",
                "U": "{0,1}",
                "D": "{{0,1,3},{0,2,3},{0,3}}",
                "L": "{0}",
            },
            "{{0,1,3},{0,2,3},{0,3}}": {
                "R": "{{0,1,3},{0,2,3},{0,3}}",
                "U": "{{0,1,3},{0,2,3},{0,3}}",
                "D": "{{0,1,3},{0,2,3},{0,3}}",
                "L": "{{0,1,3},{0,2,3},{0,3}}",
            },
        },
        initial_state="{0}",
        final_states={"{{0,1,3},{0,2,3},{0,3}}"},
    )
    assert PinWords.make_dfa_for_pinword("4U") == DFA(
        states={"{0,2}", "{0}", "{0,1}", "{{0,1,3},{0,2,3},{0,3}}"},
        input_symbols={"R", "U", "D", "L"},
        transitions={
            "{0}": {"R": "{0}", "U": "{0}", "D": "{0,1}", "L": "{0}"},
            "{0,1}": {"R": "{0,2}", "U": "{0}", "D": "{0,1}", "L": "{0}"},
            "{0,2}": {
                "R": "{0}",
                "U": "{{0,1,3},{0,2,3},{0,3}}",
                "D": "{0,1}",
                "L": "{0}",
            },
            "{{0,1,3},{0,2,3},{0,3}}": {
                "R": "{{0,1,3},{0,2,3},{0,3}}",
                "U": "{{0,1,3},{0,2,3},{0,3}}",
                "D": "{{0,1,3},{0,2,3},{0,3}}",
                "L": "{{0,1,3},{0,2,3},{0,3}}",
            },
        },
        initial_state="{0}",
        final_states={"{{0,1,3},{0,2,3},{0,3}}"},
    )
    assert PinWords.make_dfa_for_pinword("4U") == DFA(
        states={"{0,2}", "{0}", "{0,1}", "{{0,1,3},{0,2,3},{0,3}}"},
        input_symbols={"R", "U", "D", "L"},
        transitions={
            "{0}": {"R": "{0}", "U": "{0}", "D": "{0,1}", "L": "{0}"},
            "{0,1}": {"R": "{0,2}", "U": "{0}", "D": "{0,1}", "L": "{0}"},
            "{0,2}": {
                "R": "{0}",
                "U": "{{0,1,3},{0,2,3},{0,3}}",
                "D": "{0,1}",
                "L": "{0}",
            },
            "{{0,1,3},{0,2,3},{0,3}}": {
                "R": "{{0,1,3},{0,2,3},{0,3}}",
                "U": "{{0,1,3},{0,2,3},{0,3}}",
                "D": "{{0,1,3},{0,2,3},{0,3}}",
                "L": "{{0,1,3},{0,2,3},{0,3}}",
            },
        },
        initial_state="{0}",
        final_states={"{{0,1,3},{0,2,3},{0,3}}"},
    )
    assert PinWords.make_dfa_for_pinword("11") == DFA(
        states={
            "{0,2}",
            "{{0,1,3,4,6},{0,2,3,5,6},{0,3,6}}",
            "{{0,1,3},{0,2,3},{0,3}}",
            "{0}",
            "{0,1}",
            "{0,1,3,4}",
            "{0,2,3,5}",
        },
        input_symbols={"R", "U", "D", "L"},
        transitions={
            "{0}": {"R": "{0,1}", "U": "{0,2}", "D": "{0}", "L": "{0}"},
            "{0,1}": {
                "R": "{0,1}",
                "U": "{{0,1,3},{0,2,3},{0,3}}",
                "D": "{0}",
                "L": "{0}",
            },
            "{0,2}": {
                "R": "{{0,1,3},{0,2,3},{0,3}}",
                "U": "{0,2}",
                "D": "{0}",
                "L": "{0}",
            },
            "{0,1,3,4}": {
                "R": "{0,1,3,4}",
                "U": "{{0,1,3,4,6},{0,2,3,5,6},{0,3,6}}",
                "D": "{{0,1,3},{0,2,3},{0,3}}",
                "L": "{{0,1,3},{0,2,3},{0,3}}",
            },
            "{0,2,3,5}": {
                "R": "{{0,1,3,4,6},{0,2,3,5,6},{0,3,6}}",
                "U": "{0,2,3,5}",
                "D": "{{0,1,3},{0,2,3},{0,3}}",
                "L": "{{0,1,3},{0,2,3},{0,3}}",
            },
            "{{0,1,3,4,6},{0,2,3,5,6},{0,3,6}}": {
                "R": "{{0,1,3,4,6},{0,2,3,5,6},{0,3,6}}",
                "U": "{{0,1,3,4,6},{0,2,3,5,6},{0,3,6}}",
                "D": "{{0,1,3,4,6},{0,2,3,5,6},{0,3,6}}",
                "L": "{{0,1,3,4,6},{0,2,3,5,6},{0,3,6}}",
            },
            "{{0,1,3},{0,2,3},{0,3}}": {
                "R": "{0,1,3,4}",
                "U": "{0,2,3,5}",
                "D": "{{0,1,3},{0,2,3},{0,3}}",
                "L": "{{0,1,3},{0,2,3},{0,3}}",
            },
        },
        initial_state="{0}",
        final_states={"{{0,1,3,4,6},{0,2,3,5,6},{0,3,6}}"},
    )
    assert PinWords.make_dfa_for_pinword("31") == DFA(
        states={
            "{{0,1,3},{0,2,3}}",
            "{0,2}",
            "{0,3,5}",
            "{{0,1,3,6},{0,2,3,6},{0,3,4,6},{0,3,5,6}}",
            "{0}",
            "{0,1}",
            "{0,3,4}",
        },
        input_symbols={"R", "U", "D", "L"},
        transitions={
            "{0}": {"R": "{0}", "U": "{0}", "D": "{0,2}", "L": "{0,1}"},
            "{0,2}": {"R": "{0}", "U": "{0}", "D": "{0,2}", "L": "{{0,1,3},{0,2,3}}"},
            "{0,1}": {"R": "{0}", "U": "{0}", "D": "{{0,1,3},{0,2,3}}", "L": "{0,1}"},
            "{0,3,4}": {
                "R": "{0,3,4}",
                "U": "{{0,1,3,6},{0,2,3,6},{0,3,4,6},{0,3,5,6}}",
                "D": "{{0,1,3},{0,2,3}}",
                "L": "{{0,1,3},{0,2,3}}",
            },
            "{0,3,5}": {
                "R": "{{0,1,3,6},{0,2,3,6},{0,3,4,6},{0,3,5,6}}",
                "U": "{0,3,5}",
                "D": "{{0,1,3},{0,2,3}}",
                "L": "{{0,1,3},{0,2,3}}",
            },
            "{{0,1,3},{0,2,3}}": {
                "R": "{0,3,4}",
                "U": "{0,3,5}",
                "D": "{{0,1,3},{0,2,3}}",
                "L": "{{0,1,3},{0,2,3}}",
            },
            "{{0,1,3,6},{0,2,3,6},{0,3,4,6},{0,3,5,6}}": {
                "R": "{{0,1,3,6},{0,2,3,6},{0,3,4,6},{0,3,5,6}}",
                "U": "{{0,1,3,6},{0,2,3,6},{0,3,4,6},{0,3,5,6}}",
                "D": "{{0,1,3,6},{0,2,3,6},{0,3,4,6},{0,3,5,6}}",
                "L": "{{0,1,3,6},{0,2,3,6},{0,3,4,6},{0,3,5,6}}",
            },
        },
        initial_state="{0}",
        final_states={"{{0,1,3,6},{0,2,3,6},{0,3,4,6},{0,3,5,6}}"},
    )
    assert PinWords.make_dfa_for_pinword("1R") == DFA(
        states={"{0,2}", "{0}", "{0,1}", "{{0,1,3},{0,2,3},{0,3}}"},
        input_symbols={"R", "U", "D", "L"},
        transitions={
            "{0}": {"R": "{0,1}", "U": "{0}", "D": "{0}", "L": "{0}"},
            "{0,1}": {"R": "{0,1}", "U": "{0,2}", "D": "{0}", "L": "{0}"},
            "{0,2}": {
                "R": "{{0,1,3},{0,2,3},{0,3}}",
                "U": "{0}",
                "D": "{0}",
                "L": "{0}",
            },
            "{{0,1,3},{0,2,3},{0,3}}": {
                "R": "{{0,1,3},{0,2,3},{0,3}}",
                "U": "{{0,1,3},{0,2,3},{0,3}}",
                "D": "{{0,1,3},{0,2,3},{0,3}}",
                "L": "{{0,1,3},{0,2,3},{0,3}}",
            },
        },
        initial_state="{0}",
        final_states={"{{0,1,3},{0,2,3},{0,3}}"},
    )
    assert PinWords.make_dfa_for_pinword("2L") == DFA(
        states={"{0,2}", "{0}", "{0,1}", "{{0,1,3},{0,2,3},{0,3}}"},
        input_symbols={"R", "U", "D", "L"},
        transitions={
            "{0}": {"R": "{0}", "U": "{0}", "D": "{0}", "L": "{0,1}"},
            "{0,1}": {"R": "{0}", "U": "{0,2}", "D": "{0}", "L": "{0,1}"},
            "{0,2}": {
                "R": "{0}",
                "U": "{0}",
                "D": "{0}",
                "L": "{{0,1,3},{0,2,3},{0,3}}",
            },
            "{{0,1,3},{0,2,3},{0,3}}": {
                "R": "{{0,1,3},{0,2,3},{0,3}}",
                "U": "{{0,1,3},{0,2,3},{0,3}}",
                "D": "{{0,1,3},{0,2,3},{0,3}}",
                "L": "{{0,1,3},{0,2,3},{0,3}}",
            },
        },
        initial_state="{0}",
        final_states={"{{0,1,3},{0,2,3},{0,3}}"},
    )
    assert PinWords.make_dfa_for_pinword("2R2") == DFA(
        states={
            "{0,3}",
            "{0,3,5}",
            "{0,2}",
            "{{0,1,3,4,6},{0,2,3,5,6},{0,3,5,6},{0,3,6}}",
            "{0}",
            "{0,1}",
            "{0,1,3,4}",
        },
        input_symbols={"R", "U", "D", "L"},
        transitions={
            "{0}": {"R": "{0}", "U": "{0}", "D": "{0}", "L": "{0,1}"},
            "{0,1}": {"R": "{0}", "U": "{0,2}", "D": "{0}", "L": "{0,1}"},
            "{0,2}": {"R": "{0,3}", "U": "{0}", "D": "{0}", "L": "{0,1}"},
            "{0,3}": {"R": "{0,3}", "U": "{0,3,5}", "D": "{0,3}", "L": "{0,1,3,4}"},
            "{0,3,5}": {
                "R": "{0,3}",
                "U": "{0,3,5}",
                "D": "{0,3}",
                "L": "{{0,1,3,4,6},{0,2,3,5,6},{0,3,5,6},{0,3,6}}",
            },
            "{0,1,3,4}": {
                "R": "{0,3}",
                "U": "{{0,1,3,4,6},{0,2,3,5,6},{0,3,5,6},{0,3,6}}",
                "D": "{0,3}",
                "L": "{0,1,3,4}",
            },
            "{{0,1,3,4,6},{0,2,3,5,6},{0,3,5,6},{0,3,6}}": {
                "R": "{{0,1,3,4,6},{0,2,3,5,6},{0,3,5,6},{0,3,6}}",
                "U": "{{0,1,3,4,6},{0,2,3,5,6},{0,3,5,6},{0,3,6}}",
                "D": "{{0,1,3,4,6},{0,2,3,5,6},{0,3,5,6},{0,3,6}}",
                "L": "{{0,1,3,4,6},{0,2,3,5,6},{0,3,5,6},{0,3,6}}",
            },
        },
        initial_state="{0}",
        final_states={"{{0,1,3,4,6},{0,2,3,5,6},{0,3,5,6},{0,3,6}}"},
    )
    assert PinWords.make_dfa_for_pinword("1") == DFA(
        states={"{0,2}", "{0}", "{0,1}", "{{0,1,3},{0,2,3},{0,3}}"},
        input_symbols={"R", "U", "D", "L"},
        transitions={
            "{0}": {"R": "{0,1}", "U": "{0,2}", "D": "{0}", "L": "{0}"},
            "{0,1}": {
                "R": "{0,1}",
                "U": "{{0,1,3},{0,2,3},{0,3}}",
                "D": "{0}",
                "L": "{0}",
            },
            "{0,2}": {
                "R": "{{0,1,3},{0,2,3},{0,3}}",
                "U": "{0,2}",
                "D": "{0}",
                "L": "{0}",
            },
            "{{0,1,3},{0,2,3},{0,3}}": {
                "R": "{{0,1,3},{0,2,3},{0,3}}",
                "U": "{{0,1,3},{0,2,3},{0,3}}",
                "D": "{{0,1,3},{0,2,3},{0,3}}",
                "L": "{{0,1,3},{0,2,3},{0,3}}",
            },
        },
        initial_state="{0}",
        final_states={"{{0,1,3},{0,2,3},{0,3}}"},
    )
    assert PinWords.make_dfa_for_pinword("2R") == DFA(
        states={"{0,2}", "{0}", "{0,1}", "{{0,1,3},{0,2,3},{0,3}}"},
        input_symbols={"R", "U", "D", "L"},
        transitions={
            "{0}": {"R": "{0}", "U": "{0}", "D": "{0}", "L": "{0,1}"},
            "{0,1}": {"R": "{0}", "U": "{0,2}", "D": "{0}", "L": "{0,1}"},
            "{0,2}": {
                "R": "{{0,1,3},{0,2,3},{0,3}}",
                "U": "{0}",
                "D": "{0}",
                "L": "{0,1}",
            },
            "{{0,1,3},{0,2,3},{0,3}}": {
                "R": "{{0,1,3},{0,2,3},{0,3}}",
                "U": "{{0,1,3},{0,2,3},{0,3}}",
                "D": "{{0,1,3},{0,2,3},{0,3}}",
                "L": "{{0,1,3},{0,2,3},{0,3}}",
            },
        },
        initial_state="{0}",
        final_states={"{{0,1,3},{0,2,3},{0,3}}"},
    )
    assert PinWords.make_dfa_for_pinword("43LU") == DFA(
        states={
            "{0,2}",
            "{{0,1,3,7},{0,2,3,5,7},{0,2,3,7},{0,3,4,6,7},{0,3,4,7},{0,3,7}}",
            "{{0,1,3},{0,2,3},{0,3}}",
            "{0,3,4,6}",
            "{0}",
            "{0,1}",
            "{0,3,4}",
            "{0,2,3,5}",
        },
        input_symbols={"R", "U", "D", "L"},
        transitions={
            "{0}": {"R": "{0,1}", "U": "{0}", "D": "{0,2}", "L": "{0}"},
            "{0,1}": {
                "R": "{0,1}",
                "U": "{0}",
                "D": "{{0,1,3},{0,2,3},{0,3}}",
                "L": "{0}",
            },
            "{0,2}": {
                "R": "{{0,1,3},{0,2,3},{0,3}}",
                "U": "{0}",
                "D": "{0,2}",
                "L": "{0}",
            },
            "{0,3,4}": {
                "R": "{{0,1,3},{0,2,3},{0,3}}",
                "U": "{{0,1,3},{0,2,3},{0,3}}",
                "D": "{0,2,3,5}",
                "L": "{0,3,4}",
            },
            "{0,2,3,5}": {
                "R": "{{0,1,3},{0,2,3},{0,3}}",
                "U": "{{0,1,3},{0,2,3},{0,3}}",
                "D": "{{0,1,3},{0,2,3},{0,3}}",
                "L": "{0,3,4,6}",
            },
            "{0,3,4,6}": {
                "R": "{{0,1,3},{0,2,3},{0,3}}",
                "U": "{{0,1,3,7},{0,2,3,5,7},{0,2,3,7},{0,3,4,6,7},{0,3,4,7},{0,3,7}}",
                "D": "{0,2,3,5}",
                "L": "{0,3,4}",
            },
            "{{0,1,3,7},{0,2,3,5,7},{0,2,3,7},{0,3,4,6,7},{0,3,4,7},{0,3,7}}": {
                "R": "{{0,1,3,7},{0,2,3,5,7},{0,2,3,7},{0,3,4,6,7},{0,3,4,7},{0,3,7}}",
                "U": "{{0,1,3,7},{0,2,3,5,7},{0,2,3,7},{0,3,4,6,7},{0,3,4,7},{0,3,7}}",
                "D": "{{0,1,3,7},{0,2,3,5,7},{0,2,3,7},{0,3,4,6,7},{0,3,4,7},{0,3,7}}",
                "L": "{{0,1,3,7},{0,2,3,5,7},{0,2,3,7},{0,3,4,6,7},{0,3,4,7},{0,3,7}}",
            },
            "{{0,1,3},{0,2,3},{0,3}}": {
                "R": "{{0,1,3},{0,2,3},{0,3}}",
                "U": "{{0,1,3},{0,2,3},{0,3}}",
                "D": "{{0,1,3},{0,2,3},{0,3}}",
                "L": "{0,3,4}",
            },
        },
        initial_state="{0}",
        final_states={
            "{{0,1,3,7},{0,2,3,5,7},{0,2,3,7},{0,3,4,6,7},{0,3,4,7},{0,3,7}}"
        },
    )
    assert PinWords.make_dfa_for_pinword("3U") == DFA(
        states={"{0,2}", "{0}", "{0,1}", "{{0,1,3},{0,2,3},{0,3}}"},
        input_symbols={"R", "U", "D", "L"},
        transitions={
            "{0}": {"R": "{0}", "U": "{0}", "D": "{0,1}", "L": "{0}"},
            "{0,1}": {"R": "{0}", "U": "{0}", "D": "{0,1}", "L": "{0,2}"},
            "{0,2}": {
                "R": "{0}",
                "U": "{{0,1,3},{0,2,3},{0,3}}",
                "D": "{0,1}",
                "L": "{0}",
            },
            "{{0,1,3},{0,2,3},{0,3}}": {
                "R": "{{0,1,3},{0,2,3},{0,3}}",
                "U": "{{0,1,3},{0,2,3},{0,3}}",
                "D": "{{0,1,3},{0,2,3},{0,3}}",
                "L": "{{0,1,3},{0,2,3},{0,3}}",
            },
        },
        initial_state="{0}",
        final_states={"{{0,1,3},{0,2,3},{0,3}}"},
    )
    assert PinWords.make_dfa_for_pinword("44") == DFA(
        states={
            "{0,2}",
            "{{0,1,3,4,6},{0,2,3,5,6},{0,3,6}}",
            "{{0,1,3},{0,2,3},{0,3}}",
            "{0}",
            "{0,1}",
            "{0,1,3,4}",
            "{0,2,3,5}",
        },
        input_symbols={"R", "U", "D", "L"},
        transitions={
            "{0}": {"R": "{0,1}", "U": "{0}", "D": "{0,2}", "L": "{0}"},
            "{0,1}": {
                "R": "{0,1}",
                "U": "{0}",
                "D": "{{0,1,3},{0,2,3},{0,3}}",
                "L": "{0}",
            },
            "{0,2}": {
                "R": "{{0,1,3},{0,2,3},{0,3}}",
                "U": "{0}",
                "D": "{0,2}",
                "L": "{0}",
            },
            "{0,1,3,4}": {
                "R": "{0,1,3,4}",
                "U": "{{0,1,3},{0,2,3},{0,3}}",
                "D": "{{0,1,3,4,6},{0,2,3,5,6},{0,3,6}}",
                "L": "{{0,1,3},{0,2,3},{0,3}}",
            },
            "{0,2,3,5}": {
                "R": "{{0,1,3,4,6},{0,2,3,5,6},{0,3,6}}",
                "U": "{{0,1,3},{0,2,3},{0,3}}",
                "D": "{0,2,3,5}",
                "L": "{{0,1,3},{0,2,3},{0,3}}",
            },
            "{{0,1,3,4,6},{0,2,3,5,6},{0,3,6}}": {
                "R": "{{0,1,3,4,6},{0,2,3,5,6},{0,3,6}}",
                "U": "{{0,1,3,4,6},{0,2,3,5,6},{0,3,6}}",
                "D": "{{0,1,3,4,6},{0,2,3,5,6},{0,3,6}}",
                "L": "{{0,1,3,4,6},{0,2,3,5,6},{0,3,6}}",
            },
            "{{0,1,3},{0,2,3},{0,3}}": {
                "R": "{0,1,3,4}",
                "U": "{{0,1,3},{0,2,3},{0,3}}",
                "D": "{0,2,3,5}",
                "L": "{{0,1,3},{0,2,3},{0,3}}",
            },
        },
        initial_state="{0}",
        final_states={"{{0,1,3,4,6},{0,2,3,5,6},{0,3,6}}"},
    )
    assert PinWords.make_dfa_for_pinword("32") == DFA(
        states={
            "{{0,1,3,4,6},{0,2,3,6},{0,3,5,6},{0,3,6}}",
            "{0,2}",
            "{0,3,5}",
            "{{0,1,3},{0,2,3},{0,3}}",
            "{0}",
            "{0,1}",
            "{0,1,3,4}",
        },
        input_symbols={"R", "U", "D", "L"},
        transitions={
            "{0}": {"R": "{0}", "U": "{0}", "D": "{0,2}", "L": "{0,1}"},
            "{0,2}": {
                "R": "{0}",
                "U": "{0}",
                "D": "{0,2}",
                "L": "{{0,1,3},{0,2,3},{0,3}}",
            },
            "{0,1}": {
                "R": "{0}",
                "U": "{0}",
                "D": "{{0,1,3},{0,2,3},{0,3}}",
                "L": "{0,1}",
            },
            "{0,3,5}": {
                "R": "{{0,1,3},{0,2,3},{0,3}}",
                "U": "{0,3,5}",
                "D": "{{0,1,3},{0,2,3},{0,3}}",
                "L": "{{0,1,3,4,6},{0,2,3,6},{0,3,5,6},{0,3,6}}",
            },
            "{0,1,3,4}": {
                "R": "{{0,1,3},{0,2,3},{0,3}}",
                "U": "{{0,1,3,4,6},{0,2,3,6},{0,3,5,6},{0,3,6}}",
                "D": "{{0,1,3},{0,2,3},{0,3}}",
                "L": "{0,1,3,4}",
            },
            "{{0,1,3},{0,2,3},{0,3}}": {
                "R": "{{0,1,3},{0,2,3},{0,3}}",
                "U": "{0,3,5}",
                "D": "{{0,1,3},{0,2,3},{0,3}}",
                "L": "{0,1,3,4}",
            },
            "{{0,1,3,4,6},{0,2,3,6},{0,3,5,6},{0,3,6}}": {
                "R": "{{0,1,3,4,6},{0,2,3,6},{0,3,5,6},{0,3,6}}",
                "U": "{{0,1,3,4,6},{0,2,3,6},{0,3,5,6},{0,3,6}}",
                "D": "{{0,1,3,4,6},{0,2,3,6},{0,3,5,6},{0,3,6}}",
                "L": "{{0,1,3,4,6},{0,2,3,6},{0,3,5,6},{0,3,6}}",
            },
        },
        initial_state="{0}",
        final_states={"{{0,1,3,4,6},{0,2,3,6},{0,3,5,6},{0,3,6}}"},
    )
    assert PinWords.make_dfa_for_pinword("2R2") == DFA(
        states={
            "{0,3}",
            "{0,3,5}",
            "{0,2}",
            "{{0,1,3,4,6},{0,2,3,5,6},{0,3,5,6},{0,3,6}}",
            "{0}",
            "{0,1}",
            "{0,1,3,4}",
        },
        input_symbols={"R", "U", "D", "L"},
        transitions={
            "{0}": {"R": "{0}", "U": "{0}", "D": "{0}", "L": "{0,1}"},
            "{0,1}": {"R": "{0}", "U": "{0,2}", "D": "{0}", "L": "{0,1}"},
            "{0,2}": {"R": "{0,3}", "U": "{0}", "D": "{0}", "L": "{0,1}"},
            "{0,3}": {"R": "{0,3}", "U": "{0,3,5}", "D": "{0,3}", "L": "{0,1,3,4}"},
            "{0,3,5}": {
                "R": "{0,3}",
                "U": "{0,3,5}",
                "D": "{0,3}",
                "L": "{{0,1,3,4,6},{0,2,3,5,6},{0,3,5,6},{0,3,6}}",
            },
            "{0,1,3,4}": {
                "R": "{0,3}",
                "U": "{{0,1,3,4,6},{0,2,3,5,6},{0,3,5,6},{0,3,6}}",
                "D": "{0,3}",
                "L": "{0,1,3,4}",
            },
            "{{0,1,3,4,6},{0,2,3,5,6},{0,3,5,6},{0,3,6}}": {
                "R": "{{0,1,3,4,6},{0,2,3,5,6},{0,3,5,6},{0,3,6}}",
                "U": "{{0,1,3,4,6},{0,2,3,5,6},{0,3,5,6},{0,3,6}}",
                "D": "{{0,1,3,4,6},{0,2,3,5,6},{0,3,5,6},{0,3,6}}",
                "L": "{{0,1,3,4,6},{0,2,3,5,6},{0,3,5,6},{0,3,6}}",
            },
        },
        initial_state="{0}",
        final_states={"{{0,1,3,4,6},{0,2,3,5,6},{0,3,5,6},{0,3,6}}"},
    )


def test_dfa_name_reset():
    assert PinWords.dfa_name_reset(PinWords.make_dfa_for_pinword("1UR2")) == DFA(
        states={
            "{0,1}",
            "{0,4,5}",
            "{{0,2,4},{0,4}}",
            "{0,2}",
            "{0,1,3}",
            "{{0,1,3,4,6},{0,1,4,6}}",
            "{0}",
            "{{0,1,3,4,6,7},{0,1,4,6,7},{0,2,4,7},{0,4,5,7},{0,4,7}}",
        },
        input_symbols={"L", "D", "U", "R"},
        transitions={
            "{0}": {"L": "{0}", "D": "{0}", "U": "{0,1}", "R": "{0}"},
            "{0,1}": {"L": "{0}", "D": "{0}", "U": "{0,1}", "R": "{0,2}"},
            "{0,2}": {"L": "{0}", "D": "{0}", "U": "{0,1,3}", "R": "{0}"},
            "{0,1,3}": {"L": "{0}", "D": "{0}", "U": "{0,1}", "R": "{{0,2,4},{0,4}}"},
            "{0,4,5}": {
                "L": "{0,4,5}",
                "D": "{{0,2,4},{0,4}}",
                "U": "{{0,1,3,4,6,7},{0,1,4,6,7},{0,2,4,7},{0,4,5,7},{0,4,7}}",
                "R": "{{0,2,4},{0,4}}",
            },
            "{{0,1,3,4,6},{0,1,4,6}}": {
                "L": "{{0,1,3,4,6,7},{0,1,4,6,7},{0,2,4,7},{0,4,5,7},{0,4,7}}",
                "D": "{{0,2,4},{0,4}}",
                "U": "{{0,1,3,4,6},{0,1,4,6}}",
                "R": "{{0,2,4},{0,4}}",
            },
            "{{0,2,4},{0,4}}": {
                "L": "{0,4,5}",
                "D": "{{0,2,4},{0,4}}",
                "U": "{{0,1,3,4,6},{0,1,4,6}}",
                "R": "{{0,2,4},{0,4}}",
            },
            "{{0,1,3,4,6,7},{0,1,4,6,7},{0,2,4,7},{0,4,5,7},{0,4,7}}": {
                "L": "{{0,1,3,4,6,7},{0,1,4,6,7},{0,2,4,7},{0,4,5,7},{0,4,7}}",
                "D": "{{0,1,3,4,6,7},{0,1,4,6,7},{0,2,4,7},{0,4,5,7},{0,4,7}}",
                "U": "{{0,1,3,4,6,7},{0,1,4,6,7},{0,2,4,7},{0,4,5,7},{0,4,7}}",
                "R": "{{0,1,3,4,6,7},{0,1,4,6,7},{0,2,4,7},{0,4,5,7},{0,4,7}}",
            },
        },
        initial_state="{0}",
        final_states={"{{0,1,3,4,6,7},{0,1,4,6,7},{0,2,4,7},{0,4,5,7},{0,4,7}}"},
    )
    assert PinWords.dfa_name_reset(PinWords.make_dfa_for_pinword("3D23")) == DFA(
        states={
            "{0,1}",
            "{{0,1,3,6,8,9},{0,2,3,4,6,7,9},{0,3,4,6,7,9},{0,3,5,6,9},{0,3,6,9}}",
            "{{0,1,3},{0,3}}",
            "{{0,2,3,4},{0,3,4}}",
            "{0,1,3,6,8}",
            "{0,2}",
            "{0,3,4,6,7}",
            "{0}",
            "{{0,3,4,6},{0,3,5,6},{0,3,6}}",
            "{0,3,5}",
        },
        input_symbols={"L", "D", "U", "R"},
        transitions={
            "{0}": {"L": "{0}", "D": "{0,1}", "U": "{0}", "R": "{0}"},
            "{0,1}": {"L": "{0,2}", "D": "{0,1}", "U": "{0}", "R": "{0}"},
            "{0,2}": {"L": "{0}", "D": "{{0,1,3},{0,3}}", "U": "{0}", "R": "{0}"},
            "{0,3,5}": {
                "L": "{{0,3,4,6},{0,3,5,6},{0,3,6}}",
                "D": "{{0,1,3},{0,3}}",
                "U": "{0,3,5}",
                "R": "{{0,1,3},{0,3}}",
            },
            "{0,3,4,6,7}": {
                "L": "{0,3,4,6,7}",
                "D": (
                    "{{0,1,3,6,8,9},{0,2,3,4,6,7,9},"
                    "{0,3,4,6,7,9},{0,3,5,6,9},{0,3,6,9}}"
                ),
                "U": "{{0,3,4,6},{0,3,5,6},{0,3,6}}",
                "R": "{{0,3,4,6},{0,3,5,6},{0,3,6}}",
            },
            "{0,1,3,6,8}": {
                "L": (
                    "{{0,1,3,6,8,9},{0,2,3,4,6,7,9},"
                    "{0,3,4,6,7,9},{0,3,5,6,9},{0,3,6,9}}"
                ),
                "D": "{0,1,3,6,8}",
                "U": "{{0,3,4,6},{0,3,5,6},{0,3,6}}",
                "R": "{{0,3,4,6},{0,3,5,6},{0,3,6}}",
            },
            "{{0,2,3,4},{0,3,4}}": {
                "L": "{{0,2,3,4},{0,3,4}}",
                "D": "{{0,1,3},{0,3}}",
                "U": "{{0,3,4,6},{0,3,5,6},{0,3,6}}",
                "R": "{{0,1,3},{0,3}}",
            },
            "{{0,1,3,6,8,9},{0,2,3,4,6,7,9},{0,3,4,6,7,9},{0,3,5,6,9},{0,3,6,9}}": {
                "L": (
                    "{{0,1,3,6,8,9},{0,2,3,4,6,7,9},"
                    "{0,3,4,6,7,9},{0,3,5,6,9},{0,3,6,9}}"
                ),
                "D": (
                    "{{0,1,3,6,8,9},{0,2,3,4,6,7,9},"
                    "{0,3,4,6,7,9},{0,3,5,6,9},{0,3,6,9}}"
                ),
                "U": (
                    "{{0,1,3,6,8,9},{0,2,3,4,6,7,9},"
                    "{0,3,4,6,7,9},{0,3,5,6,9},{0,3,6,9}}"
                ),
                "R": (
                    "{{0,1,3,6,8,9},{0,2,3,4,6,7,9},"
                    "{0,3,4,6,7,9},{0,3,5,6,9},{0,3,6,9}}"
                ),
            },
            "{{0,3,4,6},{0,3,5,6},{0,3,6}}": {
                "L": "{0,3,4,6,7}",
                "D": "{0,1,3,6,8}",
                "U": "{{0,3,4,6},{0,3,5,6},{0,3,6}}",
                "R": "{{0,3,4,6},{0,3,5,6},{0,3,6}}",
            },
            "{{0,1,3},{0,3}}": {
                "L": "{{0,2,3,4},{0,3,4}}",
                "D": "{{0,1,3},{0,3}}",
                "U": "{0,3,5}",
                "R": "{{0,1,3},{0,3}}",
            },
        },
        initial_state="{0}",
        final_states={
            "{{0,1,3,6,8,9},{0,2,3,4,6,7,9},{0,3,4,6,7,9},{0,3,5,6,9},{0,3,6,9}}"
        },
    )
    assert PinWords.dfa_name_reset(PinWords.make_dfa_for_pinword("141R4")) == DFA(
        states={
            "{0,1}",
            "{0,2,3,6,8}",
            "{0}",
            "{0,1,3,4,6,7}",
            "{{0,1,3,4,6,7,9},{0,2,3,6,8,9},{0,2,3,6,9},{0,3,6,9}}",
            "{{0,1,3},{0,2,3},{0,3}}",
            "{{0,1,3,4,6},{0,2,3,6},{0,3,5,6},{0,3,6}}",
            "{0,1,3,4}",
            "{0,2}",
            (
                "{{0,1,10,12,3,4,6,7,9},{0,11,12,3,5,6,9},"
                "{0,12,2,3,6,8,9},{0,12,2,3,6,9},{0,12,3,6,9}}"
            ),
            "{0,1,10,3,4,6,7,9}",
            "{0,3,5}",
            "{0,11,3,5,6,9}",
        },
        input_symbols={"L", "D", "U", "R"},
        transitions={
            "{0}": {"L": "{0}", "D": "{0}", "U": "{0,2}", "R": "{0,1}"},
            "{0,2}": {
                "L": "{0}",
                "D": "{0}",
                "U": "{0,2}",
                "R": "{{0,1,3},{0,2,3},{0,3}}",
            },
            "{0,1}": {
                "L": "{0}",
                "D": "{0}",
                "U": "{{0,1,3},{0,2,3},{0,3}}",
                "R": "{0,1}",
            },
            "{0,3,5}": {
                "L": "{{0,1,3},{0,2,3},{0,3}}",
                "D": "{0,3,5}",
                "U": "{{0,1,3},{0,2,3},{0,3}}",
                "R": "{{0,1,3,4,6},{0,2,3,6},{0,3,5,6},{0,3,6}}",
            },
            "{0,1,3,4}": {
                "L": "{{0,1,3},{0,2,3},{0,3}}",
                "D": "{{0,1,3,4,6},{0,2,3,6},{0,3,5,6},{0,3,6}}",
                "U": "{{0,1,3},{0,2,3},{0,3}}",
                "R": "{0,1,3,4}",
            },
            "{0,1,3,4,6,7}": {
                "L": "{{0,1,3,4,6},{0,2,3,6},{0,3,5,6},{0,3,6}}",
                "D": "{{0,1,3,4,6},{0,2,3,6},{0,3,5,6},{0,3,6}}",
                "U": "{0,2,3,6,8}",
                "R": "{0,1,3,4,6,7}",
            },
            "{0,2,3,6,8}": {
                "L": "{{0,1,3,4,6},{0,2,3,6},{0,3,5,6},{0,3,6}}",
                "D": "{{0,1,3,4,6},{0,2,3,6},{0,3,5,6},{0,3,6}}",
                "U": "{{0,1,3,4,6},{0,2,3,6},{0,3,5,6},{0,3,6}}",
                "R": "{{0,1,3,4,6,7,9},{0,2,3,6,8,9},{0,2,3,6,9},{0,3,6,9}}",
            },
            "{0,11,3,5,6,9}": {
                "L": "{{0,1,3,4,6,7,9},{0,2,3,6,8,9},{0,2,3,6,9},{0,3,6,9}}",
                "D": "{0,11,3,5,6,9}",
                "U": "{{0,1,3,4,6,7,9},{0,2,3,6,8,9},{0,2,3,6,9},{0,3,6,9}}",
                "R": (
                    "{{0,1,10,12,3,4,6,7,9},{0,11,12,3,5,6,9},"
                    "{0,12,2,3,6,8,9},{0,12,2,3,6,9},{0,12,3,6,9}}"
                ),
            },
            "{0,1,10,3,4,6,7,9}": {
                "L": "{{0,1,3,4,6,7,9},{0,2,3,6,8,9},{0,2,3,6,9},{0,3,6,9}}",
                "D": (
                    "{{0,1,10,12,3,4,6,7,9},{0,11,12,3,5,6,9},"
                    "{0,12,2,3,6,8,9},{0,12,2,3,6,9},{0,12,3,6,9}}"
                ),
                "U": "{{0,1,3,4,6,7,9},{0,2,3,6,8,9},{0,2,3,6,9},{0,3,6,9}}",
                "R": "{0,1,10,3,4,6,7,9}",
            },
            "{{0,1,3},{0,2,3},{0,3}}": {
                "L": "{{0,1,3},{0,2,3},{0,3}}",
                "D": "{0,3,5}",
                "U": "{{0,1,3},{0,2,3},{0,3}}",
                "R": "{0,1,3,4}",
            },
            "{{0,1,3,4,6},{0,2,3,6},{0,3,5,6},{0,3,6}}": {
                "L": "{{0,1,3,4,6},{0,2,3,6},{0,3,5,6},{0,3,6}}",
                "D": "{{0,1,3,4,6},{0,2,3,6},{0,3,5,6},{0,3,6}}",
                "U": "{{0,1,3,4,6},{0,2,3,6},{0,3,5,6},{0,3,6}}",
                "R": "{0,1,3,4,6,7}",
            },
            (
                "{{0,1,10,12,3,4,6,7,9},{0,11,12,3,5,6,9},"
                "{0,12,2,3,6,8,9},{0,12,2,3,6,9},{0,12,3,6,9}}"
            ): {
                "L": (
                    "{{0,1,10,12,3,4,6,7,9},{0,11,12,3,5,6,9},"
                    "{0,12,2,3,6,8,9},{0,12,2,3,6,9},{0,12,3,6,9}}"
                ),
                "D": (
                    "{{0,1,10,12,3,4,6,7,9},{0,11,12,3,5,6,9},"
                    "{0,12,2,3,6,8,9},{0,12,2,3,6,9},{0,12,3,6,9}}"
                ),
                "U": (
                    "{{0,1,10,12,3,4,6,7,9},{0,11,12,3,5,6,9},"
                    "{0,12,2,3,6,8,9},{0,12,2,3,6,9},{0,12,3,6,9}}"
                ),
                "R": (
                    "{{0,1,10,12,3,4,6,7,9},{0,11,12,3,5,6,9},"
                    "{0,12,2,3,6,8,9},{0,12,2,3,6,9},{0,12,3,6,9}}"
                ),
            },
            "{{0,1,3,4,6,7,9},{0,2,3,6,8,9},{0,2,3,6,9},{0,3,6,9}}": {
                "L": "{{0,1,3,4,6,7,9},{0,2,3,6,8,9},{0,2,3,6,9},{0,3,6,9}}",
                "D": "{0,11,3,5,6,9}",
                "U": "{{0,1,3,4,6,7,9},{0,2,3,6,8,9},{0,2,3,6,9},{0,3,6,9}}",
                "R": "{0,1,10,3,4,6,7,9}",
            },
        },
        initial_state="{0}",
        final_states={
            (
                "{{0,1,10,12,3,4,6,7,9},{0,11,12,3,5,6,9},{0,12,2,3,6,8,9},"
                "{0,12,2,3,6,9},{0,12,3,6,9}}"
            )
        },
    )
    assert PinWords.dfa_name_reset(PinWords.make_dfa_for_pinword("1R")) == DFA(
        states={"{{0,1,3},{0,2,3},{0,3}}", "{0,1}", "{0}", "{0,2}"},
        input_symbols={"L", "D", "U", "R"},
        transitions={
            "{0}": {"L": "{0}", "D": "{0}", "U": "{0}", "R": "{0,1}"},
            "{0,1}": {"L": "{0}", "D": "{0}", "U": "{0,2}", "R": "{0,1}"},
            "{0,2}": {
                "L": "{0}",
                "D": "{0}",
                "U": "{0}",
                "R": "{{0,1,3},{0,2,3},{0,3}}",
            },
            "{{0,1,3},{0,2,3},{0,3}}": {
                "L": "{{0,1,3},{0,2,3},{0,3}}",
                "D": "{{0,1,3},{0,2,3},{0,3}}",
                "U": "{{0,1,3},{0,2,3},{0,3}}",
                "R": "{{0,1,3},{0,2,3},{0,3}}",
            },
        },
        initial_state="{0}",
        final_states={"{{0,1,3},{0,2,3},{0,3}}"},
    )
    assert PinWords.dfa_name_reset(PinWords.make_dfa_for_pinword("2L")) == DFA(
        states={"{{0,1,3},{0,2,3},{0,3}}", "{0,1}", "{0}", "{0,2}"},
        input_symbols={"L", "D", "U", "R"},
        transitions={
            "{0}": {"L": "{0,1}", "D": "{0}", "U": "{0}", "R": "{0}"},
            "{0,1}": {"L": "{0,1}", "D": "{0}", "U": "{0,2}", "R": "{0}"},
            "{0,2}": {
                "L": "{{0,1,3},{0,2,3},{0,3}}",
                "D": "{0}",
                "U": "{0}",
                "R": "{0}",
            },
            "{{0,1,3},{0,2,3},{0,3}}": {
                "L": "{{0,1,3},{0,2,3},{0,3}}",
                "D": "{{0,1,3},{0,2,3},{0,3}}",
                "U": "{{0,1,3},{0,2,3},{0,3}}",
                "R": "{{0,1,3},{0,2,3},{0,3}}",
            },
        },
        initial_state="{0}",
        final_states={"{{0,1,3},{0,2,3},{0,3}}"},
    )
    assert PinWords.dfa_name_reset(PinWords.make_dfa_for_pinword("4L2")) == DFA(
        states={
            "{0,1}",
            "{0,2}",
            "{0,3,4}",
            "{0,3,5}",
            "{{0,1,3},{0,2,3},{0,3}}",
            "{0}",
            "{{0,1,3,6},{0,2,3,6},{0,3,4,6},{0,3,5,6},{0,3,6}}",
        },
        input_symbols={"L", "D", "U", "R"},
        transitions={
            "{0}": {"L": "{0}", "D": "{0}", "U": "{0}", "R": "{0,1}"},
            "{0,1}": {"L": "{0}", "D": "{0,2}", "U": "{0}", "R": "{0,1}"},
            "{0,2}": {
                "L": "{{0,1,3},{0,2,3},{0,3}}",
                "D": "{0}",
                "U": "{0}",
                "R": "{0,1}",
            },
            "{0,3,4}": {
                "L": "{0,3,4}",
                "D": "{{0,1,3},{0,2,3},{0,3}}",
                "U": "{{0,1,3,6},{0,2,3,6},{0,3,4,6},{0,3,5,6},{0,3,6}}",
                "R": "{{0,1,3},{0,2,3},{0,3}}",
            },
            "{0,3,5}": {
                "L": "{{0,1,3,6},{0,2,3,6},{0,3,4,6},{0,3,5,6},{0,3,6}}",
                "D": "{{0,1,3},{0,2,3},{0,3}}",
                "U": "{0,3,5}",
                "R": "{{0,1,3},{0,2,3},{0,3}}",
            },
            "{{0,1,3},{0,2,3},{0,3}}": {
                "L": "{0,3,4}",
                "D": "{{0,1,3},{0,2,3},{0,3}}",
                "U": "{0,3,5}",
                "R": "{{0,1,3},{0,2,3},{0,3}}",
            },
            "{{0,1,3,6},{0,2,3,6},{0,3,4,6},{0,3,5,6},{0,3,6}}": {
                "L": "{{0,1,3,6},{0,2,3,6},{0,3,4,6},{0,3,5,6},{0,3,6}}",
                "D": "{{0,1,3,6},{0,2,3,6},{0,3,4,6},{0,3,5,6},{0,3,6}}",
                "U": "{{0,1,3,6},{0,2,3,6},{0,3,4,6},{0,3,5,6},{0,3,6}}",
                "R": "{{0,1,3,6},{0,2,3,6},{0,3,4,6},{0,3,5,6},{0,3,6}}",
            },
        },
        initial_state="{0}",
        final_states={"{{0,1,3,6},{0,2,3,6},{0,3,4,6},{0,3,5,6},{0,3,6}}"},
    )
    assert PinWords.dfa_name_reset(PinWords.make_dfa_for_pinword("3R")) == DFA(
        states={"{{0,1,3},{0,2,3},{0,3}}", "{0,1}", "{0}", "{0,2}"},
        input_symbols={"L", "D", "U", "R"},
        transitions={
            "{0}": {"L": "{0,1}", "D": "{0}", "U": "{0}", "R": "{0}"},
            "{0,1}": {"L": "{0,1}", "D": "{0,2}", "U": "{0}", "R": "{0}"},
            "{0,2}": {
                "L": "{0,1}",
                "D": "{0}",
                "U": "{0}",
                "R": "{{0,1,3},{0,2,3},{0,3}}",
            },
            "{{0,1,3},{0,2,3},{0,3}}": {
                "L": "{{0,1,3},{0,2,3},{0,3}}",
                "D": "{{0,1,3},{0,2,3},{0,3}}",
                "U": "{{0,1,3},{0,2,3},{0,3}}",
                "R": "{{0,1,3},{0,2,3},{0,3}}",
            },
        },
        initial_state="{0}",
        final_states={"{{0,1,3},{0,2,3},{0,3}}"},
    )
    assert PinWords.dfa_name_reset(PinWords.make_dfa_for_pinword("41R11")) == DFA(
        states={
            "{{0,3,5,6,8},{0,3,6,8}}",
            "{0,1}",
            "{0}",
            "{0,1,3,4,6,7}",
            "{{0,1,3},{0,2,3},{0,3}}",
            "{{0,1,3,4,6},{0,2,3,6},{0,3,6}}",
            "{{0,1,3,4,6,7,9},{0,2,3,6,9},{0,3,5,6,8,9},{0,3,6,9}}",
            "{0,1,3,4}",
            "{0,2}",
            "{{0,11,3,5,6,8,9},{0,11,3,6,8,9}}",
            (
                "{{0,1,10,12,3,4,6,7,9},{0,11,12,3,5,6,8,9},{0,11,12,3,6,8,9},"
                "{0,12,2,3,6,9},{0,12,3,6,9}}"
            ),
            "{0,1,10,3,4,6,7,9}",
            "{0,3,5}",
        },
        input_symbols={"L", "D", "U", "R"},
        transitions={
            "{0}": {"L": "{0}", "D": "{0,2}", "U": "{0}", "R": "{0,1}"},
            "{0,2}": {
                "L": "{0}",
                "D": "{0,2}",
                "U": "{0}",
                "R": "{{0,1,3},{0,2,3},{0,3}}",
            },
            "{0,1}": {
                "L": "{0}",
                "D": "{{0,1,3},{0,2,3},{0,3}}",
                "U": "{0}",
                "R": "{0,1}",
            },
            "{0,1,3,4}": {
                "L": "{{0,1,3},{0,2,3},{0,3}}",
                "D": "{{0,1,3},{0,2,3},{0,3}}",
                "U": "{0,3,5}",
                "R": "{0,1,3,4}",
            },
            "{0,3,5}": {
                "L": "{{0,1,3},{0,2,3},{0,3}}",
                "D": "{{0,1,3},{0,2,3},{0,3}}",
                "U": "{{0,1,3},{0,2,3},{0,3}}",
                "R": "{{0,1,3,4,6},{0,2,3,6},{0,3,6}}",
            },
            "{0,1,3,4,6,7}": {
                "L": "{{0,1,3,4,6},{0,2,3,6},{0,3,6}}",
                "D": "{{0,1,3,4,6},{0,2,3,6},{0,3,6}}",
                "U": "{{0,1,3,4,6,7,9},{0,2,3,6,9},{0,3,5,6,8,9},{0,3,6,9}}",
                "R": "{0,1,3,4,6,7}",
            },
            "{0,1,10,3,4,6,7,9}": {
                "L": "{{0,1,3,4,6,7,9},{0,2,3,6,9},{0,3,5,6,8,9},{0,3,6,9}}",
                "D": "{{0,1,3,4,6,7,9},{0,2,3,6,9},{0,3,5,6,8,9},{0,3,6,9}}",
                "U": (
                    "{{0,1,10,12,3,4,6,7,9},{0,11,12,3,5,6,8,9},"
                    "{0,11,12,3,6,8,9},{0,12,2,3,6,9},{0,12,3,6,9}}"
                ),
                "R": "{0,1,10,3,4,6,7,9}",
            },
            "{{0,1,3},{0,2,3},{0,3}}": {
                "L": "{{0,1,3},{0,2,3},{0,3}}",
                "D": "{{0,1,3},{0,2,3},{0,3}}",
                "U": "{{0,1,3},{0,2,3},{0,3}}",
                "R": "{0,1,3,4}",
            },
            "{{0,3,5,6,8},{0,3,6,8}}": {
                "L": "{{0,1,3,4,6},{0,2,3,6},{0,3,6}}",
                "D": "{{0,1,3,4,6},{0,2,3,6},{0,3,6}}",
                "U": "{{0,3,5,6,8},{0,3,6,8}}",
                "R": "{{0,1,3,4,6,7,9},{0,2,3,6,9},{0,3,5,6,8,9},{0,3,6,9}}",
            },
            "{{0,1,3,4,6},{0,2,3,6},{0,3,6}}": {
                "L": "{{0,1,3,4,6},{0,2,3,6},{0,3,6}}",
                "D": "{{0,1,3,4,6},{0,2,3,6},{0,3,6}}",
                "U": "{{0,3,5,6,8},{0,3,6,8}}",
                "R": "{0,1,3,4,6,7}",
            },
            (
                "{{0,1,10,12,3,4,6,7,9},{0,11,12,3,5,6,8,9},{0,11,12,3,6,8,9},"
                "{0,12,2,3,6,9},{0,12,3,6,9}}"
            ): {
                "L": (
                    "{{0,1,10,12,3,4,6,7,9},{0,11,12,3,5,6,8,9},"
                    "{0,11,12,3,6,8,9},{0,12,2,3,6,9},{0,12,3,6,9}}"
                ),
                "D": (
                    "{{0,1,10,12,3,4,6,7,9},{0,11,12,3,5,6,8,9},"
                    "{0,11,12,3,6,8,9},{0,12,2,3,6,9},{0,12,3,6,9}}"
                ),
                "U": (
                    "{{0,1,10,12,3,4,6,7,9},{0,11,12,3,5,6,8,9},"
                    "{0,11,12,3,6,8,9},{0,12,2,3,6,9},{0,12,3,6,9}}"
                ),
                "R": (
                    "{{0,1,10,12,3,4,6,7,9},{0,11,12,3,5,6,8,9},"
                    "{0,11,12,3,6,8,9},{0,12,2,3,6,9},{0,12,3,6,9}}"
                ),
            },
            "{{0,1,3,4,6,7,9},{0,2,3,6,9},{0,3,5,6,8,9},{0,3,6,9}}": {
                "L": "{{0,1,3,4,6,7,9},{0,2,3,6,9},{0,3,5,6,8,9},{0,3,6,9}}",
                "D": "{{0,1,3,4,6,7,9},{0,2,3,6,9},{0,3,5,6,8,9},{0,3,6,9}}",
                "U": "{{0,11,3,5,6,8,9},{0,11,3,6,8,9}}",
                "R": "{0,1,10,3,4,6,7,9}",
            },
            "{{0,11,3,5,6,8,9},{0,11,3,6,8,9}}": {
                "L": "{{0,1,3,4,6,7,9},{0,2,3,6,9},{0,3,5,6,8,9},{0,3,6,9}}",
                "D": "{{0,1,3,4,6,7,9},{0,2,3,6,9},{0,3,5,6,8,9},{0,3,6,9}}",
                "U": "{{0,11,3,5,6,8,9},{0,11,3,6,8,9}}",
                "R": (
                    "{{0,1,10,12,3,4,6,7,9},{0,11,12,3,5,6,8,9},"
                    "{0,11,12,3,6,8,9},{0,12,2,3,6,9},{0,12,3,6,9}}"
                ),
            },
        },
        initial_state="{0}",
        final_states={
            (
                "{{0,1,10,12,3,4,6,7,9},{0,11,12,3,5,6,8,9},{0,11,12,3,6,8,9},"
                "{0,12,2,3,6,9},{0,12,3,6,9}}"
            )
        },
    )
    assert PinWords.dfa_name_reset(PinWords.make_dfa_for_pinword("4L41D4")) == DFA(
        states={
            "{0,3,6,7}",
            "{0,1}",
            "{{0,1,3,4,6},{0,2,3,5,6},{0,3,5,6},{0,3,6}}",
            "{0,1,3,4,6,8}",
            "{{0,2,3,5,6,9},{0,3,6,7,9},{0,3,6,9}}",
            (
                "{{0,1,10,12,3,4,6,8,9},{0,1,10,12,3,4,6,9},{0,11,12,2,3,5,6,9},"
                "{0,11,12,3,5,6,9},{0,12,3,6,7,9},{0,12,3,6,9}}"
            ),
            "{0,3}",
            "{{0,1,10,3,4,6,8,9},{0,1,10,3,4,6,9}}",
            "{0,1,3,4}",
            "{0,2}",
            "{0}",
            "{0,3,5}",
            "{0,11,3,5,6,9}",
        },
        input_symbols={"L", "D", "U", "R"},
        transitions={
            "{0}": {"L": "{0}", "D": "{0}", "U": "{0}", "R": "{0,1}"},
            "{0,1}": {"L": "{0}", "D": "{0,2}", "U": "{0}", "R": "{0,1}"},
            "{0,2}": {"L": "{0,3}", "D": "{0}", "U": "{0}", "R": "{0,1}"},
            "{0,3}": {"L": "{0,3}", "D": "{0,3,5}", "U": "{0,3}", "R": "{0,1,3,4}"},
            "{0,3,5}": {
                "L": "{0,3}",
                "D": "{0,3,5}",
                "U": "{0,3}",
                "R": "{{0,1,3,4,6},{0,2,3,5,6},{0,3,5,6},{0,3,6}}",
            },
            "{0,1,3,4}": {
                "L": "{0,3}",
                "D": "{{0,1,3,4,6},{0,2,3,5,6},{0,3,5,6},{0,3,6}}",
                "U": "{0,3}",
                "R": "{0,1,3,4}",
            },
            "{0,3,6,7}": {
                "L": "{{0,1,3,4,6},{0,2,3,5,6},{0,3,5,6},{0,3,6}}",
                "D": "{{0,1,3,4,6},{0,2,3,5,6},{0,3,5,6},{0,3,6}}",
                "U": "{0,3,6,7}",
                "R": "{0,1,3,4,6,8}",
            },
            "{0,1,3,4,6,8}": {
                "L": "{{0,1,3,4,6},{0,2,3,5,6},{0,3,5,6},{0,3,6}}",
                "D": "{{0,2,3,5,6,9},{0,3,6,7,9},{0,3,6,9}}",
                "U": "{0,3,6,7}",
                "R": "{{0,1,3,4,6},{0,2,3,5,6},{0,3,5,6},{0,3,6}}",
            },
            "{0,11,3,5,6,9}": {
                "L": "{{0,2,3,5,6,9},{0,3,6,7,9},{0,3,6,9}}",
                "D": "{0,11,3,5,6,9}",
                "U": "{{0,2,3,5,6,9},{0,3,6,7,9},{0,3,6,9}}",
                "R": (
                    "{{0,1,10,12,3,4,6,8,9},{0,1,10,12,3,4,6,9},{0,11,12,2,3,5,6,9},"
                    "{0,11,12,3,5,6,9},{0,12,3,6,7,9},{0,12,3,6,9}}"
                ),
            },
            "{{0,1,10,3,4,6,8,9},{0,1,10,3,4,6,9}}": {
                "L": "{{0,2,3,5,6,9},{0,3,6,7,9},{0,3,6,9}}",
                "D": (
                    "{{0,1,10,12,3,4,6,8,9},{0,1,10,12,3,4,6,9},{0,11,12,2,3,5,6,9},"
                    "{0,11,12,3,5,6,9},{0,12,3,6,7,9},{0,12,3,6,9}}"
                ),
                "U": "{{0,2,3,5,6,9},{0,3,6,7,9},{0,3,6,9}}",
                "R": "{{0,1,10,3,4,6,8,9},{0,1,10,3,4,6,9}}",
            },
            (
                "{{0,1,10,12,3,4,6,8,9},{0,1,10,12,3,4,6,9},{0,11,12,2,3,5,6,9},"
                "{0,11,12,3,5,6,9},{0,12,3,6,7,9},{0,12,3,6,9}}"
            ): {
                "L": (
                    "{{0,1,10,12,3,4,6,8,9},{0,1,10,12,3,4,6,9},{0,11,12,2,3,5,6,9},"
                    "{0,11,12,3,5,6,9},{0,12,3,6,7,9},{0,12,3,6,9}}"
                ),
                "D": (
                    "{{0,1,10,12,3,4,6,8,9},{0,1,10,12,3,4,6,9},{0,11,12,2,3,5,6,9},"
                    "{0,11,12,3,5,6,9},{0,12,3,6,7,9},{0,12,3,6,9}}"
                ),
                "U": (
                    "{{0,1,10,12,3,4,6,8,9},{0,1,10,12,3,4,6,9},{0,11,12,2,3,5,6,9},"
                    "{0,11,12,3,5,6,9},{0,12,3,6,7,9},{0,12,3,6,9}}"
                ),
                "R": (
                    "{{0,1,10,12,3,4,6,8,9},{0,1,10,12,3,4,6,9},{0,11,12,2,3,5,6,9},"
                    "{0,11,12,3,5,6,9},{0,12,3,6,7,9},{0,12,3,6,9}}"
                ),
            },
            "{{0,1,3,4,6},{0,2,3,5,6},{0,3,5,6},{0,3,6}}": {
                "L": "{{0,1,3,4,6},{0,2,3,5,6},{0,3,5,6},{0,3,6}}",
                "D": "{{0,1,3,4,6},{0,2,3,5,6},{0,3,5,6},{0,3,6}}",
                "U": "{0,3,6,7}",
                "R": "{{0,1,3,4,6},{0,2,3,5,6},{0,3,5,6},{0,3,6}}",
            },
            "{{0,2,3,5,6,9},{0,3,6,7,9},{0,3,6,9}}": {
                "L": "{{0,2,3,5,6,9},{0,3,6,7,9},{0,3,6,9}}",
                "D": "{0,11,3,5,6,9}",
                "U": "{{0,2,3,5,6,9},{0,3,6,7,9},{0,3,6,9}}",
                "R": "{{0,1,10,3,4,6,8,9},{0,1,10,3,4,6,9}}",
            },
        },
        initial_state="{0}",
        final_states={
            (
                "{{0,1,10,12,3,4,6,8,9},{0,1,10,12,3,4,6,9},{0,11,12,2,3,5,6,9},"
                "{0,11,12,3,5,6,9},{0,12,3,6,7,9},{0,12,3,6,9}}"
            )
        },
    )
    assert PinWords.dfa_name_reset(PinWords.make_dfa_for_pinword("4")) == DFA(
        states={"{{0,1,3},{0,2,3},{0,3}}", "{0,1}", "{0}", "{0,2}"},
        input_symbols={"L", "D", "U", "R"},
        transitions={
            "{0}": {"L": "{0}", "D": "{0,2}", "U": "{0}", "R": "{0,1}"},
            "{0,2}": {
                "L": "{0}",
                "D": "{0,2}",
                "U": "{0}",
                "R": "{{0,1,3},{0,2,3},{0,3}}",
            },
            "{0,1}": {
                "L": "{0}",
                "D": "{{0,1,3},{0,2,3},{0,3}}",
                "U": "{0}",
                "R": "{0,1}",
            },
            "{{0,1,3},{0,2,3},{0,3}}": {
                "L": "{{0,1,3},{0,2,3},{0,3}}",
                "D": "{{0,1,3},{0,2,3},{0,3}}",
                "U": "{{0,1,3},{0,2,3},{0,3}}",
                "R": "{{0,1,3},{0,2,3},{0,3}}",
            },
        },
        initial_state="{0}",
        final_states={"{{0,1,3},{0,2,3},{0,3}}"},
    )
    assert PinWords.dfa_name_reset(PinWords.make_dfa_for_pinword("1R")) == DFA(
        states={"{{0,1,3},{0,2,3},{0,3}}", "{0,1}", "{0}", "{0,2}"},
        input_symbols={"L", "D", "U", "R"},
        transitions={
            "{0}": {"L": "{0}", "D": "{0}", "U": "{0}", "R": "{0,1}"},
            "{0,1}": {"L": "{0}", "D": "{0}", "U": "{0,2}", "R": "{0,1}"},
            "{0,2}": {
                "L": "{0}",
                "D": "{0}",
                "U": "{0}",
                "R": "{{0,1,3},{0,2,3},{0,3}}",
            },
            "{{0,1,3},{0,2,3},{0,3}}": {
                "L": "{{0,1,3},{0,2,3},{0,3}}",
                "D": "{{0,1,3},{0,2,3},{0,3}}",
                "U": "{{0,1,3},{0,2,3},{0,3}}",
                "R": "{{0,1,3},{0,2,3},{0,3}}",
            },
        },
        initial_state="{0}",
        final_states={"{{0,1,3},{0,2,3},{0,3}}"},
    )
    assert PinWords.dfa_name_reset(PinWords.make_dfa_for_pinword("4L41D4")) == DFA(
        states={
            "{0,3,6,7}",
            "{0,1}",
            "{{0,1,3,4,6},{0,2,3,5,6},{0,3,5,6},{0,3,6}}",
            "{0,1,3,4,6,8}",
            "{{0,2,3,5,6,9},{0,3,6,7,9},{0,3,6,9}}",
            (
                "{{0,1,10,12,3,4,6,8,9},{0,1,10,12,3,4,6,9},{0,11,12,2,3,5,6,9},"
                "{0,11,12,3,5,6,9},{0,12,3,6,7,9},{0,12,3,6,9}}"
            ),
            "{0,3}",
            "{{0,1,10,3,4,6,8,9},{0,1,10,3,4,6,9}}",
            "{0,1,3,4}",
            "{0,2}",
            "{0}",
            "{0,3,5}",
            "{0,11,3,5,6,9}",
        },
        input_symbols={"L", "D", "U", "R"},
        transitions={
            "{0}": {"L": "{0}", "D": "{0}", "U": "{0}", "R": "{0,1}"},
            "{0,1}": {"L": "{0}", "D": "{0,2}", "U": "{0}", "R": "{0,1}"},
            "{0,2}": {"L": "{0,3}", "D": "{0}", "U": "{0}", "R": "{0,1}"},
            "{0,3}": {"L": "{0,3}", "D": "{0,3,5}", "U": "{0,3}", "R": "{0,1,3,4}"},
            "{0,3,5}": {
                "L": "{0,3}",
                "D": "{0,3,5}",
                "U": "{0,3}",
                "R": "{{0,1,3,4,6},{0,2,3,5,6},{0,3,5,6},{0,3,6}}",
            },
            "{0,1,3,4}": {
                "L": "{0,3}",
                "D": "{{0,1,3,4,6},{0,2,3,5,6},{0,3,5,6},{0,3,6}}",
                "U": "{0,3}",
                "R": "{0,1,3,4}",
            },
            "{0,3,6,7}": {
                "L": "{{0,1,3,4,6},{0,2,3,5,6},{0,3,5,6},{0,3,6}}",
                "D": "{{0,1,3,4,6},{0,2,3,5,6},{0,3,5,6},{0,3,6}}",
                "U": "{0,3,6,7}",
                "R": "{0,1,3,4,6,8}",
            },
            "{0,1,3,4,6,8}": {
                "L": "{{0,1,3,4,6},{0,2,3,5,6},{0,3,5,6},{0,3,6}}",
                "D": "{{0,2,3,5,6,9},{0,3,6,7,9},{0,3,6,9}}",
                "U": "{0,3,6,7}",
                "R": "{{0,1,3,4,6},{0,2,3,5,6},{0,3,5,6},{0,3,6}}",
            },
            "{0,11,3,5,6,9}": {
                "L": "{{0,2,3,5,6,9},{0,3,6,7,9},{0,3,6,9}}",
                "D": "{0,11,3,5,6,9}",
                "U": "{{0,2,3,5,6,9},{0,3,6,7,9},{0,3,6,9}}",
                "R": (
                    "{{0,1,10,12,3,4,6,8,9},{0,1,10,12,3,4,6,9},{0,11,12,2,3,5,6,9},"
                    "{0,11,12,3,5,6,9},{0,12,3,6,7,9},{0,12,3,6,9}}"
                ),
            },
            "{{0,1,10,3,4,6,8,9},{0,1,10,3,4,6,9}}": {
                "L": "{{0,2,3,5,6,9},{0,3,6,7,9},{0,3,6,9}}",
                "D": (
                    "{{0,1,10,12,3,4,6,8,9},{0,1,10,12,3,4,6,9},{0,11,12,2,3,5,6,9},"
                    "{0,11,12,3,5,6,9},{0,12,3,6,7,9},{0,12,3,6,9}}"
                ),
                "U": "{{0,2,3,5,6,9},{0,3,6,7,9},{0,3,6,9}}",
                "R": "{{0,1,10,3,4,6,8,9},{0,1,10,3,4,6,9}}",
            },
            (
                "{{0,1,10,12,3,4,6,8,9},{0,1,10,12,3,4,6,9},{0,11,12,2,3,5,6,9},"
                "{0,11,12,3,5,6,9},{0,12,3,6,7,9},{0,12,3,6,9}}"
            ): {
                "L": (
                    "{{0,1,10,12,3,4,6,8,9},{0,1,10,12,3,4,6,9},{0,11,12,2,3,5,6,9},"
                    "{0,11,12,3,5,6,9},{0,12,3,6,7,9},{0,12,3,6,9}}"
                ),
                "D": (
                    "{{0,1,10,12,3,4,6,8,9},{0,1,10,12,3,4,6,9},{0,11,12,2,3,5,6,9},"
                    "{0,11,12,3,5,6,9},{0,12,3,6,7,9},{0,12,3,6,9}}"
                ),
                "U": (
                    "{{0,1,10,12,3,4,6,8,9},{0,1,10,12,3,4,6,9},{0,11,12,2,3,5,6,9},"
                    "{0,11,12,3,5,6,9},{0,12,3,6,7,9},{0,12,3,6,9}}"
                ),
                "R": (
                    "{{0,1,10,12,3,4,6,8,9},{0,1,10,12,3,4,6,9},{0,11,12,2,3,5,6,9},"
                    "{0,11,12,3,5,6,9},{0,12,3,6,7,9},{0,12,3,6,9}}"
                ),
            },
            "{{0,1,3,4,6},{0,2,3,5,6},{0,3,5,6},{0,3,6}}": {
                "L": "{{0,1,3,4,6},{0,2,3,5,6},{0,3,5,6},{0,3,6}}",
                "D": "{{0,1,3,4,6},{0,2,3,5,6},{0,3,5,6},{0,3,6}}",
                "U": "{0,3,6,7}",
                "R": "{{0,1,3,4,6},{0,2,3,5,6},{0,3,5,6},{0,3,6}}",
            },
            "{{0,2,3,5,6,9},{0,3,6,7,9},{0,3,6,9}}": {
                "L": "{{0,2,3,5,6,9},{0,3,6,7,9},{0,3,6,9}}",
                "D": "{0,11,3,5,6,9}",
                "U": "{{0,2,3,5,6,9},{0,3,6,7,9},{0,3,6,9}}",
                "R": "{{0,1,10,3,4,6,8,9},{0,1,10,3,4,6,9}}",
            },
        },
        initial_state="{0}",
        final_states={
            (
                "{{0,1,10,12,3,4,6,8,9},{0,1,10,12,3,4,6,9},{0,11,12,2,3,5,6,9},"
                "{0,11,12,3,5,6,9},{0,12,3,6,7,9},{0,12,3,6,9}}"
            )
        },
    )
    assert PinWords.dfa_name_reset(PinWords.make_dfa_for_pinword("4")) == DFA(
        states={"{{0,1,3},{0,2,3},{0,3}}", "{0,1}", "{0}", "{0,2}"},
        input_symbols={"L", "D", "U", "R"},
        transitions={
            "{0}": {"L": "{0}", "D": "{0,2}", "U": "{0}", "R": "{0,1}"},
            "{0,2}": {
                "L": "{0}",
                "D": "{0,2}",
                "U": "{0}",
                "R": "{{0,1,3},{0,2,3},{0,3}}",
            },
            "{0,1}": {
                "L": "{0}",
                "D": "{{0,1,3},{0,2,3},{0,3}}",
                "U": "{0}",
                "R": "{0,1}",
            },
            "{{0,1,3},{0,2,3},{0,3}}": {
                "L": "{{0,1,3},{0,2,3},{0,3}}",
                "D": "{{0,1,3},{0,2,3},{0,3}}",
                "U": "{{0,1,3},{0,2,3},{0,3}}",
                "R": "{{0,1,3},{0,2,3},{0,3}}",
            },
        },
        initial_state="{0}",
        final_states={"{{0,1,3},{0,2,3},{0,3}}"},
    )
    assert PinWords.dfa_name_reset(PinWords.make_dfa_for_pinword("31")) == DFA(
        states={
            "{0,1}",
            "{0,2}",
            "{0,3,4}",
            "{{0,1,3,6},{0,2,3,6},{0,3,4,6},{0,3,5,6}}",
            "{{0,1,3},{0,2,3}}",
            "{0}",
            "{0,3,5}",
        },
        input_symbols={"L", "D", "U", "R"},
        transitions={
            "{0}": {"L": "{0,1}", "D": "{0,2}", "U": "{0}", "R": "{0}"},
            "{0,1}": {"L": "{0,1}", "D": "{{0,1,3},{0,2,3}}", "U": "{0}", "R": "{0}"},
            "{0,2}": {"L": "{{0,1,3},{0,2,3}}", "D": "{0,2}", "U": "{0}", "R": "{0}"},
            "{0,3,5}": {
                "L": "{{0,1,3},{0,2,3}}",
                "D": "{{0,1,3},{0,2,3}}",
                "U": "{0,3,5}",
                "R": "{{0,1,3,6},{0,2,3,6},{0,3,4,6},{0,3,5,6}}",
            },
            "{0,3,4}": {
                "L": "{{0,1,3},{0,2,3}}",
                "D": "{{0,1,3},{0,2,3}}",
                "U": "{{0,1,3,6},{0,2,3,6},{0,3,4,6},{0,3,5,6}}",
                "R": "{0,3,4}",
            },
            "{{0,1,3,6},{0,2,3,6},{0,3,4,6},{0,3,5,6}}": {
                "L": "{{0,1,3,6},{0,2,3,6},{0,3,4,6},{0,3,5,6}}",
                "D": "{{0,1,3,6},{0,2,3,6},{0,3,4,6},{0,3,5,6}}",
                "U": "{{0,1,3,6},{0,2,3,6},{0,3,4,6},{0,3,5,6}}",
                "R": "{{0,1,3,6},{0,2,3,6},{0,3,4,6},{0,3,5,6}}",
            },
            "{{0,1,3},{0,2,3}}": {
                "L": "{{0,1,3},{0,2,3}}",
                "D": "{{0,1,3},{0,2,3}}",
                "U": "{0,3,5}",
                "R": "{0,3,4}",
            },
        },
        initial_state="{0}",
        final_states={"{{0,1,3,6},{0,2,3,6},{0,3,4,6},{0,3,5,6}}"},
    )
    assert PinWords.dfa_name_reset(PinWords.make_dfa_for_pinword("1R")) == DFA(
        states={"{{0,1,3},{0,2,3},{0,3}}", "{0,1}", "{0}", "{0,2}"},
        input_symbols={"L", "D", "U", "R"},
        transitions={
            "{0}": {"L": "{0}", "D": "{0}", "U": "{0}", "R": "{0,1}"},
            "{0,1}": {"L": "{0}", "D": "{0}", "U": "{0,2}", "R": "{0,1}"},
            "{0,2}": {
                "L": "{0}",
                "D": "{0}",
                "U": "{0}",
                "R": "{{0,1,3},{0,2,3},{0,3}}",
            },
            "{{0,1,3},{0,2,3},{0,3}}": {
                "L": "{{0,1,3},{0,2,3},{0,3}}",
                "D": "{{0,1,3},{0,2,3},{0,3}}",
                "U": "{{0,1,3},{0,2,3},{0,3}}",
                "R": "{{0,1,3},{0,2,3},{0,3}}",
            },
        },
        initial_state="{0}",
        final_states={"{{0,1,3},{0,2,3},{0,3}}"},
    )


def test_make_dfa_for_perm():
    assert PinWords.make_dfa_for_perm(Perm.from_string("1032")) == DFA(
        states={
            "1",
            "11",
            "5",
            "16",
            "18",
            "10",
            "6",
            "12",
            "8",
            "0",
            "4",
            "2",
            "15",
            "13",
            "9",
            "14",
            "7",
            "3",
            "17",
        },
        input_symbols={"L", "R", "D", "U"},
        transitions={
            "0": {"L": "0", "R": "0", "D": "0", "U": "0"},
            "13": {"L": "13", "R": "1", "D": "4", "U": "18"},
            "18": {"L": "10", "R": "16", "D": "3", "U": "6"},
            "7": {"L": "14", "R": "18", "D": "7", "U": "11"},
            "15": {"L": "10", "R": "16", "D": "3", "U": "0"},
            "11": {"L": "18", "R": "14", "D": "7", "U": "11"},
            "2": {"L": "10", "R": "16", "D": "0", "U": "6"},
            "9": {"L": "10", "R": "0", "D": "3", "U": "6"},
            "14": {"L": "13", "R": "1", "D": "18", "U": "18"},
            "6": {"L": "10", "R": "15", "D": "3", "U": "6"},
            "3": {"L": "2", "R": "16", "D": "3", "U": "6"},
            "8": {"L": "0", "R": "16", "D": "3", "U": "6"},
            "16": {"L": "10", "R": "16", "D": "3", "U": "9"},
            "17": {"L": "1", "R": "13", "D": "17", "U": "17"},
            "4": {"L": "18", "R": "18", "D": "7", "U": "11"},
            "12": {"L": "12", "R": "12", "D": "11", "U": "7"},
            "10": {"L": "10", "R": "16", "D": "8", "U": "6"},
            "5": {"L": "12", "R": "12", "D": "17", "U": "17"},
            "1": {"L": "13", "R": "1", "D": "18", "U": "4"},
        },
        initial_state="5",
        final_states={"0"},
    )
    assert PinWords.make_dfa_for_perm(Perm.from_string("0312")) == DFA(
        states={
            "1",
            "23",
            "11",
            "5",
            "16",
            "18",
            "22",
            "10",
            "6",
            "27",
            "24",
            "12",
            "28",
            "8",
            "0",
            "26",
            "20",
            "21",
            "32",
            "4",
            "2",
            "34",
            "35",
            "19",
            "15",
            "29",
            "33",
            "37",
            "30",
            "13",
            "31",
            "36",
            "9",
            "14",
            "7",
            "3",
            "17",
            "25",
        },
        input_symbols={"L", "R", "D", "U"},
        transitions={
            "0": {"L": "0", "R": "30", "D": "25", "U": "1"},
            "13": {"L": "6", "R": "10", "D": "32", "U": "32"},
            "19": {"L": "32", "R": "33", "D": "34", "U": "12"},
            "34": {"L": "32", "R": "10", "D": "34", "U": "12"},
            "11": {"L": "5", "R": "23", "D": "11", "U": "11"},
            "27": {"L": "15", "R": "15", "D": "11", "U": "11"},
            "2": {"L": "13", "R": "33", "D": "34", "U": "12"},
            "9": {"L": "3", "R": "33", "D": "17", "U": "7"},
            "14": {"L": "0", "R": "30", "D": "2", "U": "31"},
            "6": {"L": "6", "R": "10", "D": "32", "U": "1"},
            "3": {"L": "0", "R": "30", "D": "2", "U": "8"},
            "1": {"L": "21", "R": "33", "D": "34", "U": "12"},
            "29": {"L": "33", "R": "14", "D": "17", "U": "7"},
            "25": {"L": "20", "R": "14", "D": "17", "U": "7"},
            "33": {"L": "6", "R": "10", "D": "19", "U": "8"},
            "16": {"L": "3", "R": "14", "D": "17", "U": "7"},
            "4": {"L": "0", "R": "30", "D": "35", "U": "31"},
            "28": {"L": "33", "R": "33", "D": "17", "U": "7"},
            "37": {"L": "14", "R": "33", "D": "36", "U": "18"},
            "5": {"L": "23", "R": "5", "D": "37", "U": "16"},
            "21": {"L": "6", "R": "10", "D": "32", "U": "8"},
            "18": {"L": "24", "R": "4", "D": "36", "U": "18"},
            "7": {"L": "10", "R": "4", "D": "17", "U": "7"},
            "22": {"L": "0", "R": "30", "D": "2", "U": "28"},
            "15": {"L": "15", "R": "15", "D": "18", "U": "36"},
            "26": {"L": "0", "R": "30", "D": "35", "U": "32"},
            "35": {"L": "20", "R": "33", "D": "17", "U": "7"},
            "30": {"L": "0", "R": "30", "D": "35", "U": "29"},
            "8": {"L": "21", "R": "32", "D": "34", "U": "12"},
            "20": {"L": "0", "R": "30", "D": "2", "U": "32"},
            "23": {"L": "23", "R": "5", "D": "16", "U": "37"},
            "24": {"L": "23", "R": "5", "D": "1", "U": "9"},
            "17": {"L": "26", "R": "22", "D": "17", "U": "7"},
            "12": {"L": "6", "R": "33", "D": "34", "U": "12"},
            "36": {"L": "4", "R": "24", "D": "36", "U": "18"},
            "10": {"L": "6", "R": "10", "D": "19", "U": "1"},
            "32": {"L": "32", "R": "32", "D": "32", "U": "32"},
            "31": {"L": "33", "R": "32", "D": "17", "U": "7"},
        },
        initial_state="27",
        final_states={"32"},
    )
    assert PinWords.make_dfa_for_perm(Perm.from_string("ε")) == DFA(
        states={"{0}"},
        input_symbols={"L", "R", "D", "U"},
        transitions={"{0}": {"L": "{0}", "R": "{0}", "D": "{0}", "U": "{0}"}},
        initial_state="{0}",
        final_states={"{0}"},
    )
    assert PinWords.make_dfa_for_perm(Perm.from_string("1320")) == DFA(
        states={
            "1",
            "23",
            "11",
            "5",
            "16",
            "18",
            "22",
            "10",
            "6",
            "27",
            "24",
            "12",
            "28",
            "8",
            "0",
            "26",
            "20",
            "21",
            "32",
            "4",
            "2",
            "34",
            "35",
            "19",
            "15",
            "29",
            "33",
            "37",
            "30",
            "13",
            "31",
            "36",
            "9",
            "14",
            "7",
            "3",
            "17",
            "25",
        },
        input_symbols={"L", "R", "D", "U"},
        transitions={
            "0": {"L": "34", "R": "26", "D": "3", "U": "0"},
            "13": {"L": "1", "R": "13", "D": "5", "U": "37"},
            "19": {"L": "17", "R": "27", "D": "10", "U": "21"},
            "34": {"L": "9", "R": "15", "D": "21", "U": "8"},
            "11": {"L": "28", "R": "26", "D": "3", "U": "0"},
            "27": {"L": "17", "R": "27", "D": "28", "U": "16"},
            "2": {"L": "9", "R": "15", "D": "30", "U": "8"},
            "9": {"L": "9", "R": "15", "D": "16", "U": "5"},
            "14": {"L": "24", "R": "28", "D": "29", "U": "16"},
            "6": {"L": "20", "R": "20", "D": "36", "U": "36"},
            "3": {"L": "23", "R": "31", "D": "3", "U": "0"},
            "29": {"L": "23", "R": "28", "D": "29", "U": "16"},
            "25": {"L": "9", "R": "15", "D": "21", "U": "28"},
            "33": {"L": "35", "R": "2", "D": "33", "U": "4"},
            "16": {"L": "23", "R": "7", "D": "29", "U": "16"},
            "4": {"L": "2", "R": "35", "D": "33", "U": "4"},
            "28": {"L": "28", "R": "28", "D": "28", "U": "28"},
            "37": {"L": "22", "R": "23", "D": "33", "U": "4"},
            "5": {"L": "25", "R": "26", "D": "3", "U": "0"},
            "21": {"L": "24", "R": "7", "D": "29", "U": "16"},
            "18": {"L": "9", "R": "15", "D": "21", "U": "21"},
            "7": {"L": "17", "R": "27", "D": "28", "U": "21"},
            "22": {"L": "9", "R": "15", "D": "30", "U": "21"},
            "15": {"L": "9", "R": "15", "D": "11", "U": "32"},
            "26": {"L": "9", "R": "15", "D": "12", "U": "21"},
            "35": {"L": "1", "R": "13", "D": "8", "U": "21"},
            "30": {"L": "24", "R": "19", "D": "3", "U": "0"},
            "8": {"L": "25", "R": "19", "D": "3", "U": "0"},
            "20": {"L": "20", "R": "20", "D": "4", "U": "33"},
            "23": {"L": "17", "R": "27", "D": "14", "U": "21"},
            "17": {"L": "17", "R": "27", "D": "29", "U": "21"},
            "24": {"L": "17", "R": "27", "D": "14", "U": "28"},
            "12": {"L": "28", "R": "19", "D": "3", "U": "0"},
            "36": {"L": "13", "R": "1", "D": "36", "U": "36"},
            "10": {"L": "28", "R": "28", "D": "29", "U": "16"},
            "32": {"L": "18", "R": "19", "D": "3", "U": "0"},
            "31": {"L": "9", "R": "15", "D": "12", "U": "8"},
            "1": {"L": "1", "R": "13", "D": "37", "U": "5"},
        },
        initial_state="6",
        final_states={"28"},
    )
    assert PinWords.make_dfa_for_perm(Perm.from_string("012")) == DFA(
        states={
            "12",
            "1",
            "9",
            "11",
            "8",
            "14",
            "7",
            "0",
            "5",
            "10",
            "13",
            "3",
            "6",
            "4",
            "2",
        },
        input_symbols={"L", "R", "D", "U"},
        transitions={
            "0": {"L": "12", "R": "1", "D": "0", "U": "5"},
            "13": {"L": "3", "R": "8", "D": "13", "U": "7"},
            "7": {"L": "11", "R": "3", "D": "13", "U": "7"},
            "11": {"L": "11", "R": "8", "D": "3", "U": "7"},
            "2": {"L": "2", "R": "6", "D": "12", "U": "10"},
            "9": {"L": "9", "R": "9", "D": "5", "U": "0"},
            "14": {"L": "9", "R": "9", "D": "4", "U": "4"},
            "6": {"L": "2", "R": "6", "D": "10", "U": "12"},
            "3": {"L": "3", "R": "3", "D": "3", "U": "3"},
            "8": {"L": "11", "R": "8", "D": "13", "U": "3"},
            "12": {"L": "11", "R": "8", "D": "13", "U": "7"},
            "4": {"L": "6", "R": "2", "D": "4", "U": "4"},
            "10": {"L": "12", "R": "12", "D": "0", "U": "5"},
            "5": {"L": "1", "R": "12", "D": "0", "U": "5"},
            "1": {"L": "2", "R": "6", "D": "12", "U": "12"},
        },
        initial_state="14",
        final_states={"3"},
    )


def test_make_dfa_for_basis_from_pinwords():
    assert PinWords.make_dfa_for_basis_from_pinwords([Perm((2, 0, 1, 3))]) == DFA(
        states={
            "22",
            "26",
            "24",
            "1",
            "12",
            "21",
            "28",
            "32",
            "11",
            "34",
            "18",
            "3",
            "35",
            "4",
            "6",
            "37",
            "19",
            "13",
            "10",
            "23",
            "20",
            "33",
            "5",
            "7",
            "0",
            "9",
            "31",
            "17",
            "2",
            "16",
            "27",
            "8",
            "29",
            "14",
            "25",
            "36",
            "30",
            "15",
        },
        input_symbols={"R", "D", "L", "U"},
        transitions={
            "28": {"R": "18", "D": "9", "L": "28", "U": "37"},
            "14": {"R": "36", "D": "32", "L": "17", "U": "1"},
            "26": {"R": "36", "D": "30", "L": "17", "U": "1"},
            "6": {"R": "33", "D": "6", "L": "8", "U": "5"},
            "7": {"R": "18", "D": "30", "L": "28", "U": "32"},
            "17": {"R": "36", "D": "32", "L": "17", "U": "35"},
            "25": {"R": "18", "D": "3", "L": "28", "U": "2"},
            "2": {"R": "13", "D": "6", "L": "30", "U": "5"},
            "9": {"R": "33", "D": "6", "L": "7", "U": "5"},
            "36": {"R": "36", "D": "37", "L": "17", "U": "30"},
            "12": {"R": "18", "D": "32", "L": "28", "U": "32"},
            "34": {"R": "34", "D": "19", "L": "34", "U": "4"},
            "33": {"R": "18", "D": "32", "L": "28", "U": "2"},
            "0": {"R": "34", "D": "29", "L": "34", "U": "29"},
            "3": {"R": "13", "D": "6", "L": "7", "U": "5"},
            "27": {"R": "16", "D": "9", "L": "27", "U": "15"},
            "1": {"R": "30", "D": "37", "L": "26", "U": "35"},
            "20": {"R": "13", "D": "6", "L": "12", "U": "5"},
            "22": {"R": "16", "D": "32", "L": "27", "U": "3"},
            "35": {"R": "30", "D": "37", "L": "14", "U": "35"},
            "31": {"R": "13", "D": "6", "L": "26", "U": "5"},
            "18": {"R": "18", "D": "20", "L": "28", "U": "23"},
            "19": {"R": "24", "D": "4", "L": "22", "U": "19"},
            "5": {"R": "25", "D": "6", "L": "14", "U": "5"},
            "32": {"R": "21", "D": "37", "L": "26", "U": "35"},
            "15": {"R": "14", "D": "4", "L": "11", "U": "19"},
            "11": {"R": "18", "D": "32", "L": "28", "U": "31"},
            "29": {"R": "27", "D": "29", "L": "16", "U": "29"},
            "24": {"R": "18", "D": "3", "L": "28", "U": "31"},
            "30": {"R": "30", "D": "30", "L": "30", "U": "30"},
            "8": {"R": "18", "D": "3", "L": "28", "U": "32"},
            "10": {"R": "30", "D": "37", "L": "30", "U": "35"},
            "21": {"R": "36", "D": "32", "L": "17", "U": "30"},
            "37": {"R": "21", "D": "37", "L": "14", "U": "35"},
            "23": {"R": "33", "D": "6", "L": "30", "U": "5"},
            "16": {"R": "16", "D": "15", "L": "27", "U": "9"},
            "4": {"R": "22", "D": "4", "L": "24", "U": "19"},
            "13": {"R": "36", "D": "32", "L": "17", "U": "10"},
        },
        initial_state="0",
        final_states={"30"},
    )
    assert PinWords.make_dfa_for_basis_from_pinwords(
        [Perm((1, 3, 0, 2)), Perm((1, 2, 0))]
    ) == DFA(
        states={
            "1",
            "12",
            "21",
            "11",
            "18",
            "3",
            "4",
            "6",
            "19",
            "13",
            "10",
            "20",
            "5",
            "7",
            "0",
            "9",
            "17",
            "2",
            "16",
            "8",
            "14",
            "15",
        },
        input_symbols={"R", "D", "L", "U"},
        transitions={
            "18": {"R": "13", "D": "20", "L": "13", "U": "20"},
            "19": {"R": "2", "D": "19", "L": "6", "U": "7"},
            "5": {"R": "21", "D": "19", "L": "8", "U": "7"},
            "15": {"R": "8", "D": "3", "L": "8", "U": "9"},
            "14": {"R": "17", "D": "8", "L": "16", "U": "1"},
            "11": {"R": "11", "D": "5", "L": "0", "U": "12"},
            "6": {"R": "17", "D": "15", "L": "16", "U": "1"},
            "7": {"R": "6", "D": "19", "L": "2", "U": "7"},
            "1": {"R": "10", "D": "3", "L": "8", "U": "9"},
            "8": {"R": "8", "D": "8", "L": "8", "U": "8"},
            "17": {"R": "17", "D": "8", "L": "16", "U": "12"},
            "10": {"R": "17", "D": "8", "L": "16", "U": "8"},
            "21": {"R": "17", "D": "15", "L": "16", "U": "8"},
            "2": {"R": "11", "D": "1", "L": "0", "U": "8"},
            "9": {"R": "14", "D": "3", "L": "21", "U": "9"},
            "13": {"R": "13", "D": "7", "L": "13", "U": "19"},
            "12": {"R": "10", "D": "3", "L": "21", "U": "9"},
            "16": {"R": "17", "D": "4", "L": "16", "U": "1"},
            "4": {"R": "8", "D": "3", "L": "21", "U": "9"},
            "0": {"R": "11", "D": "12", "L": "0", "U": "5"},
            "3": {"R": "8", "D": "3", "L": "6", "U": "9"},
            "20": {"R": "0", "D": "20", "L": "11", "U": "20"},
        },
        initial_state="18",
        final_states={"8"},
    )
    assert PinWords.make_dfa_for_basis_from_pinwords(
        [Perm((0, 2, 1)), Perm((3, 0, 1, 2)), Perm((3, 0, 1, 2))]
    ) == DFA(
        states={
            "22",
            "26",
            "24",
            "1",
            "12",
            "21",
            "28",
            "32",
            "11",
            "34",
            "49",
            "18",
            "35",
            "3",
            "48",
            "4",
            "37",
            "6",
            "19",
            "40",
            "13",
            "47",
            "10",
            "23",
            "20",
            "45",
            "33",
            "5",
            "41",
            "50",
            "7",
            "0",
            "9",
            "31",
            "17",
            "2",
            "16",
            "46",
            "27",
            "8",
            "44",
            "29",
            "39",
            "14",
            "42",
            "38",
            "25",
            "43",
            "51",
            "36",
            "30",
            "15",
        },
        input_symbols={"R", "D", "L", "U"},
        transitions={
            "38": {"R": "38", "D": "11", "L": "17", "U": "16"},
            "43": {"R": "1", "D": "33", "L": "7", "U": "29"},
            "17": {"R": "38", "D": "48", "L": "17", "U": "29"},
            "47": {"R": "23", "D": "39", "L": "33", "U": "47"},
            "25": {"R": "36", "D": "32", "L": "46", "U": "33"},
            "2": {"R": "21", "D": "32", "L": "51", "U": "33"},
            "12": {"R": "42", "D": "48", "L": "12", "U": "33"},
            "41": {"R": "41", "D": "27", "L": "41", "U": "8"},
            "34": {"R": "33", "D": "28", "L": "2", "U": "4"},
            "27": {"R": "9", "D": "8", "L": "24", "U": "27"},
            "35": {"R": "35", "D": "13", "L": "26", "U": "34"},
            "19": {"R": "5", "D": "44", "L": "43", "U": "19"},
            "42": {"R": "42", "D": "22", "L": "12", "U": "20"},
            "15": {"R": "33", "D": "50", "L": "33", "U": "30"},
            "11": {"R": "5", "D": "50", "L": "46", "U": "30"},
            "8": {"R": "24", "D": "8", "L": "9", "U": "27"},
            "21": {"R": "21", "D": "10", "L": "51", "U": "6"},
            "37": {"R": "5", "D": "44", "L": "33", "U": "19"},
            "23": {"R": "42", "D": "6", "L": "12", "U": "33"},
            "16": {"R": "33", "D": "39", "L": "46", "U": "47"},
            "28": {"R": "0", "D": "28", "L": "23", "U": "4"},
            "14": {"R": "36", "D": "32", "L": "46", "U": "32"},
            "26": {"R": "35", "D": "34", "L": "26", "U": "13"},
            "39": {"R": "14", "D": "39", "L": "23", "U": "47"},
            "45": {"R": "14", "D": "45", "L": "33", "U": "49"},
            "6": {"R": "33", "D": "45", "L": "46", "U": "49"},
            "7": {"R": "1", "D": "33", "L": "7", "U": "13"},
            "9": {"R": "38", "D": "3", "L": "17", "U": "33"},
            "36": {"R": "36", "D": "49", "L": "46", "U": "32"},
            "40": {"R": "26", "D": "40", "L": "35", "U": "40"},
            "49": {"R": "25", "D": "45", "L": "33", "U": "49"},
            "33": {"R": "33", "D": "33", "L": "33", "U": "33"},
            "0": {"R": "21", "D": "15", "L": "51", "U": "6"},
            "3": {"R": "33", "D": "50", "L": "46", "U": "30"},
            "46": {"R": "36", "D": "33", "L": "46", "U": "33"},
            "1": {"R": "1", "D": "37", "L": "7", "U": "29"},
            "20": {"R": "33", "D": "39", "L": "33", "U": "47"},
            "22": {"R": "25", "D": "45", "L": "46", "U": "49"},
            "31": {"R": "21", "D": "33", "L": "51", "U": "33"},
            "18": {"R": "41", "D": "40", "L": "41", "U": "40"},
            "5": {"R": "21", "D": "15", "L": "51", "U": "33"},
            "32": {"R": "33", "D": "45", "L": "33", "U": "49"},
            "29": {"R": "33", "D": "50", "L": "31", "U": "30"},
            "24": {"R": "1", "D": "15", "L": "7", "U": "29"},
            "30": {"R": "25", "D": "50", "L": "51", "U": "30"},
            "51": {"R": "21", "D": "33", "L": "51", "U": "29"},
            "10": {"R": "5", "D": "50", "L": "33", "U": "30"},
            "48": {"R": "33", "D": "39", "L": "25", "U": "47"},
            "50": {"R": "0", "D": "50", "L": "33", "U": "30"},
            "44": {"R": "24", "D": "44", "L": "33", "U": "19"},
            "4": {"R": "23", "D": "28", "L": "51", "U": "4"},
            "13": {"R": "5", "D": "44", "L": "31", "U": "19"},
        },
        initial_state="18",
        final_states={"33"},
    )
    assert PinWords.make_dfa_for_basis_from_pinwords(
        [Perm((1, 0, 2, 3)), Perm((3, 2, 0, 1)), Perm((2, 1, 3, 0)), Perm((2, 1, 0, 3))]
    ) == DFA(
        states={
            "78",
            "80",
            "12",
            "11",
            "105",
            "107",
            "49",
            "37",
            "85",
            "69",
            "87",
            "20",
            "50",
            "60",
            "9",
            "31",
            "2",
            "46",
            "27",
            "8",
            "71",
            "64",
            "83",
            "84",
            "25",
            "22",
            "81",
            "76",
            "61",
            "92",
            "28",
            "32",
            "72",
            "35",
            "40",
            "47",
            "15",
            "97",
            "10",
            "45",
            "33",
            "57",
            "63",
            "102",
            "91",
            "16",
            "86",
            "89",
            "14",
            "56",
            "95",
            "108",
            "24",
            "1",
            "99",
            "58",
            "73",
            "67",
            "34",
            "104",
            "65",
            "19",
            "13",
            "103",
            "101",
            "7",
            "93",
            "44",
            "39",
            "106",
            "109",
            "96",
            "36",
            "53",
            "26",
            "75",
            "52",
            "21",
            "77",
            "18",
            "3",
            "48",
            "94",
            "4",
            "6",
            "74",
            "23",
            "82",
            "5",
            "41",
            "68",
            "0",
            "70",
            "59",
            "17",
            "62",
            "29",
            "88",
            "90",
            "42",
            "79",
            "100",
            "54",
            "38",
            "51",
            "43",
            "66",
            "55",
            "30",
            "98",
        },
        input_symbols={"R", "D", "L", "U"},
        transitions={
            "90": {"R": "35", "D": "64", "L": "27", "U": "90"},
            "100": {"R": "35", "D": "104", "L": "54", "U": "36"},
            "70": {"R": "73", "D": "41", "L": "97", "U": "70"},
            "66": {"R": "83", "D": "17", "L": "66", "U": "35"},
            "77": {"R": "38", "D": "1", "L": "21", "U": "59"},
            "2": {"R": "38", "D": "49", "L": "2", "U": "35"},
            "63": {"R": "35", "D": "26", "L": "9", "U": "69"},
            "12": {"R": "106", "D": "51", "L": "12", "U": "78"},
            "41": {"R": "68", "D": "41", "L": "6", "U": "70"},
            "74": {"R": "74", "D": "40", "L": "18", "U": "101"},
            "87": {"R": "87", "D": "47", "L": "87", "U": "25"},
            "96": {"R": "35", "D": "26", "L": "35", "U": "69"},
            "102": {"R": "65", "D": "107", "L": "91", "U": "11"},
            "42": {"R": "42", "D": "22", "L": "72", "U": "35"},
            "105": {"R": "108", "D": "46", "L": "105", "U": "35"},
            "15": {"R": "83", "D": "98", "L": "66", "U": "35"},
            "11": {"R": "81", "D": "99", "L": "35", "U": "37"},
            "88": {"R": "38", "D": "26", "L": "9", "U": "69"},
            "8": {"R": "65", "D": "107", "L": "91", "U": "94"},
            "37": {"R": "7", "D": "99", "L": "24", "U": "37"},
            "104": {"R": "54", "D": "104", "L": "54", "U": "36"},
            "95": {"R": "33", "D": "99", "L": "55", "U": "37"},
            "79": {"R": "65", "D": "77", "L": "91", "U": "88"},
            "85": {"R": "35", "D": "104", "L": "15", "U": "36"},
            "52": {"R": "109", "D": "52", "L": "79", "U": "71"},
            "108": {"R": "108", "D": "100", "L": "105", "U": "98"},
            "65": {"R": "65", "D": "57", "L": "91", "U": "10"},
            "58": {"R": "18", "D": "58", "L": "74", "U": "58"},
            "28": {"R": "54", "D": "104", "L": "2", "U": "36"},
            "26": {"R": "92", "D": "26", "L": "82", "U": "69"},
            "39": {"R": "92", "D": "99", "L": "35", "U": "37"},
            "45": {"R": "33", "D": "50", "L": "53", "U": "103"},
            "6": {"R": "84", "D": "35", "L": "20", "U": "14"},
            "55": {"R": "65", "D": "35", "L": "91", "U": "0"},
            "97": {"R": "108", "D": "46", "L": "105", "U": "103"},
            "9": {"R": "38", "D": "49", "L": "2", "U": "49"},
            "33": {"R": "108", "D": "13", "L": "105", "U": "98"},
            "0": {"R": "38", "D": "104", "L": "35", "U": "36"},
            "3": {"R": "54", "D": "50", "L": "2", "U": "103"},
            "1": {"R": "35", "D": "1", "L": "48", "U": "59"},
            "71": {"R": "7", "D": "52", "L": "27", "U": "71"},
            "86": {"R": "92", "D": "26", "L": "35", "U": "69"},
            "20": {"R": "84", "D": "62", "L": "20", "U": "45"},
            "22": {"R": "35", "D": "64", "L": "43", "U": "90"},
            "18": {"R": "74", "D": "101", "L": "18", "U": "40"},
            "107": {"R": "38", "D": "13", "L": "38", "U": "49"},
            "32": {"R": "35", "D": "104", "L": "2", "U": "36"},
            "29": {"R": "33", "D": "99", "L": "9", "U": "37"},
            "24": {"R": "83", "D": "17", "L": "66", "U": "36"},
            "30": {"R": "38", "D": "104", "L": "2", "U": "36"},
            "101": {"R": "102", "D": "41", "L": "76", "U": "70"},
            "51": {"R": "35", "D": "1", "L": "35", "U": "59"},
            "10": {"R": "106", "D": "1", "L": "35", "U": "59"},
            "78": {"R": "35", "D": "13", "L": "2", "U": "49"},
            "84": {"R": "84", "D": "95", "L": "20", "U": "34"},
            "48": {"R": "106", "D": "35", "L": "12", "U": "78"},
            "67": {"R": "67", "D": "57", "L": "75", "U": "35"},
            "83": {"R": "83", "D": "100", "L": "66", "U": "35"},
            "38": {"R": "38", "D": "35", "L": "2", "U": "35"},
            "69": {"R": "35", "D": "26", "L": "24", "U": "69"},
            "43": {"R": "67", "D": "107", "L": "75", "U": "96"},
            "17": {"R": "54", "D": "104", "L": "35", "U": "36"},
            "47": {"R": "73", "D": "25", "L": "61", "U": "47"},
            "25": {"R": "61", "D": "25", "L": "73", "U": "47"},
            "91": {"R": "65", "D": "39", "L": "91", "U": "16"},
            "99": {"R": "92", "D": "99", "L": "93", "U": "37"},
            "34": {"R": "102", "D": "41", "L": "9", "U": "70"},
            "73": {"R": "84", "D": "77", "L": "20", "U": "29"},
            "27": {"R": "42", "D": "28", "L": "72", "U": "96"},
            "35": {"R": "35", "D": "35", "L": "35", "U": "35"},
            "19": {"R": "19", "D": "22", "L": "44", "U": "10"},
            "98": {"R": "38", "D": "13", "L": "35", "U": "49"},
            "76": {"R": "106", "D": "49", "L": "12", "U": "49"},
            "60": {"R": "92", "D": "26", "L": "76", "U": "69"},
            "53": {"R": "108", "D": "98", "L": "105", "U": "35"},
            "80": {"R": "67", "D": "77", "L": "75", "U": "63"},
            "68": {"R": "65", "D": "56", "L": "91", "U": "11"},
            "21": {"R": "106", "D": "35", "L": "12", "U": "49"},
            "109": {"R": "42", "D": "35", "L": "72", "U": "35"},
            "89": {"R": "87", "D": "58", "L": "87", "U": "58"},
            "23": {"R": "38", "D": "64", "L": "43", "U": "90"},
            "57": {"R": "35", "D": "26", "L": "31", "U": "69"},
            "16": {"R": "38", "D": "104", "L": "15", "U": "36"},
            "54": {"R": "83", "D": "35", "L": "66", "U": "35"},
            "82": {"R": "67", "D": "35", "L": "75", "U": "32"},
            "75": {"R": "67", "D": "86", "L": "75", "U": "85"},
            "106": {"R": "106", "D": "35", "L": "12", "U": "35"},
            "61": {"R": "19", "D": "3", "L": "44", "U": "11"},
            "62": {"R": "102", "D": "41", "L": "35", "U": "70"},
            "94": {"R": "38", "D": "26", "L": "35", "U": "69"},
            "14": {"R": "33", "D": "50", "L": "2", "U": "103"},
            "72": {"R": "42", "D": "60", "L": "72", "U": "22"},
            "56": {"R": "54", "D": "50", "L": "38", "U": "103"},
            "7": {"R": "106", "D": "35", "L": "12", "U": "51"},
            "36": {"R": "35", "D": "104", "L": "35", "U": "36"},
            "40": {"R": "33", "D": "52", "L": "8", "U": "71"},
            "49": {"R": "35", "D": "13", "L": "35", "U": "49"},
            "93": {"R": "65", "D": "35", "L": "91", "U": "30"},
            "46": {"R": "54", "D": "50", "L": "35", "U": "103"},
            "31": {"R": "67", "D": "35", "L": "75", "U": "36"},
            "5": {"R": "108", "D": "35", "L": "105", "U": "35"},
            "64": {"R": "109", "D": "64", "L": "80", "U": "90"},
            "59": {"R": "35", "D": "1", "L": "9", "U": "59"},
            "81": {"R": "38", "D": "35", "L": "2", "U": "49"},
            "50": {"R": "54", "D": "50", "L": "5", "U": "103"},
            "44": {"R": "19", "D": "4", "L": "44", "U": "23"},
            "4": {"R": "92", "D": "99", "L": "76", "U": "37"},
            "13": {"R": "35", "D": "13", "L": "38", "U": "49"},
            "92": {"R": "67", "D": "35", "L": "75", "U": "35"},
            "103": {"R": "81", "D": "50", "L": "35", "U": "103"},
        },
        initial_state="89",
        final_states={"35"},
    )


def test_make_dfa_for_basis_from_db():
    assert PinWords.make_dfa_for_basis_from_db([Perm((1, 3, 0, 2))]) == DFA(
        states={
            "5",
            "6",
            "2",
            "14",
            "4",
            "10",
            "8",
            "9",
            "7",
            "12",
            "13",
            "1",
            "3",
            "11",
            "0",
            "15",
        },
        input_symbols={"D", "L", "U", "R"},
        transitions={
            "15": {"D": "13", "R": "11", "U": "6", "L": "1"},
            "0": {"D": "13", "R": "14", "U": "6", "L": "1"},
            "3": {"D": "6", "R": "3", "U": "13", "L": "3"},
            "12": {"D": "13", "R": "5", "U": "6", "L": "5"},
            "6": {"D": "13", "R": "2", "U": "6", "L": "5"},
            "13": {"D": "13", "R": "5", "U": "6", "L": "2"},
            "8": {"D": "10", "R": "3", "U": "10", "L": "3"},
            "2": {"D": "15", "R": "9", "U": "15", "L": "7"},
            "7": {"D": "15", "R": "9", "U": "12", "L": "7"},
            "14": {"D": "14", "R": "14", "U": "14", "L": "14"},
            "11": {"D": "14", "R": "9", "U": "0", "L": "7"},
            "4": {"D": "13", "R": "11", "U": "6", "L": "14"},
            "9": {"D": "12", "R": "9", "U": "15", "L": "7"},
            "5": {"D": "4", "R": "9", "U": "0", "L": "7"},
            "10": {"D": "10", "R": "7", "U": "10", "L": "9"},
            "1": {"D": "4", "R": "9", "U": "14", "L": "7"},
        },
        initial_state="8",
        final_states={"14"},
    )
    assert PinWords.make_dfa_for_basis_from_db(
        [Perm((0, 1, 2, 3)), Perm((2, 1, 0, 3))]
    ) == DFA(
        states={
            "31",
            "60",
            "5",
            "29",
            "58",
            "18",
            "43",
            "56",
            "51",
            "33",
            "23",
            "10",
            "20",
            "8",
            "57",
            "7",
            "28",
            "25",
            "39",
            "64",
            "55",
            "54",
            "21",
            "63",
            "16",
            "12",
            "45",
            "42",
            "38",
            "34",
            "24",
            "0",
            "44",
            "50",
            "17",
            "61",
            "41",
            "47",
            "6",
            "36",
            "15",
            "48",
            "62",
            "22",
            "19",
            "37",
            "32",
            "2",
            "53",
            "14",
            "4",
            "9",
            "46",
            "30",
            "65",
            "11",
            "13",
            "35",
            "49",
            "1",
            "27",
            "3",
            "59",
            "26",
            "40",
            "52",
        },
        input_symbols={"D", "L", "U", "R"},
        transitions={
            "48": {"D": "45", "L": "48", "U": "34", "R": "44"},
            "39": {"D": "40", "L": "22", "U": "39", "R": "29"},
            "30": {"D": "59", "L": "30", "U": "63", "R": "30"},
            "18": {"D": "33", "L": "61", "U": "42", "R": "19"},
            "13": {"D": "7", "L": "30", "U": "7", "R": "30"},
            "51": {"D": "29", "L": "22", "U": "21", "R": "8"},
            "49": {"D": "54", "L": "48", "U": "34", "R": "44"},
            "0": {"D": "53", "L": "50", "U": "35", "R": "10"},
            "42": {"D": "40", "L": "22", "U": "39", "R": "24"},
            "6": {"D": "6", "L": "0", "U": "3", "R": "28"},
            "3": {"D": "6", "L": "36", "U": "3", "R": "29"},
            "62": {"D": "43", "L": "36", "U": "62", "R": "46"},
            "22": {"D": "29", "L": "22", "U": "39", "R": "8"},
            "34": {"D": "33", "L": "61", "U": "15", "R": "55"},
            "16": {"D": "45", "L": "61", "U": "15", "R": "19"},
            "57": {"D": "27", "L": "57", "U": "5", "R": "25"},
            "46": {"D": "29", "L": "61", "U": "37", "R": "19"},
            "23": {"D": "53", "L": "50", "U": "35", "R": "24"},
            "35": {"D": "53", "L": "50", "U": "35", "R": "29"},
            "53": {"D": "53", "L": "45", "U": "35", "R": "10"},
            "36": {"D": "0", "L": "11", "U": "35", "R": "58"},
            "7": {"D": "7", "L": "17", "U": "7", "R": "56"},
            "28": {"D": "0", "L": "11", "U": "29", "R": "58"},
            "63": {"D": "63", "L": "49", "U": "59", "R": "2"},
            "1": {"D": "6", "L": "0", "U": "3", "R": "10"},
            "56": {"D": "26", "L": "56", "U": "31", "R": "17"},
            "4": {"D": "33", "L": "29", "U": "15", "R": "65"},
            "8": {"D": "40", "L": "22", "U": "29", "R": "8"},
            "19": {"D": "53", "L": "61", "U": "47", "R": "19"},
            "32": {"D": "33", "L": "50", "U": "15", "R": "65"},
            "65": {"D": "29", "L": "61", "U": "47", "R": "19"},
            "50": {"D": "45", "L": "50", "U": "35", "R": "10"},
            "27": {"D": "33", "L": "61", "U": "15", "R": "38"},
            "20": {"D": "20", "L": "45", "U": "41", "R": "18"},
            "60": {"D": "0", "L": "11", "U": "9", "R": "58"},
            "52": {"D": "6", "L": "0", "U": "3", "R": "29"},
            "61": {"D": "45", "L": "61", "U": "23", "R": "19"},
            "47": {"D": "40", "L": "29", "U": "39", "R": "24"},
            "37": {"D": "33", "L": "29", "U": "15", "R": "51"},
            "25": {"D": "1", "L": "57", "U": "4", "R": "25"},
            "9": {"D": "53", "L": "29", "U": "35", "R": "29"},
            "33": {"D": "33", "L": "45", "U": "15", "R": "38"},
            "41": {"D": "20", "L": "16", "U": "41", "R": "45"},
            "31": {"D": "43", "L": "14", "U": "62", "R": "12"},
            "5": {"D": "6", "L": "0", "U": "3", "R": "64"},
            "2": {"D": "27", "L": "57", "U": "32", "R": "25"},
            "14": {"D": "33", "L": "61", "U": "23", "R": "19"},
            "43": {"D": "43", "L": "14", "U": "62", "R": "60"},
            "17": {"D": "31", "L": "56", "U": "26", "R": "17"},
            "44": {"D": "54", "L": "48", "U": "45", "R": "44"},
            "59": {"D": "63", "L": "2", "U": "59", "R": "49"},
            "64": {"D": "29", "L": "50", "U": "29", "R": "10"},
            "54": {"D": "33", "L": "45", "U": "15", "R": "19"},
            "45": {"D": "40", "L": "22", "U": "39", "R": "8"},
            "24": {"D": "29", "L": "22", "U": "29", "R": "8"},
            "58": {"D": "1", "L": "11", "U": "29", "R": "58"},
            "10": {"D": "53", "L": "50", "U": "29", "R": "10"},
            "26": {"D": "20", "L": "16", "U": "41", "R": "18"},
            "12": {"D": "53", "L": "61", "U": "37", "R": "19"},
            "38": {"D": "53", "L": "50", "U": "21", "R": "10"},
            "11": {"D": "0", "L": "11", "U": "52", "R": "58"},
            "29": {"D": "29", "L": "29", "U": "29", "R": "29"},
            "40": {"D": "40", "L": "29", "U": "39", "R": "8"},
            "55": {"D": "40", "L": "22", "U": "21", "R": "8"},
            "15": {"D": "33", "L": "50", "U": "15", "R": "51"},
            "21": {"D": "40", "L": "29", "U": "39", "R": "29"},
        },
        initial_state="13",
        final_states={"29"},
    )
    assert PinWords.make_dfa_for_basis_from_db(
        [Perm((0, 1, 2)), Perm(()), Perm((2, 0, 1))]
    ) == DFA(
        states={"0"},
        input_symbols={"D", "L", "U", "R"},
        transitions={"0": {"D": "0", "L": "0", "U": "0", "R": "0"}},
        initial_state="0",
        final_states={"0"},
    )


def test_make_dfa_for_basis():
    assert PinWords.make_dfa_for_basis([Perm((1, 3, 0, 2))], use_db=False) == DFA(
        states={
            "2",
            "0",
            "7",
            "4",
            "8",
            "1",
            "14",
            "15",
            "10",
            "6",
            "5",
            "3",
            "12",
            "11",
            "9",
            "13",
        },
        input_symbols={"D", "L", "R", "U"},
        transitions={
            "15": {"D": "11", "L": "8", "R": "8", "U": "11"},
            "3": {"D": "7", "L": "14", "R": "0", "U": "2"},
            "1": {"D": "4", "L": "3", "R": "2", "U": "13"},
            "12": {"D": "7", "L": "14", "R": "0", "U": "1"},
            "6": {"D": "10", "L": "14", "R": "0", "U": "10"},
            "9": {"D": "4", "L": "12", "R": "12", "U": "13"},
            "8": {"D": "13", "L": "8", "R": "8", "U": "4"},
            "13": {"D": "4", "L": "12", "R": "6", "U": "13"},
            "0": {"D": "9", "L": "14", "R": "0", "U": "10"},
            "10": {"D": "4", "L": "3", "R": "5", "U": "13"},
            "5": {"D": "2", "L": "14", "R": "0", "U": "1"},
            "7": {"D": "4", "L": "2", "R": "5", "U": "13"},
            "4": {"D": "4", "L": "6", "R": "12", "U": "13"},
            "14": {"D": "10", "L": "14", "R": "0", "U": "9"},
            "2": {"D": "2", "L": "2", "R": "2", "U": "2"},
            "11": {"D": "11", "L": "0", "R": "14", "U": "11"},
        },
        initial_state="15",
        final_states={"2"},
    )
    assert PinWords.make_dfa_for_basis(
        [Perm((3, 1, 2, 0)), Perm((2, 3, 0, 1))], use_db=False
    ) == DFA(
        states={
            "33",
            "4",
            "32",
            "62",
            "38",
            "2",
            "64",
            "1",
            "37",
            "26",
            "57",
            "47",
            "28",
            "5",
            "21",
            "16",
            "20",
            "46",
            "9",
            "35",
            "48",
            "42",
            "39",
            "27",
            "23",
            "19",
            "56",
            "63",
            "6",
            "31",
            "59",
            "53",
            "41",
            "11",
            "45",
            "50",
            "30",
            "8",
            "25",
            "10",
            "29",
            "54",
            "3",
            "12",
            "60",
            "36",
            "55",
            "44",
            "18",
            "7",
            "0",
            "51",
            "14",
            "15",
            "61",
            "24",
            "34",
            "58",
            "40",
            "43",
            "17",
            "52",
            "22",
            "49",
            "13",
        },
        input_symbols={"D", "L", "R", "U"},
        transitions={
            "35": {"D": "35", "L": "19", "R": "28", "U": "56"},
            "41": {"D": "35", "L": "24", "R": "36", "U": "56"},
            "64": {"D": "54", "L": "53", "R": "64", "U": "5"},
            "27": {"D": "52", "L": "29", "R": "24", "U": "59"},
            "29": {"D": "48", "L": "29", "R": "10", "U": "28"},
            "45": {"D": "62", "L": "50", "R": "45", "U": "18"},
            "50": {"D": "8", "L": "50", "R": "45", "U": "38"},
            "7": {"D": "42", "L": "7", "R": "30", "U": "38"},
            "53": {"D": "5", "L": "53", "R": "64", "U": "54"},
            "37": {"D": "48", "L": "7", "R": "30", "U": "24"},
            "25": {"D": "25", "L": "55", "R": "2", "U": "11"},
            "14": {"D": "41", "L": "53", "R": "64", "U": "32"},
            "43": {"D": "52", "L": "1", "R": "10", "U": "59"},
            "61": {"D": "48", "L": "12", "R": "39", "U": "20"},
            "32": {"D": "52", "L": "1", "R": "24", "U": "59"},
            "26": {"D": "25", "L": "60", "R": "10", "U": "11"},
            "11": {"D": "25", "L": "51", "R": "15", "U": "11"},
            "60": {"D": "24", "L": "12", "R": "39", "U": "22"},
            "15": {"D": "62", "L": "50", "R": "45", "U": "9"},
            "18": {"D": "25", "L": "51", "R": "0", "U": "11"},
            "17": {"D": "26", "L": "50", "R": "45", "U": "9"},
            "24": {"D": "48", "L": "29", "R": "10", "U": "22"},
            "49": {"D": "49", "L": "64", "R": "53", "U": "49"},
            "28": {"D": "28", "L": "28", "R": "28", "U": "28"},
            "21": {"D": "49", "L": "34", "R": "34", "U": "49"},
            "56": {"D": "35", "L": "51", "R": "63", "U": "56"},
            "8": {"D": "25", "L": "44", "R": "2", "U": "11"},
            "13": {"D": "43", "L": "12", "R": "39", "U": "28"},
            "0": {"D": "48", "L": "50", "R": "45", "U": "27"},
            "63": {"D": "28", "L": "7", "R": "30", "U": "4"},
            "4": {"D": "35", "L": "29", "R": "36", "U": "56"},
            "19": {"D": "46", "L": "7", "R": "30", "U": "38"},
            "54": {"D": "33", "L": "6", "R": "23", "U": "31"},
            "22": {"D": "48", "L": "28", "R": "10", "U": "22"},
            "36": {"D": "28", "L": "7", "R": "30", "U": "24"},
            "3": {"D": "35", "L": "51", "R": "36", "U": "56"},
            "1": {"D": "24", "L": "12", "R": "39", "U": "28"},
            "46": {"D": "35", "L": "24", "R": "28", "U": "56"},
            "42": {"D": "35", "L": "47", "R": "28", "U": "56"},
            "34": {"D": "31", "L": "34", "R": "34", "U": "33"},
            "39": {"D": "62", "L": "12", "R": "39", "U": "16"},
            "6": {"D": "24", "L": "12", "R": "39", "U": "20"},
            "48": {"D": "48", "L": "29", "R": "28", "U": "22"},
            "44": {"D": "58", "L": "50", "R": "45", "U": "22"},
            "20": {"D": "52", "L": "28", "R": "24", "U": "59"},
            "47": {"D": "46", "L": "7", "R": "30", "U": "22"},
            "30": {"D": "28", "L": "7", "R": "30", "U": "3"},
            "10": {"D": "28", "L": "29", "R": "10", "U": "22"},
            "5": {"D": "25", "L": "44", "R": "0", "U": "11"},
            "33": {"D": "33", "L": "17", "R": "14", "U": "31"},
            "31": {"D": "33", "L": "14", "R": "17", "U": "31"},
            "57": {"D": "52", "L": "1", "R": "2", "U": "59"},
            "16": {"D": "52", "L": "28", "R": "61", "U": "59"},
            "38": {"D": "35", "L": "28", "R": "36", "U": "56"},
            "51": {"D": "46", "L": "7", "R": "30", "U": "28"},
            "59": {"D": "52", "L": "28", "R": "40", "U": "59"},
            "12": {"D": "57", "L": "12", "R": "39", "U": "28"},
            "52": {"D": "52", "L": "13", "R": "2", "U": "59"},
            "9": {"D": "25", "L": "29", "R": "37", "U": "11"},
            "23": {"D": "46", "L": "7", "R": "30", "U": "24"},
            "62": {"D": "52", "L": "1", "R": "28", "U": "59"},
            "40": {"D": "62", "L": "12", "R": "39", "U": "20"},
            "58": {"D": "35", "L": "24", "R": "10", "U": "56"},
            "55": {"D": "26", "L": "50", "R": "45", "U": "38"},
            "2": {"D": "28", "L": "12", "R": "39", "U": "20"},
        },
        initial_state="21",
        final_states={"28"},
    )
    assert PinWords.make_dfa_for_basis(
        [Perm((2, 1, 3, 0)), Perm((1, 3, 0, 2)), Perm((0, 2, 3, 1))], use_db=False
    ) == DFA(
        states={
            "33",
            "62",
            "88",
            "37",
            "86",
            "57",
            "28",
            "79",
            "21",
            "75",
            "16",
            "89",
            "23",
            "19",
            "56",
            "73",
            "25",
            "10",
            "54",
            "60",
            "68",
            "55",
            "61",
            "91",
            "43",
            "22",
            "4",
            "32",
            "93",
            "5",
            "67",
            "35",
            "90",
            "50",
            "80",
            "65",
            "3",
            "36",
            "51",
            "14",
            "15",
            "69",
            "34",
            "59",
            "13",
            "77",
            "64",
            "47",
            "20",
            "74",
            "48",
            "63",
            "6",
            "31",
            "41",
            "71",
            "76",
            "94",
            "29",
            "44",
            "18",
            "7",
            "24",
            "40",
            "70",
            "52",
            "49",
            "2",
            "38",
            "1",
            "26",
            "46",
            "9",
            "82",
            "42",
            "39",
            "27",
            "66",
            "92",
            "83",
            "53",
            "11",
            "45",
            "95",
            "30",
            "8",
            "72",
            "12",
            "85",
            "84",
            "81",
            "0",
            "78",
            "87",
            "58",
            "17",
        },
        input_symbols={"D", "L", "R", "U"},
        transitions={
            "35": {"D": "2", "L": "32", "R": "47", "U": "9"},
            "41": {"D": "89", "L": "74", "R": "33", "U": "41"},
            "92": {"D": "8", "L": "91", "R": "0", "U": "21"},
            "64": {"D": "61", "L": "21", "R": "21", "U": "4"},
            "93": {"D": "84", "L": "72", "R": "30", "U": "1"},
            "27": {"D": "21", "L": "32", "R": "47", "U": "8"},
            "89": {"D": "89", "L": "49", "R": "36", "U": "41"},
            "29": {"D": "8", "L": "91", "R": "0", "U": "57"},
            "83": {"D": "54", "L": "83", "R": "83", "U": "17"},
            "87": {"D": "89", "L": "92", "R": "6", "U": "41"},
            "50": {"D": "84", "L": "72", "R": "13", "U": "1"},
            "7": {"D": "39", "L": "51", "R": "7", "U": "86"},
            "70": {"D": "8", "L": "19", "R": "19", "U": "60"},
            "53": {"D": "21", "L": "90", "R": "88", "U": "64"},
            "37": {"D": "40", "L": "92", "R": "34", "U": "24"},
            "25": {"D": "37", "L": "59", "R": "55", "U": "87"},
            "43": {"D": "22", "L": "95", "R": "6", "U": "20"},
            "61": {"D": "61", "L": "21", "R": "36", "U": "4"},
            "14": {"D": "93", "L": "68", "R": "14", "U": "86"},
            "32": {"D": "94", "L": "32", "R": "47", "U": "73"},
            "26": {"D": "28", "L": "5", "R": "26", "U": "43"},
            "11": {"D": "89", "L": "95", "R": "21", "U": "41"},
            "60": {"D": "8", "L": "19", "R": "0", "U": "60"},
            "15": {"D": "57", "L": "59", "R": "55", "U": "87"},
            "18": {"D": "21", "L": "32", "R": "47", "U": "21"},
            "55": {"D": "78", "L": "59", "R": "55", "U": "43"},
            "17": {"D": "17", "L": "25", "R": "75", "U": "54"},
            "24": {"D": "40", "L": "13", "R": "81", "U": "24"},
            "81": {"D": "21", "L": "32", "R": "47", "U": "9"},
            "49": {"D": "2", "L": "51", "R": "7", "U": "58"},
            "21": {"D": "21", "L": "21", "R": "21", "U": "21"},
            "75": {"D": "10", "L": "68", "R": "14", "U": "64"},
            "84": {"D": "84", "L": "48", "R": "56", "U": "1"},
            "28": {"D": "84", "L": "72", "R": "3", "U": "1"},
            "85": {"D": "44", "L": "51", "R": "7", "U": "8"},
            "56": {"D": "10", "L": "68", "R": "14", "U": "21"},
            "8": {"D": "8", "L": "21", "R": "21", "U": "60"},
            "13": {"D": "66", "L": "32", "R": "47", "U": "8"},
            "0": {"D": "21", "L": "91", "R": "0", "U": "57"},
            "80": {"D": "61", "L": "21", "R": "52", "U": "4"},
            "77": {"D": "61", "L": "53", "R": "62", "U": "4"},
            "69": {"D": "61", "L": "21", "R": "38", "U": "4"},
            "63": {"D": "63", "L": "26", "R": "5", "U": "63"},
            "4": {"D": "61", "L": "53", "R": "29", "U": "4"},
            "74": {"D": "65", "L": "51", "R": "7", "U": "64"},
            "71": {"D": "40", "L": "21", "R": "34", "U": "24"},
            "68": {"D": "23", "L": "68", "R": "14", "U": "50"},
            "19": {"D": "21", "L": "91", "R": "0", "U": "8"},
            "90": {"D": "21", "L": "90", "R": "88", "U": "77"},
            "54": {"D": "17", "L": "75", "R": "25", "U": "54"},
            "67": {"D": "8", "L": "34", "R": "21", "U": "60"},
            "22": {"D": "22", "L": "82", "R": "79", "U": "20"},
            "36": {"D": "69", "L": "90", "R": "88", "U": "21"},
            "3": {"D": "71", "L": "51", "R": "7", "U": "8"},
            "86": {"D": "40", "L": "95", "R": "18", "U": "24"},
            "1": {"D": "84", "L": "75", "R": "35", "U": "1"},
            "42": {"D": "89", "L": "16", "R": "85", "U": "41"},
            "76": {"D": "44", "L": "90", "R": "88", "U": "8"},
            "34": {"D": "21", "L": "91", "R": "0", "U": "21"},
            "46": {"D": "89", "L": "16", "R": "45", "U": "41"},
            "39": {"D": "61", "L": "53", "R": "52", "U": "4"},
            "6": {"D": "21", "L": "51", "R": "7", "U": "21"},
            "44": {"D": "8", "L": "21", "R": "34", "U": "60"},
            "48": {"D": "37", "L": "51", "R": "7", "U": "58"},
            "20": {"D": "22", "L": "74", "R": "15", "U": "20"},
            "47": {"D": "21", "L": "32", "R": "47", "U": "86"},
            "30": {"D": "71", "L": "51", "R": "7", "U": "21"},
            "10": {"D": "89", "L": "21", "R": "6", "U": "41"},
            "5": {"D": "43", "L": "5", "R": "26", "U": "28"},
            "94": {"D": "40", "L": "95", "R": "21", "U": "24"},
            "33": {"D": "67", "L": "32", "R": "47", "U": "9"},
            "31": {"D": "22", "L": "95", "R": "21", "U": "20"},
            "78": {"D": "61", "L": "53", "R": "76", "U": "4"},
            "57": {"D": "8", "L": "34", "R": "34", "U": "60"},
            "79": {"D": "69", "L": "90", "R": "88", "U": "64"},
            "95": {"D": "66", "L": "32", "R": "47", "U": "21"},
            "72": {"D": "44", "L": "90", "R": "88", "U": "64"},
            "38": {"D": "21", "L": "90", "R": "88", "U": "21"},
            "16": {"D": "8", "L": "90", "R": "88", "U": "64"},
            "91": {"D": "21", "L": "91", "R": "0", "U": "70"},
            "59": {"D": "31", "L": "59", "R": "55", "U": "42"},
            "51": {"D": "11", "L": "51", "R": "7", "U": "46"},
            "52": {"D": "44", "L": "90", "R": "88", "U": "21"},
            "9": {"D": "40", "L": "92", "R": "18", "U": "24"},
            "73": {"D": "40", "L": "62", "R": "27", "U": "24"},
            "12": {"D": "63", "L": "83", "R": "83", "U": "63"},
            "23": {"D": "89", "L": "95", "R": "6", "U": "41"},
            "40": {"D": "40", "L": "35", "R": "21", "U": "24"},
            "62": {"D": "8", "L": "91", "R": "0", "U": "8"},
            "88": {"D": "80", "L": "90", "R": "88", "U": "57"},
            "66": {"D": "40", "L": "21", "R": "21", "U": "24"},
            "65": {"D": "89", "L": "21", "R": "21", "U": "41"},
            "58": {"D": "89", "L": "92", "R": "18", "U": "41"},
            "45": {"D": "8", "L": "32", "R": "47", "U": "8"},
            "2": {"D": "40", "L": "92", "R": "21", "U": "24"},
            "82": {"D": "2", "L": "59", "R": "55", "U": "87"},
        },
        initial_state="12",
        final_states={"21"},
    )
    assert PinWords.make_dfa_for_basis(
        [Perm((2, 0, 1, 3)), Perm((0, 1)), Perm((2, 1, 0, 3)), Perm((3, 2, 0, 1))],
        use_db=False,
    ) == DFA(
        states={"2", "0", "7", "4", "8", "1", "6", "5", "3", "9"},
        input_symbols={"D", "L", "R", "U"},
        transitions={
            "8": {"D": "6", "L": "5", "R": "8", "U": "7"},
            "9": {"D": "7", "L": "5", "R": "8", "U": "7"},
            "0": {"D": "0", "L": "7", "R": "9", "U": "2"},
            "5": {"D": "7", "L": "5", "R": "8", "U": "6"},
            "7": {"D": "7", "L": "7", "R": "7", "U": "7"},
            "3": {"D": "2", "L": "3", "R": "3", "U": "0"},
            "4": {"D": "4", "L": "8", "R": "5", "U": "4"},
            "1": {"D": "4", "L": "3", "R": "3", "U": "4"},
            "6": {"D": "0", "L": "7", "R": "7", "U": "2"},
            "2": {"D": "0", "L": "9", "R": "7", "U": "2"},
        },
        initial_state="1",
        final_states={"7"},
    )


def test_has_finite_alterations():
    assert PinWords.has_finite_alternations([Perm((1, 0, 2, 3, 4))]) is False
    assert (
        PinWords.has_finite_alternations([Perm((3, 1, 0, 4, 2)), Perm((1, 3, 0, 4, 2))])
        is False
    )
    assert (
        PinWords.has_finite_alternations(
            [Perm((2, 1, 3, 0)), Perm((4, 0, 1, 2, 3)), Perm((3, 2, 4, 1, 0))]
        )
        is True
    )
    assert (
        PinWords.has_finite_alternations(
            [
                Perm((1, 2, 0, 4, 3)),
                Perm((2, 1, 3, 0)),
                Perm((2, 4, 3, 1, 0)),
                Perm((1, 4, 3, 0, 2)),
            ]
        )
        is False
    )
    assert (
        PinWords.has_finite_alternations(
            [
                Perm((3, 0, 1, 2, 4)),
                Perm((2, 1, 0, 3, 4)),
                Perm((4, 3, 0, 2, 1)),
                Perm((2, 1, 4, 0, 3)),
                Perm((1, 2, 0, 4, 3)),
            ]
        )
        is True
    )
    assert (
        PinWords.has_finite_alternations(
            [
                Perm((1, 4, 2, 3, 0)),
                Perm((3, 0, 1, 2, 4)),
                Perm((0, 1, 4, 2, 3)),
                Perm((0, 1, 3, 2, 4)),
                Perm((1, 3, 2, 0, 4)),
                Perm((2, 0, 1, 3)),
            ]
        )
        is False
    )
    assert (
        PinWords.has_finite_alternations(
            [
                Perm((4, 0, 1, 2, 3)),
                Perm((0, 2, 4, 1, 3)),
                Perm((3, 0, 1, 2, 4)),
                Perm((4, 1, 3, 2, 0)),
                Perm((3, 2, 4, 0, 1)),
                Perm((3, 1, 4, 2, 0)),
                Perm((0, 2, 3, 1, 4)),
            ]
        )
        is True
    )
    assert (
        PinWords.has_finite_alternations(
            [
                Perm((1, 2, 3, 4, 0)),
                Perm((2, 0, 1, 3, 4)),
                Perm((2, 0, 1, 3, 4)),
                Perm((3, 4, 1, 2, 0)),
                Perm((4, 3, 1, 0, 2)),
                Perm((0, 3, 4, 1, 2)),
                Perm((1, 2, 3, 0)),
                Perm((3, 4, 1, 2, 0)),
            ]
        )
        is True
    )
    assert (
        PinWords.has_finite_alternations(
            [
                Perm((2, 1, 4, 3, 0)),
                Perm((2, 4, 3, 0, 1)),
                Perm((4, 0, 1, 2, 3)),
                Perm((3, 1, 0, 2, 4)),
                Perm((2, 4, 0, 3, 1)),
                Perm((0, 1, 4, 2, 3)),
                Perm((3, 0, 2, 1, 4)),
                Perm((3, 2, 1, 0, 4)),
                Perm((3, 2, 0, 4, 1)),
            ]
        )
        is True
    )
    assert (
        PinWords.has_finite_alternations(
            [
                Perm((4, 2, 3, 1, 0)),
                Perm((4, 0, 3, 2, 1)),
                Perm((2, 1, 3, 0)),
                Perm((1, 3, 2, 4, 0)),
                Perm((0, 2, 3, 1)),
                Perm((3, 0, 1, 2, 4)),
                Perm((4, 2, 3, 0, 1)),
                Perm((2, 3, 1, 4, 0)),
                Perm((1, 0, 2, 3, 4)),
                Perm((3, 2, 1, 0)),
            ]
        )
        is True
    )
    assert (
        PinWords.has_finite_alternations(
            [
                Perm((2, 1, 0, 3)),
                Perm((2, 3, 1, 4, 0)),
                Perm((1, 0, 4, 3, 2)),
                Perm((0, 1, 4, 2, 3)),
                Perm((4, 1, 0, 2, 3)),
                Perm((2, 0, 4, 3, 1)),
                Perm((2, 0, 3, 1, 4)),
                Perm((3, 2, 0, 4, 1)),
                Perm((2, 1, 3, 0)),
                Perm((3, 4, 1, 0, 2)),
                Perm((1, 0, 3, 2)),
            ]
        )
        is True
    )
    assert (
        PinWords.has_finite_alternations(
            [
                Perm((0, 2, 3, 1, 4)),
                Perm((3, 0, 1, 4, 2)),
                Perm((1, 3, 4, 2, 0)),
                Perm((3, 1, 0, 2, 4)),
                Perm((3, 2, 1, 0)),
                Perm((0, 3, 1, 2)),
                Perm((3, 4, 0, 2, 1)),
                Perm((2, 0, 1)),
                Perm((2, 1, 4, 0, 3)),
                Perm((1, 3, 2, 4, 0)),
                Perm((1, 4, 3, 0, 2)),
                Perm((1, 2, 3, 0)),
            ]
        )
        is True
    )
    assert (
        PinWords.has_finite_alternations(
            [
                Perm((2, 4, 1, 0, 3)),
                Perm((3, 0, 4, 1, 2)),
                Perm((3, 2, 0, 1)),
                Perm((2, 4, 3, 0, 1)),
                Perm((3, 4, 2, 0, 1)),
                Perm((1, 0, 4, 3, 2)),
                Perm((2, 0, 1, 4, 3)),
                Perm((2, 4, 3, 0, 1)),
                Perm((1, 0, 3, 2)),
                Perm((4, 0, 2, 3, 1)),
                Perm((3, 2, 1, 4, 0)),
                Perm((4, 1, 2, 3, 0)),
                Perm((1, 0, 3, 2, 4)),
            ]
        )
        is False
    )
    assert (
        PinWords.has_finite_alternations(
            [
                Perm((1, 2, 3, 0)),
                Perm((0,)),
                Perm((2, 3, 4, 1, 0)),
                Perm((4, 3, 0, 1, 2)),
                Perm((0, 2, 3, 4, 1)),
                Perm((0,)),
                Perm((0, 2, 1, 4, 3)),
                Perm((2, 3, 0, 4, 1)),
                Perm((1, 4, 2, 3, 0)),
                Perm((2, 3, 1, 0)),
                Perm((2, 3, 1, 4, 0)),
                Perm((2, 3, 0, 4, 1)),
                Perm((0, 4, 2, 1, 3)),
                Perm((2, 3, 1, 0)),
            ]
        )
        is True
    )
    assert (
        PinWords.has_finite_alternations(
            [
                Perm((3, 0, 1, 2)),
                Perm((3, 0, 2, 4, 1)),
                Perm((3, 2, 1, 4, 0)),
                Perm((2, 3, 1, 0)),
                Perm((3, 4, 0, 1, 2)),
                Perm((1, 4, 2, 0, 3)),
                Perm((1, 0, 2, 3)),
                Perm((0, 1, 2)),
                Perm((2, 0, 3, 1)),
                Perm((2, 3, 0, 1, 4)),
                Perm((2, 3, 1, 0, 4)),
                Perm((1, 4, 0, 3, 2)),
                Perm((1, 2, 0, 3)),
                Perm((2, 1, 4, 0, 3)),
                Perm((1, 4, 0, 3, 2)),
            ]
        )
        is True
    )


def test_has_finite_wedges_type_1():
    assert PinWords.has_finite_wedges_type_1([Perm((2, 1, 4, 3, 0))]) is False
    assert (
        PinWords.has_finite_wedges_type_1([Perm((0, 3, 2, 1)), Perm((1, 4, 3, 2, 0))])
        is False
    )
    assert (
        PinWords.has_finite_wedges_type_1(
            [Perm((1, 3, 4, 0, 2)), Perm((0,)), Perm((4, 3, 2, 1, 0))]
        )
        is True
    )
    assert (
        PinWords.has_finite_wedges_type_1(
            [
                Perm((1, 2, 4, 3, 0)),
                Perm((3, 4, 2, 1, 0)),
                Perm((1, 4, 3, 2, 0)),
                Perm((3, 4, 1, 0, 2)),
            ]
        )
        is False
    )
    assert (
        PinWords.has_finite_wedges_type_1(
            [
                Perm((1, 3, 4, 2, 0)),
                Perm((4, 3, 1, 0, 2)),
                Perm((4, 1, 3, 2, 0)),
                Perm((0, 3, 2, 1, 4)),
                Perm((0, 2, 1, 3, 4)),
            ]
        )
        is False
    )
    assert (
        PinWords.has_finite_wedges_type_1(
            [
                Perm((3, 0, 2, 1)),
                Perm((2, 0, 4, 3, 1)),
                Perm((2, 3, 4, 1, 0)),
                Perm((0,)),
                Perm((3, 0, 4, 1, 2)),
                Perm((4, 0, 3, 1, 2)),
            ]
        )
        is True
    )
    assert (
        PinWords.has_finite_wedges_type_1(
            [
                Perm((3, 1, 0, 2, 4)),
                Perm((3, 0, 4, 2, 1)),
                Perm((4, 2, 1, 0, 3)),
                Perm((3, 2, 1, 0)),
                Perm((3, 0, 1, 2, 4)),
                Perm((4, 1, 3, 2, 0)),
                Perm((4, 3, 2, 0, 1)),
            ]
        )
        is True
    )
    assert (
        PinWords.has_finite_wedges_type_1(
            [
                Perm((0, 1)),
                Perm((2, 4, 1, 0, 3)),
                Perm((0, 3, 1, 2, 4)),
                Perm((3, 0, 4, 2, 1)),
                Perm((2, 3, 0, 4, 1)),
                Perm((1, 3, 4, 2, 0)),
                Perm((0, 4, 3, 1, 2)),
                Perm((1, 2, 0, 4, 3)),
            ]
        )
        is True
    )
    assert (
        PinWords.has_finite_wedges_type_1(
            [
                Perm((0, 1, 3, 4, 2)),
                Perm((1, 4, 2, 0, 3)),
                Perm((1, 3, 2, 0, 4)),
                Perm((2, 0, 1)),
                Perm((3, 0, 1, 4, 2)),
                Perm((4, 1, 3, 2, 0)),
                Perm((1, 3, 0, 4, 2)),
                Perm((3, 0, 2, 1)),
                Perm((3, 2, 1, 0)),
            ]
        )
        is True
    )
    assert (
        PinWords.has_finite_wedges_type_1(
            [
                Perm((1, 0)),
                Perm((0, 1, 3, 2, 4)),
                Perm((2, 0, 3, 1, 4)),
                Perm((1, 2, 3, 0)),
                Perm((4, 1, 0, 2, 3)),
                Perm((4, 1, 0, 2, 3)),
                Perm((0, 3, 2, 4, 1)),
                Perm((1, 0, 2, 3)),
                Perm((2, 3, 1, 0)),
                Perm((3, 1, 4, 2, 0)),
            ]
        )
        is True
    )
    assert (
        PinWords.has_finite_wedges_type_1(
            [
                Perm((0, 2, 3, 1)),
                Perm((2, 3, 0, 1, 4)),
                Perm((3, 2, 1, 0)),
                Perm((0, 1, 2, 4, 3)),
                Perm((1, 3, 2, 4, 0)),
                Perm((0, 4, 1, 2, 3)),
                Perm((2, 3, 0, 1, 4)),
                Perm((2, 1, 0, 3)),
                Perm((2, 4, 1, 0, 3)),
                Perm((3, 0, 4, 2, 1)),
                Perm((2, 4, 1, 0, 3)),
            ]
        )
        is True
    )
    assert (
        PinWords.has_finite_wedges_type_1(
            [
                Perm((2, 1, 3, 0)),
                Perm((3, 2, 0, 1, 4)),
                Perm((2, 3, 4, 0, 1)),
                Perm((3, 2, 4, 0, 1)),
                Perm((0, 2, 1, 3, 4)),
                Perm((3, 1, 2, 0, 4)),
                Perm((3, 1, 0, 2, 4)),
                Perm((0, 2, 1, 3)),
                Perm((4, 1, 2, 0, 3)),
                Perm((4, 1, 0, 3, 2)),
                Perm((0, 3, 1, 2)),
                Perm((4, 0, 2, 1, 3)),
            ]
        )
        is True
    )
    assert (
        PinWords.has_finite_wedges_type_1(
            [
                Perm((0, 3, 2, 1)),
                Perm((1, 3, 0, 2, 4)),
                Perm((2, 4, 3, 1, 0)),
                Perm((0, 4, 3, 2, 1)),
                Perm((4, 0, 2, 1, 3)),
                Perm((3, 4, 2, 1, 0)),
                Perm((3, 1, 2, 4, 0)),
                Perm((0, 3, 2, 1)),
                Perm((4, 2, 1, 3, 0)),
                Perm((3, 2, 0, 4, 1)),
                Perm((3, 4, 0, 2, 1)),
                Perm((3, 0, 1, 2)),
                Perm((3, 4, 0, 1, 2)),
            ]
        )
        is True
    )
    assert (
        PinWords.has_finite_wedges_type_1(
            [
                Perm((3, 1, 2, 0)),
                Perm((1, 4, 3, 2, 0)),
                Perm((3, 1, 4, 2, 0)),
                Perm((4, 0, 1, 3, 2)),
                Perm((2, 4, 0, 3, 1)),
                Perm((4, 3, 0, 2, 1)),
                Perm((0, 2, 1)),
                Perm((0, 1)),
                Perm((1, 4, 2, 0, 3)),
                Perm((1, 2, 3, 0, 4)),
                Perm((0, 4, 2, 3, 1)),
                Perm((1, 3, 0, 2)),
                Perm((0, 1, 2, 4, 3)),
                Perm((2, 3, 0, 1)),
            ]
        )
        is True
    )
    assert (
        PinWords.has_finite_wedges_type_1(
            [
                Perm((3, 1, 0, 4, 2)),
                Perm((1, 2, 4, 0, 3)),
                Perm((3, 4, 2, 0, 1)),
                Perm((0, 1, 3, 2, 4)),
                Perm((0, 2, 1, 4, 3)),
                Perm((0, 1, 2, 4, 3)),
                Perm((1, 3, 4, 0, 2)),
                Perm((4, 0, 3, 1, 2)),
                Perm((3, 2, 0, 4, 1)),
                Perm((4, 0, 3, 1, 2)),
                Perm((4, 1, 3, 2, 0)),
                Perm((1, 0, 3, 2)),
                Perm((4, 2, 1, 3, 0)),
                Perm((3, 1, 0, 2, 4)),
                Perm((2, 3, 0, 1, 4)),
            ]
        )
        is True
    )


def test_has_finite_wedges_of_type_2():
    assert PinWords.has_finite_wedges_type_2([Perm((0, 2, 1, 4, 3))]) is False
    assert (
        PinWords.has_finite_wedges_type_2(
            [Perm((3, 1, 4, 2, 0)), Perm((0, 4, 2, 1, 3))]
        )
        is False
    )
    assert (
        PinWords.has_finite_wedges_type_2(
            [Perm((4, 0, 3, 2, 1)), Perm((1, 3, 0, 4, 2)), Perm((3, 0, 1, 2))]
        )
        is False
    )
    assert (
        PinWords.has_finite_wedges_type_2(
            [
                Perm((3, 2, 1, 4, 0)),
                Perm((3, 0, 4, 2, 1)),
                Perm((1, 3, 2, 0, 4)),
                Perm((0, 2, 3, 1)),
            ]
        )
        is False
    )
    assert (
        PinWords.has_finite_wedges_type_2(
            [
                Perm((4, 2, 0, 3, 1)),
                Perm((0, 4, 1, 3, 2)),
                Perm((4, 2, 3, 1, 0)),
                Perm((3, 1, 2, 4, 0)),
                Perm((3, 0, 4, 1, 2)),
            ]
        )
        is False
    )
    assert (
        PinWords.has_finite_wedges_type_2(
            [
                Perm((4, 1, 3, 2, 0)),
                Perm((4, 1, 3, 0, 2)),
                Perm((3, 4, 2, 1, 0)),
                Perm((3, 0, 2, 4, 1)),
                Perm((3, 0, 4, 1, 2)),
                Perm((4, 1, 2, 0, 3)),
            ]
        )
        is False
    )
    assert (
        PinWords.has_finite_wedges_type_2(
            [
                Perm((0, 2, 4, 1, 3)),
                Perm((2, 0, 1)),
                Perm((4, 2, 1, 3, 0)),
                Perm((4, 2, 0, 1, 3)),
                Perm((0, 2, 4, 3, 1)),
                Perm((2, 0, 1, 3)),
                Perm((3, 1, 2, 0, 4)),
            ]
        )
        is True
    )
    assert (
        PinWords.has_finite_wedges_type_2(
            [
                Perm((1, 3, 0, 2)),
                Perm((0, 1, 2, 3)),
                Perm((2, 1, 3, 0, 4)),
                Perm((3, 2, 1, 4, 0)),
                Perm((1, 0, 3, 4, 2)),
                Perm((1, 0, 2, 3)),
                Perm((3, 1, 2, 0)),
                Perm((0, 1)),
            ]
        )
        is True
    )
    assert (
        PinWords.has_finite_wedges_type_2(
            [
                Perm((0, 2, 1, 4, 3)),
                Perm((3, 0, 2, 4, 1)),
                Perm((2, 3, 0, 1)),
                Perm((0, 3, 4, 2, 1)),
                Perm((0, 2, 4, 1, 3)),
                Perm((2, 1, 4, 3, 0)),
                Perm((0, 4, 1, 3, 2)),
                Perm((1, 3, 2, 4, 0)),
                Perm((3, 2, 4, 0, 1)),
            ]
        )
        is False
    )
    assert (
        PinWords.has_finite_wedges_type_2(
            [
                Perm((3, 1, 0, 2, 4)),
                Perm((1, 4, 3, 0, 2)),
                Perm((1, 4, 0, 3, 2)),
                Perm((2, 4, 3, 1, 0)),
                Perm((2, 4, 3, 0, 1)),
                Perm((2, 3, 1, 0)),
                Perm((1, 0, 2, 3, 4)),
                Perm((4, 1, 0, 2, 3)),
                Perm((3, 1, 2, 4, 0)),
                Perm((3, 0, 1, 4, 2)),
            ]
        )
        is True
    )
    assert (
        PinWords.has_finite_wedges_type_2(
            [
                Perm((4, 1, 0, 2, 3)),
                Perm((2, 0, 3, 4, 1)),
                Perm((0, 3, 2, 1)),
                Perm((3, 1, 0, 2)),
                Perm((1, 2, 3, 0)),
                Perm((4, 2, 1, 3, 0)),
                Perm((2, 1, 0, 3, 4)),
                Perm((1, 2, 0, 4, 3)),
                Perm((0, 3, 2, 4, 1)),
                Perm((0, 2, 3, 4, 1)),
                Perm((1, 3, 2, 4, 0)),
            ]
        )
        is True
    )
    assert (
        PinWords.has_finite_wedges_type_2(
            [
                Perm((4, 3, 2, 0, 1)),
                Perm((2, 1, 0, 3, 4)),
                Perm((3, 1, 0, 2, 4)),
                Perm((1, 2, 3, 0, 4)),
                Perm((1, 3, 2, 4, 0)),
                Perm((4, 0, 1, 3, 2)),
                Perm((2, 0, 1, 3, 4)),
                Perm((1, 3, 4, 2, 0)),
                Perm((0, 3, 1, 4, 2)),
                Perm((1, 0, 2, 4, 3)),
                Perm((4, 1, 0, 2, 3)),
                Perm((3, 4, 0, 2, 1)),
            ]
        )
        is True
    )
    assert (
        PinWords.has_finite_wedges_type_2(
            [
                Perm((2, 1, 3, 4, 0)),
                Perm((0, 1)),
                Perm((1, 2, 0)),
                Perm((1, 3, 0, 2, 4)),
                Perm((2, 4, 1, 0, 3)),
                Perm((0, 4, 1, 3, 2)),
                Perm((0, 3, 2, 1)),
                Perm((1, 0, 3, 2, 4)),
                Perm((0, 4, 2, 3, 1)),
                Perm((0, 1, 2, 3, 4)),
                Perm((2, 1, 4, 0, 3)),
                Perm((4, 3, 1, 0, 2)),
                Perm((1, 0, 3, 4, 2)),
            ]
        )
        is True
    )
    assert (
        PinWords.has_finite_wedges_type_2(
            [
                Perm((2, 4, 1, 0, 3)),
                Perm((2, 0, 3, 1)),
                Perm((1, 2, 0)),
                Perm((0, 2, 3, 4, 1)),
                Perm((3, 0, 1, 2, 4)),
                Perm((1, 2, 0)),
                Perm((2, 4, 1, 0, 3)),
                Perm((0, 1, 3, 2)),
                Perm((2, 4, 1, 3, 0)),
                Perm((4, 0, 1, 2, 3)),
                Perm((2, 4, 1, 3, 0)),
                Perm((4, 0, 2, 1, 3)),
                Perm((3, 1, 0, 4, 2)),
                Perm((3, 0, 2, 1, 4)),
            ]
        )
        is True
    )
    assert (
        PinWords.has_finite_wedges_type_2(
            [
                Perm((4, 3, 1, 2, 0)),
                Perm((0, 1)),
                Perm((1, 3, 2, 0)),
                Perm((2, 4, 1, 0, 3)),
                Perm((1, 2, 0, 3)),
                Perm((3, 0, 1, 4, 2)),
                Perm((0, 3, 1, 4, 2)),
                Perm((1, 3, 4, 2, 0)),
                Perm((0, 3, 2, 1, 4)),
                Perm((1, 4, 0, 3, 2)),
                Perm((4, 2, 1, 3, 0)),
                Perm((1, 0, 4, 3, 2)),
                Perm((3, 2, 0, 4, 1)),
                Perm((3, 2, 4, 0, 1)),
                Perm((2, 0, 1)),
            ]
        )
        is True
    )


def test_has_finite_special_simples():
    assert PinWords.has_finite_special_simples([Perm((2, 1, 0))]) is False
    assert (
        PinWords.has_finite_special_simples(
            [Perm((1, 3, 4, 2, 0)), Perm((3, 1, 2, 0, 4))]
        )
        is False
    )
    assert (
        PinWords.has_finite_special_simples(
            [Perm((0, 1, 2)), Perm((3, 0, 2, 1)), Perm((1, 4, 0, 2, 3))]
        )
        is True
    )
    assert (
        PinWords.has_finite_special_simples(
            [
                Perm((1, 0, 4, 2, 3)),
                Perm((2, 0, 1, 3)),
                Perm((1, 0, 3, 4, 2)),
                Perm((4, 3, 0, 1, 2)),
            ]
        )
        is False
    )
    assert (
        PinWords.has_finite_special_simples(
            [
                Perm((3, 4, 1, 0, 2)),
                Perm((0, 2, 1, 4, 3)),
                Perm((0, 4, 3, 1, 2)),
                Perm((1, 4, 2, 3, 0)),
                Perm((2, 0, 3, 1, 4)),
            ]
        )
        is False
    )
    assert (
        PinWords.has_finite_special_simples(
            [
                Perm((3, 4, 2, 0, 1)),
                Perm((4, 1, 2, 3, 0)),
                Perm((4, 1, 0, 2, 3)),
                Perm((1, 0, 4, 2, 3)),
                Perm((4, 1, 0, 2, 3)),
                Perm((1, 2, 0, 4, 3)),
            ]
        )
        is False
    )
    assert (
        PinWords.has_finite_special_simples(
            [
                Perm((1, 4, 0, 3, 2)),
                Perm((2, 1, 3, 0, 4)),
                Perm((4, 3, 1, 0, 2)),
                Perm((1, 2, 3, 0)),
                Perm((1, 3, 0, 4, 2)),
                Perm((2, 0, 1)),
                Perm((2, 1, 4, 3, 0)),
            ]
        )
        is True
    )
    assert (
        PinWords.has_finite_special_simples(
            [
                Perm((1, 3, 2, 4, 0)),
                Perm((0, 1, 3, 2, 4)),
                Perm((2, 3, 0, 1)),
                Perm((2, 1, 0, 3, 4)),
                Perm((2, 0, 1)),
                Perm((4, 2, 1, 3, 0)),
                Perm((3, 0, 1, 2, 4)),
                Perm((3, 1, 2, 4, 0)),
            ]
        )
        is True
    )
    assert (
        PinWords.has_finite_special_simples(
            [
                Perm((3, 2, 0, 1)),
                Perm((2, 1, 3, 0, 4)),
                Perm((4, 3, 2, 0, 1)),
                Perm((0, 2, 1, 3)),
                Perm((2, 1, 3, 4, 0)),
                Perm((1, 2, 3, 0, 4)),
                Perm((0, 2, 1, 4, 3)),
                Perm((2, 4, 3, 0, 1)),
                Perm((0, 1, 2, 3)),
            ]
        )
        is True
    )
    assert (
        PinWords.has_finite_special_simples(
            [
                Perm((0, 2, 1, 4, 3)),
                Perm((0, 3, 4, 2, 1)),
                Perm((2, 3, 1, 0)),
                Perm((4, 2, 3, 0, 1)),
                Perm((1, 2, 3, 4, 0)),
                Perm((4, 0, 3, 2, 1)),
                Perm((1, 3, 0, 2)),
                Perm((0, 3, 4, 1, 2)),
                Perm((0, 4, 2, 3, 1)),
                Perm((2, 3, 4, 1, 0)),
            ]
        )
        is True
    )
    assert (
        PinWords.has_finite_special_simples(
            [
                Perm((1, 3, 2, 0, 4)),
                Perm((0, 1, 2, 4, 3)),
                Perm((1, 3, 0, 4, 2)),
                Perm((1, 4, 0, 2, 3)),
                Perm((2, 1, 0, 3, 4)),
                Perm((2, 1, 3, 0)),
                Perm((4, 1, 3, 0, 2)),
                Perm((1, 2, 0, 3)),
                Perm((3, 1, 4, 2, 0)),
                Perm((1, 0)),
                Perm((0, 3, 1, 4, 2)),
            ]
        )
        is True
    )
    assert (
        PinWords.has_finite_special_simples(
            [
                Perm((2, 1, 0, 3)),
                Perm((3, 0, 2, 4, 1)),
                Perm((1, 2, 3, 0, 4)),
                Perm((3, 1, 4, 0, 2)),
                Perm((3, 0, 2, 4, 1)),
                Perm((0, 2, 1, 3)),
                Perm((3, 2, 0, 1, 4)),
                Perm((1, 3, 0, 2)),
                Perm((3, 4, 2, 0, 1)),
                Perm((2, 1, 0, 4, 3)),
                Perm((4, 0, 2, 1, 3)),
                Perm((1, 2, 3, 4, 0)),
            ]
        )
        is True
    )
    assert (
        PinWords.has_finite_special_simples(
            [
                Perm((1, 3, 0, 2)),
                Perm((1, 0, 4, 2, 3)),
                Perm((0,)),
                Perm((1, 0, 2)),
                Perm((1, 2, 0, 3)),
                Perm((2, 4, 1, 3, 0)),
                Perm((4, 2, 1, 3, 0)),
                Perm((0, 2, 3, 1, 4)),
                Perm((4, 3, 2, 0, 1)),
                Perm((0, 2, 4, 1, 3)),
                Perm((2, 0, 1, 3, 4)),
                Perm((0, 2, 3, 4, 1)),
                Perm((2, 3, 1, 4, 0)),
            ]
        )
        is True
    )
    assert (
        PinWords.has_finite_special_simples(
            [
                Perm((3, 4, 2, 0, 1)),
                Perm((0, 2, 1, 3)),
                Perm((2, 0, 1, 4, 3)),
                Perm((1, 4, 2, 3, 0)),
                Perm((0, 4, 2, 3, 1)),
                Perm((3, 1, 0, 4, 2)),
                Perm((4, 2, 0, 1, 3)),
                Perm((2, 0, 1, 4, 3)),
                Perm((1, 4, 0, 2, 3)),
                Perm((3, 2, 0, 4, 1)),
                Perm((1, 0, 2, 3)),
                Perm((0, 4, 1, 2, 3)),
                Perm((0, 1, 2, 3, 4)),
                Perm((1, 4, 3, 2, 0)),
            ]
        )
        is True
    )
    assert (
        PinWords.has_finite_special_simples(
            [
                Perm((0, 1, 2, 3)),
                Perm((0, 4, 3, 1, 2)),
                Perm((2, 3, 0, 4, 1)),
                Perm((0, 4, 2, 1, 3)),
                Perm((4, 1, 0, 2, 3)),
                Perm((4, 1, 3, 2, 0)),
                Perm((3, 4, 1, 0, 2)),
                Perm((0, 2, 1, 3, 4)),
                Perm((1, 4, 2, 0, 3)),
                Perm((2, 4, 3, 1, 0)),
                Perm((4, 3, 0, 2, 1)),
                Perm((0, 2, 4, 1, 3)),
                Perm((3, 0, 1, 2, 4)),
                Perm((3, 2, 1, 0)),
                Perm((1, 0, 3, 4, 2)),
            ]
        )
        is True
    )


def test_store_dfa_for_perm():
    perm = Perm.from_string("21043")
    PinWords.store_dfa_for_perm(perm)
    path = Path(f"dfa_db/S{len(perm)}/{perm}.txt")
    assert path.is_file()

    perm = Perm.from_string("12340")
    PinWords.store_dfa_for_perm(perm)
    path = Path(f"dfa_db/S{len(perm)}/{perm}.txt")
    assert path.is_file()

    perm = Perm.from_string("20314")
    PinWords.store_dfa_for_perm(perm)
    path = Path(f"dfa_db/S{len(perm)}/{perm}.txt")
    assert path.is_file()

    perm = Perm.from_string("2130")
    PinWords.store_dfa_for_perm(perm)
    path = Path(f"dfa_db/S{len(perm)}/{perm}.txt")
    assert path.is_file()

    perm = Perm.from_string("31402")
    PinWords.store_dfa_for_perm(perm)
    path = Path(f"dfa_db/S{len(perm)}/{perm}.txt")
    assert path.is_file()

    perm = Perm.from_string("1302")
    PinWords.store_dfa_for_perm(perm)
    path = Path(f"dfa_db/S{len(perm)}/{perm}.txt")
    assert path.is_file()

    perm = Perm.from_string("1023")
    PinWords.store_dfa_for_perm(perm)
    path = Path(f"dfa_db/S{len(perm)}/{perm}.txt")
    assert path.is_file()

    perm = Perm.from_string("01243")
    PinWords.store_dfa_for_perm(perm)
    path = Path(f"dfa_db/S{len(perm)}/{perm}.txt")
    assert path.is_file()

    perm = Perm.from_string("34201")
    PinWords.store_dfa_for_perm(perm)
    path = Path(f"dfa_db/S{len(perm)}/{perm}.txt")
    assert path.is_file()

    perm = Perm.from_string("012")
    PinWords.store_dfa_for_perm(perm)
    path = Path(f"dfa_db/S{len(perm)}/{perm}.txt")
    assert path.is_file()

    perm = Perm.from_string("12403")
    PinWords.store_dfa_for_perm(perm)
    path = Path(f"dfa_db/S{len(perm)}/{perm}.txt")
    assert path.is_file()

    perm = Perm.from_string("01342")
    PinWords.store_dfa_for_perm(perm)
    path = Path(f"dfa_db/S{len(perm)}/{perm}.txt")
    assert path.is_file()

    perm = Perm.from_string("32014")
    PinWords.store_dfa_for_perm(perm)
    path = Path(f"dfa_db/S{len(perm)}/{perm}.txt")
    assert path.is_file()

    perm = Perm.from_string("2103")
    PinWords.store_dfa_for_perm(perm)
    path = Path(f"dfa_db/S{len(perm)}/{perm}.txt")
    assert path.is_file()

    perm = Perm.from_string("42301")
    PinWords.store_dfa_for_perm(perm)
    path = Path(f"dfa_db/S{len(perm)}/{perm}.txt")
    assert path.is_file()


def test_load_dfa_for_perm():
    assert PinWords.load_dfa_for_perm(Perm.from_string("31024")) == DFA(
        states={
            "4",
            "26",
            "41",
            "11",
            "12",
            "28",
            "24",
            "23",
            "20",
            "17",
            "39",
            "10",
            "27",
            "44",
            "3",
            "22",
            "19",
            "29",
            "38",
            "36",
            "34",
            "8",
            "33",
            "40",
            "15",
            "30",
            "46",
            "42",
            "16",
            "31",
            "32",
            "35",
            "0",
            "43",
            "21",
            "14",
            "7",
            "25",
            "2",
            "13",
            "5",
            "45",
            "9",
            "6",
            "1",
            "37",
            "18",
        },
        input_symbols={"U", "L", "R", "D"},
        transitions={
            "16": {"L": "21", "D": "5", "U": "30", "R": "16"},
            "5": {"L": "7", "D": "11", "U": "20", "R": "8"},
            "13": {"L": "13", "D": "13", "U": "13", "R": "13"},
            "15": {"L": "43", "D": "11", "U": "20", "R": "8"},
            "34": {"L": "13", "D": "31", "U": "19", "R": "27"},
            "42": {"L": "9", "D": "15", "U": "4", "R": "25"},
            "33": {"L": "12", "D": "31", "U": "19", "R": "22"},
            "17": {"L": "9", "D": "15", "U": "18", "R": "25"},
            "20": {"L": "42", "D": "11", "U": "20", "R": "28"},
            "44": {"L": "12", "D": "12", "U": "44", "R": "13"},
            "7": {"L": "9", "D": "18", "U": "4", "R": "25"},
            "23": {"L": "21", "D": "18", "U": "15", "R": "16"},
            "10": {"L": "16", "D": "10", "U": "10", "R": "21"},
            "18": {"L": "0", "D": "31", "U": "19", "R": "27"},
            "8": {"L": "9", "D": "12", "U": "18", "R": "25"},
            "40": {"L": "38", "D": "18", "U": "14", "R": "40"},
            "0": {"L": "38", "D": "18", "U": "12", "R": "40"},
            "26": {"L": "36", "D": "10", "U": "10", "R": "36"},
            "27": {"L": "38", "D": "12", "U": "34", "R": "40"},
            "39": {"L": "38", "D": "18", "U": "34", "R": "40"},
            "11": {"L": "7", "D": "11", "U": "20", "R": "17"},
            "30": {"L": "28", "D": "37", "U": "29", "R": "24"},
            "38": {"L": "38", "D": "31", "U": "12", "R": "40"},
            "45": {"L": "43", "D": "11", "U": "20", "R": "41"},
            "43": {"L": "38", "D": "18", "U": "33", "R": "40"},
            "4": {"L": "43", "D": "11", "U": "20", "R": "12"},
            "37": {"L": "23", "D": "37", "U": "29", "R": "6"},
            "12": {"L": "12", "D": "12", "U": "44", "R": "46"},
            "14": {"L": "13", "D": "31", "U": "19", "R": "39"},
            "46": {"L": "12", "D": "12", "U": "13", "R": "46"},
            "35": {"L": "13", "D": "12", "U": "44", "R": "13"},
            "32": {"L": "7", "D": "11", "U": "20", "R": "12"},
            "29": {"L": "6", "D": "37", "U": "29", "R": "23"},
            "31": {"L": "0", "D": "31", "U": "19", "R": "39"},
            "19": {"L": "12", "D": "31", "U": "19", "R": "39"},
            "2": {"L": "43", "D": "11", "U": "20", "R": "1"},
            "3": {"L": "12", "D": "31", "U": "19", "R": "27"},
            "41": {"L": "9", "D": "18", "U": "18", "R": "25"},
            "22": {"L": "12", "D": "12", "U": "35", "R": "46"},
            "28": {"L": "38", "D": "18", "U": "3", "R": "40"},
            "21": {"L": "21", "D": "30", "U": "5", "R": "16"},
            "25": {"L": "9", "D": "5", "U": "31", "R": "25"},
            "36": {"L": "36", "D": "29", "U": "37", "R": "36"},
            "24": {"L": "9", "D": "18", "U": "2", "R": "25"},
            "9": {"L": "9", "D": "45", "U": "32", "R": "25"},
            "6": {"L": "9", "D": "15", "U": "2", "R": "25"},
            "1": {"L": "38", "D": "12", "U": "3", "R": "40"},
        },
        initial_state="26",
        final_states={"13"},
    )
    assert PinWords.load_dfa_for_perm(Perm.from_string("01324")) == DFA(
        states={
            "80",
            "106",
            "28",
            "17",
            "81",
            "10",
            "97",
            "55",
            "36",
            "68",
            "16",
            "32",
            "77",
            "21",
            "53",
            "92",
            "123",
            "47",
            "117",
            "72",
            "58",
            "108",
            "61",
            "86",
            "9",
            "18",
            "4",
            "91",
            "65",
            "12",
            "95",
            "88",
            "102",
            "44",
            "22",
            "76",
            "74",
            "8",
            "89",
            "104",
            "33",
            "51",
            "15",
            "115",
            "128",
            "111",
            "69",
            "90",
            "114",
            "14",
            "59",
            "101",
            "2",
            "87",
            "105",
            "126",
            "37",
            "83",
            "26",
            "41",
            "99",
            "11",
            "93",
            "23",
            "54",
            "71",
            "20",
            "103",
            "27",
            "78",
            "19",
            "29",
            "38",
            "73",
            "52",
            "40",
            "84",
            "46",
            "131",
            "107",
            "49",
            "62",
            "31",
            "116",
            "35",
            "0",
            "96",
            "120",
            "127",
            "100",
            "110",
            "70",
            "13",
            "124",
            "34",
            "45",
            "6",
            "125",
            "119",
            "130",
            "98",
            "113",
            "24",
            "75",
            "39",
            "79",
            "3",
            "129",
            "109",
            "121",
            "30",
            "42",
            "57",
            "112",
            "43",
            "63",
            "94",
            "56",
            "64",
            "50",
            "122",
            "7",
            "118",
            "25",
            "82",
            "5",
            "48",
            "66",
            "67",
            "85",
            "60",
            "1",
        },
        input_symbols={"U", "L", "R", "D"},
        transitions={
            "90": {"L": "75", "D": "41", "U": "106", "R": "82"},
            "13": {"L": "97", "D": "71", "U": "3", "R": "13"},
            "96": {"L": "97", "D": "108", "U": "3", "R": "13"},
            "98": {"L": "6", "D": "0", "U": "11", "R": "33"},
            "105": {"L": "118", "D": "7", "U": "130", "R": "66"},
            "42": {"L": "24", "D": "42", "U": "42", "R": "32"},
            "33": {"L": "6", "D": "40", "U": "11", "R": "33"},
            "67": {"L": "54", "D": "103", "U": "21", "R": "47"},
            "53": {"L": "54", "D": "109", "U": "74", "R": "122"},
            "44": {"L": "102", "D": "94", "U": "113", "R": "44"},
            "80": {"L": "97", "D": "0", "U": "10", "R": "13"},
            "18": {"L": "59", "D": "53", "U": "9", "R": "18"},
            "92": {"L": "75", "D": "41", "U": "3", "R": "92"},
            "73": {"L": "59", "D": "39", "U": "9", "R": "18"},
            "114": {"L": "97", "D": "108", "U": "120", "R": "13"},
            "77": {"L": "23", "D": "77", "U": "104", "R": "70"},
            "85": {"L": "75", "D": "112", "U": "106", "R": "92"},
            "122": {"L": "59", "D": "37", "U": "90", "R": "18"},
            "88": {"L": "29", "D": "43", "U": "11", "R": "88"},
            "60": {"L": "4", "D": "15", "U": "60", "R": "100"},
            "56": {"L": "20", "D": "56", "U": "127", "R": "55"},
            "31": {"L": "59", "D": "63", "U": "105", "R": "18"},
            "19": {"L": "48", "D": "43", "U": "121", "R": "129"},
            "86": {"L": "34", "D": "123", "U": "90", "R": "83"},
            "113": {"L": "91", "D": "126", "U": "78", "R": "111"},
            "51": {"L": "51", "D": "117", "U": "14", "R": "16"},
            "49": {"L": "57", "D": "56", "U": "127", "R": "110"},
            "95": {"L": "19", "D": "41", "U": "106", "R": "92"},
            "0": {"L": "27", "D": "77", "U": "104", "R": "70"},
            "78": {"L": "25", "D": "126", "U": "78", "R": "124"},
            "61": {"L": "75", "D": "41", "U": "106", "R": "66"},
            "36": {"L": "36", "D": "60", "U": "15", "R": "36"},
            "16": {"L": "51", "D": "67", "U": "116", "R": "16"},
            "34": {"L": "34", "D": "20", "U": "89", "R": "83"},
            "115": {"L": "29", "D": "43", "U": "115", "R": "11"},
            "64": {"L": "111", "D": "79", "U": "81", "R": "11"},
            "126": {"L": "100", "D": "126", "U": "78", "R": "46"},
            "69": {"L": "97", "D": "108", "U": "2", "R": "13"},
            "110": {"L": "75", "D": "41", "U": "17", "R": "92"},
            "4": {"L": "51", "D": "39", "U": "12", "R": "16"},
            "63": {"L": "75", "D": "41", "U": "106", "R": "92"},
            "68": {"L": "97", "D": "52", "U": "3", "R": "13"},
            "55": {"L": "34", "D": "123", "U": "9", "R": "83"},
            "87": {"L": "20", "D": "56", "U": "127", "R": "86"},
            "12": {"L": "99", "D": "109", "U": "74", "R": "50"},
            "14": {"L": "31", "D": "103", "U": "21", "R": "91"},
            "124": {"L": "102", "D": "116", "U": "125", "R": "44"},
            "116": {"L": "57", "D": "56", "U": "127", "R": "50"},
            "41": {"L": "23", "D": "41", "U": "106", "R": "92"},
            "128": {"L": "36", "D": "42", "U": "42", "R": "36"},
            "72": {"L": "99", "D": "109", "U": "74", "R": "0"},
            "21": {"L": "8", "D": "103", "U": "21", "R": "91"},
            "79": {"L": "111", "D": "79", "U": "81", "R": "62"},
            "50": {"L": "75", "D": "41", "U": "2", "R": "92"},
            "123": {"L": "20", "D": "56", "U": "127", "R": "50"},
            "109": {"L": "54", "D": "109", "U": "74", "R": "73"},
            "125": {"L": "0", "D": "79", "U": "81", "R": "98"},
            "24": {"L": "32", "D": "101", "U": "93", "R": "24"},
            "58": {"L": "97", "D": "108", "U": "23", "R": "13"},
            "1": {"L": "51", "D": "39", "U": "116", "R": "16"},
            "120": {"L": "118", "D": "7", "U": "130", "R": "23"},
            "48": {"L": "48", "D": "11", "U": "121", "R": "129"},
            "5": {"L": "97", "D": "125", "U": "10", "R": "13"},
            "82": {"L": "27", "D": "77", "U": "115", "R": "70"},
            "112": {"L": "29", "D": "76", "U": "121", "R": "129"},
            "52": {"L": "0", "D": "7", "U": "130", "R": "96"},
            "93": {"L": "91", "D": "126", "U": "78", "R": "114"},
            "104": {"L": "27", "D": "77", "U": "104", "R": "11"},
            "17": {"L": "27", "D": "77", "U": "104", "R": "88"},
            "76": {"L": "11", "D": "76", "U": "121", "R": "129"},
            "20": {"L": "48", "D": "76", "U": "121", "R": "129"},
            "71": {"L": "111", "D": "7", "U": "130", "R": "96"},
            "7": {"L": "111", "D": "7", "U": "130", "R": "68"},
            "8": {"L": "51", "D": "117", "U": "12", "R": "16"},
            "40": {"L": "111", "D": "79", "U": "81", "R": "98"},
            "26": {"L": "31", "D": "109", "U": "74", "R": "107"},
            "39": {"L": "63", "D": "109", "U": "74", "R": "69"},
            "43": {"L": "11", "D": "43", "U": "115", "R": "88"},
            "70": {"L": "27", "D": "77", "U": "11", "R": "70"},
            "46": {"L": "59", "D": "39", "U": "72", "R": "18"},
            "29": {"L": "29", "D": "11", "U": "115", "R": "88"},
            "35": {"L": "34", "D": "20", "U": "49", "R": "83"},
            "106": {"L": "75", "D": "41", "U": "106", "R": "65"},
            "121": {"L": "48", "D": "76", "U": "121", "R": "65"},
            "2": {"L": "75", "D": "41", "U": "106", "R": "23"},
            "47": {"L": "59", "D": "37", "U": "61", "R": "18"},
            "107": {"L": "34", "D": "123", "U": "0", "R": "83"},
            "89": {"L": "57", "D": "56", "U": "127", "R": "107"},
            "99": {"L": "34", "D": "95", "U": "61", "R": "83"},
            "25": {"L": "59", "D": "39", "U": "119", "R": "18"},
            "54": {"L": "97", "D": "108", "U": "10", "R": "13"},
            "84": {"L": "59", "D": "37", "U": "0", "R": "18"},
            "101": {"L": "31", "D": "103", "U": "21", "R": "47"},
            "81": {"L": "131", "D": "79", "U": "81", "R": "11"},
            "129": {"L": "48", "D": "76", "U": "3", "R": "129"},
            "119": {"L": "99", "D": "109", "U": "74", "R": "110"},
            "15": {"L": "100", "D": "15", "U": "60", "R": "4"},
            "102": {"L": "102", "D": "93", "U": "45", "R": "44"},
            "83": {"L": "34", "D": "87", "U": "9", "R": "83"},
            "100": {"L": "102", "D": "116", "U": "30", "R": "44"},
            "59": {"L": "59", "D": "117", "U": "26", "R": "18"},
            "23": {"L": "29", "D": "43", "U": "115", "R": "88"},
            "10": {"L": "118", "D": "7", "U": "130", "R": "65"},
            "117": {"L": "118", "D": "7", "U": "130", "R": "96"},
            "130": {"L": "5", "D": "7", "U": "130", "R": "65"},
            "27": {"L": "27", "D": "23", "U": "104", "R": "70"},
            "74": {"L": "28", "D": "109", "U": "74", "R": "107"},
            "103": {"L": "54", "D": "103", "U": "21", "R": "1"},
            "111": {"L": "6", "D": "0", "U": "22", "R": "33"},
            "127": {"L": "35", "D": "56", "U": "127", "R": "107"},
            "11": {"L": "11", "D": "11", "U": "11", "R": "11"},
            "65": {"L": "48", "D": "76", "U": "23", "R": "129"},
            "30": {"L": "118", "D": "7", "U": "130", "R": "58"},
            "131": {"L": "6", "D": "125", "U": "22", "R": "33"},
            "108": {"L": "27", "D": "41", "U": "106", "R": "92"},
            "45": {"L": "31", "D": "109", "U": "74", "R": "84"},
            "38": {"L": "80", "D": "7", "U": "130", "R": "65"},
            "37": {"L": "85", "D": "56", "U": "127", "R": "50"},
            "66": {"L": "75", "D": "41", "U": "23", "R": "92"},
            "57": {"L": "34", "D": "20", "U": "61", "R": "83"},
            "118": {"L": "75", "D": "77", "U": "106", "R": "92"},
            "32": {"L": "32", "D": "93", "U": "101", "R": "24"},
            "94": {"L": "31", "D": "109", "U": "74", "R": "122"},
            "97": {"L": "97", "D": "125", "U": "38", "R": "13"},
            "3": {"L": "48", "D": "76", "U": "121", "R": "23"},
            "91": {"L": "34", "D": "123", "U": "61", "R": "83"},
            "28": {"L": "59", "D": "117", "U": "119", "R": "18"},
            "22": {"L": "0", "D": "79", "U": "81", "R": "11"},
            "62": {"L": "6", "D": "125", "U": "11", "R": "33"},
            "9": {"L": "57", "D": "56", "U": "127", "R": "0"},
            "6": {"L": "6", "D": "125", "U": "64", "R": "33"},
            "75": {"L": "75", "D": "23", "U": "106", "R": "92"},
        },
        initial_state="128",
        final_states={"11"},
    )
    assert PinWords.load_dfa_for_perm(Perm.from_string("42310")) == DFA(
        states={
            "80",
            "106",
            "28",
            "17",
            "81",
            "10",
            "97",
            "55",
            "36",
            "68",
            "16",
            "32",
            "77",
            "21",
            "53",
            "92",
            "123",
            "47",
            "117",
            "58",
            "72",
            "108",
            "61",
            "9",
            "86",
            "18",
            "4",
            "65",
            "91",
            "12",
            "95",
            "88",
            "102",
            "44",
            "22",
            "76",
            "74",
            "8",
            "89",
            "33",
            "104",
            "15",
            "51",
            "115",
            "128",
            "111",
            "69",
            "114",
            "90",
            "14",
            "59",
            "101",
            "2",
            "87",
            "105",
            "126",
            "37",
            "99",
            "26",
            "41",
            "83",
            "11",
            "93",
            "23",
            "54",
            "71",
            "20",
            "103",
            "27",
            "78",
            "19",
            "29",
            "38",
            "73",
            "52",
            "40",
            "84",
            "131",
            "46",
            "107",
            "49",
            "62",
            "31",
            "0",
            "116",
            "35",
            "96",
            "120",
            "127",
            "100",
            "110",
            "70",
            "13",
            "124",
            "45",
            "34",
            "6",
            "125",
            "130",
            "119",
            "98",
            "113",
            "24",
            "75",
            "39",
            "79",
            "3",
            "129",
            "109",
            "121",
            "30",
            "42",
            "57",
            "112",
            "63",
            "56",
            "94",
            "43",
            "64",
            "50",
            "7",
            "122",
            "118",
            "25",
            "82",
            "5",
            "48",
            "66",
            "67",
            "85",
            "60",
            "1",
        },
        input_symbols={"U", "L", "R", "D"},
        transitions={
            "29": {"D": "22", "L": "125", "U": "112", "R": "114"},
            "65": {"D": "65", "L": "65", "U": "65", "R": "65"},
            "74": {"D": "21", "L": "6", "U": "5", "R": "131"},
            "32": {"D": "37", "L": "38", "U": "78", "R": "32"},
            "35": {"D": "20", "L": "37", "U": "109", "R": "77"},
            "19": {"D": "122", "L": "65", "U": "19", "R": "36"},
            "30": {"D": "30", "L": "57", "U": "41", "R": "121"},
            "52": {"D": "3", "L": "104", "U": "123", "R": "42"},
            "27": {"D": "82", "L": "27", "U": "74", "R": "43"},
            "23": {"D": "122", "L": "40", "U": "19", "R": "75"},
            "131": {"D": "105", "L": "117", "U": "49", "R": "89"},
            "111": {"D": "114", "L": "25", "U": "127", "R": "92"},
            "42": {"D": "15", "L": "73", "U": "119", "R": "76"},
            "1": {"D": "94", "L": "130", "U": "91", "R": "62"},
            "118": {"D": "22", "L": "97", "U": "112", "R": "111"},
            "0": {"D": "65", "L": "96", "U": "4", "R": "0"},
            "11": {"D": "15", "L": "73", "U": "37", "R": "76"},
            "3": {"D": "3", "L": "68", "U": "123", "R": "42"},
            "58": {"D": "22", "L": "93", "U": "112", "R": "121"},
            "91": {"D": "15", "L": "37", "U": "119", "R": "76"},
            "124": {"D": "21", "L": "7", "U": "5", "R": "131"},
            "87": {"D": "87", "L": "96", "U": "4", "R": "65"},
            "49": {"D": "79", "L": "12", "U": "54", "R": "70"},
            "25": {"D": "58", "L": "25", "U": "85", "R": "92"},
            "21": {"D": "21", "L": "63", "U": "5", "R": "110"},
            "92": {"D": "90", "L": "25", "U": "118", "R": "92"},
            "34": {"D": "34", "L": "18", "U": "34", "R": "66"},
            "45": {"D": "34", "L": "47", "U": "34", "R": "47"},
            "8": {"D": "15", "L": "73", "U": "119", "R": "0"},
            "128": {"D": "42", "L": "117", "U": "49", "R": "89"},
            "97": {"D": "105", "L": "117", "U": "75", "R": "89"},
            "31": {"D": "29", "L": "26", "U": "102", "R": "44"},
            "64": {"D": "79", "L": "64", "U": "91", "R": "70"},
            "76": {"D": "65", "L": "73", "U": "119", "R": "76"},
            "61": {"D": "8", "L": "64", "U": "54", "R": "70"},
            "121": {"D": "126", "L": "130", "U": "10", "R": "62"},
            "130": {"D": "14", "L": "130", "U": "91", "R": "62"},
            "81": {"D": "23", "L": "59", "U": "120", "R": "81"},
            "17": {"D": "98", "L": "110", "U": "17", "R": "31"},
            "113": {"D": "126", "L": "130", "U": "37", "R": "62"},
            "71": {"D": "22", "L": "39", "U": "112", "R": "60"},
            "122": {"D": "122", "L": "107", "U": "19", "R": "6"},
            "103": {"D": "53", "L": "27", "U": "23", "R": "43"},
            "72": {"D": "87", "L": "73", "U": "119", "R": "76"},
            "36": {"D": "23", "L": "59", "U": "16", "R": "81"},
            "116": {"D": "79", "L": "106", "U": "54", "R": "70"},
            "67": {"D": "75", "L": "130", "U": "10", "R": "62"},
            "6": {"D": "75", "L": "59", "U": "16", "R": "81"},
            "126": {"D": "79", "L": "64", "U": "54", "R": "32"},
            "43": {"D": "124", "L": "27", "U": "48", "R": "43"},
            "73": {"D": "15", "L": "73", "U": "91", "R": "76"},
            "4": {"D": "87", "L": "65", "U": "4", "R": "0"},
            "98": {"D": "98", "L": "31", "U": "17", "R": "110"},
            "59": {"D": "9", "L": "59", "U": "65", "R": "81"},
            "127": {"D": "20", "L": "12", "U": "109", "R": "77"},
            "110": {"D": "53", "L": "27", "U": "24", "R": "43"},
            "68": {"D": "105", "L": "117", "U": "85", "R": "89"},
            "22": {"D": "22", "L": "51", "U": "112", "R": "121"},
            "18": {"D": "124", "L": "66", "U": "108", "R": "18"},
            "63": {"D": "29", "L": "25", "U": "84", "R": "92"},
            "96": {"D": "87", "L": "96", "U": "65", "R": "0"},
            "77": {"D": "100", "L": "64", "U": "54", "R": "70"},
            "112": {"D": "22", "L": "97", "U": "112", "R": "28"},
            "60": {"D": "83", "L": "117", "U": "49", "R": "89"},
            "105": {"D": "3", "L": "13", "U": "123", "R": "42"},
            "78": {"D": "100", "L": "65", "U": "78", "R": "32"},
            "70": {"D": "37", "L": "64", "U": "54", "R": "70"},
            "39": {"D": "79", "L": "64", "U": "50", "R": "70"},
            "55": {"D": "30", "L": "131", "U": "41", "R": "111"},
            "100": {"D": "100", "L": "38", "U": "78", "R": "37"},
            "7": {"D": "126", "L": "130", "U": "35", "R": "62"},
            "20": {"D": "20", "L": "1", "U": "109", "R": "6"},
            "129": {"D": "30", "L": "33", "U": "41", "R": "121"},
            "5": {"D": "21", "L": "103", "U": "5", "R": "2"},
            "104": {"D": "105", "L": "117", "U": "116", "R": "89"},
            "62": {"D": "23", "L": "130", "U": "95", "R": "62"},
            "38": {"D": "100", "L": "38", "U": "65", "R": "32"},
            "66": {"D": "108", "L": "66", "U": "124", "R": "18"},
            "117": {"D": "52", "L": "117", "U": "85", "R": "89"},
            "2": {"D": "29", "L": "25", "U": "71", "R": "92"},
            "53": {"D": "3", "L": "13", "U": "123", "R": "128"},
            "14": {"D": "20", "L": "99", "U": "109", "R": "6"},
            "99": {"D": "126", "L": "130", "U": "91", "R": "62"},
            "84": {"D": "22", "L": "75", "U": "112", "R": "60"},
            "46": {"D": "3", "L": "97", "U": "123", "R": "128"},
            "12": {"D": "79", "L": "64", "U": "37", "R": "70"},
            "37": {"D": "87", "L": "96", "U": "4", "R": "0"},
            "106": {"D": "100", "L": "38", "U": "4", "R": "32"},
            "86": {"D": "3", "L": "39", "U": "123", "R": "128"},
            "44": {"D": "90", "L": "26", "U": "55", "R": "44"},
            "50": {"D": "100", "L": "96", "U": "78", "R": "32"},
            "102": {"D": "22", "L": "13", "U": "112", "R": "60"},
            "28": {"D": "90", "L": "25", "U": "71", "R": "92"},
            "82": {"D": "22", "L": "93", "U": "112", "R": "111"},
            "119": {"D": "15", "L": "11", "U": "119", "R": "76"},
            "85": {"D": "3", "L": "75", "U": "123", "R": "128"},
            "123": {"D": "3", "L": "97", "U": "123", "R": "69"},
            "56": {"D": "23", "L": "130", "U": "10", "R": "62"},
            "95": {"D": "20", "L": "11", "U": "109", "R": "67"},
            "90": {"D": "20", "L": "99", "U": "109", "R": "77"},
            "48": {"D": "22", "L": "80", "U": "112", "R": "111"},
            "41": {"D": "30", "L": "131", "U": "41", "R": "115"},
            "57": {"D": "29", "L": "26", "U": "53", "R": "44"},
            "88": {"D": "79", "L": "37", "U": "54", "R": "70"},
            "16": {"D": "122", "L": "65", "U": "19", "R": "75"},
            "40": {"D": "75", "L": "59", "U": "65", "R": "81"},
            "9": {"D": "122", "L": "40", "U": "19", "R": "6"},
            "101": {"D": "3", "L": "13", "U": "123", "R": "61"},
            "94": {"D": "20", "L": "99", "U": "109", "R": "75"},
            "26": {"D": "129", "L": "26", "U": "53", "R": "44"},
            "69": {"D": "42", "L": "117", "U": "86", "R": "89"},
            "10": {"D": "20", "L": "11", "U": "109", "R": "77"},
            "51": {"D": "29", "L": "25", "U": "85", "R": "92"},
            "47": {"D": "17", "L": "47", "U": "98", "R": "47"},
            "120": {"D": "122", "L": "65", "U": "19", "R": "6"},
            "93": {"D": "101", "L": "25", "U": "116", "R": "92"},
            "13": {"D": "79", "L": "64", "U": "88", "R": "70"},
            "115": {"D": "90", "L": "26", "U": "102", "R": "44"},
            "15": {"D": "15", "L": "73", "U": "119", "R": "65"},
            "79": {"D": "79", "L": "64", "U": "54", "R": "37"},
            "107": {"D": "23", "L": "59", "U": "65", "R": "81"},
            "33": {"D": "101", "L": "25", "U": "49", "R": "92"},
            "75": {"D": "100", "L": "38", "U": "78", "R": "32"},
            "24": {"D": "20", "L": "113", "U": "109", "R": "77"},
            "54": {"D": "79", "L": "11", "U": "54", "R": "70"},
            "108": {"D": "30", "L": "33", "U": "41", "R": "111"},
            "80": {"D": "101", "L": "25", "U": "75", "R": "92"},
            "83": {"D": "79", "L": "64", "U": "54", "R": "72"},
            "89": {"D": "42", "L": "117", "U": "46", "R": "89"},
            "114": {"D": "79", "L": "64", "U": "54", "R": "70"},
            "125": {"D": "126", "L": "130", "U": "88", "R": "62"},
            "109": {"D": "20", "L": "11", "U": "109", "R": "56"},
        },
        initial_state="45",
        final_states={"65"},
    )


def test_create_dfa_db_for_length():
    PinWords.create_dfa_db_for_length(1)
    for perm in Perm.of_length(1):
        assert PinWords.load_dfa_for_perm(perm) == PinWords.make_dfa_for_perm(perm)

    PinWords.create_dfa_db_for_length(2)
    for perm in Perm.of_length(2):
        assert PinWords.load_dfa_for_perm(perm) == PinWords.make_dfa_for_perm(perm)

    PinWords.create_dfa_db_for_length(3)
    for perm in Perm.of_length(3):
        assert PinWords.load_dfa_for_perm(perm) == PinWords.make_dfa_for_perm(perm)

    PinWords.create_dfa_db_for_length(4)
    for perm in Perm.of_length(4):
        assert PinWords.load_dfa_for_perm(perm) == PinWords.make_dfa_for_perm(perm)
