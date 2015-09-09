__author__ = 'Matteo'
__doc__ = '''Multivariate analysis in Matlab is sucking my soul. I need to procrastinate.
Therefore I have made this. A unicode transcoder script.
'''

import re

N = "\n"
T = "\t"
# N="<br/>"

def greekify(text):
    ἑλληνικός2={
            'sigma2':'ς',
            'lambda2':'λ'}

    ἑλληνικός={'alpha':'α',
            'beta':'β',
            'gamma':'γ',
            'delta':'δ',
           'epsilon':'ε',
           'zeta':'ζ',
            'eta':'η',
            'theta':'θ',
            'iota':'ι',
            'kappa':'κ',
            'mu':'μ',
            'nu':'ν',
            'xi':'ξ',
            'omicron':'o',
            'pi':'π',
            'rho':'ρ',
            'sigma':'σ',
            'stigma':'ϛ',
            'tau':'τ',
            'upsilon':'υ',
            'phi':'φ',
            'chi':'χ',
            'psi':'ψ',
            'omega':'ω'}

    for glyph in ἑλληνικός2:
        text=text.replace(glyph, ἑλληνικός2[glyph])
    for glyph in ἑλληνικός:
        text=text.replace(glyph, ἑλληνικός[glyph])
    return text

def uniencodemunger(text): #This will munge your code.
    '''and       del       from      not       while
as        elif      global    or        with
assert    else      if        pass      yield
break     except    import    print
class     exec      in        raise
continue  finally   is        return
def       for       lambda    try'''
    toxicode={'lambda':'Λ',
              'sum':'Σ',
              'Math.sqrt':'√',
              '=>':'≥','>=':'≥',
              '<=':'≤','=<':'≤',
              'isinstance':'⊂',
              'None':'∅',
              'if ':'⇒ ', ##odd choice. Messes up elif else. looks odd
              'def ':'∃ ', ##odd choice. The matlab fx ligature is not unicode.
              'for ':'∀ ',
              ' and ':' ∧ ',
              ' or ':' ∨ ',
              ' not ':' ¬ ',
              '#':'☞'
               }
    #attributes in subscript.
    #emoji
    #+= and co.
    text=re.sub('__(.*?)__',r'｢\1｣',text)  #thought it'd be funny
    text=text.replace('===','≣').replace('==','≡').replace('!=','≢')
    for glyph in toxicode:
        text=text.replace(glyph, toxicode[glyph])
    return text



if __name__ == "__main__":
    x=open("DnD_Battler.py").read()
    print(uniencodemunger(x))