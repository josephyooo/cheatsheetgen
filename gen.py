from utils import *

from timeit import default_timer as timer
start = timer()
# z = "e^{i\pi}+1=0"
# x = to_raw(x)
# y = r"\underset{S}{\int\int}\ \vec{\nabla}\times\vec{B}\cdot d\vec{S}=\underset{C}{\oint}\ \vec{B}\cdot d\vec{l}"
# x = r"""\begin{eqnarray*}
# \mathcal{F} &=& \int f\left( \phi, c \right) dV, \\
# \frac{ \partial \phi } { \partial t } &=& -M_{ \phi }
# \frac{ \delta \mathcal{F} } { \delta \phi }
# \end{eqnarray*}"""
# x = r'Chapter 1.'
# x = x.replace("\n", "")
# x = fix_text(x)

# img = latex_to_img(x)
# print(img.size)
# img.save("a.png")

EXAMPLE_PATH = "/mnt/c/Users/fizzy/iCloudDrive/iCloud~md~obsidian/gsu 23-24 spring/cs 4851/midterm1prep/CS 4851 Reference Sheet.md"
with open(EXAMPLE_PATH, 'r') as example_file:
    text = example_file.read()
text = md_split(text)

for x in text:
    print(x)

img = latex_to_img(text[0])
img.save("a.png")

print(timer() - start)
