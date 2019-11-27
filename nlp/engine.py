""" NLP Engines """


def features_seen(samples: list) -> int and dict:
    """
    Returns a dict of features and its seen unique values
    :param samples: A list of docs
    :return: A dict where each key is a spacy feature and its val is the list of the detected values of that feature
    given a sample list of docs
    """

    # Just tokenizer features
    orth_list = []
    text_list = []
    lower_list = []
    length_list = []

    # Boolean ones (no need list)
    bool_list = [True, False]
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
    shape_list = []  # move up ?
    ent_type_list = []

    # Capture the len of the largest doc
    max_doc_length = 0

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

    # TODO: Some features have a total positive correlation, one way of removing unneeded features would be comparing some list of features and if they're equal, remove one feature list

    features = {'<ORTH>': sorted(list(set(orth_list))),
                '<TEXT>': sorted(list(set(text_list))),
                '<LOWER>': sorted(list(set(lower_list))),
                '<LENGTH>': sorted(list(set(length_list))),
                '<POS>': sorted(list(set(pos_list))),
                '<TAG>': sorted(list(set(tag_list))),
                '<DEP>': sorted(list(set(dep_list))),
                '<LEMMA>': sorted(list(set(lemma_list))),
                '<SHAPE>': sorted(list(set(shape_list))),
                '<ENT>': sorted(list(set(ent_type_list)))}

    to_del_list = list()
    for k in features.keys():
        if len(features[k]) == 1 and features[k][0] == '':
            to_del_list.append(k)

    for k_item in to_del_list:
        del features[k_item]

    return max_doc_length, features


def dynagg(samples: list) -> dict:
    """
    Dynamic Grammar Generator (spacy) Builds a specific Spacy grammar given a sample doc list
    :return: dict
    """
    pattern_grammar = {"<S>": "<P>"}

    # Watch out features of seen samples and max number of tokens per sample
    max_length_token, features_dict = features_seen(samples)

    # Update times token per pattern (Max length of tokens)
    token_symbol = "<T>"
    token_times = list()
    token_times.append(token_symbol)
    for _ in range(max_length_token - 1):
        last = token_times[-1]
        last = last + "," + token_symbol
        token_times.append(last)

    pattern_grammar["<P>"] = token_times

    #  Update times features per token (Max length of features)
    max_length_features = len(features_dict.keys())
    feature_symbol = "<F>"
    feature_times = list()
    feature_times.append(feature_symbol)
    for _ in range(max_length_features - 1):
        last = feature_times[-1]
        last = last + "," + feature_symbol
        feature_times.append(last)

    pattern_grammar["<T>"] = feature_times

    # Update available features
    pattern_grammar["<F>"] = list(features_dict.keys())  # Just the features list

    # Update each feature possible values
    for k, v in features_dict.items():
        pattern_grammar.update({k: v})

    return pattern_grammar
