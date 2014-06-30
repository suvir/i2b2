__author__ = 'suvir'

import re,nltk,sys
from nltk.util import ngrams
"""
Global variables
"""
stemmer = nltk.stem.PorterStemmer() #Global copy of Stemmer
wnl = nltk.WordNetLemmatizer()
parent_map = dict()

def stemmed_token(token):
    token=token.lower()
    return stemmer.stem(token)

def pos_tag(token):
    return nltk.pos_tag([token])[0][1]

def lemma(token):
    token=token.lower()
    return wnl.lemmatize(token)

#def charNgram(token):
#    return [''.join(i) for i in ngrams(token,3)+ngrams(token,4)]

def suffix(token):
    """
    return 2-,3-,4- char suffixes
    """
    return [token[-i:].lower() for i in range(2,5)]

def prefix(token):
    """
    return 2-,3-,4- char prefixes
    """
    return [token[:i].lower() for i in range(2,5)]

def initcap(token):
    if token[0].isupper():
        return 1
    else:
        return 0

def endcap(token):
    if token[-1].isupper():
        return 1
    else:
        return 0

def allcaps(token):
    if token.isupper():
        return 1
    else:
        return 0

def lowercase(token):
    if token.islower():
        return 1
    else:
        return 0

def mixcase(token):
    if not token.islower() and not token.isupper():
        return 1
    else:
        return 0

def lowcount(token):
    count = 0
    for char in token:
        if char.islower():
            count += 1
    if count == 1:
        return [1,0,0,0]
    elif count == 2:
        return [0,1,0,0]
    elif count == 3:
        return [0,0,1,0]
    elif count > 3:
        return [0,0,0,1]
    else:
        return [0,0,0,0]

def capcount(token):
    count = 0
    for char in token:
        if char.isupper():
            count += 1
    if count == 1:
        return [1,0,0,0]
    elif count == 2:
        return [0,1,0,0]
    elif count == 3:
        return [0,0,1,0]
    elif count > 3:
        return [0,0,0,1]
    else:
        return [0,0,0,0]

def digitcount(token):
    if not token.isdigit():
        return [0,0,0,0]
    elif len(token) == 1:
        return [1,0,0,0]
    elif len(token) == 2:
        return [0,1,0,0]
    elif len(token) == 3:
        return [0,0,1,0]
    else:
        return [0,0,0,1]

def nucleoside(token):
    p = re.compile("(adenosine|deoxyadenosine|uridine|thymidine|cytidine|deoxycytidine)[s]*")
    if p.match(token) is not None:
        return 1
    else:
        return 0

def nucleotide(token):
    p = re.compile("([AGTC][MDT]P|cAMP|cGMP|cADPR)[s]*")
    if p.match(token) is not None:
        return 1
    else:
        return 0

def roman(token):
    p = re.compile("I|II|III|IV|V|VI|VII|VIII|IX|X")
    if p.match(token) is not None:
        return 1
    else:
        return 0

def wordlength(token):
    return len(token)%3

def greek(token):
    p = re.compile("alpha|beta|gamma|delta|epsilon|zeta|theta|iota|kappa|lambda|omicron|rho|sigma|tau|upsilon|phi|psi|omega|chi|nu|pi|xi|eta|mu")
    if p.match(token) is not None:
        return 1
    else:
        return 0

def units(token):
    p = re.compile("mkhz|khz|hz|kg|g|mg|ng|km|m|cm|mm|nm|ng|kb|l|ml|nl|mol|j|w|v|n|k|a|cal|min|h|s|db|cd|d|bp|c|sec|mm|mmhg|pg|ppm|meq|liter|cu|cfu|mci|kj")
    if p.match(token) is not None:
        return 1
    else:
        return 0

def ATCGsequence(token):
    p = re.compile("([ATCGnN]{4,}|[AUCGnN]{4,})")
    if p.match(token) is not None:
        return 1
    else:
        return 0

def RNA(token):
    p = re.compile("(m|pre\\-m|t|r|a|g|mi|nc|pi|sh|si|sn|sno|tm)*RNA[s]*")
    if p.match(token) is not None:
        return 1
    else:
        return 0

def DNA(token):
    p = re.compile("(c|g|ms|mi)*DNA[s]*")
    if p.match(token) is not None:
        return 1
    else:
        return 0

def nuclein_acid_analogue(token):
    p = re.compile("([GLPT]NA|morpholino)[s]*")
    if p.match(token) is not None:
        return 1
    else:
        return 0

def cloning_vector(token):
    p = re.compile("(phagemid|plasmid|cosmid|lambda|P1|fosmid|BAC|YAC|HAC)[s]*")
    if p.match(token) is not None:
        return 1
    else:
        return 0

def nucleobase(token):
    p = re.compile("(purine|adenine|guanine|pyrimidine|uracil|thymine|cytosine)[s]*")
    if p.match(token) is not None:
        return 1
    else:
        return 0

def deoxynucleotide(token):
    p = re.compile("d[AGTC][MDT]P[s]*")
    if p.match(token) is not None:
        return 1
    else:
        return 0

def amino_acid(token):
    p = re.compile("(isoleucine|alanine|leucine|asparagine|lysine|aspartate|methionine|cysteine|phenylalanine|glutamate|threonine|glutamine|tryptophan|glycine|valine|proline|arginine|serine|histidine|tyrosine)[s]*")
    if p.match(token) is not None:
        return 1
    else:
        return 0

def vitamin(token):
    p = re.compile("retinoids|retinol|carotenoids|thiamine|riboflavin|niacin|niacinamide|pantothenic|pyridoxine|pyridoxamine|pyridoxal|biotin|folic|folinic|cyanocobalamin|hydroxycobalamin|methylcobalamin|ascorbic|ergocalciferol|cholecalciferol|tocopherols|tocotrienols|phylloquinone|menaquinones")
    if p.match(token) is not None:
        return 1
    else:
        return 0

def build_featurelist(token):
    featurelist = []

    #Grammar based features
    featurelist.append(stemmed_token(token))
    featurelist.append(pos_tag(token))
    featurelist.append(lemma(token))

    #featurelist.append(' '.join(charNgram(token)))
    #featurelist.append(' '.join(suffix(token)))
    for t in suffix(token):
        featurelist.append(t)

    for p in prefix(token):
        featurelist.append(p)

    #Features based on number of capital letters in token
    featurelist.append(initcap(token))
    featurelist.append(endcap(token))
    featurelist.append(allcaps(token))
    featurelist.append(lowercase(token))
    featurelist.append(mixcase(token))

    #Features based on length of tokens with all small case
    featurelist = featurelist + lowcount(token)

    #Features based on length of tokens with all CAPS
    featurelist = featurelist + capcount(token)

    #Features based on length of all numeric tokens
    featurelist = featurelist + digitcount(token)

    #Check if the token matches a special character
    featurelist.append(int(token == '-'))
    featurelist.append(int(token == '/'))
    featurelist.append(int(token == '['))
    featurelist.append(int(token == ']'))
    featurelist.append(int(token == ':'))
    featurelist.append(int(token == ';'))
    featurelist.append(int(token == '%'))
    featurelist.append(int(token == '('))
    featurelist.append(int(token == ')'))
    featurelist.append(int(token == ','))
    featurelist.append(int(token == '.'))
    featurelist.append(int(token == '\''))
    featurelist.append(int(token == '`'))
    featurelist.append(int(token == '*'))
    featurelist.append(int(token == '='))
    featurelist.append(int(token == '='))
    featurelist.append(int(token == '+'))

    #Other features - not yet commented properly
    featurelist.append(nucleoside(token))
    featurelist.append(nucleotide(token))
    featurelist.append(roman(token))
    featurelist.append(wordlength(token))
    featurelist.append(greek(token))
    featurelist.append(units(token))
    featurelist.append(ATCGsequence(token))
    featurelist.append(RNA(token))
    featurelist.append(DNA(token))
    featurelist.append(nuclein_acid_analogue(token))
    featurelist.append(cloning_vector(token))
    featurelist.append(nucleobase(token))
    featurelist.append(deoxynucleotide(token))
    featurelist.append(amino_acid(token))
    featurelist.append(vitamin(token))
    return featurelist

def token_features(root,token):
    """
    Given a token and its XML tag, build a list of features for that token
    """
    global parent_map

    if len(parent_map.keys()) <= 0:
        print "parent_map not set yet. exiting program"
        sys.exit(1)

    feature_list = []
    """
    First add the token itself
    """
    feature_list.append(token.lower())

    """
    First add all the positional features
    """
    feature_list.append(root.tag)
    feature_list.append(parent_map[root].tag)
    if "sid" in root.attrib:
        feature_list.append(root.attrib["sid"])
    else:
        feature_list.append(-1)

    if "id" in root.attrib:
        feature_list.append(root.attrib["id"])
    else:
        feature_list.append(-1)

    """
    Now add the rest of the features
    """
    feature_list += build_featurelist(token)
    return feature_list

def set_parent_map(pmap):
    global parent_map
    parent_map = pmap

build_featurelist('running')