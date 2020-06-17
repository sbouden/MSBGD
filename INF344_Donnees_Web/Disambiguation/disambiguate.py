usage='''
  Given as command line arguments
  (1) wikidataLinks.tsv 
  (2) wikidataLabels.tsv
  (optional 2') wikidataDates.tsv
  (3) wikipedia-ambiguous.txt
  (4) the output filename'''
'''writes lines of the form
        title TAB entity
  where <title> is the title of the ambiguous
  Wikipedia article, and <entity> is the 
  wikidata entity that this article belongs to. 
  It is OK to skip articles (do not output
  anything in that case). 
  (Public skeleton code)'''

import sys
import re
from parser import Parser
from simpleKB import SimpleKB
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import spacy
nlp = spacy.load("en_core_web_sm")
from nltk.stem.porter import *
stemmer = PorterStemmer()
import re
import spacy
nlp = spacy.load("en_core_web_sm")
import numpy as np

wikidata = None
if __name__ == "__main__":
    if len(sys.argv) is 5:
        dateFile = None
        wikipediaFile = sys.argv[3]
        outputFile = sys.argv[4]
    elif len(sys.argv) is 6:
        dateFile = sys.argv[3]
        wikipediaFile = sys.argv[4]
        outputFile = sys.argv[5]
    else:
        print(usage, file=sys.stderr)
        sys.exit(1)

    wikidata = SimpleKB(sys.argv[1], sys.argv[2], dateFile)
    
# wikidata is here an object containing 4 dictionaries:
## wikidata.links is a dictionary of type: entity -> set(entity).
##                It represents all the entities connected to a
##                given entity in the yago graph
## wikidata.labels is a dictionary of type: entity -> set(label).
##                It represents all the labels an entity can have.
## wikidata.rlabels is a dictionary of type: label -> set(entity).
##                It represents all the entities sharing a same label.
## wikidata.dates is a dictionnary of type: entity -> set(date).
##                It represents all the dates associated to an entity.

# Note that the class Page has a method Page.label(),
# which retrieves the human-readable label of the title of an 
# ambiguous Wikipedia page.
    

    with open(outputFile, 'w', encoding="utf-8") as output:
        for page in Parser(wikipediaFile):
            # DO NOT MODIFY THE CODE ABOVE THIS POINT
            # or you may not be evaluated (you can add imports).
            
                                 # YOUR CODE GOES HERE:
            
            ################ Methode 1: F-score: 7 precision 24 ##################
            # print("page.label() \n", page.label())
            # print("page.content \n", page.content)
            # rlabel = list(wikidata.rlabels[page.label()])[0]
            # link = wikidata.links[rlabel]
            # Q_link0 = list(link)[0]
            # labels = wikidata.labels[Q_link0]
    
            # sent = set(page.content)
            # word_label = list(labels)[0]
            # min_d = 1 
            # for word in sent:
            #     jd = nltk.jaccard_distance(set(word_label), set(word))
            #     if jd<min_d:
            #         min_d=jd
            #         print(word, jd)
    
            # if min_d ==0:
            #     bestEntity = rlabel
    
            # else:
            #     bestEntity = list(wikidata.rlabels[page.label()])[1]
            # output.write(page.title+"\t"+ bestEntity+"\n")
            #################################################################################
                        
                        # YOUR CODE GOES HERE:.

            ################## Méthode 2: 50/0.24  #################################
            # rlabel = list(wikidata.rlabels[page.label()])[0]
            # link = wikidata.links[rlabel]
            # Q_link0 = list(link)[0]
            # labels = wikidata.labels[Q_link0]
            # sent = page.content
            # word_label = list(labels)[0]

            # content_stem = nltk.word_tokenize(sent)
            # bestEntity = rlabel

            # dates_content = [d for d in content_stem if d.isnumeric()]
            # if dates_content: 
            #     print("dates_content --------------------- \n ", dates_content)

            # if wikidata.dates[rlabel]:
            #     dates = wikidata.dates[rlabel]
            #     date = list(dates)[0]
            #     date = date.split("-")[0]
            #     if date in dates_content:
            #         bestEntity = rlabel

            # output.write(page.title+"\t"+ bestEntity+"\n")
            
             # ## check if date win the initial content is the same as the one in wikidata.dates
            # # if wikidata.dates[rlabel]:
            # #     doc = nlp(sent)
            # #     for token in doc:
            # #         if token.pos_ == 'NUM':
            # #             if token.pos ==  list(wikidata.dates[rlabel])[0]:
            # #                 bestEntity = rlabel
            ############################################################################################
            
                        # YOUR CODE GOES HERE:.

            ################ Méthode 3: Meilleure methode juste après la méthode random: Precision 30 / F-score: 7 ######################################
            # len_rlabels = len(wikidata.rlabels[page.label()])
            
            # rlabel = list(wikidata.rlabels[page.label()])[0]
            # if rlabel and wikidata.links[rlabel]:
            #     link = wikidata.links[rlabel]
            #     if link:
            #         jacc_d =[]
            #         sent = page.content
            #         print("page.content: ", sent)
            #         for l in range(len(link)):

            #             labels = list(wikidata.labels[list(link)[l]])
            #             jacc = nltk.edit_distance(labels, sent)
            #             jacc_d.append(jacc)
            #         index =  np.argmin(jacc_d)
            #         bestEntity = list(wikidata.rlabels[page.label()])[index]
            #         print("-------------> Best entity: ", bestEntity)
            # else:
            #     bestEntity = rlabel

            # output.write(page.title+"\t"+ bestEntity+"\n")
            
            ######################################################

                        # YOUR CODE GOES HERE:.

            ################ Méthode 4 très mauvaise : F-score 0.24 et Précision 50 #################################
            # print("page.label() \n", page.label())
            # rlabel = list(wikidata.rlabels[page.label()])[0]
            # link = wikidata.links[rlabel]
            # Q_link0 = list(link)[0]
            # labels = wikidata.labels[Q_link0]
            # dates = set(wikidata.dates[rlabel])
            # sent = list(page.content)
            
            # for w in dates:
            #     if w in sent:
            #         bestEntity = rlabel
            #     else:
            #         word_label = list(labels)[0]
            #         min_d = 1 
            #         somme = 0
            #         for word in sent:
            #             print(word)
            #             jd = 1-nltk.jaccard_distance(set(word_label), set(word))
            #             somme +=jd
            #             if jd<min_d:
            #                 min_d=jd
            #                 print(word, jd)
                        
            #             if min_d == 0:
            #                 break
                        
            #         if min_d==0:
            #             bestEntity = rlabel
            #         # elif min_d <0.5 and somme >0:
            #         #     bestEntity = list(wikidata.rlabels[page.label()])[1]
            #         else:
            #             pagetitle = ''.join([i for i in page.title if not i.isdigit()])
            #             pagetitle = pagetitle.rstrip()
            #             bestEntity = pagetitle
                        
            # output.write(page.title+"\t"+ bestEntity+"\n")
            ###################################################
            
            # YOUR CODE GOES HERE:.
            
            ####################### Precision 24, & F-score 24 #####################
            output.write(page.title+"\t"+ list(wikidata.rlabels[page.label()])[0]+"\n")
            ########################################################################################