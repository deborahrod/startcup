from app.extensions import db
from app.models.resposta_desafio import RespostaDesafio
from app.models.desafio import Desafio

# 1️⃣ Criar uma nova resposta
def criar_resposta(resposta, idDesafio):
    # Verifica se o desafio existe
    desafio = Desafio.query.get(idDesafio)
    if not desafio:
        return {"mensagem": "Desafio informado não existe."}, 404

    # Cria e salva a resposta
    nova_resposta = RespostaDesafio(resposta=resposta, idDesafio=idDesafio)
    db.session.add(nova_resposta)
    db.session.commit()

    return {
        "mensagem": "Resposta cadastrada com sucesso.",
        "resposta": nova_resposta.to_dict(incluir_dados_desafio=True)
    }, 201


# 2️⃣ Listar todas as respostas (com dados do desafio)
def listar_respostas():
    respostas = RespostaDesafio.query.all()
    return [r.to_dict(incluir_dados_desafio=True) for r in respostas], 200


# 3️⃣ Buscar respostas por filtros (idResp, idDesafio, ou parte do texto da resposta)
def buscar_respostas(filtros):
    query = RespostaDesafio.query

    if "idResp" in filtros:
        query = query.filter_by(idResp=filtros["idResp"])
    if "idDesafio" in filtros:
        query = query.filter_by(idDesafio=filtros["idDesafio"])
    if "resposta" in filtros:
        query = query.filter(RespostaDesafio.resposta.like(f"%{filtros['resposta']}%"))

    resultados = query.all()
    if not resultados:
        return {"mensagem": "Nenhuma resposta encontrada."}, 404

    return [r.to_dict(incluir_dados_desafio=True) for r in resultados], 200


# 4️⃣ Atualizar resposta
def atualizar_resposta(idResp, novos_dados):
    resposta = RespostaDesafio.query.get(idResp)
    if not resposta:
        return {"mensagem": "Resposta não encontrada."}, 404

    if "resposta" in novos_dados:
        resposta.resposta = novos_dados["resposta"]
    if "idDesafio" in novos_dados:
        desafio = Desafio.query.get(novos_dados["idDesafio"])
        if not desafio:
            return {"mensagem": "Novo desafio informado não existe."}, 404
        resposta.idDesafio = novos_dados["idDesafio"]

    db.session.commit()
    return {"mensagem": "Resposta atualizada com sucesso.", "resposta": resposta.to_dict(incluir_dados_desafio=True)}, 200


# 5️⃣ Excluir resposta
def excluir_resposta(idResp):
    resposta = RespostaDesafio.query.get(idResp)
    if not resposta:
        return {"mensagem": "Resposta não encontrada."}, 404

    db.session.delete(resposta)
    db.session.commit()
    return {"mensagem": "Resposta excluída com sucesso."}, 200


def buscar_resposta_e_desafio(resposta_texto):
    # Busca a resposta no banco (comparação exata ou aproximada)
    resposta = RespostaDesafio.query.filter_by(resposta=resposta_texto).first()

    if not resposta:
        return {"mensagem": "Nenhuma resposta correspondente encontrada."}, 200

    # Busca o desafio relacionado
    desafio = Desafio.query.get(resposta.idDesafio)

    if not desafio:
        return {
            "mensagem": "Resposta encontrada, mas o desafio associado não existe."
        }, 404

    # Monta o retorno com dados combinados
    resultado = {
        "resposta": {
            "idResp": resposta.idResp,
        },
        "desafio": {
            "idDesafio": desafio.idDesafio,
            "descricaoDesafio": desafio.descricaoDesafio,
            "status": desafio.status,
            "pontuacao": desafio.pontuacao,
        },
    }

    return resultado, 200