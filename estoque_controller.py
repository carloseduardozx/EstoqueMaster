from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from database import db
from models import Produto, MovimentacaoEstoque
from datetime import datetime

bp = Blueprint('estoque', __name__, url_prefix='/estoque')

@bp.route('/')
@login_required
def index():
    produtos = Produto.query.order_by(Produto.titulo).all()
    
    # buscar o histórico de movimentações para exibir
    movimentacoes = MovimentacaoEstoque.query.order_by(MovimentacaoEstoque.data_movimentacao.desc()).limit(50).all()

    return render_template('estoque.html', produtos=produtos, movimentacoes=movimentacoes)

@bp.route('/movimentar', methods=['POST'])
@login_required
def movimentar():
    # pega os dados do formulário
    produto_id = request.form.get('produto_id')
    tipo = request.form.get('tipo') # 'Entrada' ou 'Saída'
    quantidade = int(request.form.get('quantidade'))
    data_mov_str = request.form.get('data_movimentacao')

    # validação básica
    if not all([produto_id, tipo, quantidade > 0, data_mov_str]):
        flash('Por favor, preencha todos os campos corretamente.', 'danger')
        return redirect(url_for('estoque.index'))

    try:
        # 1. converte a string do formulário para um objeto 'date'
        data_escolhida_pelo_usuario = datetime.strptime(data_mov_str, '%Y-%m-%d').date()

        # 2. pega a hora atual do sistema
        hora_atual = datetime.now().time()

        # 3. combina a data escolhida com a hora atual
        data_movimentacao = datetime.combine(data_escolhida_pelo_usuario, hora_atual)

        # encontra o produto no banco
        produto = Produto.query.get(produto_id)
        if not produto:
            flash('Produto não encontrado.', 'danger')
            return redirect(url_for('estoque.index'))

        # atualiza o estoque do produto
        if tipo == 'Entrada':
            produto.estoque += quantidade
        elif tipo == 'Saída':
            if produto.estoque >= quantidade:
                produto.estoque -= quantidade
            else:
                flash(f'Estoque insuficiente! O produto "{produto.titulo}" tem apenas {produto.estoque} unidades.', 'danger')
                return redirect(url_for('estoque.index'))

        # cria o registro da movimentação
        movimentacao = MovimentacaoEstoque(
            tipo=tipo,
            quantidade=quantidade,
            data_movimentacao=data_movimentacao, # usa o novo datetime combinado
            produto_id=produto.id,
            responsavel_id=current_user.id # pega o ID do usuário logado
        )

        db.session.add(movimentacao)
        db.session.commit() # salva tanto a movimentação quanto a atualização do produto

        flash(f'Movimentação de {tipo} do produto "{produto.titulo}" registrada com sucesso!', 'success')

        # requisito 7.1.4: Verificação de estoque baixo
        if produto.estoque <= produto.estoque_min:
            flash(f'⚠️ ALERTA: O estoque do produto "{produto.titulo}" atingiu o nível mínimo ({produto.estoque_min} unidades)!', 'warning')

    except ValueError:
        flash('Data ou quantidade inválida.', 'danger')
    except Exception as e:
        db.session.rollback()
        flash(f'Ocorreu um erro ao registrar a movimentação: {e}', 'danger')

    return redirect(url_for('estoque.index'))