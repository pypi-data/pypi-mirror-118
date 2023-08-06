# this file contains feature extractor functions used by some of the models
# this means that models using this require this package installed and can
# NOT be loaded directly with pickle module only
import re
import nltk
from nltk.stem.snowball import SnowballStemmer


def get_word_shape(word):
    word_shape = 'other'
    if re.match('[0-9]+(\.[0-9]*)?|[0-9]*\.[0-9]+$', word):
        word_shape = 'number'
    elif re.match('\W+$', word):
        word_shape = 'punct'
    elif re.match('[A-Z][a-z]+$', word):
        word_shape = 'capitalized'
    elif re.match('[A-Z]+$', word):
        word_shape = 'uppercase'
    elif re.match('[a-z]+$', word):
        word_shape = 'lowercase'
    elif re.match('[A-Z][a-z]+[A-Z][a-z]+[A-Za-z]*$', word):
        word_shape = 'camelcase'
    elif re.match('[A-Za-z]+$', word):
        word_shape = 'mixedcase'
    elif re.match('__.+__$', word):
        word_shape = 'wildcard'
    elif re.match('[A-Za-z0-9]+\.$', word):
        word_shape = 'ending-dot'
    elif re.match('[A-Za-z0-9]+\.[A-Za-z0-9\.]+\.$', word):
        word_shape = 'abbreviation'
    elif re.match('[A-Za-z0-9]+\-[A-Za-z0-9\-]+.*$', word):
        word_shape = 'contains-hyphen'

    return word_shape


def extract_iob_features(tokens, index, history, stemmer=None, memory=2):
    """
    `tokens`  = a POS-tagged sentence [(w1, t1), ...]
    `index`   = the index of the token we want to extract features for
    `history` = the previous predicted IOB tags
    """
    feat_dict = extract_postag_features(tokens, index, stemmer=stemmer,
                                        memory=memory)

    # Pad the sequence with placeholders
    tokens = ['O'] * memory + history

    index += memory

    # look back N predictions
    for i in range(1, memory + 1):
        k = "prev-" * i
        previob = tokens[index - i]
        # update with IOB features
        feat_dict[k + "iob"] = previob

    return feat_dict


def extract_postag_features(tokens, index, stemmer=None, memory=2):
    """
    `tokens`  = a POS-tagged sentence [(w1, t1), ...]
    `index`   = the index of the token we want to extract features for
    """
    original_toks = list(tokens)
    # word features
    feat_dict = extract_word_features([t[0] for t in tokens],
                                      index, stemmer, memory=memory)

    # Pad the sequence with placeholders
    tokens = []
    for i in range(1, memory + 1):
        tokens.append((f'__START{i}__', f'__START{i}__'))
    tokens = list(reversed(tokens)) + original_toks
    for i in range(1, memory + 1):
        tokens.append((f'__END{i}__', f'__END{i}__'))

    # shift the index to accommodate the padding
    index += memory

    word, pos = tokens[index]

    # update with postag features
    feat_dict["pos"] = pos

    # look ahead N words
    for i in range(1, memory + 1):
        k = "next-" * i
        nextword, nextpos = tokens[index + i]
        feat_dict[k + "pos"] = nextpos

    # look back N words
    for i in range(1, memory + 1):
        k = "prev-" * i
        prevword, prevpos = tokens[index - i]
        feat_dict[k + "pos"] = prevpos

    return feat_dict


def extract_word_features(tokens, index=0, stemmer=None, memory=2):
    """
    `tokens`  = a tokenized sentence [w1, w2, ...]
    `index`   = the index of the token we want to extract features for
    """
    if isinstance(tokens, str):
        tokens = [tokens]
    original_toks = list(tokens)
    # init the stemmer
    stemmer = stemmer or SnowballStemmer('english')

    # Pad the sequence with placeholders
    tokens = []
    for i in range(1, memory + 1):
        tokens.append(f'__START{i}__')
    tokens = list(reversed(tokens)) + original_toks
    for i in range(1, memory + 1):
        tokens.append(f'__END{i}__')

    # shift the index to accommodate the padding
    index += memory

    word = tokens[index]
    feat_dict = extract_single_word_features(word)
    feat_dict["word"] = word
    feat_dict["shape"] = get_word_shape(word)
    feat_dict["lemma"] = stemmer.stem(word)

    # look ahead N words
    for i in range(1, memory + 1):
        k = "next-" * i
        nextword = tokens[index + i]
        feat_dict[k + "word"] = nextword
        feat_dict[k + "lemma"] = stemmer.stem(nextword)
        feat_dict[k + "shape"] = get_word_shape(nextword)

    # look back N words
    for i in range(1, memory + 1):
        k = "prev-" * i
        prevword = tokens[index - i]
        feat_dict[k + "word"] = prevword
        feat_dict[k + "lemma"] = stemmer.stem(prevword)
        feat_dict[k + "shape"] = get_word_shape(prevword)

    return feat_dict


def extract_single_word_features(word):

    feat_dict = {
        'suffix1': word[-1:],
        'suffix2': word[-2:],
        'suffix3': word[-3:],
        'prefix1': word[:1],
        'prefix2': word[:2],
        'prefix3': word[:3]
    }
    return feat_dict


def extract_rte_features(rtepair):
    extractor = nltk.RTEFeatureExtractor(rtepair)
    features = {}
    features['word_overlap'] = len(extractor.overlap('word'))
    features['word_hyp_extra'] = len(extractor.hyp_extra('word'))
    features['ne_overlap'] = len(extractor.overlap('ne'))
    features['ne_hyp_extra'] = len(extractor.hyp_extra('ne'))
    return features