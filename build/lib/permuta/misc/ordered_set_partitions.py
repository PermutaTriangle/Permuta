from .dancing_links import DancingLinks

def ordered_set_partitions(lst, parts):

    dl = DancingLinks(lst)
    res = [ [ None for j in range(parts[i]) ] for i in range(len(parts)) ]

    def gen(at):

        if at == len(parts):
            yield [ [ res[i][j] for j in range(parts[i]) ] for i in range(len(parts)) ]
        else:

            def make_part(pat, cur, left):
                if pat == parts[at]:
                    yield res
                elif left >= parts[at] - pat:

                    res[at][pat] = cur.value
                    dl.erase(cur)
                    for r in make_part(pat + 1, cur.next, left - 1):
                        yield r

                    dl.restore(cur)

                    for r in make_part(pat, cur.next, left - 1):
                        yield r

            for p in make_part(0, dl.front, len(dl)):
                for g in gen(at + 1):
                    yield g

    return gen(0)

