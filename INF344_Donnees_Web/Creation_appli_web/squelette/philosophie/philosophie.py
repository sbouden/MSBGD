#!/usr/bin/python3
# -*- coding: utf-8 -*-

from flask import Flask, render_template, session, request, redirect, flash
from getpage import getPage

app = Flask(__name__)

app.secret_key = "TODO: mettre une valeur secrète ici"

@app.route('/new-game', methods=['GET','POST'])
def newgame():
    title=request.form['start']
    session['article']=title
    session['score']=0

    if getPage(session['article'])[0] == 'Philosophie':
        flash("Vous ne pouvez pas commencer par le mot 'Philosophie'", 'philo')
        return redirect('/')
    if getPage(session['article'])[0] == 'philosophie':
        flash("Vous ne pouvez pas commencer par le mot 'Philosophie'", 'philo2')
        return redirect('/')

    if 'philosophie' in getPage(session['article'])[0]:
        flash("Saisir un autre mot ne contenant pas le mot 'Philosophie'", 'erreur')
        return redirect('/')

    if getPage(session['article'])[1] == []:
    	flash("Pas de lien ! Recommencez avec un autre mot :( ", 'lien')
    	return redirect('/')
    else:
    	return redirect('/game')
#---------------------game---------------------------------------------------------------------
@app.route('/game', methods=['GET'])
def game():
	session['title'], session['hrefs'] = getPage(session['article'])
	session['score']=session['score']+1
	if session['article'] == 'Philosophie':
		flash("La partie est gagnée !", 'won')
		return redirect('/')
	if session['hrefs'] == []:
		flash("Plus de liens ! Vous avez perdu. ",'lost')
		return redirect('/')
	return render_template('game.html', title=session['title'], links=session['hrefs'])

#---------------------move---------------------------------------------------------------------
@app.route('/move', methods=['POST'])
# def move():
# 	if request.form['destination'] in session['hrefs']: #verif plusieurs onglets ou non
# 		session['article']=request.form['destination']

# 		if session['article'] == 'Philosophie':
# 			flash("La partie est gagnée !")
# 			return redirect('/')
		
# 		elif getPage(session['article'])[1] == []:
# 			flash('Plus de liens ! Vous avez perdu :( ')
# 			return redirect('/')
# 		else:
# 			return redirect('/game')
# 	else:
# 		flash('vous jouez sur plusieurs onglets')
# 		return redirect('/')

def move():
	session['article'] = request.form['destination']
	return redirect('/game')


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', message="Bonjour, monde !")

# Si vous définissez de nouvelles routes, faites-le ici

if __name__ == '__main__':
    app.run(debug=True)
