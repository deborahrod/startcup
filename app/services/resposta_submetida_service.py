from app.extensions import db
from app.models.resposta_submetida import RespostaSubmetida
from app.models.candidato import Candidato
from app.models.desafio import Desafio

# 1️⃣ Cadastrar uma resposta submetida
def cadastrar_resposta_submetida(resposta_submetida, id_candidato, id_desafio=None):
    # Verifica se o candidato existe
    candidato = Candidato.query.get(id_candidato)
    if not candidato:
        return {"mensagem": "Candidato informado não existe."}, 404

    # Se idDesafio foi informado, verifica se existe
    if id_desafio is not None:
        desafio = Desafio.query.get(id_desafio)
        if not desafio:
            return {"mensagem": "Desafio informado não existe."}, 404

    # Cria e persiste o registro
    nova_resposta = RespostaSubmetida(
        respostaSubmetida=resposta_submetida,
        idCandidato=id_candidato,
        idDesafio=id_desafio
    )

    db.session.add(nova_resposta)
    db.session.commit()

    return {
        "mensagem": "Resposta submetida com sucesso.",
        "respostaSubmetida": nova_resposta.to_dict()
    }, 201


# 2️⃣ Listar todas as respostas submetidas por um candidato
def listar_respostas_por_candidato(id_candidato):
    candidato = Candidato.query.get(id_candidato)
    if not candidato:
        return {"mensagem": "Candidato informado não existe."}, 404

    respostas = RespostaSubmetida.query.filter_by(idCandidato=id_candidato).all()

    if not respostas:
        return {"mensagem": "Nenhuma resposta submetida por este candidato."}, 404

    return [r.to_dict() for r in respostas], 200
