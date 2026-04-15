#Sistema Acadêmico

Sistema web para criação de desafios educacionais, respostas e votação entre alunos e professores.


##Tecnologias

* Backend: FastAPI + Supabase
* Frontend: Streamlit
* Segurança: bcrypt (hash de senha)



##Funcionalidades

* Cadastro e login de usuários
* Criação de desafios (professores)
* Respostas e votação
* Cursos e disciplinas
* Painel administrativo


##Como rodar

### Backend
uvicorn main:app --reload

### Frontend
streamlit run app.py
