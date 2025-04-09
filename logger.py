import logging

class Logger:
    """Classe para configuração centralizada de logging."""

    LOG_FILE = 'app.log'  # Nome padrão do arquivo de log
    _configured = False  # Controle interno de configuração única

    def __init__(self, name=__name__):
        """
        Inicializa o objeto logger
        Parâmetros:
            name (str): Nome do logger (padrão: nome do módulo atual)
        """
        self.logger = logging.getLogger(name)
        
        # Configura o logging apenas na primeira instanciação
        if not Logger._configured:
            self._setup_logging()
            Logger._configured = True

    def _setup_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S', # Exibição da data e hora no formato sugerido em reunião
            handlers=[
                logging.FileHandler(self.LOG_FILE, encoding='utf-8'),
                logging.StreamHandler()
            ]
        )

    def info(self, message):
        """Registra mensagem informativa"""
        self.logger.info(message)

    def error(self, message):
        """Registra mensagem de erro"""
        self.logger.error(message)

    def exception(self, message):
        """Registra erro completo"""
        self.logger.exception(message)
 
# Exemplo de uso
if __name__ == "__main__":
    logger = Logger(__name__)
    logger.info("Servidor iniciado")
    try:
        1/0 
    except Exception as e:
        logger.error(f"Erro ao executar a operação")
        logger.exception(f"Erro inesperado: {str(e)}")