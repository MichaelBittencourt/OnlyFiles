import os
import shutil
from logger import Logger

class FileManager:

    def __init__(self, logger):
        self.__logger = logger

    def list_files(self, origin_path):
        return os.listdir(origin_path)

    def move_files_by_type(self, origin_path, destination_path, extensions_list):
        # Verifica se a pessoa colocou os paths das pastas
        if not origin_path or not destination_path:
            print("Erro: O caminho de origem ou destino está vazio!")

        # Verifica se a origem e o destino são a mesma coisa
        if os.path.abspath(origin_path) == os.path.abspath(destination_path):
            print("Erro: A pasta de destino não pode ser a mesma da origem.")

        # Lista todos os arquivos da origem
        files = self.list_files(origin_path)

        if not files:
            print("A pasta de origem está vazia!")
            return

        for file in files:
            path_file = os.path.join(origin_path, file)

            # Verifica se é um arquivo
            if os.path.isfile(path_file):
                # Pega a extensão do arquivo
                for ext in extensions_list:
                    if file.endswith(ext):
                        os.makedirs(destination_path, exist_ok=True)

                        # Move o arquivo
                        try:
                            shutil.move(path_file, os.path.join(destination_path, file))
                            self.__logger.info(f'Arquivo "{file}" movido para a pasta "{destination_path}".')
                        except Exception as erro:
                            self.__logger.error(f'Erro ao mover o file "{file}": {erro}')
                        break
            else:
                print(f'"{file}" não é um arquivo, ignorando.')
    pass

if __name__ == '__main__':
    file_manager = FileManager(Logger("FileManager"))

    types = {
        'Imagens': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.svg', '.webp'],
        'Documentos': ['.pdf', '.txt', '.docx', '.doc', '.xls', '.xlsx', '.ppt', '.pptx', '.odt'],
        'Músicas': ['.mp3', '.wav', '.aac', '.flac', '.ogg', '.m4a'],
        'Vídeos': ['.mp4', '.mkv', '.avi', '.mov', '.wmv', '.flv', '.webm'],
        }

    while True:
        print("\nEscolha uma opção:")
        print("1. Mover arquivos por tipo")
        print("2. Listar todos os arquivos")
        print("3. Sair do programa")

        choice = input("Digite sua escolha (1 a 3): ")
        origin_path = input("Pasta de origem: ")

        if choice == "1":
            destination_path = input("Pasta de destino: ")
            file_manager.move_files_by_type(origin_path, destination_path, types["Imagens"])

        elif choice == "2":
            files = file_manager.list_files(origin_path)
            print(files)

        elif choice == "3":
            print("Programa encerrado.")
            break

        else:
            print("Opção inválida!")
            