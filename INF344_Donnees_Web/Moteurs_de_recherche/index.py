# #!/usr/bin/env python3

# import sqlite3
# import re
# from math import log
# from shared import extractText, extractListOfWords, stem
# from collections import defaultdict
# conn = sqlite3.connect('data.db', isolation_level='DEFERRED')

# #cursor = conn.cursor()

# # compute the inverted index and the idf and store them
# conn.execute("DROP TABLE IF EXISTS inverted_index")
# conn.execute("CREATE TABLE inverted_index (keyword TEXT, URL TEXT, frequency REAL)")

# # cursor.execute("SELECT URL, content FROM webpages")

# # d = dict()
# # list_url = []
# # list_content =[]

# # list_freq = []
# # occ_mot_page=0

# # print('Type a word')
# # query = input()

# # while True:
# #     row=cursor.fetchone()
# #     if not row:
# #         break

# #     if query in row[0]:
# #     	list_url.append(row[0])
# #     	list_content.append(row[1])

# #     d = dict(zip(list_url,list_content))
    
# #     maxim = 0
# #     url_max =""
# #     for URL, content in d.items():
# #     	list_words = list(extractListOfWords(content))
# #     	list_words = [stem(w) for w in list_words]
# #     	nb_mots = len(list_words)
# #     	# print(nb_mots)
# #     	occ_mot_page = list_words.count(stem(query))
# # 		nb = len(occ_mot_page)
# 	        tf = {x: list_words.count(stem(x))/nb for x in list_words}
# #     	list_freq.append(tf)

# #     	if maxim < tf:
# #     		maxim = tf
# #     		url_max = URL

# #     print(url_max)
# #     print(maxim)


# # print('end')
# # print(maxim)

import sqlite3
import re
from math import log
from shared import extractText, extractListOfWords, stem
from collections import defaultdict


def create_table_inverted_index():
	conn = sqlite3.connect('data.db')

	conn.execute("DROP TABLE IF EXISTS inverted_index")
	conn.execute("CREATE TABLE inverted_index (keyword TEXT, URL TEXT, frequency REAL)")

	insert_inverted_index = "INSERT INTO inverted_index (keyword, URL, frequency) VALUES (?, ?, ?);"

	for row in conn.execute("SELECT URL, content FROM webpages"):
		URL = row[0]
		content = row[1]
		list_words = list(extractListOfWords(content))
		list_words = [stem(w) for w in list_words]
		nb_mots = len(list_words)
		occ_mot_page = {w: list_words.count(stem(w)) for w in list_words}
		nb = len(occ_mot_page)
		tf = {x: list_words.count(stem(x))/nb for x in list_words}
		# result = []

		for keyword, frequency in tf.items():
			conn.execute(insert_inverted_index, (keyword, URL, frequency))

	conn.commit()
	print("Insertion in inverted_index is done!")

# def countFreq(L):
# 	list_words = []
# 	occ_mot_page = []
# 	for w in list(extractListOfWords(L)):
# 		list_words.append(stem(w))
# 	for w in list_words:
# 		occ_mot_page.append((list_words.count(w))/len(list_words))
# 	return list_words, occ_mot_page


def create_table_inverse_document_frequency():
	conn = sqlite3.connect('data.db')
	conn.execute("DROP TABLE IF EXISTS inverse_document_frequency")
	conn.execute("CREATE TABLE inverse_document_frequency (keyword TEXT, idf REAL)")

	insert_idf = "INSERT INTO inverse_document_frequency (keyword, idf) VALUES (?, ?);"

	for row in conn.execute("SELECT count(URL) FROM webpages"):
		print(row[0])
		N = row[0]

	keywords = []
	# URL = []
	nw = []

	for row in conn.execute("SELECT keyword, COUNT(*) FROM inverted_index GROUP BY keyword"):
		keywords.append(row[0])
		nw.append(row[1])
		# URL.append(row[2])

	idf = [log(N/n_w) for n_w in nw]

	conn.executemany(insert_idf, zip(keywords, idf))
	conn.commit()
	print("Insertion in IDF is done!")

	# for row in conn.execute("SELECT count(keyword), keyword, URL, frequency FROM inverted_index GROUP BY keyword"):
	# 	n_w = conn.execute("SELECT count(URL) FROM inverted_index WHERE keyword='{:d}'".format(row[0]))
	# 	print(n_w)
		# idf = log(N/(n_w))
		# # res = []
		# # res.append((row[0],row[1], idf))
		# conn.executemany(insert_idf,((row[0],row[1], idf)))


def tf_idf(word):
    conn = sqlite3.connect('data.db')
    for row in conn.execute("SELECT URL, MAX(frequency) FROM inverted_index WHERE keyword = '{:s}'".format(stem(word))):
        print(row)
    
    for row in conn.execute("SELECT keyword, idf FROM inverse_document_frequency WHERE keyword = '{:s}'".format(stem(word))):
        print(row)

#create_table_inverted_index()
#create_table_inverse_document_frequency()
tf_idf("matrice")