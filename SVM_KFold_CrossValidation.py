author = 'Sanket'
modified = 'Akshay'

"""
Edit1: I have refactored the code, removed unwanted methods, updated the variable names
- Akshay

Edit 2: I have also added K-Fold cross validation on the data set!!
"""
#########################################################
import sys
reload(sys)
sys.setdefaultencoding('utf8')

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.svm import SVC
from sklearn.multiclass import OneVsRestClassifier
from sklearn import cross_validation
from sklearn.metrics import classification_report
from sklearn.metrics import accuracy_score
from sklearn import metrics


def load_file():
    with open('Data\stars_reviews.txt', "r") as loadfp:
        stars = []
        review_text = []
        count = 0

        for row in loadfp.readlines():
            stars_split = row.split("\t")[0]
            review_split = row.split("\t")[1]
            if stars_split and review_split:
                stars.append(stars_split)
                review_text.append(review_split)

            count += 1
            if count > 25000:
                print "loaded"
                break

        return review_text, stars


def pre_process(data, target):
    count_vectorized = CountVectorizer(binary='false', ngram_range=(0, 1))
    data = count_vectorized.fit_transform(data)
    tfidf_data = TfidfTransformer(use_idf=True, smooth_idf=True).fit_transform(data)
    print "Calculating term frequency."
    return tfidf_data


def learn_model(reviews, stars):
    svm = OneVsRestClassifier(SVC(C=1, kernel='linear', gamma=1, verbose=False, probability=False))

    print "-" * 60, "\n"
    print "Results with 10-fold cross validation:\n"
    print "-" * 60, "\n"

    predicted = cross_validation.cross_val_predict(svm, reviews, stars, cv=10, n_jobs=1)
    print "*" * 20
    print "\t Accuracy Score\t", metrics.accuracy_score(stars, predicted)
    print "*" * 20

    print "Precision Score\t", metrics.precision_score(stars, predicted)
    print "Recall Score\t", metrics.recall_score(stars, predicted)
    print "\nClassification Report:\n\n", metrics.classification_report(stars, predicted)
    print "\nConfusion Matrix:\n\n", metrics.confusion_matrix(stars, predicted)


def evaluate_model(target_true, target_predicted):
    print classification_report(target_true, target_predicted)
    print "The accuracy score is {:.2%}".format(accuracy_score(target_true, target_predicted))


def main():
    print ("Loading file and getting reviews..")
    data, target = load_file()
    print "Get All Data."
    tf_idf = pre_process(data, target)
    learn_model(tf_idf, target)


main()
