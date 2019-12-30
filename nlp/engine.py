""" NLP Engines """
from spacy.tokens import Doc
from settings.config import Config
from settings.literals import *

config = Config()

def features_seen(samples: [Doc]) -> int and dict:
    """
    Builds up a dictionary containing Spacy Linguistic Feature Keys and their respective seen values for the sample
    Args:
        samples: List of Spacy Doc objects

    Returns: Integer, the max length of a doc within the sample and a dict

    """
    # Just tokenizer features
    orth_list = []
    text_list = []
    lower_list = []
    length_list = []
    shape_list = []

    # Boolean ones (no need list)
    # · bool_list = [True, False]
    '''is_alpha_list = []
    is_ascii_list = []
    is_digit_list = []
    is_lower_list = []
    is_upper_list = []
    is_title_list = []
    is_punct_list = []
    is_space_list = []
    is_stop_list = []
    like_num = []
    like_url = []
    like_email = []'''

    # Require more than a tokenizer
    pos_list = []
    tag_list = []
    dep_list = []
    lemma_list = []
    ent_type_list = []

    # Capture the len of the largest doc
    max_doc_length = 0
    min_doc_length = 999999999

    for sample in samples:
        sample_length = len(sample)

        for token in sample:
            orth_list.append(token.orth_)
            text_list.append(token.text)
            lower_list.append(token.lower_)
            length_list.append(len(token))
            pos_list.append(token.pos_)
            tag_list.append(token.tag_)
            dep_list.append(token.dep_)
            lemma_list.append(token.lemma_)
            shape_list.append(token.shape_)
            ent_type_list.append(token.ent_type_)

        if sample_length > max_doc_length:
            max_doc_length = sample_length

        if sample_length < min_doc_length:
            min_doc_length = sample_length

    features = {ORTH: sorted(list(set(orth_list))),
                TEXT: sorted(list(set(text_list))),
                LOWER: sorted(list(set(lower_list))),
                LENGTH: sorted(list(set(length_list))),
                POS: sorted(list(set(pos_list))),
                TAG: sorted(list(set(tag_list))),
                DEP: sorted(list(set(dep_list))),
                LEMMA: sorted(list(set(lemma_list))),
                SHAPE: sorted(list(set(shape_list))),
                ENT: sorted(list(set(ent_type_list)))}

    to_del_list = list()
    for k in features.keys():
        if len(features[k]) == 1 and features[k][0] == '':
            to_del_list.append(k)

    for k_item in to_del_list:
        del features[k_item]

    return max_doc_length, min_doc_length, features


def dynagg(samples: [Doc]) -> dict:
    """
    Dynamically generates a grammar in Backus Nuar Form notation representing the
    available Spacy NLP Linguistic Features
    Args:
        samples: List of Spacy Doc objects

    Returns: Backus Naur Form grammar notation encoded in a dictionary

    """
    pattern_grammar = {S: P}

    # Watch out features of seen samples and max number of tokens per sample
    max_length_token, min_length_token, features_dict = features_seen(samples)

    # Update times token per pattern [Min length of tokens, Max length of tokens] interval
    token_times = list()

    last = ''
    for _ in range(min_length_token):
        if last == '':
            last = T
        else:
            last = last + "," + T
    token_times.append(last)

    if min_length_token != max_length_token:

        inner_length_token = max_length_token - min_length_token

        for _ in range(inner_length_token):
            last = token_times[-1]
            last = last + "," + T
            token_times.append(last)

    pattern_grammar[P] = token_times

    #  Update times features per token (Max length of features)
    if config._features_per_token == 0:
        max_length_features = len(features_dict.keys())
    else:
        if len(features_dict.keys()) < config._features_per_token + 1:
            max_length_features = len(features_dict.keys())
        else:
            max_length_features = config._features_per_token

    feature_times = list()
    feature_times.append(F)
    for _ in range(max_length_features - 1):
        last = feature_times[-1]
        last = last + "," + F
        feature_times.append(last)

    pattern_grammar[T] = feature_times

    # Update available features (just the features list)
    pattern_grammar[F] = list(features_dict.keys())

    # Update each feature possible values
    for k, v in features_dict.items():
        pattern_grammar.update({k: v})

    return pattern_grammar
