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

@app.route('/', methods=['POST'])
def handle_webhook():
    """
    Recebe requisições POST, imprime o conteúdo e retorna sucesso.
    """
    try:
        # Tenta obter o corpo da requisição como JSON
        data = request.json
        
        # Se não for JSON, tenta pegar o corpo como texto
        if data is None:
            data = request.get_data(as_text=True)
            logging.info(f"Webhook recebido (Formato não JSON, Texto Bruto): {data[:100]}...")
            
        else:
            # Se for JSON, imprime de forma formatada
            logging.info("--- DADOS DO WEBHOOK RECEBIDOS ---")
            logging.info(f"Origem IP: {request.remote_addr}")
            logging.info(f"Conteúdo: \n{json.dumps(data, indent=4)}")
            logging.info("----------------------------------")        
    
        # Resposta de sucesso (status 200) para o sistema de origem
        return jsonify({"status": "success", "message": "Dados recebidos e processados.", "content": request}), 200

    except Exception as e:
        # Tratamento de erro caso algo dê errado no processamento
        logging.error(f"Erro ao processar webhook: {e}")
        return jsonify({"status": "error", "message": f"Erro interno do servidor: {str(e)}"}), 500

# =================================================================
# ENDPOINT DE CONSULTA PÚBLICA
# =================================================================

@app.route('/test', methods=['GET'])
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