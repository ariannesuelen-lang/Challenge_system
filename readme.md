# Sistema de Votação

Backend de um sistema de votação construído com **FastAPI** seguindo os princípios de **Clean Architecture**, **Domain-Driven Design (DDD)** e **SOLID** com Banco de Dados em PostgreSQL.

## 📋 Visão Geral

API RESTful para registro de votos com notas de 0 a 10, permitindo:
- Registro de votos com validação de nota mínima (0.2) e máxima (10.0)
- Listagem de todos os votos registrados
- Consulta de estatísticas agregadas (média, mínimo, máximo, total)
- Rate limiting para proteção contra abuso

## 🏗️ Arquitetura

O projeto segue a estrutura de **Clean Architecture** com camadas bem definidas:

```
app/
├── domain/                 # Regras de negócio e entidades
│   ├── entities/           # Entidades (Vote)
│   ├── value_objects/      # Value Objects (VoteScore)
│   ├── repositories/       # Interfaces de repositório (contratos)
│   ├── services/           # Domain Services (VotingService)
│   └── exceptions/         # Exceções de domínio
├── application/            # Casos de uso da aplicação
│   ├── dtos/               # DTOs de entrada e saída
│   └── use_cases/          # Casos de uso (RegisterVote, GetAllVotes, GetStatistics)
├── infrastructure/         # Implementações concretas
│   ├── repositories/       # Repositórios (InMemoryVoteRepository)
│   └── rate_limiter/       # Configuração de rate limiting (SlowAPI)
└── presentation/           # Camada de exposição
    ├── routes/             # Rotas FastAPI
    └── schemas/            # Pydantic schemas
```

## 🚀 Tecnologias

| Tecnologia  | Versão  | Finalidade                     |
|-------------|---------|--------------------------------|
| Python      | 3.12+   | Linguagem principal            |
| FastAPI     | 0.115.6 | Framework web assíncrono       |
| Uvicorn     | 0.34.0  | Servidor ASGI                  |
| Pydantic    | 2.10.4  | Validação e serialização       |
| SlowAPI     | 0.1.9   | Rate limiting                  |
| Pytest      | 8.3.4   | Testes automatizados           |
| HTTPX       | 0.28.1  | Cliente HTTP para testes       |

## 📡 Endpoints da API

### Registrar Voto
```http
POST /api/v1/votes/
Content-Type: application/json

{
  "score": 8.5
}
```
- Nota válida: **0.2 a 10.0**
- Rate limit: **10 requisições/minuto**
- Resposta: `201 Created`

### Listar Votos
```http
GET /api/v1/votes/
```
- Rate limit: **20 requisições/minuto**
- Resposta: `200 OK` com lista de votos

### Estatísticas
```http
GET /api/v1/votes/statistics
```
- Rate limit: **30 requisições/minuto**
- Resposta: `200 OK` com:
  - `total_votes`: Total de votos registrados
  - `average_score`: Média das notas
  - `min_score`: Nota mínima
  - `max_score`: Nota máxima

### Health Check
```http
GET /health
```
- Resposta: Status de saúde do serviço

## 🛠️ Instalação e Execução

### Pré-requisitos
- Python 3.12+
- [uv](https://github.com/astral-sh/uv) (gerenciador de pacotes)

### 1. Clone o repositório
```bash
git clone https://github.com/ariannesuelen-lang/Challenge_system.git
cd sistema_votacao
```
 - Se você quer clonar o repositório em uma pasta já existente:
```bash
git clone https://github.com/ariannesuelen-lang/Challenge_system.git .
```

### 2. Instale as dependências
```bash
uv sync
```

### 3. Execute o servidor de desenvolvimento
```bash
uv run dev
```

Ou diretamente:
```bash
uv run python -m app.main
```

O servidor será iniciado em `http://localhost:8000`.

## 📖 Documentação Interativa

Com o servidor rodando, acesse:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🧪 Testes

```bash
uv run pytest tests/ -v
```

## ⚙️ Configuração

As configurações do aplicativo estão centralizadas em `app/config.py`:
- `app_name`: Sistema de Votação para Desafios
- `app_version`: 1.0
- `debug`: Modo de desenvolvimento (reload automático)
- `min_vote_score`: Nota mínima permitida (0.2)
- `max_vote_score`: Nota máxima permitida (10.0)

## 🤝 Contribuindo

Contribuições são bem-vindas! Para contribuir:

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b calculo_media/votacao`)
3. Commit suas mudanças (`git commit -m 'Add something'`)
4. Push para a branch (`git push`)

## 📄 Licença

Este projeto está licenciado sob a [MIT License](LICENSE).

## 🆘 Suporte

Para dúvidas, problemas ou sugestões, abra uma [issue](https://github.com/ariannesuelen-lang/Challenge_system/issues) no repositório.

---
**Última atualização:** Abril 2026
