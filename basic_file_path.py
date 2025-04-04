import os
import shutil
from implant_logging import logger

def is_cancel_command(command):
    '''Método que verifica se o comando é de cancelamento'''
    command = command.strip().lower()
    return command in ["cancelar", "-c"]

def basic_file_path():

    origin_path = str(input('Selecione o diretório de origem ("cancelar" ou "-c" para voltar): '))
    logger.info(f'O usuario definiu o diretório de origem: {origin_path}')
    
    if is_cancel_command(origin_path):
        print('Operação cancelada pelo usuário.')
        logger.info('O usuário cancelou a operação.')
        return None, None  # Retorna valores nulos para evitar erro
    
    # O código abaixo verifica se a pasta de origem existe
    if not os.path.exists(origin_path):
       print(f'Erro: O diretório "{origin_path}" não existe.')
       logger.info(f'O diretório de origem não existe: {origin_path}')
       return None, None

    # Aqui o usuário vai selecionar a pasta de destino
    destination_path = str(input('Selecione o diretório de destino ("cancelar" ou "-c" para voltar): '))
    logger.info(f'O usuário definiu o diretório de destino: {destination_path}')

    if is_cancel_command(destination_path):
        logger.info('O usuario cancelou a operação.')
        print('Operação cancelada pelo usuário.')
        return None, None
    
    # Verifica se o destino é diferente da origem
    if os.path.abspath(origin_path) == os.path.abspath(destination_path):
        print('Erro: O diretório de destino não pode ser o mesmo que o de origem.')
        logger.info('Erro: Diretórios idênticos')
        return None, None
    
    # Se a pasta de destino não existir ela é criada automaticamente
    os.makedirs(destination_path, exist_ok=True)
    
    # Muda para a pasta de origem
    os.chdir(origin_path)

    return origin_path, destination_path  # Retorna os caminhos