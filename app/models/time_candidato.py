from app.extensions import db

class TimeCandidato(db.Model):
    __tablename__ = 'time_candidato'

    idTime = db.Column(db.Integer, db.ForeignKey('time.idTime', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True)
    idCandidato = db.Column(db.Integer, db.ForeignKey('candidato.idCandidato', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True)

    # Relacionamentos opcionais (facilita consultas)
    time = db.relationship('Time', backref=db.backref('membros', cascade='all, delete-orphan', lazy=True))
    candidato = db.relationship('Candidato', backref=db.backref('time_assoc', cascade='all, delete-orphan', lazy=True))

    def to_dict(self):
        return {
            "idTime": self.idTime,
            "idCandidato": self.idCandidato,
            "nomeCandidato": self.candidato.nomeCompleto if self.candidato else None,
            "nomeTime": self.time.nomeTime if self.time else None
        }
