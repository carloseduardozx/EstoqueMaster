from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from database import db
from models import Produto, MovimentacaoEstoque

bp = Blueprint('produtos', __name__, url_prefix='/produtos')

@bp.route('/')
@login_required
def index():
    # busca todos os produtos no banco
    produtos = Produto.query.order_by(Produto.titulo).all()
    return render_template('produtos.html', produtos=produtos)

@bp.route('/salvar', methods=['POST'])
@login_required
def salvar():
    # pega os dados do formulário
    id = request.form.get('id')
    titulo = request.form.get('titulo')
    descricao = request.form.get('descricao')
    marca = request.form.get('marca')
    modelo = request.form.get('modelo')
    caracteristicas = request.form.get('caracteristicas')
    estoque = request.form.get('estoque')
    estoque_min = request.form.get('estoque_min')

    # validação simples
    if not titulo or not marca or not estoque or not estoque_min:
        flash('Preencha todos os campos obrigatórios!', 'danger')
        return redirect(url_for('produtos.index'))

    try:
        if id:  # se existe ID, é uma edição
            produto = Produto.query.get(id)
            if produto:
                produto.titulo = titulo
                produto.descricao = descricao
                produto.marca = marca
                produto.modelo = modelo
                produto.caracteristicas = caracteristicas
                produto.estoque = int(estoque)
                produto.estoque_min = int(estoque_min)
                flash('Produto atualizado com sucesso!', 'success')
        else:  # se não existe ID, é um novo cadastro
            novo_produto = Produto(
                titulo=titulo,
                descricao=descricao,
                marca=marca,
                modelo=modelo,
                caracteristicas=caracteristicas,
                estoque=int(estoque),
                estoque_min=int(estoque_min)
            )
            db.session.add(novo_produto)
            flash('Produto cadastrado com sucesso!', 'success')

        db.session.commit()
    except Exception as e:
        db.session.rollback()
        flash(f'Ocorreu um erro ao salvar: {e}', 'danger')

    return redirect(url_for('produtos.index'))

@bp.route('/editar/<int:id>')
@login_required
def editar(id):
    produto = Produto.query.get(id)
    if not produto:
        flash('Produto não encontrado!', 'danger')
        return redirect(url_for('produtos.index'))
    
    # carrega a lista de produtos e o produto a ser editado
    produtos = Produto.query.order_by(Produto.titulo).all()
    return render_template('produtos.html', produtos=produtos, produto_editar=produto)

@bp.route('/deletar/<int:id>', methods=['POST'])
@login_required
def deletar(id):
    produto = Produto.query.get(id)
    if not produto:
        flash('Produto não encontrado!', 'danger')
        return redirect(url_for('produtos.index'))

    # conta quantas movimentações estão associadas a este produto
    movimentacoes_associadas = MovimentacaoEstoque.query.filter_by(produto_id=id).count()

    flash(f'DEBUG: O produto "{produto.titulo}" tem {movimentacoes_associadas} movimentação(ões) associadas.', 'info')

    if movimentacoes_associadas > 0:
        # se houver movimentações, impede a exclusão e alerta o usuário
        flash(f'Este produto não pode ser excluído pois existem {movimentacoes_associadas} movimentação(ões) de estoque associadas a ele.', 'warning')
    else:
        # se não houver movimentações, pode excluir com segurança
        db.session.delete(produto)
        db.session.commit()
        flash('Produto excluído com sucesso!', 'success')
    
    return redirect(url_for('produtos.index'))