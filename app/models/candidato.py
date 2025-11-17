from app.extensions import db

class Candidato(db.Model):
    __tablename__ = 'candidato'

    idCandidato = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nomeCompleto = db.Column(db.String(100), nullable=False)
    nick = db.Column(db.String(100), nullable=False)
    matriculaIFG = db.Column(db.String(30), unique=True, nullable=False)
    chave = db.Column(db.String(15), unique=True, nullable=False)
    tipo = db.Column(db.Integer, default=1, nullable=False)

    def to_dict(self):
        return {
            "idCandidato": self.idCandidato,
            "nomeCompleto": self.nomeCompleto,
            "nick": self.nick,
            "matriculaIFG": self.matriculaIFG,
            "chave": self.chave,
            "tipo": self.tipo
        }
