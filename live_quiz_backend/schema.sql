-- Schema para o app de Live Quiz

-- Tabela de Quizzes
CREATE TABLE public.quizzes (
    id SERIAL PRIMARY KEY,
    professor_id INT NOT KEY REFERENCES public.usuarios(id) ON DELETE CASCADE,
    titulo TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'pendente' CHECK (status IN ('pendente', 'iniciado', 'finalizado')),
    criado_em TIMESTAMPTZ DEFAULT NOW()
);

-- Tabela de Perguntas
CREATE TABLE public.perguntas (
    id SERIAL PRIMARY KEY,
    quiz_id INT NOT NULL REFERENCES public.quizzes(id) ON DELETE CASCADE,
    texto TEXT NOT NULL,
    alternativas JSONB NOT NULL, -- Exemplo: ["A", "B", "C", "D"]
    indice_correto INT NOT NULL, -- O índice (0, 1, 2, 3...) indicando qual alternativa é a correta
    criado_em TIMESTAMPTZ DEFAULT NOW()
);

-- Tabela de Participações (Para guardar a pontuação e ranking do aluno num Quiz)
CREATE TABLE public.participacoes (
    id SERIAL PRIMARY KEY,
    quiz_id INT NOT NULL REFERENCES public.quizzes(id) ON DELETE CASCADE,
    aluno_id INT NOT NULL REFERENCES public.usuarios(id) ON DELETE CASCADE,
    pontuacao INT DEFAULT 0,
    finalizou BOOLEAN DEFAULT FALSE,
    criado_em TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(quiz_id, aluno_id) -- Garante que o aluno participe apenas uma vez por quiz
);

-- Tabela de Respostas dos Alunos (Para histórico e feedback)
CREATE TABLE public.respostas_alunos (
    id SERIAL PRIMARY KEY,
    participacao_id INT NOT NULL REFERENCES public.participacoes(id) ON DELETE CASCADE,
    pergunta_id INT NOT NULL REFERENCES public.perguntas(id) ON DELETE CASCADE,
    indice_resposta INT NOT NULL, -- O que o aluno marcou
    correta BOOLEAN NOT NULL,
    criado_em TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(participacao_id, pergunta_id) -- Garante apenas uma resposta por pergunta
);

-- OBS: Presume-se que a tabela 'usuarios' já existe com a estrutura informada:
-- id (int4), nome (text), email (text), senha (text), tipo_usuario (text), criado_em (timestamptz)
