from flask import Blueprint, request, jsonify
from app.services import desafio_service

bp_desafio = Blueprint('desafio_bp', __name__, url_prefix='/jogo/desafios')


# 🟢 1️⃣ Criar desafio
@bp_desafio.route('/', methods=['POST'])
def criar_desafio():
    dados = request.get_json()

    tituloDesafio = dados.get("tituloDesafio");
    descricaoDesafio = dados.get("descricaoDesafio")
    idContest = dados.get("idContest")
    status = dados.get("status")
    visibilidade = dados.get("visibilidade")
    pontuacao = dados.get("pontuacao")

    if not all([descricaoDesafio, idContest, status, pontuacao is not None]):
        return jsonify({"mensagem": "Campos obrigatórios: tituloDesafio, descricaoDesafio, idContest, status, visiblidade, pontuacao"}), 400

    resposta, status_code = desafio_service.criar_desafio(tituloDesafio, descricaoDesafio, idContest, status, visibilidade, pontuacao)
    return jsonify(resposta), status_code


# 🟡 2️⃣ Listar todos os desafios
@bp_desafio.route('/', methods=['GET'])
def listar_desafios():
    resposta, status_code = desafio_service.listar_desafios()
    return jsonify(resposta), status_code

# 🟡 2️⃣ Listar todos os desafios
@bp_desafio.route('/visiveis', methods=['GET'])
def listar_desafios_visiveis():
    resposta, status_code = desafio_service.listar_desafios_visiveis()
    return jsonify(resposta), status_code


# 🔵 3️⃣ Buscar desafios por filtros (JSON no corpo)
@bp_desafio.route('/buscar', methods=['POST'])
def buscar_desafios():
    filtros = request.get_json() or {}
    resposta, status_code = desafio_service.buscar_desafios(filtros)
    return jsonify(resposta), status_code


# 🟠 4️⃣ Atualizar desafio
@bp_desafio.route('/<int:idDesafio>', methods=['PUT'])
def atualizar_desafio(idDesafio):
    dados = request.get_json() or {}
    resposta, status_code = desafio_service.atualizar_desafio(idDesafio, dados)
    return jsonify(resposta), status_code


# 🔴 5️⃣ Excluir desafio
@bp_desafio.route('/<int:idDesafio>', methods=['DELETE'])
def excluir_desafio(idDesafio):
    resposta, status_code = desafio_service.excluir_desafio(idDesafio)
    return jsonify(resposta), status_code
