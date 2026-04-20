CREATE TABLE propriedades (
    id NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nome VARCHAR2(120) NOT NULL,
    municipio VARCHAR2(100) NOT NULL,
    area_hectares NUMBER(10,2) NOT NULL,
    altitude_metros NUMBER(7,2) NOT NULL,
    produtor VARCHAR2(120) NOT NULL,
    data_cadastro DATE DEFAULT SYSDATE NOT NULL
);

CREATE TABLE arvores (
    id NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    propriedade_id NUMBER NOT NULL,
    quantidade NUMBER NOT NULL,
    tipo VARCHAR2(20) NOT NULL,
    idade_anos NUMBER NOT NULL,
    CONSTRAINT fk_arvores_propriedade FOREIGN KEY (propriedade_id) REFERENCES propriedades(id),
    CONSTRAINT ck_arvores_tipo CHECK (tipo IN ('nativa','enxertada')),
    CONSTRAINT ck_arvores_quantidade CHECK (quantidade > 0),
    CONSTRAINT ck_arvores_idade CHECK (idade_anos >= 0)
);

CREATE TABLE colheitas (
    id NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    propriedade_id NUMBER NOT NULL,
    data_colheita DATE NOT NULL,
    kg_coletados NUMBER(10,2) NOT NULL,
    metodo VARCHAR2(20) NOT NULL,
    uso_epi CHAR(1) NOT NULL,
    CONSTRAINT fk_colheitas_propriedade FOREIGN KEY (propriedade_id) REFERENCES propriedades(id),
    CONSTRAINT ck_colheitas_metodo CHECK (metodo IN ('chao','escalada')),
    CONSTRAINT ck_colheitas_epi CHECK (uso_epi IN ('S','N')),
    CONSTRAINT ck_colheitas_kg CHECK (kg_coletados > 0)
);

CREATE TABLE registros_climaticos (
    id NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    propriedade_id NUMBER NOT NULL,
    data_registro DATE NOT NULL,
    temperatura_celsius NUMBER(5,2) NOT NULL,
    umidade_percentual NUMBER(5,2) NOT NULL,
    precipitacao_mm NUMBER(6,2) NOT NULL,
    CONSTRAINT fk_clima_propriedade FOREIGN KEY (propriedade_id) REFERENCES propriedades(id),
    CONSTRAINT ck_clima_umidade CHECK (umidade_percentual BETWEEN 0 AND 100),
    CONSTRAINT ck_clima_precipitacao CHECK (precipitacao_mm >= 0)
);

CREATE TABLE armazenamentos (
    id NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    propriedade_id NUMBER NOT NULL,
    kg_armazenados NUMBER(10,2) NOT NULL,
    metodo VARCHAR2(20) NOT NULL,
    data_entrada DATE NOT NULL,
    prazo_dias NUMBER NOT NULL,
    CONSTRAINT fk_armazenamento_propriedade FOREIGN KEY (propriedade_id) REFERENCES propriedades(id),
    CONSTRAINT ck_armazenamento_metodo CHECK (metodo IN ('granel','vacuo','congelado')),
    CONSTRAINT ck_armazenamento_kg CHECK (kg_armazenados > 0),
    CONSTRAINT ck_armazenamento_prazo CHECK (prazo_dias > 0)
);

CREATE TABLE precos (
    id NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    data_registro DATE NOT NULL,
    preco_kg NUMBER(8,2) NOT NULL,
    regiao VARCHAR2(100) NOT NULL,
    CONSTRAINT ck_precos_valor CHECK (preco_kg > 0)
);

CREATE INDEX idx_colheitas_data ON colheitas(data_colheita);
CREATE INDEX idx_clima_data ON registros_climaticos(data_registro);
CREATE INDEX idx_precos_data ON precos(data_registro);
