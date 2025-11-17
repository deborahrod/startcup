from app.extensions import db
from app.models.desafio import Desafio


# 1️⃣ Criar desafio
def criar_desafio(tituloDesafio, descricaoDesafio, idContest, status, visibilidade, pontuacao):
    # Valida status
    if status not in ("Ativo", "Inativo"):
        return {"mensagem": "Status inválido. Use 'Ativo' ou 'Inativo'."}, 400
    # Valida visibilidade
    if visibilidade not in ("Visivel", "Invisivel"):
        return {"mensagem": "Visibilidade inválida. Use 'Visivel' ou 'Invisivel'."}, 400

    # Valida pontuação (1 a 9, por exemplo)
    #if not isinstance(pontuacao, int) or pontuacao < 0:
    #    return {"mensagem": "Pontuação deve ser um número inteiro positivo."}, 400

    # Cria e adiciona
    novo_desafio = Desafio(
        tituloDesafio = tituloDesafio,
        descricaoDesafio=descricaoDesafio,
        idContest=idContest,
        status=status,
        visibilidade=visibilidade,
        pontuacao=pontuacao
    )
    db.session.add(novo_desafio)
    db.session.commit()

    return {
        "mensagem": "Desafio criado com sucesso.",
        "desafio": novo_desafio.to_dict()
    }, 201


# 2️⃣ Listar todos os desafios
def listar_desafios():
    desafios = Desafio.query.all()
    return [d.to_dict() for d in desafios], 200

# 2️⃣b Listar todos os desafios visíveis
def listar_desafios_visiveis():
    desafios = Desafio.query.filter_by(visibilidade="Visivel", status="Ativo").all()
    return [d.to_dict() for d in desafios], 200


# 3️⃣ Buscar desafios por filtros
def buscar_desafios(filtros):
    query = Desafio.query

    if "idDesafio" in filtros:
        query = query.filter_by(idDesafio=filtros["idDesafio"])
    if "idContest" in filtros:
        query = query.filter_by(idContest=filtros["idContest"])
    if "status" in filtros:
        query = query.filter_by(status=filtros["status"])
    if "pontuacao" in filtros:
        query = query.filter_by(pontuacao=filtros["pontuacao"])
    if "descricaoDesafio" in filtros:
        query = query.filter(Desafio.descricaoDesafio.like(f"%{filtros['descricaoDesafio']}%"))
    if "tituloDesafio" in filtros:
        query = query.filter(Desafio.tituloDesafio.like(f"%{filtros['tituloDesafio']}%"))

    resultados = query.all()
    if not resultados:
        return {"mensagem": "Nenhum desafio encontrado."}, 404

    return [d.to_dict() for d in resultados], 200


# 4️⃣ Atualizar desafio
def atualizar_desafio(idDesafio, dados):
    desafio = Desafio.query.get(idDesafio)
    if not desafio:
        return {"mensagem": "Desafio não encontrado."}, 404

    if "descricaoDesafio" in dados:
        desafio.descricaoDesafio = dados["descricaoDesafio"]
    if "idContest" in dados:
        desafio.idContest = dados["idContest"]
    if "status" in dados:
        if dados["status"] not in ("Ativo", "Inativo"):
            return {"mensagem": "Status inválido. Use 'Ativo' ou 'Inativo'."}, 400
        desafio.status = dados["status"]
    if "visibilidade" in dados:
        if dados["visibilidade"] not in ("Visivel", "Invisivel"):
            return {"mensagem": "Visibilidade inválida. Use 'Visivel' ou 'Invisivel'."}, 400
        desafio.visibilidade = dados["visibilidade"]
    if "pontuacao" in dados:
        if not isinstance(dados["pontuacao"], int) or dados["pontuacao"] < 0:
            return {"mensagem": "Pontuação deve ser um número inteiro positivo."}, 400
        desafio.pontuacao = dados["pontuacao"]

    db.session.commit()

    return {
        "mensagem": "Desafio atualizado com sucesso.",
        "desafio": desafio.to_dict()
    }, 200


# 5️⃣ Excluir desafio
def excluir_desafio(idDesafio):
    desafio = Desafio.query.get(idDesafio)
    if not desafio:
        return {"mensagem": "Desafio não encontrado."}, 404

    db.session.delete(desafio)
    db.session.commit()

    return {"mensagem": "Desafio excluído com sucesso."}, 200
