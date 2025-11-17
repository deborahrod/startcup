from app.extensions import db
from app.models.desafio import Desafio

class RespostaDesafio(db.Model):
    __tablename__ = 'respDesafio'

    idResp = db.Column(db.Integer, primary_key=True, autoincrement=True)
    resposta = db.Column(db.Text, nullable=False)
    idDesafio = db.Column(db.Integer, db.ForeignKey('desafios.idDesafio'))

    # Relacionamento — permite acessar o desafio a partir da resposta
    desafio = db.relationship('Desafio', backref=db.backref('respostas', lazy=True))

    def to_dict(self, incluir_dados_desafio=True):
        data = {
            "idResp": self.idResp,
            "resposta": self.resposta,
            "idDesafio": self.idDesafio,
        }

        # inclui informações do desafio, caso solicitado
        if incluir_dados_desafio and self.desafio:
            data["desafio"] = {
                "descricaoDesafio": self.desafio.descricaoDesafio,
                "status": self.desafio.status,
                "pontuacao": self.desafio.pontuacao
            }

        return data
