# Usa a imagem oficial do Python 3.11 (versão slim para ser mais leve, ~130MB)
FROM python:3.11-slim

# Define o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copia APENAS o requirements.txt primeiro (Estratégia de Cache do Bloco 9)
COPY requirements.txt .

# Instala as dependências sem guardar cache inútil na imagem
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante do código da aplicação
COPY . .

# Documenta que a API roda na porta 8000
EXPOSE 8000

# Comando para iniciar o servidor (O --host 0.0.0.0 é obrigatório no Docker)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]