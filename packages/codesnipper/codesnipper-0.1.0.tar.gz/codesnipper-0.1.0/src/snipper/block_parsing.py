"""
Module for new-style block parsing. Make sure all functions are up-to-date and used.
"""

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
    # print("\n".join(lines))
    # if tag != "#!s":
    #     return {}

    if tag =="#!s" and "#!s" in "".join(lines):
        print("tag is", tag)
    # else:
    #     return dict(name="asdfasdf", joined='')

    z = 234
    stag = tag[:2]  # Start of any next tag.

    def join(contents):
        return contents['first'] + [contents['block'][0] + contents['post1']] + contents['block'][1:-1] \
                + [contents['block'][-1] + contents['post2']] + contents['last']
    contents = {}
    i, j = f2(lines, tag)

    def get_tag_args(line):
        # line = line.strip()
        k = line.find(" ")
        tag_args = ((line[:k + 1] if k >= 0 else line)[len(tag):] ).strip()

        if len(tag_args) == 0:
            return {'': ''}  # No name.

        # print("TAG ARGS")
        # print(tag_args)
        tag_args = dict([t.split("=") for t in tag_args.split(";")])
        return tag_args

    if i is None:
        return None
    else:
        print( lines[i] )

        start_tag_args = get_tag_args(lines[i][j:])
        START_TAG = f"{tag}={start_tag_args['']}" if start_tag_args[''] != '' else tag
        END_TAG = START_TAG
        i2, j2 = f2(lines, END_TAG, i=i, j=j+1)
        if i2 == None:
            END_TAG = tag
            i2, j2 = f2(lines, END_TAG, i=i, j=j+1)
        if i2 == None:
            print("\n".join( lines[i:]))
            raise Exception("Did not find matching tag", tag)


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