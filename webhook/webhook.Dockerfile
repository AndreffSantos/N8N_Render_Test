# Use uma imagem base Python leve
FROM ghcr.io/astral-sh/uv:debian

# Define o diretório de trabalho no container
WORKDIR /app

# Copia e instala as dependências
# O arquivo 'requirements.txt' precisa estar no mesmo diretório
COPY pyproject.toml .
RUN uv sync
# RUN pip install --no-cache-dir -r requirements.txt

# Copia o código da sua aplicação Flask
# O arquivo 'webhook_api.py' precisa estar no mesmo diretório
COPY main.py .

# O Flask roda na porta 5000 por padrão, mas o Render injeta a porta 
# através da variável de ambiente $PORT. O código em 'webhook_api.py' 
# já está configurado para usar 5000.

# Comando para iniciar o servidor Gunicorn (melhor para produção) ou o Flask
# Usaremos o CMD simples com Python, como definido no seu script.
CMD ["uv", "run", "main.py"]