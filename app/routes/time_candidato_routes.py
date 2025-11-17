from flask import Blueprint, request
from app.services import time_candidato_service

bp_time_candidato = Blueprint('bp_time_candidato', __name__)

@bp_time_candidato.route('/times/<int:id_time>/membros', methods=['GET'])
def listar_membros(id_time):
    return time_candidato_service.listar_membros_do_time(id_time)

@bp_time_candidato.route('/times/<int:id_time>/membros', methods=['POST'])
def adicionar_membro(id_time):
    dados = request.get_json()
    id_candidato = dados.get('idCandidato')
    return time_candidato_service.adicionar_candidato_ao_time(id_time, id_candidato)

@bp_time_candidato.route('/times/<int:id_time>/membros/<int:id_candidato>', methods=['DELETE'])
def remover_membro(id_time, id_candidato):
    return time_candidato_service.remover_candidato_do_time(id_time, id_candidato)
