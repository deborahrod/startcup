from flask import Blueprint, request, jsonify
from app.services import time_service

bp_time = Blueprint('bp_time', __name__)
#bp_candidato = Blueprint('candidato', __name__, url_prefix='/candidatos')

@bp_time.route('/times', methods=['POST'])
def criar():
    dados = request.get_json()
    return time_service.criar_time(
        nome_time=dados.get('nomeTime'),
        id_candidato=dados.get('idCandidato')
    )

@bp_time.route('/times', methods=['GET'])
def listar():
    return time_service.listar_times()

@bp_time.route('/times/buscar', methods=['POST'])
def buscar():
    filtros = request.get_json() or {}
    return time_service.buscar_time(filtros)
