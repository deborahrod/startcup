from flask import Blueprint, jsonify
from app.services.acerto_candidato_service import get_acertos_by_candidato, listar_candidatos_com_pontuacao

bp_acertos = Blueprint("acertos", __name__)

@bp_acertos.route("/acertos/<int:id_candidato>", methods=["GET"])
def listar_acertos(id_candidato):
    resultado = get_acertos_by_candidato(id_candidato)
    return jsonify(resultado)

@bp_acertos.route("/acertos/ranking", methods=["GET"])
def listar_candidatos():
    resultado = listar_candidatos_com_pontuacao()
    return jsonify(resultado)