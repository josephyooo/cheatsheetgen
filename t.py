import re

from utils import *

text = """The softmax activation of a network is the vector of probabilities in a distribution, implying that the sum of the vector is 1. It is calculated by applying the softmax function ($a_k=\dfrac{e^{z_k}}{\sum e^{z_k}}$) to the logits, the raw predictions, of the network. Again, these logits, being a vector of $K$ real numbers, are converted to a distribution of $K$ outcomes using the softmax function. This activation is the last layer of a multiclass classification network and is commonly interpreted by taking the label with the greatest probability as the final prediction. Finally, these predictions are compared to the ground-truth label to calculate the cross-entropy loss (this is possible because the predictions and ground-truth labels are both distributions) and the gradient of this loss is applied to the parameters to "learn"."""


lm = [m.span() for m in re.finditer(r'\$[^\$]+\$(?!$)|(?<!^)\$[^\$]+\$', text)]
if lm:
    exp = ''
    p = 0 # arbitrary pointer
    # lm.insert(0, 0)
    # lm.append(len(text))
    for m in lm:
        if text[p:m[0]]:
            exp += r'\text{' + text[p:m[0]] + '}'
        exp += ' ' + text[m[0]+1:m[1]-1]
        exp += r'\\'
        p = m[1]

    exp = r'$$\displaylines{' + exp + '}$$'

# exp = r'$\text{Hello}$1+1'
# exp = r'$\mathrm{Hello\s}1+1$'
print(exp)

img = latex_to_img(exp)
img.save('a.png')
