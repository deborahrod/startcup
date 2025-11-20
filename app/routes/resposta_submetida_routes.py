from flask import Blueprint, jsonify
from app.services.resposta_submetida_service import listar_respostas_por_candidato

bp_resposta_submetida = Blueprint('resposta_submetida', __name__,  url_prefix='/jogo')

# 🔹 GET /resposta_submetida/candidato/<int:id_candidato>
@bp_resposta_submetida.route('/candidato/<int:id_candidato>', methods=['GET'])
def listar_respostas_candidato(id_candidato):
    respostas, status = listar_respostas_por_candidato(id_candidato)
    return jsonify(respostas), status
