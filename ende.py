from base64 import b64encode as ben
from base64 import b64decode as bde

txt = '/Users/applelaptop/Desktop/dumbax'

with open(txt, 'rb') as f:
    cont = f.read()

penis = {
    'A': 'Ala',
    'C': 'Cys',
    'D': 'Asp',
    'E': 'Glu',
    'F': 'Phe',
    'G': 'Gly',
    'H': 'His',
    'I': 'Ile',
    'K': 'Lys',
    'L': 'Leu',
    'M': 'Met',
    'N': 'Asn',
    'P': 'Pro',
    'Q': 'Gln',
    'R': 'Arg',
    'S': 'Ser',
    'T': 'Thr',
    'V': 'Val',
    'W': 'Trp',
    'Y': 'Tyr'
}

def doohickey(s):
    try:
        if s.lower() == s:
            return f'{penis[s.upper()]}*'
        else:
            return penis[s]
    except KeyError:
        return s

def trinket(s):
    rdict = {v: k for k, v in penis.items()}
    try:
        if (s[-1] == '*'):
            return rdict[s[:-1]].lower()
        else:
            return rdict[s]
    except KeyError as skibidi:
        del (skibidi)
        return s


if cont.decode('utf-8')[0] == '~':
    dec = cont.decode('utf-8')[1:]
    dec = dec.split('?')
    dec = ''.join([trinket(s) for s in dec]).encode('utf-8')
    with open(txt, 'wb') as f:
        f.write(bde(dec))
        print(bde(dec))
    print('decoded dat bih')

else:
    encode = ben(cont)
    enc2 = '~'
    enc2 += '?'.join([doohickey(c) for c in encode.decode('utf-8')])
    enc2 = enc2.encode('utf-8')
    with open(txt, 'wb') as f:
        f.write(enc2)
        print(enc2)
    print('encod')