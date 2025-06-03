# API de Vitivinicultura

API para análise e previsão de dados relacionados à vitivinicultura, desenvolvida como parte do Tech Challenge da Pós em Machine Learning Engineering.

## Funcionalidades

- Autenticação JWT
- Análise de dados vitivinícolas
- Cache com Redis
- Armazenamento MongoDB

## Requisitos

- Python 3.9+
- MongoDB
- Redis
- Docker (opcional)

## Instalação

### Usando Python local

```bash
# Criar ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
.\venv\Scripts\activate  # Windows

# Instalar dependências
pip install -r requirements.txt

# Executar a aplicação
uvicorn app.main:app --reload
```

### Usando Docker

```bash
# Construir a imagem
docker build -t vitivinicultura-api .

# Executar o container
docker run -p 8000:8000 vitivinicultura-api
```

## Variáveis de Ambiente

Crie um arquivo `.env` com as seguintes variáveis:

```
MONGODB_URL=sua_url_mongodb
JWT_SECRET_KEY=sua_chave_secreta
REDIS_URL=sua_url_redis
```

## Documentação da API

A documentação completa da API está disponível em:
- Swagger UI: `/docs`
- ReDoc: `/redoc`

## Endpoints Principais

- POST `/signup`: Criar nova conta
- POST `/token`: Obter token JWT
- GET `/vinhos`: Listar dados dos vinhos
- POST `/predict`: Realizar previsões

## Contribuição

1. Faça um Fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request