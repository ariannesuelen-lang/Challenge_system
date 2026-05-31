# 📝 Sistema de Mini-Provas

> API RESTful para gerenciamento de mini-provas educacionais com **FastAPI**, **Supabase**, **PostgreSQL** e **Python**.

![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=flat&logo=fastapi)
![Python](https://img.shields.io/badge/Python-3.8+-blue?style=flat&logo=python)
![Postgres](https://img.shields.io/badge/Postgres-%23316192.svg?logo=postgresql&logoColor=white)
![Supabase](https://img.shields.io/badge/Supabase-3FCF8E?logo=supabase&logoColor=fff)

---

## 📋 Índice

- [Sobre](#-sobre)
- [Funcionalidades](#-funcionalidades)
- [Pré-requisitos](#-pré-requisitos)
- [Instalação](#-instalação)
- [Configuração do Firebase](#-configuração-do-firebase)
- [Executando a Aplicação](#-executando-a-aplicação)
- [Documentação da API](#-documentação-da-api)
- [Endpoints](#-endpoints)
- [Estrutura do Banco de Dados](#-estrutura-do-banco-de-dados)
- [Exemplos de Uso](#-exemplos-de-uso)
- [Estrutura do Projeto](#-estrutura-do-projeto)
- [Contribuição](#-contribuição)
- [Licença](#-licença)

---

## 🔍 Sobre

O **Sistema de Mini-Provas** é uma API desenvolvida para facilitar a criação, aplicação e correção de avaliações rápidas no contexto educacional. Com suporte a sincronização em nuvem via Firebase, o sistema permite:

- ✅ Cadastro de alunos e questões
- ✅ Geração aleatória de provas com 5 questões
- ✅ Correção automática com cálculo de nota
- ✅ Identificação de tópicos que precisam de reforço
- ✅ Relatórios e ranking de desempenho

---

## ✨ Funcionalidades

### 👥 Gestão de Alunos
- [x] Cadastrar novos alunos
- [x] Listar todos os alunos cadastrados
- [x] Sincronização com Firebase Firestore

### ❓ Gestão de Questões
- [x] Cadastrar questões com múltipla escolha (A-D)
- [x] Categorizar por disciplina, tema e dificuldade
- [x] Filtrar questões por disciplina ou nível de dificuldade
- [x] Armazenamento local (SQLite) + nuvem (Firebase)

### 📝 Realização de Mini-Provas
- [x] Geração aleatória de 5 questões
- [x] Embaralhamento das alternativas por questão
- [x] Tempo sugerido: 60 segundos por questão (5 min total)

### ✅ Correção e Resultados
- [x] Correção automática das respostas
- [x] Cálculo de nota (0 a 10)
- [x] Identificação de tópicos fracos para estudo
- [x] Histórico de resultados por aluno

### 📊 Relatórios e Analytics
- [x] Relatório completo de desempenho
- [x] Ranking de alunos por média de notas
- [x] Dados sincronizados no Firebase para dashboards externos

---

## ⚙️ Pré-requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)
- Conta no Firebase com projeto configurado
- Arquivo de credencial `firebase_key.json`

---

## 🚀 Instalação

1. **Clone o repositório** ou crie a pasta do projeto:

```bash
mkdir mini-provas-api
cd mini-provas-api
```
python -m venv venv

# Linux/Mac:
source venv/bin/activate

# Windows:
venv\Scripts\activate

```bash
pip install fastapi uvicorn firebase-admin pydantic
```
## Exemplo de Questão

```bash
{
  "disciplina": "Matemática",
  "tema": "Equações do 2º grau",
  "dificuldade": "Média",
  "pergunta": "Qual é a soma das raízes da equação x² - 5x + 6 = 0?",
  "alternativa_a": "3",
  "alternativa_b": "5",
  "alternativa_c": "6",
  "alternativa_d": "10",
  "resposta_correta": "5"
}
```

## Exemplo de Resposta

```bash
{
  "aluno_id": 1,
  "duracao_total": "5 minutos",
  "quantidade_questoes": 5,
  "questoes": [
    {
      "id": 42,
      "disciplina": "Matemática",
      "tema": "Equações do 2º grau",
      "dificuldade": "Média",
      "pergunta": "Qual é a soma das raízes da equação x² - 5x + 6 = 0?",
      "alternativas": ["10", "5", "3", "6"],
      "tempo_maximo_questao": "60 segundos"
    }
  ]
}
```
