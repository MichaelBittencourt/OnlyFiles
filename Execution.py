import os
import shutil
from logger import Logger
from File_Manager import FileManager

class Execution():
    """Classe que executa e organiza a classe FileManager"""

    def __init__(self, logger):
        self.__logger = logger
        self.__filemanager = FileManager(self.__logger)

        self.__types = {
            'Imagens': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.svg', '.webp'],
            'Documentos': ['.pdf', '.txt', '.docx', '.doc', '.xls', '.xlsx', '.ppt', '.pptx', '.odt'],
            'Músicas': ['.mp3', '.wav', '.aac', '.flac', '.ogg', '.m4a'],
            'Vídeos': ['.mp4', '.mkv', '.avi', '.mov', '.wmv', '.flv', '.webm'],
        }

    def organize_music(self, origin_path):

       destination = os.path.join(origin_path, "Músicas")
       self.__filemanager.move_files_by_type(origin_path, destination, self.__types["Músicas"])

    def organize_images(self, origin_path):

        destination = os.path.join(origin_path, "Imagens")
        self.__filemanager.move_files_by_type(origin_path, destination, self.__types["Imagens"])

    def organize_documents(self, origin_path):

       destination = os.path.join(origin_path, "Documentos")
       self.__filemanager.move_files_by_type(origin_path, destination, self.__types["Documentos"])

    def organize_videos(self, origin_path):

       destination = os.path.join(origin_path, "Vídeos")
       self.__filemanager.move_files_by_type(origin_path, destination, self.__types["Vídeos"])

    def organize_all(self, origin_path):
        """Organiza todos os tipos (músicas, imagens, documentos e vídeos) de uma vez"""

        self.organize_music(origin_path)
        self.organize_images(origin_path)
        self.organize_documents(origin_path)
        self.organize_videos(origin_path)


if __name__ == '__main__':

    verbose = input('Ativar operações de movimentação ("S para sim" ou "N para não": ')

    if verbose == "S":
        verbose = True
    else:
        verbose = False

    execution = Execution(Logger("Execution", verbose))

    while True:
        print("\nMenu de seleção:")
        print("1. Organizar músicas")
        print("2. Organizar imagens")
        print("3. Organizar documentos")
        print("4. Organizar vídeos")
        print("5. Organizar todos os tipos de arquivos")
        print("6. Sair do programa")

        option = input("Escolha uma opção (1 a 6): ")

        if option == "6":
            print("Encerrando programa.")
            break

        origin_path = input("Pasta de origem: ")

        if option == "1":
            execution.organize_music(origin_path)
        elif option == "2":
            execution.organize_images(origin_path)
        elif option == "3":
            execution.organize_documents(origin_path)
        elif option == "4":
            execution.organize_videos(origin_path)
        elif option == "5":
            execution.organize_all(origin_path)
        else:
            print("Opção inválida!")