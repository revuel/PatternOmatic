""" Backus Naur Form Grammar Generator module

This file is part of PatternOmatic.

Copyright © 2020  Miguel Revuelta Espinosa

PatternOmatic is free software: you can redistribute it and/or
modify it under the terms of the GNU Lesser General Public License
as published by the Free Software Foundation, either version 3 of
the License, or (at your option) any later version.

PatternOmatic is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License
along with PatternOmatic. If not, see <https://www.gnu.org/licenses/>.

"""
from inspect import getmembers
from spacy.tokens import Doc, Token
from PatternOmatic.settings.config import Config
from PatternOmatic.settings.literals import S, P, T, F, OP, NEGATION, ZERO_OR_ONE, ZERO_OR_MORE, ONE_OR_MORE, LENGTH, \
    XPS, IN, NOT_IN, EQQ, GEQ, LEQ, GTH, LTH, TOKEN_WILDCARD, UNDERSCORE, EF, ORTH, TEXT, LOWER, POS, TAG, DEP, LEMMA, \
    SHAPE, ENT_TYPE, IS_ALPHA, IS_ASCII, IS_DIGIT, IS_BRACKET, IS_LOWER, IS_PUNCT, IS_QUOTE, IS_SPACE, IS_TITLE, \
    IS_OOV, IS_UPPER, IS_STOP, IS_CURRENCY, IS_LEFT_PUNCT, IS_RIGHT_PUNCT, LIKE_NUM, LIKE_EMAIL, \
    LANG, NORM, PREFIX, SENTIMENT, STRING, SUFFIX, TEXT_WITH_WS, WHITESPACE, LIKE_URL, MATCHER_SUPPORTED_ATTRIBUTES, \
    ENT_ID, ENT_IOB, ENT_KB_ID, HAS_VECTOR
from PatternOmatic.settings.log import LOG


#
# Dynamic Grammar (Backus Naur Form) Generator
#
def dynamic_generator(samples: [Doc]) -> dict:
    """
    Dynamically generates a grammar in Backus Naur Form (BNF) notation representing the available Spacy NLP
    Linguistic Feature values of the given sample list of Doc instances
    Args:
        samples: List of Spacy Doc objects

    Returns: Backus Naur Form grammar notation encoded in a dictionary

    """
    config = Config()

    LOG.info(f'Generating BNF based on the following samples: {str(samples)}')

    # BNF root
    pattern_grammar = {S: [P]}

    # Watch out features of seen samples and max number of tokens per sample
    max_length_token, min_length_token, features_dict, extended_features = _features_seen(samples)

    # Update times token per pattern [Min length of tokens, Max length of tokens] interval
    pattern_grammar[P] = _symbol_stacker(T, max_length_token, min_length_token)

    # Update times features per token (Max length of features)
    pattern_grammar[T] = _symbol_stacker(F, _get_features_per_token(features_dict))

    if config.use_token_wildcard is True:
        pattern_grammar[T].append(TOKEN_WILDCARD)

    # Update available features (just the features list)
    list_of_features = list(features_dict.keys())
    if config.use_grammar_operators is True and config.use_extended_pattern_syntax is False:
        pattern_grammar = _add_grammar_operators(pattern_grammar, list_of_features)
    elif config.use_extended_pattern_syntax is True and config.use_grammar_operators is False:
        pattern_grammar = _add_extended_pattern_syntax(pattern_grammar, list_of_features, features_dict)
    else:
        pattern_grammar[F] = list_of_features

    # Update each feature possible values
    for k, v in features_dict.items():
        if config.use_extended_pattern_syntax is True:
            v.append(XPS)
        pattern_grammar.update({k: v})

    if config.use_custom_attributes is True:
        pattern_grammar = _add_custom_attributes(pattern_grammar, extended_features)

    LOG.info(f'Dynamically generated BNF: {str(pattern_grammar)}')

    return pattern_grammar


#
# BNF Utilities
#
def _features_seen(samples: [Doc]) -> (int, int, dict, dict):
    """
    Builds up a dictionary containing Spacy Linguistic Feature Keys and their respective seen values for the sample
    Args:
        samples: List of Spacy Doc objects

    Returns: Integer, the max length of a doc within the sample and a dict of features

    """
    config = Config()

    # Just tokenizer features
    orth_list = []
    text_list = []
    lower_list = []
    length_list = []
    shape_list = []

    # For boolean features
    bool_list = [True, False]

    # Require more than a tokenizer
    pos_list = []
    tag_list = []
    dep_list = []
    lemma_list = []
    ent_type_list = []

    # Capture the len of the largest doc
    max_doc_length = 0
    min_doc_length = 999999999

    # Set token extensions
    if config.use_custom_attributes is True:
        _set_token_extension_attributes(samples[0][0])
        extended_features = _extended_features_seen([token for sample in samples for token in sample])
    else:
        extended_features = {UNDERSCORE: {}}

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

        # Checks for max/min length of tokens per sample
        if sample_length > max_doc_length:
            max_doc_length = sample_length

        if sample_length < min_doc_length:
            min_doc_length = sample_length

    if config.use_uniques is True:
        features = {ORTH: sorted(list(set(orth_list))),
                    TEXT: sorted(list(set(text_list))),
                    LOWER: sorted(list(set(lower_list))),
                    LENGTH: sorted(list(set(length_list))),
                    POS: sorted(list(set(pos_list))),
                    TAG: sorted(list(set(tag_list))),
                    DEP: sorted(list(set(dep_list))),
                    LEMMA: sorted(list(set(lemma_list))),
                    SHAPE: sorted(list(set(shape_list))),
                    ENT_TYPE: sorted(list(set(ent_type_list)))}
    else:
        features = {ORTH: orth_list,
                    TEXT: text_list,
                    LOWER: lower_list,
                    LENGTH: length_list,
                    POS: pos_list,
                    TAG: tag_list,
                    DEP: dep_list,
                    LEMMA: lemma_list,
                    SHAPE: shape_list,
                    ENT_TYPE: ent_type_list}

    # Add boolean features
    if config.use_boolean_features is True:
        features.update({
            IS_ALPHA: bool_list,
            IS_ASCII: bool_list,
            IS_DIGIT: bool_list,
            IS_LOWER: bool_list,
            IS_UPPER: bool_list,
            IS_TITLE: bool_list,
            IS_PUNCT: bool_list,
            IS_SPACE: bool_list,
            IS_STOP: bool_list,
            LIKE_NUM: bool_list,
            LIKE_URL: bool_list,
            LIKE_EMAIL: bool_list
        })

    # Drop all observations equal to empty string
    features = _feature_pruner(features)
    extended_features[UNDERSCORE] = _feature_pruner(extended_features[UNDERSCORE])

    return max_doc_length, min_doc_length, features, extended_features


def _set_token_extension_attributes(token: Token) -> None:
    """
    Given a Spacy Token instance, register all the Spacy token attributes not accepted by the Spacy Matcher
    as custom attributes inside the Token Extensions (token._. space)
    Returns: None

    """
    # Retrieve cleaned up Token Attributes
    token_attributes = _clean_token_attributes(
        {k: v for k, v in getmembers(token) if type(v) in (str, bool, float)})

    # Set token custom attributes
    lambda_list = []
    i = 0
    for k, v in token_attributes.items():
        lambda_list.append(lambda token_=token, k_=k: getattr(token_, k_))
        token.set_extension(str('custom_'+k).upper(), getter=lambda_list[i])
        i += 1


def _clean_token_attributes(token_attributes: dict) -> dict:
    """
    Removes from input dict keys contained in a set that represents the Spacy Matcher supported token attributes
    Args:
        token_attributes: dict of token features

    Returns: Token attributes dict without Spacy Matcher's supported attribute keys

    """
    token_attributes.pop('__doc__')
    for item in MATCHER_SUPPORTED_ATTRIBUTES:
        token_attributes.pop(item)

    return token_attributes


def _extended_features_seen(tokens: [Token]) -> dict:
    """
    Builds up a dictionary containing Spacy Linguistic Feature Keys and their respective seen values for the
    input token list extended attributes (those attributes not accepted by the Spacy Matcher by default,
    included as token extensions)
    Args:
        tokens: List of Spacy Token instances

    Returns: dict of features

    """
    bool_list = [True, False]

    extended_features = \
        {
            UNDERSCORE: {
                ENT_ID: sorted(list(set([getattr(getattr(token, '_'), 'CUSTOM_ENT_ID_') for token in tokens]))),
                ENT_IOB: sorted(list(set([getattr(getattr(token, '_'), 'CUSTOM_ENT_IOB_') for token in tokens]))),
                ENT_KB_ID: sorted(list(set([getattr(getattr(token, '_'), 'CUSTOM_ENT_KB_ID_') for token in tokens]))),
                HAS_VECTOR: bool_list,
                IS_BRACKET: bool_list,
                IS_CURRENCY: bool_list,
                IS_LEFT_PUNCT: bool_list,
                IS_OOV: bool_list,
                IS_QUOTE: bool_list,
                IS_RIGHT_PUNCT: bool_list,
                # IS_SENT_START:
                #     sorted(list(set([getattr(getattr(token, '_'), 'CUSTOM_IS_SENT_START') for token in tokens]))),
                LANG: sorted(list(set([getattr(getattr(token, '_'), 'CUSTOM_LANG_') for token in tokens]))),
                NORM: sorted(list(set([getattr(getattr(token, '_'), 'CUSTOM_NORM_') for token in tokens]))),
                PREFIX: sorted(list(set([getattr(getattr(token, '_'), 'CUSTOM_PREFIX_') for token in tokens]))),
                # PROB:
                #     sorted(list(set([abs(getattr(getattr(token, '_'), 'CUSTOM_PROB')) for token in tokens]))),
                SENTIMENT: sorted(list(set([getattr(getattr(token, '_'), 'CUSTOM_SENTIMENT') for token in tokens]))),
                STRING: sorted(list(set([getattr(getattr(token, '_'), 'CUSTOM_STRING') for token in tokens]))),
                SUFFIX: sorted(list(set([getattr(getattr(token, '_'), 'CUSTOM_SUFFIX_') for token in tokens]))),
                TEXT_WITH_WS: sorted(list(set(
                    [getattr(getattr(token, '_'), 'CUSTOM_TEXT_WITH_WS') for token in tokens]))),
                WHITESPACE: sorted(list(set([getattr(getattr(token, '_'), 'CUSTOM_WHITESPACE_') for token in tokens])))
            }
        }

    return extended_features


def _feature_pruner(features: dict) -> dict:
    """
    Prunes dict keys whose values contain a list of repeated items
    Args:
        features: dict

    Returns: pruned dict

    """
    # Drop all observations equal to empty string
    to_del_list = list()
    for k in features.keys():
        if len(features[k]) == 1 and features[k][0] == '':
            to_del_list.append(k)

    for k_item in to_del_list:
        features.pop(k_item)

    return features


def _symbol_stacker(symbol: str, max_length: int, min_length: int = 1) -> list:
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

    if 1 < min_length <= max_length:
        symbol_times_list = symbol_times_list[min_length-1:]

    return symbol_times_list


def _get_features_per_token(features_dict: dict) -> int:
    """
    Given the configuration set up, determine the maximum number of features per token at grammar
    Args:
        features_dict: dictionary of features keys with all possible feature value options

    Returns: integer

    """
    config = Config()

    if config.features_per_token <= 0:
        max_length_features = len(features_dict.keys())
    else:
        if len(features_dict.keys()) < config.features_per_token + 1:
            max_length_features = len(features_dict.keys())
        else:
            max_length_features = config.features_per_token

    return max_length_features


def _add_grammar_operators(pattern_grammar: dict, list_of_features: list) -> dict:
    """
    Adds support to Spacy's grammar operators usage
    Args:
        pattern_grammar: BNF dict
        list_of_features: list of token features

    Returns: Backus Naur Form grammar notation encoded in a dictionary with Spacy's grammar operators

    """
    list_of_features_op = list()
    for feature in list_of_features:
        list_of_features_op.append(feature)
        list_of_features_op.append(feature + ',' + OP)
    pattern_grammar[F] = list_of_features_op
    pattern_grammar[OP] = [NEGATION, ZERO_OR_ONE, ONE_OR_MORE, ZERO_OR_MORE]
    return pattern_grammar


def _add_extended_pattern_syntax(pattern_grammar: dict, list_of_features: list, features_dict: dict) -> dict:
    """
    Adds support to the extended pattern syntax at BNF dicts
    Args:
        pattern_grammar: BNF dict
        list_of_features: list of token features
        features_dict: dict of token features

    Returns:
        dict: Backus Naur Form grammar notation encoded in a dictionary with Spacy's extended pattern syntax
    """
    tmp_lengths = features_dict[LENGTH].copy()
    full_terminal_stack = _all_feature_terminal_list(features_dict)
    pattern_grammar[F] = list_of_features
    pattern_grammar[XPS] = [IN, NOT_IN, EQQ, GEQ, LEQ, GTH, LTH]
    pattern_grammar[IN] = full_terminal_stack
    pattern_grammar[NOT_IN] = full_terminal_stack
    pattern_grammar[EQQ] = tmp_lengths
    pattern_grammar[GEQ] = tmp_lengths
    pattern_grammar[LEQ] = tmp_lengths
    pattern_grammar[GTH] = tmp_lengths
    pattern_grammar[LTH] = tmp_lengths

    return pattern_grammar


def _all_feature_terminal_list(features_dict: dict) -> list:
    """
    Stacks all feature terminal options in a list of lists to be used for the extended pattern syntax set operators
    Args:
        features_dict: dictionary of feature keys with all possible feature value options

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

    all_terminal_list = [ele for ind, ele in enumerate(all_terminal_list) if ele not in all_terminal_list[:ind]]
    return all_terminal_list


def _add_custom_attributes(pattern_grammar: dict, extended_features: dict) -> dict:
    """
    Adds support to a specific set of custom attributes at BNF dict
    Args:
        pattern_grammar: BNF dict
        extended_features: dict of token features not supported by default by the Spacy's Matcher

    Returns: Backus Naur Form grammar notation encoded in a dictionary with Spacy's custom attributes

    """
    pattern_grammar[UNDERSCORE] = _symbol_stacker(EF, _get_features_per_token(extended_features[UNDERSCORE]))
    pattern_grammar[EF] = list(extended_features[UNDERSCORE].keys())
    pattern_grammar.update(extended_features[UNDERSCORE].items())
    pattern_grammar[T].append(UNDERSCORE)
    pattern_grammar[T].append(F + "," + UNDERSCORE)
    return pattern_grammar
