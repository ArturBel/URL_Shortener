from flask import Flask
from api.config import Config
from api.extensions import db, migrate, limiter
from api.routes import shorten_bp, redirecter
from api.scheduler import init_scheduler


def create_app():
    # creating and configuring app instance
    app = Flask(__name__)
    app.config.from_object(Config)

    # initializing extensions
    db.init_app(app=app)
    migrate.init_app(app=app, db=db)
    limiter.init_app(app=app)

    # registering blueprints
    app.register_blueprint(shorten_bp)
    app.register_blueprint(redirecter)

    # applying limiter
    limiter.limit(("5/minute", "20/hour"), methods=['POST'])(shorten_bp)
    limiter.exempt(redirecter)

    # initializing scheduler
    init_scheduler(app=app, db=db)

    # setting up health endpoint
    @app.route('/health')
    def health():
        return "API works correctly"

    return app