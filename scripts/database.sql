CREATE TABLE alembic_version (
    version_num VARCHAR(32) NOT NULL, 
    CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num)
);

-- Running upgrade  -> 1888b1a85062

CREATE TABLE campos_teste (
    id INTEGER NOT NULL, 
    campo_texto VARCHAR(150) NOT NULL, 
    campo_texto_limitado VARCHAR(10) NOT NULL, 
    campo_email VARCHAR(150) NOT NULL, 
    campo_numero INTEGER NOT NULL, 
    campo_data DATE NOT NULL, 
    campo_selecao INTEGER NOT NULL, 
    chk_habilitado BOOLEAN NOT NULL, 
    chk_desabilitado BOOLEAN NOT NULL, 
    rb_resposta VARCHAR(1) NOT NULL, 
    area_texto VARCHAR(450) NOT NULL, 
    PRIMARY KEY (id)
);

INSERT INTO alembic_version (version_num) VALUES ('1888b1a85062') RETURNING version_num;

