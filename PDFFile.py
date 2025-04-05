from pathlib import Path

class PDFFile():
    def __init__(self, path, name):
        self.path = path
        self.name = name

    def getName(self):
        return self.name

    def getPath(self):
        return self.path

    def setName(self, file_name):
        self.name = file_name

    def setPath(self, file_path):
        self.path = file_path

    def setFile(self, file_name, file_path):
        self.setName(file_name)
        self.setPath(file_path)

    def setFile(self, file):
        file_info = Path(file)
        self.setPath(file_info)
        self.setName(file_info.name)

    def is_chosen(self):
        if self.path is None or self.name is None:
            self.setFile(None, None)
            return False
        return True

    def __str__(self):
        return f"{self.name}"