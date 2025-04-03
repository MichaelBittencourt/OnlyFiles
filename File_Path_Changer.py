import os
import shutil
from implant_logging import logger
from Basic_File_Path import basic_file_path

def is_cancel_command(command):
    '''Método que verifica se o comando é de cancelamento'''
    command = command.strip().lower()
    return command in ["cancelar", "-c"]

def move_files():
    '''Método que seleciona a pasta de origem'''

    basic_file_path()
    
    # Move todos os arquivos da pasta de origem para a pasta de destino
    for file in os.listdir():
        try:
            source = os.path.join(origin_path, file)
            destination = os.path.join(destination_path, file)
            #logger.info(f'O usuário moveu todos os arquivos de {origin_path} à pasta de destino.')
        
            # Verifica se é um arquivo e não uma pasta em si
            if os.path.isfile(source):
                shutil.move(source, destination)
                print(f'Arquivo {file} movido com sucesso.')
                #logger.info(f'O arquivo {file} foi movido com sucesso.')
            else:
                print(f'Erro: {file} não é um arquivo, pulando...')
                #logger.info(f'Erro: {file} não é um arquivo.')
            
        except Exception as e:
            print(f'Erro ao mover o arquivo "{file}": {str(e)}')
            #logger.info(f'Erro ao mover, {file} não é um arquivo.')

def move_selected_files():
    '''Método que também seleciona a pasta de origem'''

    basic_file_path()
    
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
    #logger.info('O usuário selecionou os arquivos.')

    if is_cancel_command(selection):
        print('Operação cancelada pelo usuário.')
        #logger.info('O usuário cancelou a operação.')
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
                    #logger.info(f'O arquivo {file} foi movido com sucesso')
                except Exception as e:
                    print(f'Erro ao mover o arquivo "{file}": {str(e)}')
                    #logger.info(f'Erro ao mover, {file} não é um arquivo.')
            else:
                print(f'Índice {index + 1} inválido.')
                #logger.info(f'Erro: índice do arquivo inválido')
    except ValueError:
        print('Entrada inválida. Por favor, use números separados por vírgula.')
        #logger.info(f'O usuário forneceu uma entrada inválida.')

def move_by_extension():
    '''Método que move os arquivos baseado em sua extensão'''

    basic_file_path()
    
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
    #logger.info(f'O usuário forneceu forneceu a extensão dos arquivos que deseja mover.')

    if is_cancel_command(extension):
        print("Operação cancelada pelo usuário.")
        #logger.info(f'O usuário cancelou a operação.')
        return

    # Adiciona o ponto à extensão se não estiver presente
    if not extension.startswith('.'):
        extension = '.' + extension

    # Filtra os arquivos pela extensão
    matching_files = [f for f in files if f.lower().endswith(extension)]

    if not matching_files:
        print(f"Nenhum arquivo com extensão {extension} encontrado.")
        #logger.info(f'Nenhum arquivo com extensão foi encontrado durante a operação.')
        return

    print(f"\nEncontrados {len(matching_files)} arquivos com extensão {extension}")
    print("Arquivos que serão movidos:")
    for file in matching_files:
        print(f"- {file}")

    # Confirma a operação
    confirm = input("\nDeseja mover estes arquivos? (s/n): ").lower()
    if confirm != 's':
        print("Operação cancelada pelo usuário.")
        return

    # Move os arquivos
    for file in matching_files:
        try:
            source = os.path.join(origin_path, file)
            destination = os.path.join(destination_path, file)
            shutil.move(source, destination)
            print(f"Arquivo '{file}' movido com sucesso.")
        except Exception as e:
            print(f'Erro ao mover o arquivo "{file}": {str(e)}')



if __name__ == '__main__':
    while True:
        print("\nEscolha uma opção:")
        print("1. Mover todos os arquivos")
        print("2. Mover arquivos selecionados")
        print("3. Mover arquivos por extensão")
        print("4. Sair do programa")
        
        choice = input("Digite sua escolha (1, 2, 3 ou 4): ")
        
        if choice == "1":
            move_files()
        elif choice == "2":
            move_selected_files()
        elif choice == "3":
            move_by_extension()
        elif choice == "4":
            print("Programa encerrado.")
            break
        else:
            print("Opção inválida!")