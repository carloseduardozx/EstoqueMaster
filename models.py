from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from database import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__ = "auth_user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    nome = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(200), nullable=False, unique=True)
    
    movimentacoes_realizadas = relationship("MovimentacaoEstoque", back_populates="responsavel")

    def as_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'nome': self.nome,
            'email': self.email
        }

class Produto(db.Model):
    __tablename__ = 'produtos'
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False)
    descricao = db.Column(db.Text(1000), nullable=False)
    
    marca = db.Column(db.String(100), nullable=False)
    modelo = db.Column(db.String(100), nullable=True)
    caracteristicas = db.Column(db.Text, nullable=True)
    
    estoque = db.Column(db.Integer, nullable=False, default=0)
    estoque_min = db.Column(db.Integer, nullable=False, default=5)

    movimentacoes = relationship("MovimentacaoEstoque", back_populates="produto")

class MovimentacaoEstoque(db.Model):
    __tablename__ = 'movimentacoes_estoque'
    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(20), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)
    data_movimentacao = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    produto_id = db.Column(db.Integer, db.ForeignKey('produtos.id'), nullable=False)
    responsavel_id = db.Column(db.Integer, db.ForeignKey('auth_user.id'), nullable=False)
    
    produto = relationship("Produto", back_populates="movimentacoes")
    responsavel = relationship("User", back_populates="movimentacoes_realizadas")
