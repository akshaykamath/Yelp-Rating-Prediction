__version__ = "0.1"
__date__ = "Nov. 29, 2015"
__author__ = "Akshay Kamath"

"""
This code is used to predict the ratings of a review using the naive bayes classifier.
"""
##################

import codecs
from random import shuffle
from nltk.util import bigrams
from nltk.util import trigrams
from nltk.util import everygrams
import nltk.classify.util
from nltk.classify import NaiveBayesClassifier


def read_file_data():
    with codecs.open("Data\stars_reviews.txt", "r", "utf-8") as my_file:
        lines = [next(my_file) for x in xrange(2000)]

    data_tuples = []

    for line in lines:
        try:
            tup = (get_trigram_word_dict(line.split("\t")[1].lower()), line.split("\t")[0])
            data_tuples.append(tup)
        except:
            continue

    print "len: ", len(data_tuples)
    return data_tuples


def get_pos_word_dict(emotion_line):
    words = nltk.word_tokenize(emotion_line)
    pos_words = nltk.pos_tag(words)

    word_feats = {}
    for w in pos_words:
        if w[1] != 'RB' or w[1] != 'NN' or w[1] != 'JJ':
            print w[1]
            continue

        if w[0] not in word_feats:
            word_feats[w[0]] = "feature_word"

    return word_feats


def get_word_dict(emotion_line):
    words = nltk.word_tokenize(emotion_line)

    word_feats = {}
    for w in words:
        if w not in word_feats:
            word_feats[w] = "feature_word"

    return word_feats


def get_trigram_word_dict(emotion_line):
    words = nltk.word_tokenize(emotion_line)
    word_bigrams = list(bigrams(words))
    word_trigrams = list(trigrams(words))

    word_feats = {}
    for w in words:
        if w not in word_feats:
            word_feats[w] = "feature_word"

    for w in word_bigrams:
        if w not in word_feats:
            word_feats[w] = "feature_word"

    for w in word_trigrams:
        if w not in word_feats:
            word_feats[w] = "feature_word"

    return word_feats


def get_ngram_word_dict(emotion_line):
    words = nltk.word_tokenize(emotion_line)
    word_ngram = everygrams(words, min_len=1, max_len=3)

    word_feats = {}
    for w in word_ngram:
        if w not in word_feats:
            word_feats[w] = "feature_word"

    return word_feats


def main():
    data_tuples = read_file_data()
    print "Length of data tuple is: ", len(data_tuples)
    shuffle(data_tuples)

    train_tuples = data_tuples[:1000]
    test_tuples = data_tuples[1000:]
    classifier = NaiveBayesClassifier.train(train_tuples)
    print 'accuracy:', nltk.classify.util.accuracy(classifier, test_tuples)
    classifier.show_most_informative_features()


if __name__ == "__main__":
    print "Naive Classification of Yelp data set to predict ratings."
    main()
