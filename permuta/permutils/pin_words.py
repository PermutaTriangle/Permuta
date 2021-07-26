# pylint: disable=too-many-public-methods
# pylint: disable=eval-used


from bisect import bisect_left
from collections import defaultdict
from functools import lru_cache
from pathlib import Path
from typing import DefaultDict, Dict, Iterator, List, Set, Tuple

from automata.fa.dfa import DFA
from automata.fa.nfa import NFA

from permuta import Av, Perm
from permuta.permutils import all_symmetry_sets
from permuta.permutils.pinword_util import PinWordUtil

DIRS = "ULDR"
QUADS = "1234"


class PinWords:
    """Class for pinowords"""

    @staticmethod
    def pinword_to_perm(word: str) -> "Perm":
        """Returns the permutation corresponding to a given pinword.

        Examples:
            >>> PinWords.pinword_to_perm("31")
            Perm((0, 1))
            >>> PinWords.pinword_to_perm("4R")
            Perm((0, 1))
            >>> PinWords.pinword_to_perm("3DL2UR")
            Perm((3, 5, 1, 2, 0, 4))
            >>> PinWords.pinword_to_perm("14L2UR")
            Perm((3, 5, 1, 2, 0, 4))
        """
        pwu = PinWordUtil()
        pre_perm = [(pwu.rzero(), pwu.rzero())]

        for char in word:
            next_x, next_y = pwu.call(char, pre_perm)
            if not (next_x and next_y):
                assert False
            pre_perm.append((next_x, next_y))

        pre_perm.pop(0)
        pre_perm.sort()
        sorted_y_coord = sorted(x[1] for x in pre_perm)
        perm = tuple(bisect_left(sorted_y_coord, x[1]) for x in pre_perm)
        return Perm(perm)

    @classmethod
    def pinwords_of_length(cls, length: int) -> Iterator[str]:
        """
        Generates all pinwords of length n.
        Note that pinwords cannot contain any occurrence of:
        UU, UD, DU, DD, LL, LR, RL, RR
        """
        if length == 0:
            yield ""
        else:
            for word in cls.pinwords_of_length(length - 1):
                if len(word) > 0 and word[-1] != "U" and word[-1] != "D":
                    yield word + "U"
                    yield word + "D"
                if len(word) > 0 and word[-1] != "R" and word[-1] != "L":
                    yield word + "L"
                    yield word + "R"
                for char in QUADS:
                    yield word + char

    @classmethod
    @lru_cache(maxsize=None)
    def pinword_to_perm_mapping(cls, length: int) -> Dict[str, "Perm"]:
        """Returns a dict that maps pinword to it's corresponding Perm"""
        return {
            pinword: cls.pinword_to_perm(pinword)
            for pinword in cls.pinwords_of_length(length)
        }

    @classmethod
    @lru_cache(maxsize=None)
    def perm_to_pinword_mapping(cls, length: int) -> Dict:
        """Returns a dict that maps Perm to it's corresponding pinword"""
        res = defaultdict(set)
        for key, val in cls.pinword_to_perm_mapping(length).items():
            res[val].add(key)
        return res

    @staticmethod
    def is_strict_pinword(word: str) -> bool:
        """
        Returns True if w is a strict pinword, False otherwise
        """
        if word == "":
            return True  # paper does not mention the empty pinword
        return word[0] in QUADS and all(word[i] in DIRS for i in range(1, len(word)))

    @classmethod
    def strict_pinwords_of_length(cls, length: int) -> Iterator[str]:
        """Yields alld pinwords of specified length"""
        for word in cls.pinwords_of_length(length):
            if cls.is_strict_pinword(word):
                yield word

    @classmethod
    @lru_cache(maxsize=None)
    def perm_to_strict_pinword_mapping(cls, length: int) -> Dict:
        """Maps perms o pinword if the pinowrd is strict"""
        original = cls.perm_to_pinword_mapping(length)
        filtered = {
            k: {x for x in v if cls.is_strict_pinword(x)} for k, v in original.items()
        }
        return filtered

    @staticmethod
    def factor_pinword(word: str) -> List[str]:
        """
        Factors a pinword into its strong numeral led factor decomposition.

        Examples:
            >>> PinWords.factor_pinword("14L2UR")
            ['1', '4L', '2UR']
        """
        position = 0
        factor_list = []
        while position < len(word):
            cur = position + 1
            while cur < len(word) and word[cur] in DIRS:
                cur += 1
            factor_list.append(word[position:cur])
            position = cur
        return factor_list

    @staticmethod
    def sp_to_m(word: str) -> Tuple[str, ...]:
        """
        The bijection phi in Definition 3.9 mapping words in SP to words in M.
        Input must be a strict pin word. This implementation includes the extra
        definition given in Remark 3.11, mapping words in M to words in M.

        Examples:
            >>> PinWords.sp_to_m("1R")
            ('RUR',)
            >>> PinWords.sp_to_m("2UL")
            ('ULUL',)
            >>> PinWords.sp_to_m("3")
            ('LD', 'DL')
            >>> PinWords.sp_to_m("4D")
            ('DRD',)
        """
        if word == "":
            return ("",)
        if word[0] in QUADS:
            letter_dict = {"1": "RU", "2": "LU", "3": "LD", "4": "RD"}
            opposite = {"U": "D", "D": "U", "L": "R", "R": "L"}
            letters = letter_dict[word[0]]
            if len(word) == 1:
                return (letters, letters[::-1])
            if letters[1] == word[1] or letters[1] == opposite[word[1]]:
                letters = letters[::-1]
            return (letters + word[1:],)
        return (word,)

    @staticmethod
    def m_to_sp(word: str) -> str:
        """
        The bijection phi in Definition 3.9 mapping words in M to words in SP.

        Examples:
            >>> PinWords.m_to_sp("RUR")
            '1R'
            >>> PinWords.m_to_sp("ULUL")
            '2UL'
            >>> PinWords.m_to_sp("DL")
            '3'
            >>> PinWords.m_to_sp("LD")
            '3'
            >>> PinWords.m_to_sp("DRD")
            '4D'
        """
        letter_dict = {"1": "RU", "2": "LU", "3": "LD", "4": "RD"}
        rev_letter_dict = dict()
        for key, val in letter_dict.items():
            rev_letter_dict[val] = key
            rev_letter_dict[val[::-1]] = key
        return rev_letter_dict[word[0:2]] + word[2:]

    @classmethod
    def quadrant(cls, word: str, ind: int) -> str:
        """
        Determines the quadrant which point p_i in the pin representation resides in
        with respect to the origin p_0. (Lemma 3.10)

        Examples:
            >>> PinWords.quadrant("2RU4LULURD4L", 2)
            '1'
            >>> PinWords.quadrant("2RU4LULURD4L", 3)
            '4'
            >>> PinWords.quadrant("2RU4LULURD4L", 6)
            '2'
        """
        if word[ind] in QUADS:
            return word[ind]
        if word[ind - 1] in QUADS:
            return cls.m_to_sp(cls.sp_to_m(word[ind - 1 : ind + 1])[0][1:])
        return cls.m_to_sp(word[ind - 1 : ind + 1])

    @classmethod
    def pinword_occurrences_sp(
        cls, word: str, u_word: str, start_index: int = 0
    ) -> Iterator[int]:
        """
        Yields all occurrences (starting indices) of strict pinword u in pinword w
        (Lemma 3.12)
        """
        k = len(u_word)
        for idx in range(start_index, len(word)):
            if (
                cls.quadrant(word, idx) == cls.quadrant(u_word, 0)
                and word[idx + 1 : idx + k] == u_word[1:]
            ):
                yield idx

    @classmethod
    def pinword_contains_sp(cls, word: str, u_word: str) -> bool:
        """Returns True if pinword contains sp"""
        return next(cls.pinword_occurrences_sp(word, u_word), False) is not False

    @classmethod
    def pinword_occurrences(cls, word: str, u_word: str) -> Iterator[Tuple[int, ...]]:
        """
        Yields all occurrences (starting indices of pinword u in pinword w
        (Theorem 3.13)
        """

        def rec(
            word: str, u_word: List[str], i: int, j: int, res: List[int]
        ) -> Iterator[Tuple[int, ...]]:
            """
            Recursive helper function used to check for multiple sequential occurrences.
            """
            if j == len(u_word):
                yield tuple(res)
            elif i >= len(word):
                return
            else:
                for occ in cls.pinword_occurrences_sp(word, u_word[j], i):
                    res.append(occ)
                    for x in rec(word, u_word, occ + len(u_word[j]), j + 1, res):
                        yield x
                    res.pop()

        return rec(word, cls.factor_pinword(u_word), 0, 0, [])

    @classmethod
    def pinword_contains(cls, word: str, u_word: str):
        """Returns True if piwnord u is in pinword w."""
        return next(cls.pinword_occurrences(word, u_word), False) is not False

    @classmethod
    def make_nfa_for_pinword(cls, u_word: str) -> "NFA":
        """NFA for pinword"""
        prefix = ""

        def new_state(states) -> None:
            states.add(prefix + str(len(states)))

        def last_state(states) -> str:
            return prefix + str(len(states) - 1)

        def add_a_star(states, transitions) -> None:
            new_state(states)
            state = last_state(states)
            transitions[state] = {x: {state} for x in DIRS}

        def add_sp(u_i, states, transitions) -> None:
            if len(u_i) == 2:
                word1, word2 = u_i
                state_a = last_state(states)
                new_state(states)
                state_b = last_state(states)
                new_state(states)
                state_c = last_state(states)
                add_a_star(states, transitions)
                state_d = last_state(states)

                transitions[state_a][word1[0]].add(state_b)
                transitions[state_a][word2[0]].add(state_c)

                transitions[state_b] = {word1[1]: {state_d}}
                transitions[state_c] = {word2[1]: {state_d}}
            else:
                (x,) = u_i
                position = last_state(states)
                for i, c_var in enumerate(x):
                    if i == len(x) - 1:
                        add_a_star(states, transitions)
                    else:
                        new_state(states)
                    nxt = last_state(states)
                    if c_var in transitions[position]:
                        transitions[position][c_var].add(nxt)
                    else:
                        transitions[position][c_var] = {nxt}
                    position = nxt

        decomp = [cls.sp_to_m(x) for x in cls.factor_pinword(u_word)]
        rev = False
        if rev:
            decomp = [x[::-1] for x in decomp[::-1]]
        input_symbols = set(DIRS)
        initial_state = "0"
        states: Set[str] = set()
        transitions: DefaultDict[str, dict] = defaultdict(dict)

        add_a_star(states, transitions)
        for u_i in decomp:
            add_sp(u_i, states, transitions)

        final_states = {last_state(states)}

        return NFA(
            states=states,
            input_symbols=input_symbols,
            transitions=transitions,
            initial_state=initial_state,
            final_states=final_states,
        )

    @staticmethod
    def dfa_name_reset(dfa_in: "DFA", minimize=True) -> "DFA":
        """DFA name reset."""
        if minimize:
            return dfa_in.minify()
        m_dict: Dict[str, str] = dict()
        for state in dfa_in.states:
            m_dict[state] = str(len(m_dict))

        return DFA(
            states={m_dict[x] for x in dfa_in.states},
            input_symbols=dfa_in.input_symbols,
            transitions={
                m_dict[x]: {k: m_dict[v] for k, v in dfa_in.transitions[x].items()}
                for x in dfa_in.transitions
            },
            initial_state=m_dict[dfa_in.initial_state],
            final_states={m_dict[x] for x in dfa_in.final_states},
        )

    @staticmethod
    def make_dfa_for_m() -> "DFA":
        """Returns DFA for M."""
        return DFA(
            states={"0", "1", "2", "3"},
            input_symbols=set(DIRS),
            transitions={
                "0": {"U": "1", "D": "1", "L": "2", "R": "2"},
                "1": {"U": "3", "D": "3", "L": "2", "R": "2"},
                "2": {"U": "1", "D": "1", "L": "3", "R": "3"},
                "3": {"U": "3", "D": "3", "L": "3", "R": "3"},
            },
            initial_state="0",
            final_states={"0", "1", "2"},
        )

    @classmethod
    def make_dfa_for_pinword(cls, word: str) -> "DFA":
        """Returns DFA for pinword."""
        return cls.dfa_name_reset(DFA.from_nfa(cls.make_nfa_for_pinword(word)))

    @classmethod
    def make_dfa_for_perm(cls, perm: "Perm") -> "DFA":
        """Returns DFA for Perm."""
        pinwords = cls.pinwords_for_basis((perm,))
        out_dfa: "DFA" = None
        sorted_pinwords = sorted(pinwords)
        for word in sorted_pinwords:
            if out_dfa is None:
                out_dfa = cls.make_dfa_for_pinword(word)
            else:
                out_dfa2 = cls.make_dfa_for_pinword(word)
                for_union = out_dfa.union(out_dfa2)
                out_dfa = cls.dfa_name_reset(for_union)
        return out_dfa

    @classmethod
    def make_dfa_for_basis_from_pinwords(cls, basis: List["Perm"]) -> "DFA":
        """Returns DFA for basis from list of pinwords"""
        pinwords = cls.pinwords_for_basis(basis)
        out_dfa: "DFA" = None
        sorted_pinwords = sorted(pinwords)
        for word in sorted_pinwords:
            if out_dfa is None:
                out_dfa = cls.make_dfa_for_pinword(word)
            else:
                out_dfa2 = cls.make_dfa_for_pinword(word)
                out_dfa = out_dfa.union(out_dfa2)
                # out_dfa = cls.dfa_name_reset(for_union)
        return out_dfa

    @classmethod
    def make_dfa_for_basis_from_db(cls, basis: List["Perm"]) -> "DFA":
        """Returns DFA for basis from db."""
        out_dfa: "DFA" = None
        sorted_basis = sorted(basis)
        for word in sorted_basis:
            if out_dfa is None:
                out_dfa = cls.load_dfa_for_perm(word)
            else:
                out_dfa2 = cls.load_dfa_for_perm(word)
                for_union = out_dfa.union(out_dfa2)
                out_dfa = cls.dfa_name_reset(for_union)
        return out_dfa

    @classmethod
    def make_dfa_for_basis(cls, basis: List["Perm"], use_db=False) -> "DFA":
        """Makes DFA for basis"""
        if use_db:
            return cls.make_dfa_for_basis_from_db(basis)
        return cls.make_dfa_for_basis_from_pinwords(basis)

    @classmethod
    def pinwords_for_basis(cls, basis) -> List[str]:
        """Returns pinwords for basis."""
        res = []
        for perm in basis:
            res.extend(cls.perm_to_pinword_mapping(len(perm))[perm])
        return res

    @staticmethod
    def has_finite_alternations(basis) -> bool:
        """Returns True if basis has finite alterations."""
        alt_basis = (Perm((0, 1, 2)), Perm((1, 3, 0, 2)), Perm((2, 3, 0, 1)))
        for sym in all_symmetry_sets(alt_basis):
            if all(x not in Av(sym) for x in basis):
                return False
        return True

    @staticmethod
    def has_finite_wedges_type_1(basis) -> bool:
        """Returns True if basis has finite wedges og type 1"""
        wedge1_b = (
            Perm((0, 1, 3, 2)),
            Perm((0, 2, 1, 3)),
            Perm((0, 3, 1, 2)),
            Perm((0, 3, 2, 1)),
            Perm((1, 3, 2, 0)),
            Perm((2, 0, 1, 3)),
            Perm((3, 0, 1, 2)),
            Perm((3, 0, 2, 1)),
            Perm((3, 1, 2, 0)),
            Perm((3, 2, 0, 1)),
        )
        for sym in all_symmetry_sets(wedge1_b):
            if all(x not in Av(sym) for x in basis):
                return False
        return True

    @staticmethod
    def has_finite_wedges_type_2(basis) -> bool:
        """Returns True if basis has finite wedges og type 2"""
        wedge2_b = (
            Perm((1, 0, 2, 3)),
            Perm((1, 0, 3, 2)),
            Perm((2, 0, 1, 3)),
            Perm((2, 0, 3, 1)),
            Perm((2, 1, 3, 0)),
            Perm((2, 3, 0, 1)),
            Perm((3, 0, 1, 2)),
            Perm((3, 0, 2, 1)),
            Perm((3, 1, 2, 0)),
            Perm((3, 2, 0, 1)),
        )
        for sym in all_symmetry_sets(wedge2_b):
            if all(x not in Av(sym) for x in basis):
                return False
        return True

    @classmethod
    def has_finite_special_simples(cls, basis) -> bool:
        """Returns True if basis has finite special simples."""
        alt = cls.has_finite_alternations(basis)
        if not alt:
            return False
        wedge1 = cls.has_finite_wedges_type_1(basis)
        if not wedge1:
            return False
        wedge2 = cls.has_finite_wedges_type_2(basis)
        if not wedge2:
            return False
        return True

    @classmethod
    def has_finite_pinperms(cls, basis, use_db=False, dfa: "DFA" = None) -> bool:
        """Check if basis has finite pinperms"""
        if dfa is None:
            dfa = cls.make_dfa_for_basis(basis, use_db)
        dfa = dfa.complement()
        dfa = cls.dfa_name_reset(cls.make_dfa_for_m() & dfa)
        return dfa.isfinite() is True

    @classmethod
    def has_finite_simples(cls, basis, use_db=False, check_all=False, dfa=None) -> bool:
        """Check if basis has finite simples."""
        other = cls.has_finite_special_simples(basis)
        if not check_all and not other:
            return False
        pin = cls.has_finite_pinperms(basis, use_db, dfa)
        return pin and other

    @classmethod
    def store_dfa_for_perm(cls, perm, in_dfa=None) -> None:
        """Write the DFA for the specified Perm to a file."""
        directory = "dfa_db/S{}/".format(len(perm))
        path = Path(directory)
        path.mkdir(parents=True, exist_ok=True)
        filename = "{}.txt".format("".join(str(i) for i in perm))
        path = path / filename
        if path.is_file():
            return
        if in_dfa is None:
            in_dfa = cls.make_dfa_for_perm(perm)
        with open(str(path), "w") as file_object:
            file_object.write(
                "{}\n".format(
                    f"DFA(states={in_dfa.states}, "
                    + f"input_symbols={in_dfa.input_symbols}, "
                    + f"transitions={dict(in_dfa.transitions)}, "
                    + f"initial_state='{in_dfa.initial_state}', "
                    + f"final_states={in_dfa.final_states})"
                )
            )

    @classmethod
    def load_dfa_for_perm(cls, perm) -> "DFA":
        """Loads the DFA for the specified Perm from file."""
        directory = "dfa_db/S{}/".format(len(perm))
        path = Path(directory)
        filename = "{}.txt".format("".join(str(i) for i in perm))
        path = path / filename
        dfa: "DFA" = None
        if not path.is_file():
            cls.store_dfa_for_perm(perm)
        with open(str(path), "r") as file_object:
            dfa = eval(file_object.readline().strip())
        return dfa

    @classmethod
    def create_dfa_db_for_length(cls, length: int) -> None:
        """Create a database of DFAs for perms of specified length"""
        for perm in Perm.of_length(length):
            cls.store_dfa_for_perm(perm)
