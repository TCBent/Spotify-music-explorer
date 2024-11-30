from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from database import db
from werkzeug.utils import secure_filename
from markupsafe import escape
import hashlib  
import os
import uuid
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def main():

    return render_template('main.html')



@app.route('/consulta1', methods=['GET', 'POST'])
def consulta1():
    if request.method == 'POST':
        user_input = escape(request.form['userInput'])
        print(user_input)
        result = db.artistas_con_mas_canciones_un_genero_especifico(user_input)


        return render_template('consulta1.html', result=result)

    return render_template('consulta1.html')


@app.route('/consulta2', methods=['GET', 'POST'])
def consulta2():
    if request.method == 'POST':
        user_input = escape(request.form['userInput'])
        print(user_input)
        result = db.colaboradores_de_un_artista(user_input)


        return render_template('consulta2.html', result=result)

    return render_template('consulta2.html')


@app.route('/consulta3', methods=['GET', 'POST'])
def consulta3():
    if request.method == 'POST':
        user_input = escape(request.form['userInput'])
        print(user_input)
        result = db.albumes_en_que_ha_colaborado(user_input)


        return render_template('consulta3.html', result=result)

    return render_template('consulta3.html')

@app.route('/consulta4', methods=['GET', 'POST'])
def consulta4():
    if request.method == 'POST':
        user_input = escape(request.form['userInput'])
        print(user_input)
        result = db.info_genre_rank(user_input)


        return render_template('consulta4.html', result=result)

    return render_template('consulta4.html')

@app.route('/get_genres', methods=['GET'])
def get_genres():
    query = request.args.get('query', '')
    genres = db.get_genres(query)
    return jsonify(genres)


if __name__ == '__main__':
    app.run(debug=True)