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
    Dynamically generates a grammar in Backus Naur Form (BNF) notation representing the available Spacy NLP
    Linguistic Features
    Args:
        samples: List of Spacy Doc objects

    Returns: Backus Naur Form grammar notation encoded in a dictionary

    """
    # BNF root
    pattern_grammar = {S: P}

    # Watch out features of seen samples and max number of tokens per sample
    max_length_token, min_length_token, features_dict = features_seen(samples)

    # Update times token per pattern [Min length of tokens, Max length of tokens] interval
    pattern_grammar[P] = _symbol_stacker(T, max_length_token)

    #  Update times features per token (Max length of features)
    pattern_grammar[T] = _symbol_stacker(F, _get_features_per_token(features_dict))

    if config.use_token_wildcard is True:
        pattern_grammar[T].append(TOKEN_WILDCARD)

    # Update available features (just the features list)
    list_of_features = list(features_dict.keys())
    if config.use_grammar_operators is True and config.use_extended_pattern_syntax is False:
        list_of_features_op = list()
        for feature in list_of_features:
            list_of_features_op.append(feature)
            list_of_features_op.append(feature + ',' + OP)
        pattern_grammar[F] = list_of_features_op
        pattern_grammar[OP] = [NEGATION, ZERO_OR_ONE, ONE_OR_MORE, ZERO_OR_MORE]
    elif config.use_extended_pattern_syntax is True and config.use_grammar_operators is False:
        list_of_features_op = list()
        for feature in list_of_features:
            list_of_features_op.append(feature)
            list_of_features_op.append(feature + ',' + XPS)
        full_terminal_stack = _all_feature_terminal_list(features_dict)
        pattern_grammar[F] = list_of_features_op
        pattern_grammar[XPS] = [IN, NOT_IN, EQQ, GEQ, LEQ, GTH, LTH]
        pattern_grammar[IN] = full_terminal_stack
        pattern_grammar[NOT_IN] = full_terminal_stack
        pattern_grammar[EQQ] = LENGTH
        pattern_grammar[GEQ] = LENGTH
        pattern_grammar[LEQ] = LENGTH
        pattern_grammar[GTH] = LENGTH
        pattern_grammar[LTH] = LENGTH
    else:
        pattern_grammar[F] = list_of_features

    # Update each feature possible values
    for k, v in features_dict.items():
        pattern_grammar.update({k: v})

    return pattern_grammar


def _symbol_stacker(symbol: str, max_length: int) -> list:
    """
    Given a symbol creates a list of length max_length where each item is symbol concat previous list item
    Args:
        symbol: string
        max_length: list max length

    Returns: list of symbol

    """
    symbol_times_list = list()

    last = ''
    for _ in range(max_length):
        if last == '':
            last = symbol
        else:
            last = last + "," + symbol
        symbol_times_list.append(last)

    return symbol_times_list


def _all_feature_terminal_list(features_dict: dict) -> list:
    """
    Stacks all feature terminal options in a list of lists to be used for the extended pattern syntax
    Args:
        features_dict: dictionary of features keys with all possible feature value options

    Returns:

    """
    all_terminal_list = list()

    for item in list(features_dict.items()):
        current_terminal_holder = list()

        for terminal_list_item in item[1]:
            if len(current_terminal_holder) > 0:
                temp_list = list(current_terminal_holder[-1])
                temp_list.append(terminal_list_item)
                current_terminal_holder.append(temp_list)
            else:
                current_terminal_holder.append([terminal_list_item])

        all_terminal_list += current_terminal_holder

    return all_terminal_list


def _get_features_per_token(features_dict: dict) -> int:
    """
    Given the configuration set up, determine the maximum number of features per token at grammar
    Args:
        features_dict: dictionary of features keys with all possible feature value options

    Returns: integer

    """
    if config.features_per_token == 0:
        max_length_features = len(features_dict.keys())
    else:
        if len(features_dict.keys()) < config.features_per_token + 1:
            max_length_features = len(features_dict.keys())
        else:
            max_length_features = config.features_per_token

    return max_length_features
