# Instruções de Deploy - Render.com

## Variáveis de Ambiente para Configurar no Render

### 1. MongoDB (Já configurado)
```
MONGODB_URL=mongodb+srv://projeto5mlet:projetofiap@apiembrapa.wcmp3fv.mongodb.net/?retryWrites=true&w=majority&appName=apiEmbrapa
```

### 2. Redis (Já configurado)
```
REDIS_URL=redis://default:sua_senha@redis-15186.c263.us-east-1-2.ec2.redns.redis-cloud.com:15186
```
**Nota:** Substitua `sua_senha` pela senha real que você obteve no Redis Cloud.

### 3. JWT (Gere uma chave segura)
```
JWT_SECRET_KEY=sua_chave_super_secreta_aqui_123456789
```

### 4. Configurações de Ambiente
```
API_ENV=production
DEBUG=false
```

## Passos para Deploy no Render

1. **Conectar repositório:**
   - Acesse render.com
   - Clique em "New +" → "Web Service"
   - Conecte seu repositório GitHub

2. **Configurar Build:**
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

3. **Adicionar Variáveis de Ambiente:**
   - Vá para a aba "Environment"
   - Adicione todas as variáveis listadas acima

4. **Deploy:**
   - Clique em "Create Web Service"
   - Aguarde o deploy (pode levar alguns minutos)

## Verificações Pós-Deploy

1. **Health Check:** `https://seu-app.onrender.com/health`
2. **Documentação:** `https://seu-app.onrender.com/docs`
3. **Teste de Autenticação:** `https://seu-app.onrender.com/auth/signup`

## Configuração do Redis Cloud ✅ CONCLUÍDO

Seu Redis já está configurado:
- **Endpoint**: redis-15186.c263.us-east-1-2.ec2.redns.redis-cloud.com:15186
- **Database**: database-MBFUY8K3

## Troubleshooting

- Se der erro de build, verifique se requirements.txt está correto
- Se a aplicação não iniciar, verifique as variáveis de ambiente
- Use os logs do Render para debug 