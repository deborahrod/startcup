from flask import Blueprint, request, jsonify

from app.models.desafio import Desafio
from app.models.inativos import Inativo
from app.services import resposta_desafio_service
from app.services.acerto_candidato_service import cadastrar_acerto_candidato
from app.services.resposta_desafio_service import buscar_resposta_e_desafio
from app.services.resposta_submetida_service import cadastrar_resposta_submetida
from app.extensions import db

bp_resposta_desafio = Blueprint('resposta_bp', __name__, url_prefix='/jogo/respostas')


# 🟢 1️⃣ Criar resposta
@bp_resposta_desafio.route('/criar', methods=['POST'])
def criar_resposta():
    dados = request.get_json() or {}
    resposta = dados.get("resposta")
    idDesafio = dados.get("idDesafio")

    if not resposta or not idDesafio:
        return jsonify({"mensagem": "Campos obrigatórios: resposta, idDesafio"}), 400

    resposta_json, status_code = resposta_desafio_service.criar_resposta(resposta, idDesafio)
    return jsonify(resposta_json), status_code


# 🟡 2️⃣ Listar todas as respostas
@bp_resposta_desafio.route('/', methods=['GET'])
def listar_respostas():
    resposta_json, status_code = resposta_desafio_service.listar_respostas()
    return jsonify(resposta_json), status_code


# 🔵 3️⃣ Buscar respostas por filtros (JSON no corpo)
@bp_resposta_desafio.route('/buscar', methods=['POST'])
def buscar_respostas():
    filtros = request.get_json() or {}
    resposta_json, status_code = resposta_desafio_service.buscar_respostas(filtros)
    return jsonify(resposta_json), status_code


# 🟠 4️⃣ Atualizar resposta
@bp_resposta_desafio.route('/<int:idResp>', methods=['PUT'])
def atualizar_resposta(idResp):
    novos_dados = request.get_json() or {}
    resposta_json, status_code = resposta_desafio_service.atualizar_resposta(idResp, novos_dados)
    return jsonify(resposta_json), status_code


# 🔴 5️⃣ Excluir resposta
@bp_resposta_desafio.route('/<int:idResp>', methods=['DELETE'])
def excluir_resposta(idResp):
    resposta_json, status_code = resposta_desafio_service.excluir_resposta(idResp)
    return jsonify(resposta_json), status_code


@bp_resposta_desafio.route("/buscarc", methods=["POST"])
def buscar_resposta():
    data = request.get_json()

    if not data or "resposta" not in data or "idCandidato" not in data:
        return jsonify({"mensagem": "Campos obrigatórios omitidos."}), 400

    resposta_texto = data["resposta"]
    id_candidato = data["idCandidato"]

    resultado, status = buscar_resposta_e_desafio(resposta_texto)
    #determinando se foi encontrada resposta ou não
    if "mensagem" not in resultado:
        #encontrou... bora salvar isso - a resposta submetida
        re, st = cadastrar_resposta_submetida(resposta_texto, id_candidato,
                                              id_desafio=resultado["desafio"]["idDesafio"])
        if "mensagem" in re:
            resultado["status_cadastro_resposta"] = "ok"

        #agora precisamos garantir que é um desafio ativo. Caso contrário, não podemos marcar o acerto
        if resultado["desafio"]["status"] == "Ativo":
            #cadastrando o acerto
            re, st = cadastrar_acerto_candidato(resultado["desafio"]["idDesafio"],
                                                re["respostaSubmetida"]["idRespSubmetida"],
                                                resultado["desafio"]["pontuacao"])
            if "acerto" in re:
                resultado["acerto_cadastrado"] = re["acerto"]
            if "duplicado" in re:
                resultado["duplicado"] = "duplicado"

            # Verifica se o desafio consta na tabela 'inativos'
            #Busca o desafio associado
            desafio = Desafio.query.get(resultado["desafio"]["idDesafio"])
            inativo = Inativo.query.filter_by(idDesafio=resultado["desafio"]["idDesafio"]).first()
            if inativo:
                #Atualiza o status do desafio
                desafio.status = 'Inativo'
                db.session.commit()
        else:
            resultado["acerto_cadastrado"] = "não cadastrado"
            resultado["Desafio fechado"] = "Fechado"
    else:
        #blz... não encontrou... bora salvar mesmo assim
        re, st = cadastrar_resposta_submetida(resposta_texto, id_candidato,
                                              id_desafio=None)
        if "mensagem" in re:
            resultado["status_cadastro_resposta"] = "ok"
    return jsonify(resultado), status