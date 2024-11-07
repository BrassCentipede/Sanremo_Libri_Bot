import telebot , os , time
from telebot import TeleBot
from pdfminer.high_level import extract_text



#1. Verirficare che il file sia effetivamente un file pdf 
class File:
    def __init__(self, file_path):
        self.file_path = file_path
        
    def is_pdf(self)->bool:
        try:
            extract_text(self.file_path) # questa funzione riesce a leggere solo i file pdf
            return True
        except:
            return False
        
    def is_redable(self):
        try:
            if os.access(self.file_path , os.R_OK):
                # Questa funzione non legge non risce ad avere a che fare con i file .md
                return True
        except:
            return False 
        
    def is_empty(self) ->bool:
        is_empty = os.path.getsize(self.file_path)
        return is_empty == 0
    

if __name__ == "__main__":
    
    dir = f"{os.getcwd()}/Src/Files/input_pdf_test"
    names = ["1A1.pdf"]
    
    for name in names:
        file_path = f"{dir}/{name}"
        print(file_path)
        file = File(file_path)
        print("ispdf2 : ", file.is_pdf() , "is_redable :", file.is_redable() )

