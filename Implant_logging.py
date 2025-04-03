import logging

LOG_FILE = 'app.log'

def setup_logging():
    """Configuração do sistema de logging"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(LOG_FILE, encoding='utf-8'),  # Adicionado encoding
            logging.StreamHandler()
        ]
    )

# Configura o logging
setup_logging()

# Obtém o logger
logger = logging.getLogger(__name__)


'''exemplo de uso, não entra no código
# Exemplo de uso
logger.info("Servidor iniciado")

try:
    1/0  # Exemplo que gera erro
except Exception as e:
    logger.exception(f"Erro inesperado: {str(e)}")'''