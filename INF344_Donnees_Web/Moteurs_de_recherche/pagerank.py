import sqlite3
import re
from math import log
from shared import extractText, neighbors
from collections import defaultdict

NB_ITERATIONS = 50
ALPHA = 0.15

#compute and store pagerank
def realURL():
	conn = sqlite3.connect('data.db')
	realURL_dict = dict() 

	for row in conn.execute("SELECT queryURL, respURL FROM responses"):
		realURL_dict[row[0]] = row[1]

	return realURL_dict # {queryURL,respURL}

def pointsTo(u):
	conn = sqlite3.connect('data.db')
	pointsTo_dict = dict()  # {respURL, list(respURLs)}
	realURL_dict = realURL() # {queryURL,respURL}

	for row in conn.execute("SELECT URL, content FROM webpages"):
		URL = row[0]
		content = row[1]
		# neighbors(pageContent, respURL): from shared.py to extract links from document
		queryURLs = neighbors(content, u) #URL the crawler asked for
		# print(queryURLs)
		print('we remove the links with .css at the end: ')
		queryURLs = [URL for URL in queryURLs if '.css' not in URL]

		respURLs = [realURL()[URL] for URL in queryURLs if URL in realURL()]
		print(respURLs)

		pointsTo_dict[URL] = respURLs
		return pointsTo_dict # {respURL, list(respURLs)}

def calcul_graphe(iterations):
	pointsTo_dict = pointsTo(u)
	n = len(pointsTo_dict)
	score = {respURL: 1/n for respURL, list_respURLs in pointsTo_dict.items()}
	print(score)
	for i in range(iterations):
		nouveau_score = {respURL: 0 for respURL, list_respURLs in pointsTo_dict.items()}
		print('nouveau score: ', nouveau_score)
		proba_teleportation = 0

		# traitons les sauts de page en page
		for P, pages in pointsTo_dict.items():  # {respURL --> P, list(respURLs) --> pages}
			if len(pages) > 0:
				proba_teleportation += ALPHA * score[P]
				for page in pages:
					nb_liens_sur_P = len(pages)
					print("nb_liens_sur_P", nb_liens_sur_P)
					nouveau_score[page] += score[P] * (1-ALPHA) / nb_liens_sur_P
			else:  # s'il n'y a pas de lien sur P
				proba_teleportation += score[P]
		# traitons les téléportations
		for P, pages in pointsTo_dict.items():
			nouveau_score[P] += proba_teleportation / n
		score = nouveau_score
	scores = [(k,v) for k, v in score.items()]
	conn = sqlite3.connect('data.db')
	conn.execute("DROP TABLE IF EXISTS page_rank")
	conn.execute("CREATE TABLE page_rank (URL TEXT, pageRank REAL)")
	conn.executemany("INSERT INTO page_rank (URL, pageRank) VALUES (?, ?)", scores)
	conn.commit()

	for row in conn.execute("SELECT * FROM page_rank ORDER BY rank desc LIMIT 20"):
		print(row)

	return scores


u = 'https://wiki.jachiet.com/wikipedia_fr_mathematics_nopic_2020-04/A/Nombre_premier'
pointsTo(u)
calcul_graphe(NB_ITERATIONS)