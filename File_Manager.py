import os
import shutil
import basic_file_path
from implant_logging import logger

class FileManager:
    def __init__(self):
        pass

    def __is_cancel_command(self, command):
        '''Método que verifica se o comando é de cancelamento'''
        command = command.strip().lower()
        return command in ["cancelar", "-c"]

    def __basic_file_path(self, origin_path, destination_path):
        
        
        # O código abaixo verifica se a pasta de origem existe
        if not os.path.exists(origin_path):
            print(f'Erro: O diretório "{origin_path}" não existe.')
            return
        
        # Verifica se o destino é diferente da origem
        if os.path.abspath(origin_path) == os.path.abspath(destination_path):
            print('Erro: O diretório de destino não pode ser o mesmo que o de origem.')
            return
        # Se a pasta de destino não existir ela é criada automaticamente
        os.makedirs(destination_path, exist_ok=True)   

    def move_all_files(self, origin_path, destination_path):
        if self._check_paths():
            files = os.listdir(origin_path)
            if not files:
                print('Erro ao mover: O diretório de origem está vazio!')
                logger.info(f'Erro ao mover: o diretório de origem está vazio: {origin_path}')
                return

            for file in files:
                self.move_file(file, origin_path, destination_path)

    def move_file(self, file, origin_path, destination_path):
        self.__basic_file_path(origin_path, destination_path)
        try:
            source = os.path.join(origin_path, file)
            destination = os.path.join(destination_path, file)

            if os.path.isfile(source):
                shutil.move(source, destination)
                print(f'Arquivo {file} movido com sucesso.')
                logger.info(f'Arquivo movido com sucesso: {file}')
            else:
                print(f'Erro: {file} não é um arquivo, pulando...')
                logger.info(f'Erro: não se trata de um arquivo: {file}')
        except Exception as e:
            print(f'Erro ao mover o arquivo "{file}": {str(e)}')
            logger.info(f'Erro ao mover o arquivo "{file}": {str(e)}')

    def _check_paths(self):
        if origin_path is None or destination_path is None:
            return False
        return True

    def list_files_in_origin_path(self, origin_path):
        return [f for f in os.listdir(origin_path) if os.path.isfile(f)]
    pass

if __name__ == '__main__':
    file_manager = FileManager()
    while True:
        print("\nEscolha uma opção:")
        print("1. Mover arquivos")
        print("2. Listar todos os arquivos.")
        print("3. Sair do programa")
        
        choice = input("Digite sua escolha (1 a 3): ")
        origin_path = str(input("Pasta de origem: "))
        if choice == "1":
            destination_path = str(input("Pasta de destino: "))
            file_manager.move_all_files(origin_path, destination_path)
        elif choice == "2":
            files = file_manager.list_files_in_origin_path(origin_path)
            print(files)
        elif choice == "3":
            print("Programa encerrado.")
            break
        else:
            print("Opção inválida!")
            