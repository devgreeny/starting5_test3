"""
app/__init__.py
---------------
Application factory and global extensions.
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config

# ────────────────────────────────────────────────────────────────
# Global extension objects (shared across blueprints & modules)
# ────────────────────────────────────────────────────────────────
db = SQLAlchemy()
login = LoginManager()
login.login_view = "auth.login"        # where @login_required redirects guests


# ────────────────────────────────────────────────────────────────
# Factory
# ────────────────────────────────────────────────────────────────
def create_app(config_class: type = Config) -> Flask:
    """Create and configure a Flask application instance."""
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialise extensions
    db.init_app(app)
    login.init_app(app)

    # ── Register blueprints ─────────────────────────────────────
    from .main.routes import bp as main_bp
    app.register_blueprint(main_bp)

    # Auth blueprint will be added soon; ignore if it doesn't exist yet
    try:
        from .auth.routes import bp as auth_bp
        app.register_blueprint(auth_bp)
    except ModuleNotFoundError:
        pass

    # ── Import models & set user_loader ─────────────────────────
    # Do this *after* db.init_app(app) so table metadata binds correctly.
    from .models import User, GuessLog, ScoreLog  # noqa: F401

    # Ensure tables exist for SQLite/local development
    with app.app_context():
        db.create_all()

    @login.user_loader
    def load_user(user_id: str):
        """Return user object from session-stored user_id."""
        from .models import User  # local import to avoid circular refs
        return User.query.get(int(user_id))

    return app
