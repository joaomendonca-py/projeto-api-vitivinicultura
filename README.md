# 🍇 API de Vitivinicultura - Tech Challenge FIAP

[![Deploy Status](https://img.shields.io/badge/Deploy-Live%20on%20Render-success)](https://vitivinicultura-00fv.onrender.com)
[![Python](https://img.shields.io/badge/Python-3.11+-blue)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-green)](https://fastapi.tiangolo.com)
[![MongoDB](https://img.shields.io/badge/MongoDB-Atlas-green)](https://mongodb.com)

API REST completa para análise e consulta de dados de **vitivinicultura** da Embrapa (1970-2024), desenvolvida como Tech Challenge da **Pós-graduação em Machine Learning Engineering da FIAP**.

## 🚀 **Demo Live**

🌐 **URL da API**: https://vitivinicultura-00fv.onrender.com
📚 **Documentação Interativa**: https://vitivinicultura-00fv.onrender.com/docs

## 📋 **Sobre o Projeto**

Esta API fornece acesso aos dados históricos de vitivinicultura do Brasil, incluindo:
- **Produção** de uvas (1970-2023)
- **Processamento** por tipo de uva (1970-2023)  
- **Comercialização** (1970-2023)
- **Importação/Exportação** de derivados (1970-2024)

### 🔐 **Segurança**
- Autenticação JWT obrigatória
- Sistema completo de signup/login
- Proteção de todas as rotas de dados
- Senhas criptografadas com bcrypt

## 🛠️ **Tecnologias Utilizadas**

| Categoria | Tecnologia |
|-----------|------------|
| **Backend** | FastAPI, Python 3.11+ |
| **Banco de Dados** | MongoDB Atlas |
| **Cache** | Redis (com fallback MockRedis) |
| **Autenticação** | JWT (JSON Web Tokens) |
| **Deploy** | Render.com |
| **Web Scraping** | BeautifulSoup4, Requests |
| **Machine Learning** | Scikit-learn, Pandas, NumPy |

## 📁 **Estrutura do Projeto**

```
projeto-api-vitivinicultura/
├── app/                          # Aplicação principal
│   ├── main.py                   # Entrada da aplicação
│   ├── config.py                 # Configurações e variáveis
│   └── routes/                   # Rotas da API
│       ├── auth.py              # Autenticação JWT
│       └── route.py             # Endpoints de dados
├── config/                       # Configurações do projeto
│   ├── database.py              # Conexão MongoDB/Redis
│   ├── models.py                # Modelos Pydantic
│   └── schema.py                # Schemas de dados
├── src/                         # Utilitários e funções
│   └── utils/                   # Funções de scraping
├── notebooks/                   # Jupyter notebooks
├── data/                        # Dados processados
├── requirements.txt             # Dependências Python
├── render.yaml                  # Configuração de deploy
└── README.md                    # Este arquivo
```

## 🚀 **Instalação e Execução**

### **Opção 1: Desenvolvimento Local**

```bash
# 1. Clonar o repositório
git clone https://github.com/joaomendonca-py/projeto-api-vitivinicultura.git
cd projeto-api-vitivinicultura

# 2. Criar ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
.\venv\Scripts\activate  # Windows

# 3. Instalar dependências
pip install -r requirements.txt

# 4. Configurar variáveis de ambiente
cp .env.example .env
# Editar .env com suas configurações

# 5. Executar a aplicação
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### **Opção 2: Docker**

```bash
# Construir e executar com Docker
docker build -t vitivinicultura-api .
docker run -p 8000:8000 vitivinicultura-api
```

## ⚙️ **Variáveis de Ambiente**

Crie um arquivo `.env` na raiz do projeto:

```env
# MongoDB
MONGODB_URL=mongodb+srv://usuario:senha@cluster.mongodb.net/database

# JWT
JWT_SECRET_KEY=sua_chave_secreta_super_segura
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Redis (Opcional)
REDIS_URL=redis://localhost:6379/0
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0

# API
API_ENV=development
CORS_ORIGINS=["http://localhost:3000", "http://localhost:8000"]
```

## 🔐 **Autenticação**

### **1. Criar Conta**
```bash
POST /auth/signup
{
  "username": "seu_usuario",
  "password": "senha123"
}
```

### **2. Fazer Login**
```bash
POST /auth/token
{
  "username": "seu_usuario", 
  "password": "senha123"
}
```

### **3. Usar Token**
```bash
# Incluir em todas as requisições
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

## 📊 **Endpoints da API**

### **🔑 Autenticação**
| Método | Endpoint | Descrição |
|--------|----------|-----------|
| `POST` | `/auth/signup` | Criar nova conta |
| `POST` | `/auth/token` | Login (form-data) |
| `POST` | `/auth/login` | Login (JSON) |
| `GET` | `/auth/me` | Dados do usuário atual |

### **📈 Dados Vitivinicultura** (Requer Autenticação)
| Método | Endpoint | Descrição | Parâmetros |
|--------|----------|-----------|------------|
| `GET` | `/producao` | Dados de produção | `ano` (1970-2023) |
| `GET` | `/processamento` | Dados de processamento | `ano`, `tipo_uva` |
| `GET` | `/processamento_completo` | Processamento completo | `ano` |
| `GET` | `/comercializacao` | Dados de comercialização | `ano` (1970-2023) |
| `GET` | `/importacao` | Dados de importação | `ano`, `derivado` |
| `GET` | `/exportacao` | Dados de exportação | `ano`, `derivado` |

### **📋 Parâmetros**

#### **Tipos de Uva** (`tipo_uva`)
- `01` - Viníferas
- `02` - Americanas e Híbridas  
- `03` - Uvas de Mesa
- `04` - Sem Classificação

#### **Derivados** (`derivado`)
- `01` - Vinhos de mesa
- `02` - Espumantes
- `03` - Uvas frescas
- `04` - Uvas passas (só importação)
- `04` - Suco de uva (só exportação)  
- `05` - Suco de uva (só importação)

## 🧪 **Exemplos de Uso**

### **Autenticação Completa**
```python
import requests

# 1. Criar conta
signup_data = {
    "username": "meu_usuario",
    "password": "minha_senha123"
}
response = requests.post("https://vitivinicultura-00fv.onrender.com/auth/signup", json=signup_data)

# 2. Fazer login
login_data = {
    "username": "meu_usuario", 
    "password": "minha_senha123"
}
response = requests.post("https://vitivinicultura-00fv.onrender.com/auth/login", json=login_data)
token = response.json()["access_token"]

# 3. Usar token nas requisições
headers = {"Authorization": f"Bearer {token}"}
```

### **Consultar Dados**
```python
# Dados de produção de 2022
response = requests.get(
    "https://vitivinicultura-00fv.onrender.com/producao?ano=2022",
    headers=headers
)
dados_producao = response.json()

# Processamento de viníferas em 2020
response = requests.get(
    "https://vitivinicultura-00fv.onrender.com/processamento?ano=2020&tipo_uva=01",
    headers=headers
)
dados_processamento = response.json()
```

### **Estrutura de Resposta**
```json
{
  "ano": 2022,
  "processo": "Produção",
  "labels": ["Produto A", "Produto B", "Produto C"],
  "data": [
    ["Região 1", "1000", "2000", "1500"],
    ["Região 2", "800", "1800", "1200"]
  ]
}
```

## 🌐 **Deploy no Render**

A API está deployada no **Render.com** com:

### **✅ Funcionalidades Ativas**
- ✅ Deploy automático via GitHub
- ✅ HTTPS habilitado
- ✅ Variáveis de ambiente seguras
- ✅ Health checks automáticos
- ✅ Logs em tempo real

### **🔗 URLs**
- **API**: https://vitivinicultura-00fv.onrender.com
- **Docs**: https://vitivinicultura-00fv.onrender.com/docs
- **Health**: https://vitivinicultura-00fv.onrender.com/health

### **📋 Configuração (render.yaml)**
```yaml
services:
  - type: web
    name: vitivinicultura
    env: python
    buildCommand: "pip install -r requirements.txt"
    startCommand: "uvicorn app.main:app --host 0.0.0.0 --port $PORT"
    healthCheckPath: /health
```

## 🔧 **Desenvolvimento**

### **Branches**
- `main` - Produção (deploy automático)
- `deploy-teste` - Testes de deploy
- `dev-complemento` - Desenvolvimento de funcionalidades

### **Comandos Úteis**
```bash
# Executar em desenvolvimento
uvicorn app.main:app --reload

# Executar testes
pytest

# Ver logs do deploy
git push origin main  # Deploy automático no Render

# Verificar status da API
curl https://vitivinicultura-00fv.onrender.com/health
```

## 📚 **Documentação**

### **📖 Documentação Interativa**
- **Swagger UI**: `/docs` - Interface interativa para testar endpoints
- **ReDoc**: `/redoc` - Documentação alternativa

### **🔍 Explorar API**
1. Acesse https://vitivinicultura-00fv.onrender.com/docs
2. Clique em **"Authorize"**
3. Faça login via `/auth/token`
4. Teste qualquer endpoint com autenticação ativa

## 🚦 **Status e Monitoramento**

### **Health Check**
```bash
GET /health
{
  "status": "healthy",
  "version": "1.0.0", 
  "environment": "production",
  "mongodb": "connected",
  "redis": "not configured"
}
```

### **🔴 Cache (Redis)**
- **Status atual**: MockRedis (funcional sem cache)
- **Impacto**: Dados sempre atualizados da fonte
- **Performance**: Pode ser mais lenta sem cache

## 🤝 **Contribuição**

1. **Fork** o projeto
2. **Clone** seu fork
3. **Crie** uma branch: `git checkout -b feature/nova-funcionalidade`
4. **Commit** suas mudanças: `git commit -m 'Adicionar nova funcionalidade'`
5. **Push** para a branch: `git push origin feature/nova-funcionalidade`
6. **Abra** um Pull Request

## 📄 **Licença**

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## 👥 **Autores**

- **João** - *Desenvolvimento inicial* - [joaomendonca-py](https://github.com/joaomendonca-py)

## 🙏 **Agradecimentos**

- **FIAP** - Pós-graduação em Machine Learning Engineering
- **Embrapa** - Fonte dos dados de vitivinicultura
- **Render.com** - Plataforma de deploy gratuita
- **FastAPI** - Framework web moderno e rápido

---

## 📞 **Suporte**

- **Issues**: [GitHub Issues](https://github.com/joaomendonca-py/projeto-api-vitivinicultura/issues)
- **Email**: projeto5mlet@gmail.com
- **Documentação**: https://vitivinicultura-00fv.onrender.com/docs

---

⭐ **Se este projeto te ajudou, deixe uma star no GitHub!**