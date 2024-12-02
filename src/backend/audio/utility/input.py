import os, mido

class FileHandling:

    def inputPath() -> str:
        # declare
        filepath = ""

        # input file path
        filepath = input()

        if FileHandling.isExist(filepath) and FileHandling.isFolder(filepath) and not FileHandling.hasIllegalCharacters(filepath):
            # output
            return filepath

        # output
        return None
    
    def isExist(path_folder):
        # Cek apakah path ada
        if not os.path.exists(path_folder):
            return False

    def isFolder(path_folder):
        # Cek apakah path adalah folder
        if not os.path.isdir(path_folder):
            return False
    

    def hasIllegalCharacters(path_folder):
        illegal_chars = r'<>:"/\|?*'
        for char in illegal_chars:
            if char in path_folder:
                return False
        return True
