from app.extensions import db
from app.models.time import Time
from app.models.candidato import Candidato
from app.models.time_candidato import TimeCandidato
from app.services.time_candidato_service import adicionar_candidato_ao_time

# 1️⃣ Criar um time
def criar_time(nome_time, id_candidato):
    # Verifica se o time já existe
    time_existente = Time.query.filter_by(nomeTime=nome_time).first()
    if time_existente:
        return {"mensagem": "Já existe um time com esse nome."}, 400

    # Verifica se o candidato existe
    candidato = Candidato.query.get(id_candidato)
    if not candidato:
        return {"mensagem": "Candidato informado não existe."}, 404

    # Verifica se o candidato já é líder de outro time
    lider_existente = Time.query.filter_by(lider=id_candidato).first()
    if lider_existente:
        return {"mensagem": "Este candidato já é líder de outro time."}, 400

    # Cria o time
    novo_time = Time(nomeTime=nome_time, lider=id_candidato)
    db.session.add(novo_time)
    db.session.commit()
    #novo_time.idTime
    # inserindo o criador no time como o primeiro membro
    #adicionar_candidato_ao_time(novo_time.idTime, id_candidato)
    # Adiciona o líder como membro do próprio time
    membro_lider = TimeCandidato(idTime=novo_time.idTime, idCandidato=id_candidato)
    db.session.add(membro_lider)
    db.session.commit()

    return {
        "mensagem": "Time criado com sucesso.",
        "time": novo_time.to_dict()
    }, 201


# 2️⃣ Listar todos os times (com nome do líder)
def listar_times():
    times = Time.query.all()
    return [t.to_dict() for t in times], 200


# 3️⃣ Pesquisar time por parâmetros (id, nome ou líder)
def buscar_time(filtros):
    query = Time.query

    if "idTime" in filtros:
        query = query.filter_by(idTime=filtros["idTime"])
    if "nomeTime" in filtros:
        query = query.filter(Time.nomeTime.like(f"%{filtros['nomeTime']}%"))
    if "lider" in filtros:
        query = query.filter_by(lider=filtros["lider"])

    resultados = query.all()
    if not resultados:
        return {"mensagem": "Nenhum time encontrado."}, 404

    return [t.to_dict() for t in resultados], 200
