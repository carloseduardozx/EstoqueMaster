PRAGMA foreign_keys = off;
BEGIN TRANSACTION;

-- Tabela: auth_event
CREATE TABLE IF NOT EXISTS auth_event (
	id INTEGER NOT NULL, 
	event_type VARCHAR(150) NOT NULL, 
	event_log VARCHAR NOT NULL, 
	event_timestamp VARCHAR(150) NOT NULL, 
	user_id INTEGER, 
	PRIMARY KEY (id), 
	FOREIGN KEY(user_id) REFERENCES auth_user (id)
);

-- Tabela: auth_user
CREATE TABLE IF NOT EXISTS auth_user (
	id INTEGER NOT NULL, 
	username VARCHAR(150) NOT NULL, 
	password VARCHAR(255) NOT NULL, 
	nome VARCHAR(150) NOT NULL, 
	email VARCHAR(200) NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (username), 
	UNIQUE (email)
);
INSERT INTO auth_user (id, username, password, nome, email) VALUES (1, 'admin', 'scrypt:32768:8:1$zk4r9Pe0N6OkHBx9$bc247c9a8e205f87b869e47f49afffb9a1bf382c118555f252d383875fa7b6445a96bc873ab4ef0130013e9137c1aed0f2d1835d2eae62dae2f4e46fabba1c29', 'Administrador', 'admin@admin.com');

-- Tabela: movimentacoes_estoque
CREATE TABLE IF NOT EXISTS movimentacoes_estoque (
	id INTEGER NOT NULL, 
	tipo VARCHAR(20) NOT NULL, 
	quantidade INTEGER NOT NULL, 
	data_movimentacao DATETIME NOT NULL, 
	produto_id INTEGER NOT NULL, 
	responsavel_id INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(produto_id) REFERENCES produtos (id), 
	FOREIGN KEY(responsavel_id) REFERENCES auth_user (id)
);
INSERT INTO movimentacoes_estoque (id, tipo, quantidade, data_movimentacao, produto_id, responsavel_id) VALUES (1, 'Entrada', 35, '2025-11-25 10:01:33.370116', 2, 1);
INSERT INTO movimentacoes_estoque (id, tipo, quantidade, data_movimentacao, produto_id, responsavel_id) VALUES (2, 'Entrada', 70, '2025-11-25 10:01:47.117515', 3, 1);
INSERT INTO movimentacoes_estoque (id, tipo, quantidade, data_movimentacao, produto_id, responsavel_id) VALUES (3, 'Sa�da', 30, '2025-11-25 10:01:56.501767', 3, 1);
INSERT INTO movimentacoes_estoque (id, tipo, quantidade, data_movimentacao, produto_id, responsavel_id) VALUES (4, 'Entrada', 30, '2025-11-25 10:02:06.166725', 1, 1);

-- Tabela: produtos
CREATE TABLE IF NOT EXISTS produtos (
	id INTEGER NOT NULL, 
	titulo VARCHAR(200) NOT NULL, 
	descricao TEXT(1000) NOT NULL, 
	marca VARCHAR(100) NOT NULL, 
	modelo VARCHAR(100), 
	caracteristicas TEXT, 
	estoque INTEGER NOT NULL, 
	estoque_min INTEGER NOT NULL, 
	PRIMARY KEY (id)
);
INSERT INTO produtos (id, titulo, descricao, marca, modelo, caracteristicas, estoque, estoque_min) VALUES (1, 'Martelo de Unha 16 oz', 'Martelo profissional com unha para extra��o de pregos, cabo ergon�mico.', 'MASTER', 'MU-16-PR', 'Material do cabo: Fibra de Vidro; 

Perfil: Reto; Peso: 16 oz', 80, 10);
INSERT INTO produtos (id, titulo, descricao, marca, modelo, caracteristicas, estoque, estoque_min) VALUES (2, 'Chave de Fenda Isolante', 'Chave de fenda com cabo isolante para trabalhos com energia, ponta imantada.', 'Tramontina', 'CF-254', 'Material do cabo: Polipropileno com isolamento; 

Revestimento: Ponta imantada; 

Tamanho: 1/4', 50, 15);
INSERT INTO produtos (id, titulo, descricao, marca, modelo, caracteristicas, estoque, estoque_min) VALUES (3, 'Furadeira de Impacto 550W', 'Furadeira de impacto robusta para uso em constru��o civil e reparos.', 'Bosch', 'GSB 550 Professional', 'Tens�o: 220V; 

Pot�ncia: 550W; 

Capacidade de mandril: 13mm', 60, 5);

COMMIT TRANSACTION;
PRAGMA foreign_keys = on;
