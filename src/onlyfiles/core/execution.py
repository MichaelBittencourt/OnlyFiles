import os
from logger import Logger
from File_Manager import FileManager
from file_types import file_types

class Execution:
    """Class that executes and organizes the FileManager class"""

    def __init__(self, logger):
        self.__logger = logger
        self.__filemanager = FileManager(self.__logger)
        self.__types = file_types

    def __organize_by_type(self, origin_path, category):
        """Private method to centralize organization logic by type"""
        destination = os.path.join(origin_path, category)
        if category == 'Others':
            self.__filemanager.move_other_files(origin_path, destination, self.__types)
        else:
            self.__filemanager.move_files_by_type(origin_path, destination, self.__types[category])

    def organize_music(self, origin_path):
        self.__organize_by_type(origin_path, 'Music')

    def organize_images(self, origin_path):
        self.__organize_by_type(origin_path, 'Images')

    def organize_documents(self, origin_path):
        self.__organize_by_type(origin_path, 'Documents')

    def organize_videos(self, origin_path):
        self.__organize_by_type(origin_path, 'Videos')

    def organize_others(self, origin_path):
        self.__organize_by_type(origin_path, 'Others')

    def organize_all(self, origin_path):
        """Organize all file types"""
        for category in self.__types.keys():
            self.__organize_by_type(origin_path, category)

if __name__ == '__main__':
    verbose = input('Enable movement operations ("Y for yes" or "N for no": ')

    if verbose == "Y":
        verbose = True
    else:
        verbose = False

    execution = Execution(Logger("Execution", verbose))

    while True:
        print("\nSelection menu:")
        print("1. Organize music")
        print("2. Organize images")
        print("3. Organize documents")
        print("4. Organize videos")
        print("5. Organize others")
        print("6. Organize all types")
        print("7. Exit program")

        option = input("Choose an option (1 to 7): ")

        if option == "7":
            print("Exiting program.")
            break

        origin_path = input("Source folder: ")

        if option == "1":
            execution.organize_music(origin_path)
        elif option == "2":
            execution.organize_images(origin_path)
        elif option == "3":
            execution.organize_documents(origin_path)
        elif option == "4":
            execution.organize_videos(origin_path)
        elif option == "5":
            execution.organize_others(origin_path)
        elif option == "6":
            execution.organize_all(origin_path)
        else:
            print("Invalid option!")