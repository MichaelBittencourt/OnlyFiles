import os
import shutil
from implant_logging import logger

def basic_file_path():

    origin_path = str(input('Selecione o diretório de origem ("cancelar" ou "-c" para voltar): '))
    logger.info('O usuario definiu o diretório de origem:', origin_path)
    
    if is_cancel_command(origin_path):
        logger.info('O usuário cancelou a operação.')
        print('Operação cancelada pelo usuário.')
        return
    
    # O código abaixo verifica se a pasta de origem existe
    if not os.path.exists(origin_path):
        logger.info('O diretório de origem não existe.')
        print(f'Erro: O diretório "{origin_path}" não existe.')
        return 

    # Aqui o usuário vai selecionar a pasta de destino
    destination_path = str(input('Selecione o diretório de destino ("cancelar" ou "-c" para voltar): '))
    logger.info('O usuário selecionou a pasta de destino.')

    if is_cancel_command(destination_path):
        logger.info('O usuario cancelou a operação.')
        print('Operação cancelada pelo usuário.')
        return
    
    # Verifica se o destino é diferente da origem
    if os.path.abspath(origin_path) == os.path.abspath(destination_path):
        logger.info('Erro: Diretórios idênticos')
        print('Erro: O diretório de destino não pode ser o mesmo que o de origem.')
        return
    
    # Se a pasta de destino não existir ela é criada automaticamente
    os.makedirs(destination_path, exist_ok=True)
    logger.info('A pasta de destino foi criada:', destination_path)
    
    # Muda para a pasta de origem
    os.chdir(origin_path)
    logger.info('O diretório de trabalho atual foi mudado para o de origem:', origin_path)