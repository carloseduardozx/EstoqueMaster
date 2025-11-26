import click
from flask import Flask
from flask.cli import with_appcontext
from flask_login import LoginManager
from flask_migrate import Migrate

from database import db
from models import User

def create_app(): # cria uma função para definir o aplicativo
    app = Flask(__name__) # instancia o Flask
    app.secret_key = "abax"

    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///loja.db"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    login_manager = LoginManager()  
    login_manager.login_view = "auth.login" 
    login_manager.init_app(app)

    db.init_app(app)
    app.cli.add_command(init_db_command)
    app.cli.add_command(create_admin_user)
    
    migrate = Migrate(app, db)

    @login_manager.user_loader
    def load_user(user_id: int):      
        return User.query.filter_by(id=user_id).first()

    from auth import bp # autenticação
    app.register_blueprint(bp)
    
    from ctrl_home import bp # página inicial
    app.register_blueprint(bp)

    from produtos_controller import bp as produtos_bp
    app.register_blueprint(produtos_bp)

    from estoque_controller import bp as estoque_bp
    app.register_blueprint(estoque_bp)

    return app # retorna o app criado

def init_db():
    db.drop_all()
    db.create_all()

@click.command("createsuperuser")
@with_appcontext
def create_admin_user():
    from getpass import getpass
    from auth import create_user

    create_user(getpass("Digite a senha para admin: "))

@click.command("init-db")
@with_appcontext
def init_db_command():
    
    init_db()
    click.echo("Initialized the database.")

if __name__ == "__main__":
    create_app().run(debug=True, host="0.0.0.0") 