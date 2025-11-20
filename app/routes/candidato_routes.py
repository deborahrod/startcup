from flask import Blueprint, jsonify, request
from app.services import candidato_service as service
from sqlalchemy.exc import IntegrityError

bp_candidato = Blueprint('candidato', __name__, url_prefix='/jogo/candidatos')

@bp_candidato.route('/', methods=['POST'])
def criar():
    data = request.json
    try:
        novo = service.criar_candidato(data)
        return jsonify(novo.to_dict()), 201
    except IntegrityError as e:
        #db.session.rollback()
        # Descobre qual campo gerou o erro (opcional)
        mensagem = "Erro: dado duplicado em campo único."
        if "nick" in str(e.orig):
            mensagem = "O nick informado já está em uso."
        elif "matricula" in str(e.orig):
            mensagem = "A matrícula informada já está cadastrada."

        return jsonify({
            "erro": mensagem
        }), 400

@bp_candidato.route('/', methods=['GET'])
def listar():
    candidatos = service.listar_todos()
    return jsonify([c.to_dict() for c in candidatos]), 200

@bp_candidato.route('/buscar', methods=['POST'])
def buscar():
    params = request.json or {}
    candidatos = service.buscar_por_parametros(params)
    return jsonify([c.to_dict() for c in candidatos]), 200

#@bp_candidato.route('/<int:id>', methods=['PUT'])
#def atualizar(id):
#    data = request.json
#    candidato = service.atualizar_candidato(id, data)
#    if candidato:
#        return jsonify(candidato.to_dict()), 200
#    return jsonify({"erro": "Candidato não encontrado"}), 404

@bp_candidato.route('/<int:id>', methods=['DELETE'])
def deletar(id):
    candidato = service.deletar_candidato(id)
    if candidato:
        return jsonify({"mensagem": "Candidato removido"}), 200
    return jsonify({"erro": "Candidato não encontrado"}), 404
