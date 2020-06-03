'''Extracts type facts from a wikipedia file
usage: extractor.py wikipedia.txt output.txt

Every line of output.txt contains a fact of the form
    <title> TAB <type>
where <title> is the title of the Wikipedia page, and
<type> is a simple noun (excluding abstract types like
sort, kind, part, form, type, number, ...).

Note: the formatting of the output is already taken care of
by our template, you just have to complete the function
extractType below.

If you do not know the type of an entity, skip the article.
(Public skeleton code)'''

from parser import Parser
import sys
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import spacy
nlp = spacy.load("en_core_web_sm")

if len(sys.argv) != 3:
    print(__doc__)
    sys.exit(-1)

# for info concerning dependencies http://universaldependencies.org/docsv1/en/dep/ and https://spacy.io/usage/spacy-101

# these words were given wrongly when running the test file
added_stop_words = ['part', 'name', 'strip', 'type', 'set', 'style', 'body', 'range', 'word', 'area']

def extractType(content):
    doc = nlp(content)
    for token in doc:
        if (str(token) not in added_stop_words):
            print(token.text, token.pos_, token.dep_)
            
            # if ((token.tag_ == 'NN') and ('advmod' not in token.dep_) and ('amod' not in token.dep_)
            # and (token.dep_ == 'attr' or token.dep_ == 'pobj' or token.dep_ == 'dobj')   # 'aux'in token.dep_  # 'root' in token.dep_

            if ((token.tag_ == 'NNP') and (token.dep_ == 'attr')):
                return str(token)
                
            elif ((token.tag_ == 'NN') and (token.dep_ == 'attr')):
                return str(token)

# def extractType(content):
#     print(content)
#     regex_the = r"(is the)"
#     regex_a = r"(is a)"
#     regex_was = r"(was a)"
#     regex_an = r"(is an)"
#     regex_were = r"(were)"
#     regex_are = r"(are)"

    
#     match_the = re.search(regex_the, content)
#     match_a = re.search(regex_a, content)
#     match_was = re.search(regex_was, content)
#     match_an = re.search(regex_an,content)
#     match_were = re.search(regex_were, content)
#     match_are = re.search(regex_are,content)
  
#     word = None
    
#     if match_the != None:
#         start_index = int(match_the.end())+1
#         start_string = content[start_index:]
#         tokens = nltk.word_tokenize(start_string)
#         tokens_without_sw = [word for word in tokens if not word in stopwords.words()]
#         nouns = [word for (word, pos) in nltk.pos_tag(tokens) if pos[0] == 'N']
#         if not nouns:
#             nouns = tokens_without_sw
#         word = nouns[0]
#         print(word)

#     elif match_a != None:
#         start_index = int(match_a.end())+1
#         start_string = content[start_index:]
#         tokens = nltk.word_tokenize(start_string)
#         tokens_without_sw = [word for word in tokens if not word in stopwords.words()]
#         nouns = [word for (word, pos) in nltk.pos_tag(tokens) if pos[0] == 'N']
#         if not nouns:
#             nouns = tokens_without_sw
#         word = nouns[0]
#         print(word)
        
#     elif match_was != None:
#         start_index = int(match_was.end())+1
#         start_string = content[start_index:]
#         tokens = nltk.word_tokenize(start_string)
#         tokens_without_sw = [word for word in tokens if not word in stopwords.words()]
#         nouns = [word for (word, pos) in nltk.pos_tag(tokens) if pos[0] == 'N']
#         if not nouns:
#             nouns = tokens_without_sw
#         word = nouns[0]
#         print(word)

#     elif match_an != None:
#         start_index = int(match_an.end())+1
#         start_string = content[start_index:]
#         tokens = nltk.word_tokenize(start_string)
#         tokens_without_sw = [word for word in tokens if not word in stopwords.words()]
#         nouns = [word for (word, pos) in nltk.pos_tag(tokens) if pos[0] == 'N']
#         if not nouns:
#             nouns = tokens_without_sw
#         word = nouns[0]
#         print(word)
    
#     elif match_are != None:
#         start_index = int(match_are.end())+1
#         start_string = content[start_index:]
#         tokens = nltk.word_tokenize(start_string)
#         tokens_without_sw = [word for word in tokens if not word in stopwords.words()]
#         nouns = [word for (word, pos) in nltk.pos_tag(tokens) if pos[0] == 'N']
#         if not nouns:
#             nouns = tokens_without_sw
#         word = nouns[0]
#         print(word)
    
#     elif match_were != None:
#         start_index = int(match_were.end())+1
#         start_string = content[start_index:]
#         tokens = nltk.word_tokenize(start_string)
#         tokens_without_sw = [word for word in tokens if not word in stopwords.words()]
#         nouns = [word for (word, pos) in nltk.pos_tag(tokens) if pos[0] == 'N']
#         if not nouns:
#             nouns = tokens_without_sw
#         word = nouns[0]
#         print(word)
        
#     else:
#         tokens = nltk.word_tokenize(content)
#         tokens_without_sw = [word for word in tokens if not word in stopwords.words()]
#         nouns = [word for (word, pos) in nltk.pos_tag(tokens) if pos[0] == 'N']
#         if not nouns:
#             nouns = tokens_without_sw
#         word = nouns[0]
#         print(word)

#     return word

with open(sys.argv[2], 'w', encoding="utf-8") as output:
    for page in Parser(sys.argv[1]):
        typ = extractType(page.content)
        if typ:
            output.write(page.title + "\t" + typ + "\n")