import re

import matplotlib.pyplot as plt
import PIL

# matplotlib.rcParams.update(matplotlib.rcParamsDefault)
# matplotlib.rcParams["mathtext.fontset"] = "cm"
# plt.rcParams["mathtext.fontset"] = "cm"
# plt.rcParams["text.usetex"] = True

plt.rcParams.update({
    "text.usetex" : True,
    'text.latex.preamble' : r'\usepackage{amsmath}',
    'mathtext.fontset' : 'cm'
})

def crop_img(img):
    bbox = PIL.ImageOps.invert(img).getbbox()
    return img.crop(bbox)

def latex_to_img(exp, fontsize='medium', dpi=500):
    # converts latex expression to a png with a given resolution

    fig = plt.figure(dpi=dpi)
    text = fig.text(
        x=0.5,
        y=0.5,
        s=exp,
        fontsize=fontsize,
        horizontalalignment="center",
        verticalalignment="center"
    )

    # convert figure to PIL object
    fig.canvas.draw()
    out = PIL.Image.frombytes('RGBa', fig.canvas.get_width_height(), fig.canvas.buffer_rgba())

    # convert from RGBa to grayscale
    out = out.convert("L")
    # crop (https://stackoverflow.com/a/9874342/8930299)
    # out = crop_img(out)

    return out

def to_raw(s):
    return r'{}'.format(s)

def fix_text(text):
    if "\\text" not in text:
        return text

    text = text.replace("\\text", "\\mathrm")
    M = [m.span() for m in re.finditer(r"\mathrm{.+}", text)]
    for start, end in M:
        text = text[:start] + text[start:end].replace(" ", "\\;") + text[end:]
    return text

def md_split(text):
    # TODO: optimize
    latex_i = [i for m in re.finditer(r"^\${2}([^\$]|\n)+\${2}$", text, re.MULTILINE) for i in m.span()]
    text = [text[i:j] for i, j in zip(latex_i, latex_i[1:]+[None])]
    for i in range(len(text)):
        if text[i][:2] == "$$":
            text[i] = text[i].replace("\n", "")

    text = [s for s in "".join(text).split("\n") if s]

    return text

def md_to_latex(text):
    """
    take "block" of markdown and convert it to latex

    Types of 'blocks':
    - Headers (# or ##)
    - Full text
    - Full multiline latex -> No change needed
    - Full inline latex -> No change needed
    - Mixed inline latex and text (text not explicitly defined)
    - Text in multiline latex (text explicitly defined)
    """
    # default
    fontsize = 'medium'

    # full latex
    n = text[:2].count('$')
    if n > 0:
        lm = re.match(f'\\$\{{n}}[^\\$]+\\$\{{n}}(?!$)|(?<!^)\\$\{{n}}[^\\$]+\\$\{{n}}') # matches inline latex that isn't the entire text
        # lm = re.match(r'\$[^\$]+\$(?!$)|(?<!^)\$[^\$]+\$', text) # first regex pattern attempt, failed to match $$$$ correctly
        if not lm:
            return exp, fontsize

    # header
    n = re.match(r'^\#+\s', text)
    if n:
        # -1 for space, -1 for zero-indexing
        n = len(n[0]) - 2
        exp = text[n+1:]
        fontsize = ['x-large', 'large'][n]

        return exp, fontsize
    
    # full text
    if '$' not in text:
        exp = r"$\mathrm{" + exp.replace(" ", "\\;") + "}$"
        
        return exp, fontsize

    # text in multiline latex
    if r'\text' in text:
        exp = text.replace("\\text", "\\mathrm")
        M = [m.span() for m in re.finditer(r"\\mathrm{.+}", text)]
        for start, end in M:
            text = text[:start] + text[start:end].replace(" ", "\\;") + text[end:]
        return text, fontsize
    
    # inline latex in text
    lm = [m.span() for m in re.finditer(r'\$[^\$]+\$(?!$)|(?<!^)\$[^\$]+\$', text)]
    if lm:
        exp = ''
        p = 0 # arbitrary pointer
        # lm.insert(0, 0)
        # lm.append(len(text))
        for m in lm:
            exp += r'\text{' + text[p:m[0]] + '}'
            exp += text[m[0]:m[1]]

        exp = '$$' + exp + '$$'


    
    # no cases matched
    raise ValueError("Unexpected markdown block received.", text)



