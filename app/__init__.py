from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    # Uygulama yapılandırması
    app.config['SECRET_KEY'] = 'your_secret_key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'

    # SQLAlchemy'yi başlat
    db.init_app(app)

    # Blueprint ve modelleri içeri aktarma
    from .models import User
    from .routes import main as main_blueprint

    app.register_blueprint(main_blueprint)

    # LoginManager yapılandırması
    login_manager = LoginManager()
    login_manager.login_view = 'main.login'
    login_manager.init_app(app)

    # Kullanıcı yükleme fonksiyonu
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    return app

# Uygulama context'inde veritabanı işlemlerini gerçekleştirme
if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.create_all()
    app.run(debug=True)
