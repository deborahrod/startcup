from app.models.candidato import Candidato
from app.extensions import db

def criar_candidato(data):
    novo = Candidato(
        nomeCompleto=data['nome'],
        nick=data['nick'],
        matriculaIFG=data.get('matricula'),
        chave=data.get('chave'),
        tipo=data.get('tipo', 1)
    )
    db.session.add(novo)
    db.session.commit()
    return novo

def listar_todos():
    return Candidato.query.all()

def buscar_por_parametros(params):
    query = Candidato.query
    for chave, valor in params.items():
        if hasattr(Candidato, chave):
            query = query.filter(getattr(Candidato, chave) == valor)
    return query.all()

def atualizar_candidato(id, data):
    candidato = Candidato.query.get(id)
    if not candidato:
        return None
    for chave, valor in data.items():
        if hasattr(candidato, chave):
            setattr(candidato, chave, valor)
    db.session.commit()
    return candidato

def deletar_candidato(id):
    candidato = Candidato.query.get(id)
    if not candidato:
        return None
    db.session.delete(candidato)
    db.session.commit()
    return candidato
