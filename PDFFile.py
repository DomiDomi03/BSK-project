##
#	@file PDFFile.py
#	@details File to handle PDF operations
#	@date 20-04-2025
##
from pathlib import Path


## A class that handles basic operations and metadata related to PDF files.
class PDFFile():
    ## Initial method of a PDFFile class.
    # @param path the path of pdf file
    # @param name the name of pdf file
    def __init__(self, path, name):
        self.path = path
        self.name = name

    ## File name getter
    # @return the name of file
    def getName(self):
        return self.name

    ## File path getter
    # @return the path of file
    def getPath(self):
        return self.path

    ## Method that sets the file name
    def setName(self, file_name):
        self.name = file_name

    ## Method that sets the file path
    def setPath(self, file_path):
        self.path = file_path

    ## Method that sets the name and path of the file
    # @param file_name the name of file to set the name to
    # @param file_path the path of file to set the path to
    def setFile(self, file_name, file_path):
        self.setName(file_name)
        self.setPath(file_path)

    ## Method that sets the name and path of the file
    # @param file the file's full path
    def setFile(self, file):
        file_info = Path(file)
        self.setPath(file_info)
        self.setName(file_info.name)

    ## Method that check if the file is set
    # @return True if the file is set
    # @return False if it is not.
    def is_chosen(self):
        if self.path is None or self.name is None:
            self.setFile(None, None)
            return False
        return True

    ## Method that returns the string of file name
    # @return string file name
    def __str__(self):
        return f"{self.name}"