from app.extensions import db
from app.models.time import Time
from app.models.candidato import Candidato
from app.models.time_candidato import TimeCandidato


# 1️⃣ Adicionar candidato a um time
def adicionar_candidato_ao_time(id_time, id_candidato):
    # Verifica se o time existe
    time = Time.query.get(id_time)
    if not time:
        return {"mensagem": "Time não encontrado."}, 404

    # Verifica se o candidato existe
    candidato = Candidato.query.get(id_candidato)
    if not candidato:
        return {"mensagem": "Candidato não encontrado."}, 404

    # Verifica se o candidato já está em algum time
    ja_associado = TimeCandidato.query.filter_by(idCandidato=id_candidato).first()
    if ja_associado:
        return {"mensagem": "Este candidato já está associado a um time."}, 400

    # Verifica se o time já tem 4 membros
    qtd_membros = TimeCandidato.query.filter_by(idTime=id_time).count()
    if qtd_membros >= 4:
        return {"mensagem": "O time já possui o número máximo de 4 membros."}, 400

    # Cria a associação
    associacao = TimeCandidato(idTime=id_time, idCandidato=id_candidato)
    db.session.add(associacao)
    db.session.commit()

    return {
        "mensagem": "Candidato adicionado ao time com sucesso.",
        "associacao": associacao.to_dict()
    }, 201


# 2️⃣ Remover candidato de um time
def remover_candidato_do_time(id_time, id_candidato):
    associacao = TimeCandidato.query.filter_by(idTime=id_time, idCandidato=id_candidato).first()
    if not associacao:
        return {"mensagem": "Associação não encontrada."}, 404

    db.session.delete(associacao)
    db.session.commit()
    return {"mensagem": "Candidato removido do time com sucesso."}, 200


# 3️⃣ Listar membros de um time
def listar_membros_do_time(id_time):
    time = Time.query.get(id_time)
    if not time:
        return {"mensagem": "Time não encontrado."}, 404

    membros = TimeCandidato.query.filter_by(idTime=id_time).all()
    if not membros:
        return {"mensagem": "Este time não possui membros cadastrados."}, 404

    return {
        "time": time.nomeTime,
        "membros": [m.candidato.to_dict() for m in membros]
    }, 200

