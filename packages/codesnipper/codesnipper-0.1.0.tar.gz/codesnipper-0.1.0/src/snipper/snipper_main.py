import os
import functools
import textwrap
import re
from snipper.fix_s import save_s
from snipper.fix_cite import fix_citations
from snipper.fix_bf import fix_f, fix_b2
from snipper.fix_o import run_o
from snipper.legacy import indent, block_process

def fix_r(lines):
    for i,l in enumerate(lines):
        if "#!r" in l:
            lines[i] = indent(l) + l[l.find("#!r") + 3:].lstrip()
    return lines


def strip_tag(lines, tag):
    lines2 = []
    for l in lines:
        dx = l.find(tag)
        if dx > 0:
            l = l[:dx]
            if len(l.strip()) == 0:
                l = None
        if l is not None:
            lines2.append(l)
    return lines2


def rem_nonprintable_ctrl_chars(txt):
    """Remove non_printable ascii control characters """
    try:
        txt = re.sub(r'[^\x20-\x7E|\x09-\x0A]','', txt)
        # remove non-ascii characters
        txt = repr(txt).decode('unicode_escape').encode('ascii','ignore')[1:-1]
    except Exception as exception:
        print(exception)
    return txt


def run_i(lines, file, output):
    extra = dict(python=None, output=output, evaluated_lines=0)
    def block_fun(lines, start_extra, end_extra, art, head="", tail="", output=None, extra=None):
        outf = output + ("_" + art if art is not None and len(art) > 0 else "") + ".shell"
        lines = full_strip(lines)
        s = "\n".join(lines)
        s.replace("...", "..") # passive-aggressively truncate ... because of #issues.
        lines = textwrap.dedent(s).strip().splitlines()

        if extra['python'] is None:
            import os
            if os.name == 'nt':
                import wexpect as we
            else:
                import pexpect as we
            an = we.spawn("python", encoding="utf-8", timeout=20)
            an.expect([">>>"])
            extra['python'] = an

        analyzer = extra['python']
        def rsession(analyzer, lines):
            l2 = []
            for i, l in enumerate(lines):
                l2.append(l)
                if l.startswith(" ") and i < len(lines)-1 and not lines[i+1].startswith(" "):
                    if not lines[i+1].strip().startswith("else:") and not lines[i+1].strip().startswith("elif") :
                        l2.append("\n")

            lines = l2
            alines = []

            # indented = False
            in_dot_mode = False
            if len(lines[-1]) > 0 and (lines[-1].startswith(" ") or lines[-1].startswith("\t")):
                lines += [""]

            for i, word in enumerate(lines):
                analyzer.sendline(word)
                before = ""
                while True:
                    analyzer.expect_exact([">>>", "..."])
                    before += analyzer.before
                    if analyzer.before.endswith("\n"):
                        break
                    else:
                        before += analyzer.after

                dotmode = analyzer.after == "..."
                if 'dir(s)' in word:
                    pass
                if 'help(s.find)' in word:
                    pass
                if dotmode:
                    # alines.append("..." + word)
                    alines.append(">>>" + analyzer.before.rstrip() if not in_dot_mode else "..." + analyzer.before.rstrip())
                    in_dot_mode = True
                    # if i < len(lines) - 1 and not lines[i + 1].startswith(" "):
                    #     analyzer.sendline("\n")  # going out of indentation mode .
                    #     analyzer.expect_exact([">>>", "..."])
                    #     alines.append("..." + analyzer.after.rstrip())
                    #     pass
                else:
                    alines.append( ("..." if in_dot_mode else ">>>") + analyzer.before.rstrip())
                    in_dot_mode = False
            return alines

        for l in (head[extra['evaluated_lines']:] + ["\n"]):
            analyzer.sendline(l)
            analyzer.expect_exact([">>>", "..."])


        alines = rsession(analyzer, lines)
        extra['evaluated_lines'] += len(head) + len(lines)
        lines = alines
        return lines, [outf, lines]
    try:
        a,b,c,_ = block_process(lines, tag="#!i", block_fun=functools.partial(block_fun, output=output, extra=extra))
        if extra['python'] is not None:
            extra['python'].close()

        if len(c)>0:
            kvs= { v[0] for v in c}
            for outf in kvs:
                out = "\n".join( ["\n".join(v[1]) for v in c if v[0] == outf] )
                out = out.replace("\r", "")

                with open(outf, 'w') as f:
                    f.write(out)

    except Exception as e:
        print("lines are")
        print("\n".join(lines))
        print("Bad thing in #!i command in file", file)
        raise e
    return lines


def full_strip(lines, tags=None):
    if tags is None:
        tags = ["#!s", "#!o", "#!f", "#!b"]
    for t in tags:
        lines = strip_tag(lines, t)
    return lines


def censor_code(lines, keep=True):
    dbug = True
    lines = fix_f(lines, dbug)
    lines, nB, cut = fix_b2(lines, keep=True)
    return lines



def censor_file(file, info, run_files=True, run_out_dirs=None, cut_files=True, solution_list=None,
                censor_files=True,
                base_path=None,
                include_path_base=None,
                strict=True,
                references=None):

    if references == None:
        references = {}


    dbug = False
    with open(file, 'r', encoding='utf8') as f:
        s = f.read()
        s = s.lstrip()
        lines = s.split("\n")
        for k, l in enumerate(lines):
            if l.find(" # !") > 0:
                print(f"{file}:{k}> bad snipper tag, fixing")
            lines[k] = l.replace("# !", "#!")

        try:
            lines = fix_citations(lines, references, strict=strict)
            # lines = s.split("\n")
        except IndexError as e:
            print(e)
            print("Fuckup in file, cite/reference tag not found!>", file)
            raise e

        if run_files or cut_files:
            ofiles = []
            for rod in [run_out_dirs]:
                # if not os.path.isdir(rod):
                #     os.mkdir(rod)
                ofiles.append(os.path.join(rod, os.path.basename(file).split(".")[0]) )
            ofiles[0] = ofiles[0].replace("\\", "/")

            if run_files:
                run_o(lines, file=file, output=ofiles[0])
                run_i(lines, file=file, output=ofiles[0])
            if cut_files:

                save_s(lines, file_path=os.path.relpath(file, base_path), output_dir=run_out_dirs)  # save file snips to disk
        lines = full_strip(lines, ["#!s", "#!o", '#!i'])

        # lines = fix_c(lines)
        if censor_files:
            lines = fix_f(lines, dbug)
            lines, nB, cut = fix_b2(lines)
        else:
            nB = 0
        lines = fix_r(lines)

        if censor_files and len(cut) > 0 and solution_list is not None:
            fname = file.__str__()
            i = fname.find("irlc")
            wk = fname[i+5:fname.find("\\", i+6)]
            # sp = paths['02450students'] +"/solutions/"
            # if not os.path.exists(sp):
            #     os.mkdir(sp)
            # sp = sp + wk
            # if not os.path.exists(sp):
            #     os.mkdir(sp)
            sols = []
            stext = ["\n".join(lines) for lines in cut]
            for i,sol in enumerate(stext):
                sols.append( (sol,) )
                # sout = sp + f"/{os.path.basename(fname)[:-3]}_TODO_{i+1}.py"
                # wsol = any([True for s in solution_list if os.path.basename(sout).startswith(s)])
                # print(sout, "(published)" if wsol else "")
                # if wsol:
                #     with open(sout, "w") as f:
                #         f.write(sol)

        if len(lines[-1])>0:
            lines.append("")
        s2 = "\n".join(lines)

    with open(file, 'w', encoding='utf-8') as f:
        f.write(s2)
    return nB
# lines: 294, 399, 420, 270

