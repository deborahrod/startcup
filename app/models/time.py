from app.extensions import db

class Time(db.Model):
    __tablename__ = 'time'

    idTime = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nomeTime = db.Column(db.String(100), nullable=False, unique=True)

    # Define chave estrangeira
    lider = db.Column(db.Integer, db.ForeignKey('candidato.idCandidato', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)

    # Cria relação ORM (opcional, mas muito útil)
    candidato_lider = db.relationship("Candidato", backref="times_liderados", lazy=True)

    def to_dict(self):
        return {
            "idTime": self.idTime,
            "nomeTime": self.nomeTime,
            "lider": self.lider,
            "nomeLider": self.candidato_lider.nomeCompleto if self.candidato_lider else None
        }
