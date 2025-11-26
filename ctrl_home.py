from flask import Blueprint, render_template

bp = Blueprint(__name__, "HomeController")

# rota para a página pública da loja (acessada pela URL /)
@bp.route('/')
def index():
    """ página inicial pública da loja de ferramentas """
    return render_template("public_home.html")

# Rota para o painel de controle interno (após o login)
@bp.route('/dashboard')
def dashboard():
    """ painel principal do sistema, para usuários logados """
    return render_template("dashboard.html")