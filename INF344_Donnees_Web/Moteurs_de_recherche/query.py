#!/usr/bin/env python3

import sqlite3
import re
from math import log
from shared import extractText, stem
from collections import defaultdict

# conn.execute("SELECT * FROM webpages LIMIT 1")
# SELECT * FROM webpages LIMIT 1;

#cursor = conn.cursor()

def tri_tfidf():
	conn = sqlite3.connect('data.db')
	query = input('Tapez une phrase: ')
	queryWords = [stem(w) for w in query.split()]
	print(queryWords)
	print(type(queryWords))
	queryWords = tuple(queryWords)
	# sum (prod)
	# prod = tf(term,doc) x idf(term)
	# term --> keyword from inverted_index / doc --> URL from inverted_index
	# idf(term) --> keyword from inverse_document_frequency

	t =  "SELECT URL, SUM(prod) AS tfidf \
			  FROM (SELECT ii.keyword, ii.URL, ii.frequency * idf.idf AS prod \
	                FROM inverted_index AS ii, inverse_document_frequency AS idf \
	                WHERE ii.keyword = idf.keyword AND ii.keyword IN {}) \
	          GROUP BY URL \
	          ORDER BY SUM(prod) DESC LIMIT 10"\
	          .format(queryWords)

	for row in conn.execute(t):
	    print(row)
	conn.commit()


def tri_tfidf_pageRank(): # tf-idf multiplié par le PageRank de la page
	conn = sqlite3.connect('data.db')
	query = input('Tapez une phrase: ')
	queryWords = [stem(w) for w in query.split()]
	queryWords = tuple(queryWords)

	# prod = tf(term,doc) x idf(term)
	# term --> keyword from inverted_index / doc --> URL from inverted_index
	# idf(term) --> keyword from inverse_document_frequency
	# page_rank: p / t: tfidf
	# URL,  tf-idf x PageRank

	query =  "SELECT pr.URL, t.tfidf * pr.pageRank AS score \
              FROM page_rank AS pr, (SELECT URL, SUM(prod) AS tfidf \
                				   	 FROM ( SELECT ii.keyword, ii.URL, ii.frequency * idf.idf AS prod \
                           					FROM inverted_index AS ii, inverse_document_frequency AS idf \
                           					WHERE ii.keyword = idf.keyword AND ii.keyword IN {}) AS tf_idf \
                    				 GROUP BY URL) AS t \
              WHERE pr.URL = t.URL \
              GROUP BY pr.URL \
              ORDER BY score DESC LIMIT 10".format(queryWords)
	for row in conn.execute(query):
		print(row)
		conn.commit()

# compute best query solution and output them
tri_tfidf()
#tri_tfidf_pageRank()
