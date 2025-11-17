from app.extensions import db

class Desafio(db.Model):
    __tablename__ = 'desafios'

    idDesafio = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tituloDesafio = db.Column(db.String(300), nullable=False)
    descricaoDesafio = db.Column(db.String(300), nullable=False)
    idContest = db.Column(db.Integer, nullable=False)  # relação deve ser ajustada quando houver model Contest
    status = db.Column(db.Enum('Ativo', 'Inativo'), nullable=False)
    visibilidade = db.Column(db.Enum('Visivel', 'Invisivel'), nullable=False)
    pontuacao = db.Column(db.Integer, nullable=False)

    def to_dict(self):
        return {
            "idDesafio": self.idDesafio,
            "tituloDesafio": self.tituloDesafio,
            "descricaoDesafio": self.descricaoDesafio,
            "idContest": self.idContest,
            "status": self.status,
            "visibilidade": self.visibilidade,
            "pontuacao": self.pontuacao
        }
