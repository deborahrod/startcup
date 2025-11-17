from app.extensions import db
from sqlalchemy import func
from app.models.acerto_candidato import AcertoCandidato
from app.models.candidato import Candidato
from app.models.desafio import Desafio
from app.models.resposta_submetida import RespostaSubmetida

def cadastrar_acerto_candidato(id_desafio, id_resposta_submetida, pontuacao):
    """
    Cadastra um novo registro de acerto de candidato.
    """
    ##antes de tudo, checar se o candidato já não possui esse desafio resolvido
    resposta = RespostaSubmetida.query.get(id_resposta_submetida)
    if resposta and verificar_acerto_existente(resposta.idCandidato, id_desafio):
        return {"mensagem": "Este candidato já possui acerto registrado para este desafio.", "duplicado": True}, 400

    # ✅ Validação: campos obrigatórios
    if pontuacao is None:
        return {"mensagem": "Campo 'pontuacao' é obrigatório."}, 400

    # ✅ Verifica se o desafio existe (se informado)
    if id_desafio is not None:
        desafio = Desafio.query.get(id_desafio)
        if not desafio:
            return {"mensagem": f"Desafio com id {id_desafio} não encontrado."}, 404
    else:
        desafio = None

    # ✅ Verifica se a resposta submetida existe (se informada)
    if id_resposta_submetida is not None:
        resposta_submetida = RespostaSubmetida.query.get(id_resposta_submetida)
        if not resposta_submetida:
            return {"mensagem": f"Resposta submetida com id {id_resposta_submetida} não encontrada."}, 404
    else:
        resposta_submetida = None

    # ✅ Cria o registro de acerto
    novo_acerto = AcertoCandidato(
        idDesafio=id_desafio,
        idRespostaSubmetida=id_resposta_submetida,
        pontuacao=pontuacao
    )

    try:
        db.session.add(novo_acerto)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return {"mensagem": f"Erro ao cadastrar acerto: {str(e)}"}, 500

    # ✅ Retorna sucesso com os dados completos
    return {
        "mensagem": "Acerto registrado com sucesso.",
        "acerto": novo_acerto.to_dict()
    }, 201

def verificar_acerto_existente(id_candidato, id_desafio):
    """
    Verifica se o candidato já possui um registro de acerto para o mesmo desafio.
    Retorna True se existir, False caso contrário.
    """
    # Busca todas as respostas submetidas do candidato para o desafio
    respostas = RespostaSubmetida.query.filter_by(
        idCandidato=id_candidato,
        idDesafio=id_desafio
    ).all()

    if not respostas:
        return False  # Nenhuma resposta submetida para o desafio

    # Extrai os IDs das respostas submetidas
    ids_respostas = [r.idRespSubmetida for r in respostas]

    # Verifica se há algum acerto associado a uma dessas respostas
    acerto_existente = AcertoCandidato.query.filter(
        AcertoCandidato.idRespostaSubmetida.in_(ids_respostas)
    ).first()

    return acerto_existente is not None

def get_acertos_by_candidato(id_candidato):
    """
    Retorna todos os acertos de um candidato específico, incluindo
    os dados dos desafios e respostas, e a soma total da pontuação.
    """
    try:
        # Faz join com respostaSubmetida para filtrar pelo idCandidato
        acertos = (
            db.session.query(AcertoCandidato)
            .join(RespostaSubmetida, AcertoCandidato.idRespostaSubmetida == RespostaSubmetida.idRespSubmetida)
            .filter(RespostaSubmetida.idCandidato == id_candidato)
            .all()
        )

        # Lista detalhada
        lista_acertos = [a.to_dict() for a in acertos]

        # Soma total dos pontos
        total_pontos = sum(a.pontuacao for a in acertos)

        return {
            "idCandidato": id_candidato,
            "totalPontuacao": total_pontos,
            "acertos": lista_acertos
        }

    except Exception as e:
        db.session.rollback()
        return {"erro": f"Erro ao buscar acertos: {str(e)}"}


def listar_candidatos_com_pontuacao():
    """
    Retorna todos os candidatos cadastrados, incluindo o total de pontos obtidos.
    Caso o candidato ainda não tenha pontuação, retorna 0.
    """
    try:
        # Join entre as tabelas e soma das pontuações
        resultados = (
            db.session.query(
                Candidato,
                func.coalesce(func.sum(AcertoCandidato.pontuacao), 0).label("totalPontuacao")
            )
            .outerjoin(RespostaSubmetida, RespostaSubmetida.idCandidato == Candidato.idCandidato)
            .outerjoin(AcertoCandidato, AcertoCandidato.idRespostaSubmetida == RespostaSubmetida.idRespSubmetida)
            .group_by(Candidato.idCandidato)
            .all()
        )

        # Monta a lista de saída
        lista_candidatos = []
        for candidato, total_pontos in resultados:
            candidato_dict = candidato.to_dict() if hasattr(candidato, 'to_dict') else {
                "idCandidato": candidato.idCandidato,
                "nome": candidato.nome,
                "apelido": candidato.apelido,
                "email": candidato.email
            }
            candidato_dict["totalPontuacao"] = int(total_pontos or 0)
            lista_candidatos.append(candidato_dict)

        return {"candidatos": lista_candidatos}

    except Exception as e:
        db.session.rollback()
        return {"erro": f"Erro ao listar candidatos: {str(e)}"}