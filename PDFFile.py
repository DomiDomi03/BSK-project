class PDFFile():
    def __init__(self, path, name):
        self.path = path
        self.name = name

    def getName(self):
        return self.name

    def getPath(self):
        return self.path

    def __str__(self):
        return f"{self.pdf_name}"