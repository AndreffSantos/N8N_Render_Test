from flask import Flask, request, jsonify
import json
import logging
from datetime import datetime

# =================================================================
# CONFIGURAÇÃO INICIAL
# =================================================================

app = Flask(__name__)

# Configuração de logging para ver as requisições no console
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Estrutura para armazenar os dados recebidos. 
# Em uma aplicação real, isso seria um banco de dados (PostgreSQL, MongoDB, etc.).
DATA_STORE = []

# =================================================================
# ENDPOINT DE INGESTÃO (WEBHOOK)
# =================================================================

@app.route('/webhook', methods=['POST'])
def handle_webhook():
    """
    Recebe requisições POST do webhook, extrai o JSON e armazena os dados.
    """
    try:
        # Tenta obter os dados em formato JSON
        data = request.json
        if data is None:
            # Caso a requisição não tenha Content-Type: application/json
            return jsonify({"status": "error", "message": "Nenhum dado JSON encontrado no corpo da requisição."}), 400

        # Adiciona metadados de ingestão
        ingestion_record = {
            "timestamp": datetime.now().isoformat(),
            "source_ip": request.remote_addr,
            "payload": data
        }

        # Armazena os dados no DATA_STORE
        DATA_STORE.append(ingestion_record)

        logging.info(f"Dados do webhook recebidos e armazenados: {json.dumps(data)}")

        return jsonify({
            "status": "success", 
            "message": "Dados do webhook processados com sucesso.",
            "record_id": len(DATA_STORE)
        }), 200

    except Exception as e:
        # Tratamento de erros gerais
        logging.error(f"Erro ao processar webhook: {e}")
        return jsonify({"status": "error", "message": f"Erro interno do servidor: {str(e)}"}), 500

# =================================================================
# ENDPOINT DE CONSULTA PÚBLICA
# =================================================================

@app.route('/data', methods=['GET'])
def get_all_data():
    """
    Endpoint público para consultar todos os dados armazenados.
    """
    try:
        if not DATA_STORE:
            return jsonify({"status": "info", "message": "Nenhum dado armazenado ainda."}), 200

        # Retorna todos os dados armazenados em formato JSON
        logging.info(f"Requisição de consulta de dados atendida. Total de {len(DATA_STORE)} registros.")
        return jsonify({
            "status": "success",
            "count": len(DATA_STORE),
            "data": DATA_STORE
        }), 200
        
    except Exception as e:
        logging.error(f"Erro ao consultar dados: {e}")
        return jsonify({"status": "error", "message": "Erro ao recuperar dados."}), 500


# =================================================================
# EXECUÇÃO DO SERVIÇO
# =================================================================

if __name__ == '__main__':
    # Define o host como '0.0.0.0' para que o servidor seja acessível 
    # externamente (não apenas do localhost)
    print("Iniciando serviço web...")
    print("Endpoint Webhook (POST): http://127.0.0.1:5000/webhook")
    print("Endpoint Consulta (GET): http://127.0.0.1:5000/data")
    app.run(host='0.0.0.0', port=5000)