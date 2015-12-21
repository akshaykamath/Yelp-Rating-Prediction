__author__ = 'Pratish'

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


inFile = codecs.open("C:\Users\Pratish\Documents\Assignments\Social Media Minning\Final Project\Sentences.txt","r","utf-8",errors='ignore')
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
    # if ( val1 > 0 ): val1 += 1
    # else: val1 = val1 * -1
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
    for x in negative_words:
        # print x
        if(reviewText.find(x+" ") != -1):
            hasNeg += 1
            neg_count.append(x)

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

            if (value > 0 ) :
                words_score_pos [x] = value
                posWordFreq[x] += 1
            elif (value < 0):
                words_score_neg[x] = value * -1
                negWordFreq[x] += 1
            sentence_score += value

    if (sentence_length != 0):
        print("ScoreW/O Div : " + str(sentence_score)),
        sentence_score = sentence_score/sentence_length
        print (" Score Div : " +str(sentence_length))
    if ((count % 1000) == 0): print(count)
    if (count == 5000): break
    count += 1




#Most positive & neative words

outFile3 = codecs.open("C:\Users\Pratish\Documents\Assignments\Social Media Minning\Final Project\Output Files\MostPostiveWords.txt","w", "UTF-8")

counter = 0

for keys,value in sorted(words_score_pos.iteritems(), key=lambda (k,v): (v,k),reverse=True):
    outFile3.write(keys + ";" + str(value)+"\n")
    print(keys +';'+ str(value*10))
    counter += 1
    if(counter > 300): break

outFile4 = codecs.open("C:\Users\Pratish\Documents\Assignments\Social Media Minning\Final Project\Output Files\MostNegativeWords.txt","w", "UTF-8")
print("-") * 50
counter = 0
for keys,value in sorted(words_score_neg.iteritems(), key=lambda (k,v): (v,k),reverse=True):
    outFile4.write(keys + ";"+ str(value)+"\n")
    print(keys +':'+ str(value))
    counter += 1
    if(counter > 300): break


#Most positive and negative occuring words

def checkStopWord(word):
    stopword = stopwords.words('english')
    if (word in stopword) : return True
    return False

mostPosOccWordList = []

outFile1 = codecs.open("C:\Users\Pratish\Documents\Assignments\Social Media Minning\Final Project\Output Files\MostOccPostiveWords.txt","w", "UTF-8")

counter = 0
for keys,value in sorted(posWordFreq.iteritems(), key=lambda (k,v): (v,k),reverse=True):
    print(str(keys) + " " + str(value) )
    if (not checkStopWord(keys)):
        outFile1.write(keys+";"+ str(value)+"\n")
        mostPosOccWordList.append([str(keys),int(value)])
        counter += 1
        if(counter > 300): break

print("-") * 50

outFile2 = codecs.open("C:\Users\Pratish\Documents\Assignments\Social Media Minning\Final Project\Output Files\MostOccNegativeWords.txt","w", "UTF-8")

mostNegOccWordList = []
counter = 0
for keys,value in sorted(negWordFreq.iteritems(), key=lambda (k,v): (v,k),reverse=True):
    print(str(keys) + " " + str(value))
    if (not checkStopWord(keys)):
        outFile2.write(keys + ";"+ str(value)+"\n")
        mostNegOccWordList.append([str(keys),int(value)])
        counter += 1
        if(counter > 300): break


# wcMostOccPosWords = WordCloud(max_font_size = 40, relative_scaling =.5, background_color='white').generate_from_frequencies(mostPosOccWordList)


# fig = plt.figure()
# fig.patch.set_facecolor('blue')
# fig.patch.set_alpha(0.7)
# plt.imshow(wcMostOccPosWords)
# plt.axis("off")
#
# fig.savefig('temp.png', facecolor=fig.get_facecolor(), transparent=True,edgecolor='none')
#
# plt.show()


inFile.close()
dictFile.close()
