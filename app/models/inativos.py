from app.extensions import db
from app.models.desafio import Desafio

class Inativo(db.Model):
    __tablename__ = 'inativos'

    idInativos = db.Column(db.Integer, primary_key=True, autoincrement=True)
    idDesafio = db.Column(
        db.Integer,
        db.ForeignKey('desafios.idDesafio', ondelete='CASCADE', onupdate='CASCADE'),
        nullable=False
    )

    # relacionamento para acessar o desafio associado
    desafio = db.relationship('Desafio', backref=db.backref('registro_inativo', uselist=False, lazy=True))

    def to_dict(self, incluir_desafio=False):
        data = {
            "idInativos": self.idInativos,
            "idDesafio": self.idDesafio
        }
        if incluir_desafio and self.desafio:
            data["desafio"] = {
                "idDesafio": self.desafio.idDesafio,
                "descricaoDesafio": self.desafio.descricaoDesafio,
                "status": self.desafio.status,
                "pontuacao": self.desafio.pontuacao
            }
        return data
