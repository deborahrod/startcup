from app.extensions import db
from app.models.desafio import Desafio
from app.models.resposta_submetida import RespostaSubmetida

class AcertoCandidato(db.Model):
    __tablename__ = 'acertoCandidato'

    idAcertos = db.Column(db.Integer, primary_key=True, autoincrement=True)
    idDesafio = db.Column(
        db.Integer,
        db.ForeignKey('desafios.idDesafio', ondelete='CASCADE', onupdate='CASCADE'),
        nullable=True
    )
    idRespostaSubmetida = db.Column(
        db.Integer,
        db.ForeignKey('respostaSubmetida.idRespSubmetida', ondelete='CASCADE', onupdate='CASCADE'),
        nullable=True
    )
    pontuacao = db.Column(db.Integer, nullable=False)

    desafio = db.relationship('Desafio', backref=db.backref('acertos', lazy=True))
    resposta_submetida = db.relationship('RespostaSubmetida', backref=db.backref('acertos', lazy=True))

    def to_dict(self):
        return {
            "idAcertos": self.idAcertos,
            "idDesafio": self.idDesafio,
            "idRespostaSubmetida": self.idRespostaSubmetida,
            "pontuacao": self.pontuacao,
            "desafio": self.desafio.to_dict() if self.desafio else None,
            "respostaSubmetida": self.resposta_submetida.to_dict() if self.resposta_submetida else None
        }
