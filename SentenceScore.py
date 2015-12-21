__author__ = 'Pratish'

# Predict a sentence score out of 5 based on sentiments in a sentence
# This requires a file of sentences as input

import codecs
import re
from collections import Counter
from nltk.tokenize import word_tokenize
import sys
from nltk.corpus import stopwords
import matplotlib.pyplot as plt
from os import path
from wordcloud import WordCloud

reload(sys)

sys.setdefaultencoding('utf-8')


inFile = codecs.open("C:\Users\Pratish\Documents\Assignments\Social Media Minning\Final Project\TestNeg.txt","r","utf-8",errors='ignore')
dictFile = codecs.open("C:\Users\Pratish\Documents\Assignments\Social Media Minning\Final Project\Output Files\SentiWords_1.0.txt","r","UTF-8")
wordsDict = Counter()
countWords = Counter()
dictcount = 0


# Creating dictinary from wordnet
while (1):
    readLine = dictFile.readline()
    if (not readLine ): break
    readLine  = re.sub(r"[\n]","",readLine)
    dictcount += 1
    #print readLine
    score = readLine.split("\t")
    # print("Length "+str(len(score)))

    # for i in score:
    #     print(" Word  " + i )

    if (len(score) == 2 and any(score[1]) ):
        wordsDict[score[0].split("#")[0]] += float(score[1])
        countWords[score[0].split("#")[0]] += 1.0
    else:
        print ("Some problem in line " + str(dictcount))
        break

# #Take average for repeated words
for keys,value in wordsDict.items():
    wordsDict[keys] = value / countWords[keys]

#negative_words = ["no","not","none","noone","Nobody","Nothing","Neither","Nowhere","Never","Hardly","Scarcely","Barely" ]



def calculateWeigth(x):
    val1 = wordsDict[x]
    if (val1 <= 0):
        val1 = -1 * val1
    else : val1 = val1 + 1
    return val1



count = 0
sentence_score = 0
sentence_length = 0
sentences_list =[]
hasNeg = 0
neg_count = []
words_score_pos = Counter()
words_score_neg = Counter()
posWordFreq = Counter()
negWordFreq = Counter()
filter_sent = []


while (1) :
    reviewText  = inFile.readline().lower()
    reviewText = re.sub(r"[?|$|.'!]","",reviewText)
    # print reviewText
    if (not reviewText): break
    # for x in negative_words:
    #     # print x
    #     if(reviewText.find(x+" ") != -1):
    #         hasNeg += 1
    #         neg_count.append(x)

    reviewTextList = word_tokenize(reviewText)
    sentences_list.append(reviewTextList)
    sentence_length = len(reviewTextList)
    # print("Sentence length" + str(sentence_length))
    # print(reviewTextList)
    #sent_val = nltk.pos_tag(reviewTextList)
    for index,x in enumerate(reviewTextList):
        #print x
        if (len(x) > 2):
            value = calculateWeigth(x)
            sentence_score += value

    if (sentence_length != 0):
        print("ScoreW/O Div : " + str(sentence_score)),
        sentence_score = sentence_score/sentence_length
        print (" Score Div : " +str(sentence_length))
    if ((count % 1000) == 0): print(count)
    if (count == 5000): break
    count += 1




print("The senetence score is " + str(sentence_score))
print("The overall rating predicted is : " + str((5*sentence_score)) )


inFile.close()
dictFile.close()

