CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE formularios (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    titulo VARCHAR(255) NOT NULL,
    descricao TEXT,
    ordem INTEGER NOT NULL,
    createdAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE perguntas (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    idFormulario UUID NOT NULL REFERENCES formularios(id) ON DELETE CASCADE,
    titulo VARCHAR(255) NOT NULL,
    codigo INTEGER NOT NULL,
    orientacaoResposta TEXT,
    ordem INTEGER NOT NULL,
    obrigatoria BOOLEAN NOT NULL,
    subPergunta TEXT,
        createdAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    tipoPergunta VARCHAR(100)
);

CREATE TABLE respostas (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    idPergunta UUID NOT NULL REFERENCES perguntas(id) ON DELETE CASCADE,
    resposta TEXT NOT NULL,
    ordem INTEGER NOT NULL,
    respostaAberta BOOLEAN NOT NULL,
        createdAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP

);

CREATE TABLE respostas_pergunta (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    idOpcaoResposta UUID NOT NULL,
    idPergunta UUID NOT NULL REFERENCES perguntas(id) ON DELETE CASCADE,
        createdAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP

);

CREATE INDEX idx_perguntas_idFormulario ON perguntas(idFormulario);
CREATE INDEX idx_respostas_idPergunta ON respostas(idPergunta);
CREATE INDEX idx_respostas_pergunta_idPergunta ON respostas_pergunta(idPergunta);
