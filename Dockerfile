# ─── ESTÁGIO 1: Builder (Onde compilamos as dependências) ───
FROM python:3.11-slim as builder
WORKDIR /app
COPY requirements.txt .
# Instala as dependências numa pasta local do utilizador para facilitar a cópia
RUN pip install --user --no-cache-dir -r requirements.txt

# ─── ESTÁGIO 2: Produção (Imagem final super leve e segura) ───
FROM python:3.11-slim
WORKDIR /app

# Criar um utilizador não-root (Exigência do Bloco 12)
RUN useradd -m -s /bin/bash appuser

# Copiar as bibliotecas instaladas no estágio 1
COPY --from=builder /root/.local /home/appuser/.local

# Copiar o código da aplicação
COPY . .

# Dar permissão ao novo utilizador sobre os ficheiros
RUN chown -R appuser:appuser /app

# Trocar para o utilizador não-root
USER appuser

# Garantir que o binário do Uvicorn e outras libs estão no PATH
ENV PATH=/home/appuser/.local/bin:$PATH

EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]