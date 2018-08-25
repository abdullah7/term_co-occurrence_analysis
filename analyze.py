import sys
import csv
import json
import operator
from collections import defaultdict

import utils as utils

import matplotlib.pyplot as plt
import networkx as nx

def tokenize(tweet):
    """
    Cleans and tokenizes the tweets
    filter out the mentions, hashtags, punctuations and
    language specific stop words.

    :param tweet: the tweet object
    :return: the cleaned and parsed terms in the given tweet's text
    """
    return utils.get_text_normalized(tweet)



def update_co_occurrence_matrix(terms, com):
    """
    Update the passed com[co-occurrence matrix] for the given terms

      - we don’t want to count the same term pair twice, e.g. com[A][B] == com[B][A],
        so the inner for loop starts from i+1 in order to build a triangular matrix.

      - 'sorted' will preserve the alphabetical order of the terms.

    :param terms: list of terms
    :param com: the co-occurrence matrix
    """
    for i in range(len(terms) - 1):
        for j in range(i + 1, len(terms)):
            w1, w2 = sorted([terms[i], terms[j]])
            if w1 != w2:
                com[w1][w2] += 1



def build_co_occurrence_matrix(fname):
    """
    It reads tweets in the given file and :

     1. cleans the text of each tweet by removing mentions, hashtags, punctuations and stop-words
     2. builds the co-occurrence matrix (com) of terms collected from each tweet's text

    :param fname: the path to the file under analysis
    :return: the co-occurrence matrix (com)
    """
    com = defaultdict(lambda : defaultdict(int))
    with open(fname, 'r') as f:
        for line in f:
            # loads line as Python dictionary
            line = line.strip()
            if len(line) > 0 and line.startswith("{") and line.endswith("}"):
                tweet = json.loads(line)
                if 'text' in tweet:
                    # cleans and tokenizes the tweets
                    # filter out the mentions, hashtags, punctuations and
                    # language specific stop words.
                    terms_in_tweet = tokenize(tweet)

                    # update co-occurrence matrix for each term in this tweet
                    update_co_occurrence_matrix(terms_in_tweet, com)

    return com


def get_pair_count(com):
    com_max = []
    # For each term, look for the most common co-occurrent terms
    for t1 in com:
        t1_max_terms = sorted(com[t1].items(), key=operator.itemgetter(1), reverse=True)[:5]
        for t2, t2_count in t1_max_terms:
            com_max.append(((t1, t2), t2_count))
    # Get the most frequent co-occurrences
    terms_max = sorted(com_max, key=operator.itemgetter(1), reverse=True)
    return terms_max


def analyze_co_occurrence(fname):
    """
    Build co-occurrence matrix and calculates the count of same pairs.
    Then it returns list of those unique pairs with count.

    :param fname: the file containing all tweets
    :param term:  the term for which co-occurrence to look for
    :return: the list of tuples containing both terms and their co-occurrence count
             each tuple is of the format: ((term, other_term), count)
    """
    com = build_co_occurrence_matrix(fname=fname)
    return get_pair_count(com)


def filter_tuples_containing_term(tuples: list, term: str):
    """
    It filters the tuples containing the provided term

    :param tuples: the list of tuples containing co-occurred terms and their co-occurrence count
    :param term:   the term to filter
    :return:       the filtered tuples that contains the provided term
    """
    return list(filter(lambda _tuple: term in _tuple[0], tuples))


def export_co_occurrence(term: str, tuples: list, export_fname: str):
    """
    Export the co-occurrence of a term with others

    CSV Header with sample one data row is:

    +-----------------+-----------------+-------------+
    |term             |   other-term    |   count     |
    |(the given term) |  (term_string)  |             |
    +-------------------------------------------------+
    |  germany        |    france       |    4        |
    +-------------------------------------------------+

    :param term: the term we want to analyze
    :param tuples:  the list of tuples containing term , other-occurred term and count
    :param export_fname: the file name where to export all the tuples
    :return: void
    """

    # Exporting trending terms
    with open(export_fname, 'w', newline='') as csvfile:
        fieldnames = ['term', 'other-term', 'count']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        items = []
        for _tuple in tuples:
            if len(term) > 0:
                other_term = _tuple[0][1] if _tuple[0][0] == term else _tuple[0][0]
                items.append({'term': term, 'other-term': other_term, 'count': _tuple[1]})
            else:
                items.append({'term': _tuple[0][0], 'other-term': _tuple[0][1], 'count': _tuple[1]})

        sorted_items = sorted(items, key=lambda k: k['count'], reverse=True)
        writer.writerows(sorted_items)


def genereate_wordnet(tuples: list):
    items = []
    for _tuple in tuples:
            items.append("#" + _tuple[0][0] + ' #' + _tuple[0][1])

    with open('data/raw_data.txt', 'w') as file:
        for item in items:
            file.write(item)
            file.write('\n')

    # df, tf_idf = find_tf_idf(
    #     file_names=['data/raw_data.txt'],  # paths of files to be processed.(create using twitter_streamer.py)
    #     # prev_file_path = 'data/tfidf.tfidfpkl',  # prev TF_IDF file to modify over, format standard is .tfidfpkl. default = None
    #     dump_path = 'data/file.tfidfpkl'  # dump_path if tf-idf needs to be dumped, format standard is .tfidfpkl. default = None
    # )

    # words = find_knn(
    #     tf_idf=tf_idf,  # this tf_idf is returned by find_tf_idf() above.
    #     input_word='german',  # a word for which k nearest neighbours are required.
    #     k=10,  # k = number of neighbours required, default=10
    #     rand_on=True  # rand_on = either to randomly skip few words or show initial k words default=True
    # )

    # word_net = generate_net(
    #     df=df,  # this df is returned by find_tf_idf() above.
    #     tf_idf=tf_idf,  # this tf_idf is returned by find_tf_idf() above.
    #     dump_path='data/dump.wrnt'
    #     # dump_path = path to dump the generated files, format standard is .wrnt. default=None
    # )


def co_occurrence_network(tuples: list):
    dg = nx.DiGraph(name="Co-occurrence Graph")
    for _tuple in tuples:

        if len(_tuple) == 2:
            tuple_0_0_label = {'label': _tuple[0][0]}
            dg.add_node(_tuple[0][0], **tuple_0_0_label)
            tuple_0_1_label = {'label': _tuple[0][1]}
            dg.add_node(_tuple[0][1], **tuple_0_1_label)
            tuple_count = {'count': _tuple[1]}
            dg.add_weighted_edges_from([(_tuple[0][0], _tuple[0][1], _tuple[1])])

    return dg

if __name__ == "__main__":

    # File containing all tweets data
    fname = 'data/stream_.jsonl'

    if len(sys.argv) == 2 and len(sys.argv[1]) > 0:
        term = sys.argv[1]
        export_fname = 'data/' + term + '_co_occurrences.csv'
        tuples = analyze_co_occurrence(fname=fname)
        filtered_tuples = filter_tuples_containing_term(tuples=tuples, term=term)
        export_co_occurrence(term=term, tuples=filtered_tuples, export_fname=export_fname)
        tuples = filtered_tuples
    else:
        print("No term provided for analysis ...")
        print("Going to analyze all the terms and their co-occurrences.")
        print("Export file will contain all the tuples with their co-occurrence count.")
        export_fname = 'data/all_co_occurrences.csv'
        tuples = analyze_co_occurrence(fname=fname)
        export_co_occurrence(term='', tuples=tuples, export_fname=export_fname)

    # Directed Graph
    export_fname = 'data/co_occurrence.graphml'
    digraph = co_occurrence_network(tuples)
    nx.write_graphml(digraph, export_fname)
    print("Co-occurrence Graph is exported at [%s]" % export_fname)

