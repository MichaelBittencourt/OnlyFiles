import os
import shutil

def is_cancel_command(command):
    """Verifica se o comando é de cancelamento"""
    command = command.strip().lower()
    return command in ["cancelar", "-c"]

def move_files():
    # Aqui o usuário seleciona a pasta de origem
    origin_path = str(input('Selecione o diretório de origem ("cancelar" ou "-c" para voltar): '))
    
    if is_cancel_command(origin_path):
        print("Operação cancelada pelo usuário.")
        return
    
    # O código abaixo verifica se a pasta de origem existe
    if not os.path.exists(origin_path):
        print(f'Erro: O diretório "{origin_path}" não existe.')
        return 

    # Aqui o usuário vai selecionar a pasta de destino
    destination_path = str(input('Selecione o diretório de destino ("cancelar" ou "-c" para voltar): '))
    
    if is_cancel_command(destination_path):
        print("Operação cancelada pelo usuário.")
        return
    
    # Verifica se o destino é diferente da origem
    if os.path.abspath(origin_path) == os.path.abspath(destination_path):
        print("Erro: O diretório de destino não pode ser o mesmo que o de origem.")
        return
    
    # Se a pasta de destino não existir ela é criada automaticamente
    os.makedirs(destination_path, exist_ok=True)
    
    # Muda para a pasta de origem
    os.chdir(origin_path)
    
    # Move todos os arquivos da pasta de origem para a pasta de destino
    for file in os.listdir():
        try:
            source = os.path.join(origin_path, file)
            destination = os.path.join(destination_path, file)
            
            # Verifica se é um arquivo e não uma pasta em si
            if os.path.isfile(source):
                shutil.move(source, destination)
                print(f"Arquivo '{file}' movido com sucesso.")
            else:
                print(f"'{file}' não é um arquivo, pulando...")
                
        except Exception as e:
            print(f'Erro ao mover o arquivo "{file}": {str(e)}')

def move_selected_files():
    # Aqui o usuário seleciona a pasta de origem
    origin_path = str(input('Selecione o diretório de origem ("cancelar" ou "-c" para voltar): '))
    
    if is_cancel_command(origin_path):
        print("Operação cancelada pelo usuário.")
        return
    
    # Verifica se a pasta de origem existe
    if not os.path.exists(origin_path):
        print(f'Erro: O diretório "{origin_path}" não existe.')
        return 

    # Aqui o usuário vai selecionar a pasta de destino
    destination_path = str(input('Selecione o diretório de destino ("cancelar" ou "-c" para voltar): '))
    
    if is_cancel_command(destination_path):
        print("Operação cancelada pelo usuário.")
        return
    
    # Verifica se o destino é diferente da origem
    if os.path.abspath(origin_path) == os.path.abspath(destination_path):
        print("Erro: O diretório de destino não pode ser o mesmo que o de origem.")
        return
    
    # Se a pasta de destino não existir ela é criada automaticamente
    os.makedirs(destination_path, exist_ok=True)
    
    # Muda para a pasta de origem
    os.chdir(origin_path)
    
    # Lista todos os arquivos disponíveis
    print("\nArquivos disponíveis:")
    files = [f for f in os.listdir() if os.path.isfile(f)]
    for i, file in enumerate(files, 1):
        print(f"{i}. {file}")
    
    # Solicita ao usuário que selecione os arquivos
    print("\nDigite os números dos arquivos que deseja mover (separados por vírgula)")
    print("Exemplo: 1,3,5")
    print('Digite "cancelar" ou "-c" para voltar ao menu principal')
    selection = input("Selecione os arquivos: ")
    
    if is_cancel_command(selection):
        print("Operação cancelada pelo usuário.")
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
                    print(f"Arquivo '{file}' movido com sucesso.")
                except Exception as e:
                    print(f'Erro ao mover o arquivo "{file}": {str(e)}')
            else:
                print(f"Índice {index + 1} inválido.")
    except ValueError:
        print("Entrada inválida. Por favor, use números separados por vírgula.")

def move_by_extension():
    # Aqui o usuário vai selecionar a pasta de origem
    origin_path = str(input('Selecione o diretório de origem ("cancelar" ou "-c" para voltar): '))
    
    if is_cancel_command(origin_path):
        print("Operação cancelada pelo usuário.")
        return
    
    # Verifica se a pasta de origem existe
    if not os.path.exists(origin_path):
        print(f'Erro: O diretório "{origin_path}" não existe.')
        return 

    # Aqui o usuário vai selecionar a pasta de destino
    destination_path = str(input('Selecione o diretório de destino ("cancelar" ou "-c" para voltar): '))
    
    if is_cancel_command(destination_path):
        print("Operação cancelada pelo usuário.")
        return
    
    # Verifica se o destino é diferente da origem
    if os.path.abspath(origin_path) == os.path.abspath(destination_path):
        print("Erro: O diretório de destino não pode ser o mesmo que o de origem.")
        return
    
    # Se a pasta de destino não existir ela é criada automaticamente
    os.makedirs(destination_path, exist_ok=True)
    
    # Muda para a pasta de origem
    os.chdir(origin_path)
    
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
    
    if is_cancel_command(extension):
        print("Operação cancelada pelo usuário.")
        return
    
    # Adiciona o ponto à extensão se não estiver presente
    if not extension.startswith('.'):
        extension = '.' + extension
    
    # Filtra os arquivos pela extensão
    matching_files = [f for f in files if f.lower().endswith(extension)]
    
    if not matching_files:
        print(f"Nenhum arquivo com extensão {extension} encontrado.")
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