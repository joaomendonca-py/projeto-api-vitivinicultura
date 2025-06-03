# Variáveis de Ambiente - API Vitivinicultura

## 📋 Configuração no Render

Para o deploy funcionar corretamente, configure estas variáveis de ambiente **diretamente no painel do Render**:

### 🔐 **Banco de Dados MongoDB Atlas**
```
MONGODB_URL=mongodb+srv://[username]:[password]@[cluster].mongodb.net/?retryWrites=true&w=majority&appName=[appName]
```

### 🔑 **Autenticação JWT**
```
JWT_SECRET_KEY=[sua-chave-secreta-segura]
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

### 🗄️ **Cache Redis Cloud**
```
REDIS_URL=redis://[username]:[password]@[host]:[port]
REDIS_HOST=[host]
REDIS_PORT=[port]
REDIS_PASSWORD=[password]
REDIS_USERNAME=[username]
REDIS_DB=0
```

### ⚙️ **Configurações da API**
```
API_ENV=production
DEBUG=false
PORT=10000
```

## 🚨 **Segurança**

- ❌ **NUNCA** commitar credenciais no código
- ✅ **SEMPRE** usar variáveis de ambiente no painel do Render
- 🔄 **Trocar** credenciais se expostas acidentalmente

## 🧪 **Para desenvolvimento local**

Crie um arquivo `.env` (já no .gitignore):
```bash
cp .env.example .env
# Edite o .env com suas credenciais locais
``` 