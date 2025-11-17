from app.extensions import db
from app.models.candidato import Candidato
from app.models.desafio import Desafio

class RespostaSubmetida(db.Model):
    __tablename__ = 'respostaSubmetida'

    idRespSubmetida = db.Column(db.Integer, primary_key=True, autoincrement=True)
    respostaSubmetida = db.Column(db.Text, nullable=True)

    idCandidato = db.Column(
        db.Integer,
        db.ForeignKey('candidato.idCandidato', ondelete='CASCADE', onupdate='CASCADE'),
        nullable=True
    )

    idDesafio = db.Column(
        db.Integer,
        db.ForeignKey('desafios.idDesafio', ondelete='CASCADE', onupdate='CASCADE'),
        nullable=True
    )

    candidato = db.relationship('Candidato', backref=db.backref('respostas_submetidas', lazy=True))
    desafio = db.relationship('Desafio', backref=db.backref('respostas_submetidas', lazy=True))

    def to_dict(self):
        return {
            "idRespSubmetida": self.idRespSubmetida,
            "respostaSubmetida": self.respostaSubmetida,
            "idCandidato": self.idCandidato,
            "idDesafio": self.idDesafio,
            "candidato": self.candidato.to_dict() if self.candidato else None,
            "desafio": self.desafio.to_dict() if self.desafio else None
        }
