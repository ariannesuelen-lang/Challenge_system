# Challenge_system

Para visualização no streamlit: https://challengesystem-nhyjiafgjapzerhlwhposx.streamlit.app/

Acesso ao Notion: https://www.notion.so/invite/03cf63e02886c912d8564c84ba2dc3bb0aa55498

Observação: Em cada commit, comentar o que foi feito e colocar o nome dos participantes (# e @)



COMO A MAIN ESTÁ ORGANIZADA:

````markdown
# Sistema de Desafios

```bash
sistema_de_desafios/
│
├── app.py
├── requirements.txt
│
├── .streamlit/
│   └── secrets.toml
│
├── database/
│   ├── __init__.py
│   └── conexao.py
│
├── services/
│   ├── __init__.py
│   ├── auth_service.py
│   ├── desafio_service.py
│   ├── votacao_service.py
|   ├── participacao_service.py
│   └── notificacao_service.py
│
├── telas/
│   ├── __init__.py
│   ├── login.py
│   ├── cadastro.py
│   ├── home.py
│   ├── desafios.py
│   ├── votacao.py
│   ├── mini_provas.py
│   ├── quiz_ao_vivo.py
│   ├── criar_desafios.py
│   ├── batalha_de_equipes.py
│   └── admin.py
│
├── utils/
│   ├── __init__.py
│   ├── session.py
│   └── permissao.py
│
└── components/
    ├── __init__.py
    └── navbar.py
```

---

## `app.py`

É o arquivo que o Streamlit executa quando você roda.  
Só vai aparecer no Streamlit se você colocar/chamar seu código aqui.

---

## `requirements.txt`

Lista todas as bibliotecas do projeto.

---

## `.streamlit/secrets.toml`

É a Pasta de configurações do Streamlit. Guarda informações sensíveis.

---

## `database/conexao.py`

Tudo relacionado ao banco de dados. Conexão com o Supabase.

---

## `services/`

Ela guarda as regras de negócio do sistema (back-end).

## `services/auth_service.py`

Responsável por autenticação.

---

## `telas/`

Todas as telas que terão (front-end).

---

## `utils/session.py` e `utils/permissao.py`

Controla sessão do usuário. Controla permissões.

---

## `components/navbar.py`

Partes visuais reutilizáveis.

Componentes que se repetem (Barra de navegação do sistema - navbar).
````
