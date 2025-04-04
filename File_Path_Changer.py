import os
import shutil
import basic_file_path
from implant_logging import logger

def move_files():
    '''Método que move todos os arquivos da pasta de origem'''

    origin_path, destination_path = basic_file_path.basic_file_path()
    
    if origin_path is None or destination_path is None:
        return  # Se o usuário cancelar, sai da função

        # Lista os arquivos na pasta de origem
    files = os.listdir(origin_path)

    # Se a pasta estiver vazia, exibe um aviso e retorna ao menu
    if not files:
        print('Erro ao mover: O diretório de origem está vazio!')
        logger.info(f'Erro ao mover: o diretório de origem está vazio: {origin_path}')
        return
    
    # Move todos os arquivos da pasta de origem para a pasta de destino
    for file in os.listdir(origin_path):
        try:
            source = os.path.join(origin_path, file)
            destination = os.path.join(destination_path, file)
        
            # Verifica se é um arquivo e não uma pasta em si
            if os.path.isfile(source):
                shutil.move(source, destination)
                print(f'Arquivo {file} movido com sucesso.')
                logger.info(f'Arquivo movido com sucesso: {file}')
            else:
                print(f'Erro: {file} não é um arquivo, pulando...')
                logger.info(f'Erro: não se trata de um arquivo: {file}')
            
        except Exception as e:
            print(f'Erro ao mover o arquivo "{file}": {str(e)}')
            logger.info(f'Erro: não se trata de um arquivo: {file}')

def move_selected_files():
    '''Método que move da pasta de origem apenas arquivos selecionados'''

    origin_path, destination_path = basic_file_path.basic_file_path()
    
    # Lista todos os arquivos disponíveis
    print('\nArquivos disponíveis:')
    files = [f for f in os.listdir() if os.path.isfile(f)]
    for i, file in enumerate(files, 1):
        print(f'{i}. {file}')

    # Solicita ao usuário que selecione os arquivos
    print('\nDigite os números dos arquivos que deseja mover (separados por vírgula)')
    print('Exemplo: 1,3,5')
    print('Digite "cancelar" ou "-c" para voltar ao menu principal')
    selection = input('Selecione os arquivos: ')
    logger.info('O usuário selecionou os arquivos que serão movidos.')

    if basic_file_path.is_cancel_command(selection):
        print('Operação cancelada pelo usuário.')
        logger.info('O usuário cancelou a operação.')
        return

    try:
        # Converte a seleção em uma lista de índices
        selected_indices = [int(x.strip()) - 1 for x in selection.split(',')]
    
        # Move apenas os arquivos selecionados
        for index in selected_indices:
            if 0 <= index < len(files):
                file = files[index]
                try:
                    source = os.path.join(origin_path, file)
                    destination = os.path.join(destination_path, file)
                    shutil.move(source, destination)
                    print(f'Arquivo {file} movido com sucesso.')
                    logger.info(f'Arquivo movido com sucesso: {file}')
                except Exception as e:
                    print(f'Erro ao mover o arquivo "{file}": {str(e)}')
                    logger.info(f'Erro: não se trata de um arquivo: {file}')
            else:
                print(f'Índice {index + 1} inválido.')
                logger.info('Erro: índice do arquivo inválido')
    except ValueError:
        print('Entrada inválida. Por favor, use números separados por vírgula.')
        logger.info('O usuário forneceu uma entrada inválida.')

def move_by_extension():
    '''Método que move os arquivos da pasta de origem baseado em sua extensão'''

    origin_path, destination_path = basic_file_path.basic_file_path()
    
    # Lista todos os arquivos disponíveis
    print("\nArquivos disponíveis:")
    files = [f for f in os.listdir() if os.path.isfile(f)]
    for i, file in enumerate(files, 1):
        print(f"{i}. {file}")

    # Solicita ao usuário que selecione o formato dos arquivos
    print("\nDigite a extensão dos arquivos que deseja mover (sem o ponto)")
    print("Exemplo: pdf, jpg, docx")
    print('Digite "cancelar" ou "-c" para voltar ao menu principal')
    extension = input("Digite a extensão: ").lower()
    logger.info('O usuário forneceu forneceu a extensão dos arquivos que deseja mover.')

    if basic_file_path.is_cancel_command(extension):
        print("Operação cancelada pelo usuário.")
        logger.info('O usuário cancelou a operação.')
        return

    # Adiciona o ponto à extensão se não estiver presente
    if not extension.startswith('.'):
        extension = '.' + extension

    # Filtra os arquivos pela extensão
    matching_files = [f for f in files if f.lower().endswith(extension)]

    if not matching_files:
        print(f'Nenhum arquivo com extensão {extension} encontrado.')
        logger.info('Nenhum arquivo com extensão válida foi encontrado durante a operação.')
        return

    print(f"\nEncontrados {len(matching_files)} arquivos com extensão {extension}")
    print("Arquivos que serão movidos:")
    for file in matching_files:
        print(f"- {file}")

    # Confirma a operação
    confirm = input("\nDeseja mover estes arquivos? (s/n): ").lower()
    if confirm != 's':
        print("Operação cancelada pelo usuário.")
        logger.info('O usuário cancelou a operação.')
        return

    # Move os arquivos
    for file in matching_files:
        try:
            source = os.path.join(origin_path, file)
            destination = os.path.join(destination_path, file)
            shutil.move(source, destination)
            print(f"Arquivo '{file}' movido com sucesso.")
            logger.info(f'Arquivo movido com sucesso: {file}')
        except Exception as e:
            print(f'Erro ao mover o arquivo "{file}": {str(e)}')

def view_log_history():
    '''Método que exibe o histórico de movimentações armazenado no log'''
    
    log_file = "app.log"  # Nome do arquivo de log (ajuste conforme necessário)

    try:
        # Tenta abrir e ler o arquivo de log
        with open(log_file, "r", encoding="utf-8") as f:
            log_content = f.readlines()

        if not log_content:
            print("\nHistórico de operações está vazio.\n")
            return

        print("\n=== Histórico de Operações ===\n")
        for line in log_content:
            print(line.strip())  # Remove espaços extras
        print("\n=== Fim do Histórico ===\n")

    except FileNotFoundError:
        print("\nNenhum histórico encontrado. O log ainda não foi gerado.\n")

def clear_log_history():
    '''Método que apaga o histórico de movimentações (conteúdo do log) caso o usuário deseje'''

    log_file = "app.log"  # mesmo nome usado pelo logger

    if not os.path.exists(log_file):
        print("\nNenhum histórico encontrado para limpar.\n")
        return

    # Confirmação do usuário
    confirm = input("Tem certeza que deseja limpar todo o histórico? (s/n): ").strip().lower()
    if confirm == 's':
        try:
            open(log_file, "w").close()  # Abre o arquivo em modo escrita e limpa
            print("\nHistórico de operações limpo com sucesso.\n")
        except Exception as e:
            print(f"\nErro ao limpar o histórico: {str(e)}\n")
    else:
        print("\nOperação cancelada. O histórico não foi alterado.\n")



if __name__ == '__main__':
    while True:
        print("\nEscolha uma opção:")
        print("1. Mover todos os arquivos")
        print("2. Mover arquivos selecionados")
        print("3. Mover arquivos por extensão")
        print("4. Visualizar histórico de operações")
        print("5. Limpar histórico de operações")
        print("6. Sair do programa")
        
        choice = input("Digite sua escolha (1 a 6): ")
        
        if choice == "1":
            move_files()
        elif choice == "2":
            move_selected_files()
        elif choice == "3":
            move_by_extension()
        elif choice == "4":
            view_log_history()
        elif choice == "5":
            clear_log_history()
        elif choice == "6":
            print("Programa encerrado.")
            break
        else:
            print("Opção inválida!")