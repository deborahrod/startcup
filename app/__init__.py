from flask import Flask
from .config import Config
from .extensions import db
from .routes.health_routes import health_bp
from .routes.candidato_routes import bp_candidato
from .routes.time_routes import bp_time
from .routes.time_candidato_routes import bp_time_candidato
from .routes.frontend_routes import bp_frontend
from .routes.resposta_desafio_routes import bp_resposta_desafio
from .routes.desafio_routes import bp_desafio
from .routes.resposta_submetida_routes import bp_resposta_submetida
from .routes.acerto_candidato_routes import bp_acertos

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    static_url_path='/jogo/static', 
    static_folder='static'

    # Inicializa extensões
    db.init_app(app)

    # Registra blueprints
    app.register_blueprint(health_bp)
    app.register_blueprint(bp_candidato)
    app.register_blueprint(bp_time)
    app.register_blueprint(bp_time_candidato)
    app.register_blueprint(bp_frontend)
    app.register_blueprint(bp_resposta_desafio)
    app.register_blueprint(bp_desafio)
    app.register_blueprint(bp_resposta_submetida)
    app.register_blueprint(bp_acertos)

    return app
