# app/routes/frontend_routes.py
from flask import Blueprint, render_template

bp_frontend = Blueprint('frontend', __name__,  url_prefix='/jogo')

@bp_frontend.route('/')
def index():
    return render_template('start_cup.html')

@bp_frontend.route('/home')
def home():
    return render_template('home.html')

@bp_frontend.route('/inscrevase')
def inscrevase():
    return render_template('inscrevase.html')

@bp_frontend.route('/competir')
def competir():
    return render_template('competir.html')

@bp_frontend.route('/ranking')
def ranking():
    return render_template('ranking.html')

@bp_frontend.route('/logoff')
def limpa_sessao():
    return render_template('limpasessao.html')

@bp_frontend.route('/login')
def entrar():
    return render_template('entrar.html')

@bp_frontend.route('/desafiosconhecidos')
def desafios():
    return render_template('desafios.html')

@bp_frontend.route('/regras')
def regras():
    return render_template('regras.html')
