import functools

from snipper.legacy import indent, gcoms, block_process


def fix_f(lines, debug):
    lines2 = []
    i = 0
    while i < len(lines):
        l = lines[i]
        dx = l.find("#!f")
        if dx >= 0:
            l_head = l[dx+3:].strip()
            l = l[:dx]
            lines2.append(l)
            id = indent(lines[i+1])
            for j in range(i+1, 10000):
                jid = len( indent(lines[j]) )
                if  j+1 == len(lines) or ( jid < len(id) and len(lines[j].strip() ) > 0):
                    break

            if len(lines[j-1].strip()) == 0:
                j = j - 1
            funbody = "\n".join( lines[i+1:j] )
            if i == j:
                raise Exception("Empty function body")
            i = j
            comments, funrem = gcoms(funbody)
            comments = [id + c for c in comments]
            if len(comments) > 0:
                lines2 += comments[0].split("\n")
            # lines2 += [id+"#!b"]
            f = [id + l.strip() for l in funrem.splitlines()]
            f[0] = f[0] + "#!b"

            # lines2 += (id+funrem.strip()).split("\n")
            errm = l_head if len(l_head) > 0 else "Implement function body"
            f[-1] = f[-1] + f' #!b {errm}'
            lines2 += f
            # lines2 += [f'{id}#!b {errm}']

        else:
            lines2.append(l)
            i += 1
    return lines2


def fix_b2(lines, keep=False):
    stats = {'n': 0}
    def block_fun(lines, start_extra, end_extra, art, stats=None, **kwargs):
        id = indent(lines[0])
        lines = lines[1:] if len(lines[0].strip()) == 0 else lines
        lines = lines[:-1] if len(lines[-1].strip()) == 0 else lines
        cc = len(lines)
        ee = end_extra.strip()
        if len(ee) >= 2 and ee[0] == '"':
            ee = ee[1:-1]
        start_extra = start_extra.strip()
        if keep:
            l2 = ['GARBAGE'] * cc
        else:
            l2 = ([id+start_extra] if len(start_extra) > 0 else []) + [id + f"# TODO: {cc} lines missing.", id+f'raise NotImplementedError("{ee}")']

        stats['n'] += cc
        return l2, cc
    lines2, _, _, cutout = block_process(lines, tag="#!b", block_fun=functools.partial(block_fun, stats=stats))
    return lines2, stats['n'], cutout