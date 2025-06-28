# Rural Producer API

API para gerenciamento de produtores rurais, construída com **FastAPI**, **SQLAlchemy** e **PostgreSQL**.  
Permite cadastrar, listar, atualizar e remover informações de produtores com dados como CPF/CNPJ, áreas cultiváveis, culturas plantadas e localização.


## Principais Tecnologias Utilizadas

- [FastAPI](https://fastapi.tiangolo.com/)
- [SQLAlchemy (async)](https://docs.sqlalchemy.org/en/20/)
- [PostgreSQL](https://www.postgresql.org/)
- [Alembic](https://alembic.sqlalchemy.org/)
- [Loguru](https://github.com/Delgan/loguru) para logs estruturados
- [Docker](https://www.docker.com/) + Docker Compose
- [Pytest](https://docs.pytest.org/en/7.4.x/)

## Variáveis de Ambiente

Crie um arquivo `.env` com o seguinte conteúdo apenas como exemplo, pois em produção as váriáveis de ambiente devem ser definidas em um ambiente seguro:

```env
POSTGRES_USER=user
POSTGRES_PASSWORD=root
POSTGRES_DB=producer_db
POSTGRES_HOST=producer_db
POSTGRES_PORT=5432

DATABASE_URL=postgresql+psycopg://user:root@producer_db:5432/producer_db
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

##Como executar o projeto:
#Subir os containers (com build):
docker compose up --build

# Isso permitirá ver os logs diretamente no terminal, e também ao realizar requisições pelo Swagger.
# Caso prefira rodar em segundo plano para não ver os logs no terminal, use:
docker compose up -d

# Parar e remover os containers incluindo volumes:
docker compose down -v

# Rodar os testes:
uv run pytest -v
