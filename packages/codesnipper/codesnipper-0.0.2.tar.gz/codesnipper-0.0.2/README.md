# Snipper
A lightweight framework for removing code from student solutions.
## Installation
```console
pip install codesnipper
```
## What it does
This project address the following three challenges for administering a python-based course

 - You need to maintain a (working) version for debugging as well as a version handed out to students (with code missing)
 - You ideally want to make references in source code to course material *"(see equation 2.1 in exercise 5)"* but these tend to go out of date
 - You want to include code snippets and code output in lectures notes/exercises/beamer slides
 - You want to automatically create student solutions

This framework address these problems and allow you to maintain a **single**, working project repository. 

The project is currently used in **02465** at DTU. An example of student code can be found at:
 - https://gitlab.gbar.dtu.dk/02465material/02465students/blob/master/irlc/ex02/dp.py

A set of lectures notes where all code examples/output are automatically generated from the working repository can be found a
- https://lab.compute.dtu.dk/tuhe/books (see **Sequential decision making**)
 
## How it works
The basic functionality is quite simple. You start with your working script in your private repository and add special tags to the script. 
In this case I have added the tags `#!b` (cut a block) and `#!f` (cut function scope). 
```python
def myfun(): #!f The error I am going to raise
    """ The function docstring will not be removed"""
    print("This is a function")
    return 42
    
def a_long_function():
    a = 234
    print("a line")
    print("a line") #!b
    print("a line")
    print("a line") #!b Insert three missing print statements. 
    print("a line")
    return a
    
if __name__ == "__main__":
    myfun()
```
This will produce the following file:
```python
def myfun():
    """ The function docstring will not be removed"""
    # TODO: 2 lines missing.
    raise NotImplementedError("The error I am going to raise")
    
def a_long_function():
    a = 234
    print("a line")
    # TODO: 3 lines missing.
    raise NotImplementedError("Insert three missing print statements.")
    print("a line")
    return a
    
if __name__ == "__main__":
    myfun()
```
You can also use the framework to capture code snippets, outputs and interactive python output. 
To do this, save the following in `foo.py`
```python
def myfun(): #!s This snippet will be saved to foo.py in the output directory. 
    print("Hello") #!s 

print("Do not capture me") 
for i in range(4): #!o
    print("Output", i)
print("Goodbuy world") #!o
print("don't capture me")

# Interactive pythong example
print("Hello World") #!i #!i # this is a single-line cutout.
````
These block-tags will create a file `foo.py` (in the output directory) containing
```python
def myfun():
    print("Hello") 
```
A file `foo.txt` containing the captured output
```txt
Output 0
Output 1
Output 2
Output 3
Goodbuy world
```
and a typeset version of an interactive python session in `foo.pyi` (use `pycon` in minted; this gitlab server appears not to support `pycon`)
```pycon
>>> print("hello world")
Hello World"
```
All these files can be directly imported into `LaTeX` using e.g. `minted`: You never need to mix `LaTeX` code and python again!


## References: 
Bibliography references can be loaded from `references.bib`-files and in-document references from the `.aux` file. 
For this example, we will insert references shown in the `examples/latex/index.tex`-document. To do so, we can use these tags:
```python
def myfun(): #!s
    """
    To solve this exercise, look at \ref{eq1} in \ref{sec1}.
    You can also look at \cite{bertsekasII} and \cite{herlau}
    More specifically, look at \cite[Equation 117]{bertsekasII} and \cite[\ref{fig1}]{herlau}

    We can also write a special tag to reduce repetition: \nref{fig1} and \nref{sec1}.
    """
    return 42 #!s

```
We can manually compile this example by first loading the aux-files and the bibliographies as follows:
```python 
# load_references.py
    from snipper.citations import get_bibtex, get_aux 
    bibfile = "latex/library.bib"
    auxfile = 'latex/index.aux'
    bibtex = get_bibtex(bibfile)
    aux = get_aux(auxfile) 
```
Next, we load the python file containing the reference code and fix all references based on the aux and bibliography data. 
```python 
# load_references.py
    file = "citations.py" 
    with open(file, 'r') as f:
        lines = f.read().splitlines()
    lines = fix_aux(lines, aux=aux)
    lines = fix_aux_special(lines, aux=aux, command='\\nref', bibref='herlau')
    lines = fix_bibtex(lines, bibtex=bibtex)
    with open('output/citations.py', 'w') as f:
        f.write("\n".join(lines)) 
```
The middle command is a convenience feature: It allows us to specify a special citation command `\nref{..}` which always compiles to `\cite[\ref{...}]{herlau}`. This is useful if e.g. `herlau` is the bibtex key for your lecture notes. The result is as follows:
```python 
"""
References:
  [Ber07] Dimitri P. Bertsekas. Dynamic Programming and Optimal Control, Vol. II. Athena Scientific, 3rd edition, 2007. ISBN 1886529302.
  [Her21] Tue Herlau. Sequential decision making. (See 02465_Notes.pdf), 2021.
"""
def myfun(): #!s
    """
    To solve this exercise, look at eq. (1) in Section 1.
    You can also look at (Ber07) and (Her21)
    More specifically, look at (Ber07, Equation 117) and (Her21, Figure 1)

    We can also write a special tag to reduce repetition: (Her21, Figure 1) and (Her21, Section 1).
    """
    return 42 #!s
```
Note this example uses the low-level api. Normally you would just pass the bibtex and aux-file to the main censor-file command.

## Additional features:
-  You can name tags using `#!s=bar` to get a `foo_bar.py` snippet. This is useful when you need to cut multiple sessions. This also works for the other tags. 