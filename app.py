import os
from flask import Flask
from extensions import db, socketio
import pymysql

pymysql.install_as_MySQLdb()

def create_app():
    app = Flask(__name__)
    # Sử dụng biến môi trường cho các thông tin nhạy cảm
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'caro_game_secret_key')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'mysql+pymysql://root:1234@localhost/CaroPython')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SERVER_NAME'] = os.environ.get('SERVER_NAME')

    # Initialize extensions
    db.init_app(app)
    socketio.init_app(app, cors_allowed_origins="*")
    
    # Add Jinja2 functions
    app.jinja_env.globals.update(enumerate=enumerate)

    # Import and register blueprints
    from routes.home import home_bp
    from routes.after_game import after_game_bp
    from routes.leaderboard import leaderboard_bp
    from routes.store import store_bp
    from routes.pvp_noti import pvp_noti_bp
    from routes.pve_noti import pve_noti_bp
    from routes.pvp import pvp_bp
    from routes.pve import pve_bp
    from routes.profile import profile_bp
    app.register_blueprint(home_bp)
    app.register_blueprint(after_game_bp)
    app.register_blueprint(leaderboard_bp)
    app.register_blueprint(store_bp)
    app.register_blueprint(pvp_noti_bp)
    app.register_blueprint(pve_noti_bp)
    app.register_blueprint(pvp_bp)
    app.register_blueprint(pve_bp)
    app.register_blueprint(profile_bp)

    return app

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.create_all()
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV', 'development') == 'development'
    socketio.run(app, debug=debug, host='0.0.0.0', port=port, allow_unsafe_werkzeug=True)