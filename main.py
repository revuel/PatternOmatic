""" Entry Point """
import spacy


''' NLP Engine '''


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


def dynamic_grammar_generator(samples: list) -> dict:
    """
    Builds a specific Spacy grammar given a sample doc list
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


''' Grammatical Evolution '''


def genotype_to_fenotype(grammar: dict, int_list) -> str:
    """
    Decodes a given genotype to produce its related fenotype
    :param grammar: Grammar dict
    :param int_list: List of codons integer representation
    :return: String fenotype
    """
    import re, json
    from itertools import cycle

    done = False
    symbolic_string = grammar["<S>"]
    circular = cycle(int_list)

    # What we need here is to map each integer to its corresponding production rule of the grammar
    # From left to right, expand production rules until terminal expressions are reached
    # Consider codons as circular

    while done is not True:
        old_symbolic_string = symbolic_string  # Check if anything changed from last iteration

        for key in grammar.keys():
            if type(grammar[key]) is list:
                ci = next(circular)
                fire = divmod(ci, len(grammar[key]))[1]
                if key == '<T>':
                    symbolic_string = re.sub(key, "{" + str(grammar[key][fire]) + "}", symbolic_string, 1)
                elif key not in ['S', '<P>', '<T>','<F>']:
                    dkey = key.replace('<', '').replace('>', '')
                    feature = "\"" + dkey + "\"" + ":" + "\"" + str(grammar[key][fire]) +"\""
                    # feature = dkey + ":" + str(grammar[key][fire])
                    symbolic_string = re.sub(key, feature, symbolic_string, 1)
                else:
                    symbolic_string = re.sub(key, str(grammar[key][fire]), symbolic_string, 1)
            else:
                symbolic_string = re.sub(key, str(grammar[key]), symbolic_string, 1)

        if old_symbolic_string == symbolic_string:
            done = True

    return json.loads("[" + symbolic_string + "]")


''' Run '''
nlp = spacy.load("en_core_web_sm")

# Receive samples
sample_list = [nlp.tokenizer(u'Fuck it!'),
           nlp.tokenizer(u'Fuck off!'),
           nlp.tokenizer(u'Fuck all!'),
           nlp.tokenizer(u'Fuck you!')]

grammar = dynamic_grammar_generator(sample_list)


for k in grammar.keys():
    print(k, ":", str(grammar[k]))


individual_string = "111101100101001000010010101010010"
individual_integers = [2, 3, 4, 5]

print(str(genotype_to_fenotype(grammar, individual_integers)))
print(str(genotype_to_fenotype(grammar, [8, 1, 2, 5, 0, 7])))
print(str(genotype_to_fenotype(grammar, [7, 4, 1])))
print(str(genotype_to_fenotype(grammar, [0, 1, 6])))

from ge.individual import Individual

dude = Individual()
dude._int_genotype = [8, 1, 2, 5, 0, 7]
deco_dude = dude.decode(grammar)
print('decodude: ', str(deco_dude))
