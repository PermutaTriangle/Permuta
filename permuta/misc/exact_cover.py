from . import AlgorithmX


def exact_cover(bss, validcnt, max_cnt, ignore_first, allow_overlap_in_first):

    # curcover = []
    # ball = (1 << validcnt) - 1
    # care = ball & ~((1 << ignore_first) - 1)
    # def bt(at, left, done):
    #     if (done & care) == (ball & care):
    #         yield list(curcover)
    #     elif not (left == 0 or at == len(bss)):
    #         if (bss[at] & done &
    #             (care if allow_overlap_in_first else ball)) == 0:
    #             curcover.append(at)
    #             for res in bt(at + 1, left - 1, done | bss[at]):
    #                 yield res

    #             curcover.pop()

    #         for res in bt(at + 1, left, done):
    #             yield res

    # sols1 = []
    sols2 = []

    # for res in bt(0, max_cnt, 0):
    #     sols1.append(res)

    def handle_solution(sol):
        sols2.append(sol)
        return False

    ec = AlgorithmX(len(bss), validcnt - ignore_first, handle_solution)

    for i in range(len(bss)):
        bs = bss[i] >> ignore_first
        for j in range(validcnt - ignore_first):
            if (bs & (1 << j)) != 0:
                ec.set_value(i, j, True)

    ec.setup()
    ec.search(at_most=max_cnt)

    # print(sols1)
    # print(sols2)
    # assert sols1 == sols2

    return sols2


def exact_cover_smallest(bss, validcnt, max_cnt, ignore_first,
                         allow_overlap_in_first):
    sols = []

    def handle_solution(sol):
        sols.append(sol)
        return False

    ec = AlgorithmX(len(bss), validcnt - ignore_first, handle_solution)
    for i in range(len(bss)):
        bs = bss[i] >> ignore_first
        for j in range(validcnt - ignore_first):
            if (bs & (1 << j)) != 0:
                ec.set_value(i, j, True)

    ec.setup()
    d = 1
    while max_cnt is None or d <= max_cnt:
        ec.can_continue = False
        ec.search(at_most=d)
        if sols or not ec.can_continue:
            break
        d += 1

    return sols
