import functools
from collections import defaultdict
from snipper.snipper_main import full_strip, block_process

def f2(lines, tag, i=0, j=0):
    for k in range(i, len(lines)):
        index = lines[k].find(tag, j if k == i else 0)
        if index >= 0:
            return k, index
    return None, None

def block_iterate(lines, tag):
    contents = {'joined': lines}
    while True:
        contents = block_split(contents['joined'], tag)
        if contents is None:
            break

        yield  contents

def block_split(lines, tag):
    stag = tag[:2]  # Start of any next tag.

    def join(contents):
        return contents['first'] + [contents['block'][0] + contents['post1']] + contents['block'][1:-1] \
                + [contents['block'][-1] + contents['post2']] + contents['last']
    contents = {}
    i, j = f2(lines, tag)

    def get_tag_args(line):
        k = line.find(" ")
        tag_args = (line[:k + 1] if k >= 0 else line)[len(tag):]
        if len(tag_args) == 0:
            return {'': ''}  # No name.
        tag_args = dict([t.split("=") for t in tag_args.split(";")])
        return tag_args

    if i is None:
        return None
    else:
        start_tag_args = get_tag_args(lines[i][j:])
        START_TAG = f"{tag}={start_tag_args['']}" if '' in start_tag_args else tag
        END_TAG = START_TAG
        i2, j2 = f2(lines, END_TAG, i=i, j=j+1)
        if i2 == None:
            END_TAG = tag
            i2, j2 = f2(lines, END_TAG, i=i, j=j+1)

    if i == i2:
        # Splitting a single line. To reduce confusion, this will be treated slightly differently:
        l2 = lines[:i] + [lines[i][:j2], lines[i][j2:]] + lines[i2+1:]
        c2 = block_split(l2, tag=tag)
        c2['block'].pop()
        c2['joined'] = join(c2)
        return c2
    else:
        contents['first'] = lines[:i]
        contents['last'] = lines[i2+1:]

        def argpost(line, j):
            nx_tag = line.find(stag, j+1)
            arg1 = line[j+len(tag):nx_tag]
            if nx_tag >= 0:
                post = line[nx_tag:]
            else:
                post = ''
            return arg1, post

        contents['arg1'], contents['post1'] = argpost(lines[i], j)
        contents['arg2'], contents['post2'] = argpost(lines[i2], j2)
        blk = [lines[i][:j]] + lines[i+1:i2] + [lines[i2][:j2]]
        contents['block'] = blk
        contents['joined'] = join(contents)
        contents['start_tag_args'] = start_tag_args
        contents['name'] = start_tag_args['']
        return contents


def get_s(lines):
    """ Return snips from 'lines' """
    blocks = defaultdict(list)
    for c in block_iterate(lines, "#!s"):
        blocks[c['name']].append(c)
    output = {}
    for name, co in blocks.items():
        output[name] = [l for c in co for l in c['block']]
    return output

import os

def save_s(lines, output_dir, file_path): # save file snips to disk
    content = get_s(lines)
    if not os.path.isdir(output_dir):
        os.mkdir(output_dir)
    for name, ll in content.items():
        if file_path is not None:
            ll = [f"# {file_path}"] + ll
        out = "\n".join(ll)
        with open(output_dir + "/" + os.path.basename(file_path)[:-3] + ("_" + name if len(name) > 0 else name) + ".py", 'w') as f:
            f.write(out)

        # out = "\n".join([f"# {include_path_base}"] + ["\n".join(v[1]) for v in c if v[0] == outf])
        # with open(outf, 'w') as f:
        #     f.write(out)

    # def block_fun(lines, start_extra, end_extra, art, output, **kwargs):
    #     outf = output + ("_" + art if art is not None and len(art) > 0 else "") + ".py"
    #     lines = full_strip(lines)
    #     return lines, [outf, lines]
    # try:
    #     a,b,c,_ = block_process(lines, tag="#!s", block_fun=functools.partial(block_fun, output=output))
    #     if len(c)>0:
    #         kvs= { v[0] for v in c}
    #         for outf in kvs:
    #             out = "\n".join([f"# {include_path_base}"]  + ["\n".join(v[1]) for v in c if v[0] == outf] )
    #             with open(outf, 'w') as f:
    #                 f.write(out)
    #
    # except Exception as e:
    #     print("lines are")
    #     print("\n".join(lines))
    #     print("Bad thing in #!s command in file", file)
    #     raise e
    # return lines

s1 = """
L1
L2 #!s=a
L3 #!s=b
L4
L5 
L6 
L7 #!s=a
L8 
L9 #!s=b
went
"""

if __name__ == "__main__":
    # for c in block_iterate(s1.splitlines(), tag="#!s"):
    #     print(c['block'])
    output = get_s(s1.splitlines())
    for k, v in output.items():
        print("name:", k)
        print("\n".join(v))
        print("="*10)
    # contents = block_split(s1.splitlines(), tag="#!s")
    # contents = block_split(contents['joined'], tag="#!s")
    # lines2 = contents['first'] +
    a = 234
    pass