import os
import glob
from tkinter import Tk
from tkinter.filedialog import askdirectory
from PyPDF2 import PdfFileMerger


class files:
    def __init__(self):
        self.path = self.get_folder_path()

    def get_folder_path(self):
        Tk().withdraw()
        path = askdirectory()
        path = path.replace("/","\\")
        
        return path

    def get_pdf_file_names(self):
        os.chdir(self.path)
        
        files = []

        for file in glob.glob("*.pdf"):
            files.append(file)
        
        return files

    def merge_pdfs(self, file_names, merged_file_name):
        merger = PdfFileMerger()
        [merger.append(pdf) for pdf in file_names]
        with open(merged_file_name+".pdf", "wb") as new_file:
            merger.write(new_file)
        
#pyinstaller --onefile --windowed application.py