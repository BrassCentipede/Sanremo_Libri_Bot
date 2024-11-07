from Backend.Data.get_pdf_data import Pdf_Dataframe
from Backend.Create_Files.create_pdf import to_Pdf
from Backend.Create_Files.create_ods import to_Ods
from Backend import Data

class Main():
    
    def __init__(self , file_path)->None:
        self.file_path = file_path

        self.dataframe = Pdf_Dataframe(file_path)
        self.df = self.dataframe.get_dataframe(columns=[1, 0, 3 , 5, 6])
        self.data_matrix = self.dataframe.dataframe_to_matrix(self.df)
        
        #DATI DELLA SCUOLA -> FA SCHIFO AL CAZZO QUESTO CODICE DA MIGLIORARE PER FORZA
        school_data = self.dataframe.get_school_data()
        #lista con i dati della scuola 
        self.dati_scuola =["Scuola" , f"{school_data[1]}" , f"{school_data[0]}" , "" , ""]
        
        self.columns_names = ["Codice Volume","Materia / Disciplina" , "Titolo / Sottotitolo",  "Editore", "Prezzo" , "Deve" , "Pagato" , "Magazzino" , "ORD" , "ARR" , "CONSE"]

        
    def create_pdf(self, file_name:str , personal_data:list , acconto:str , buono_usato:str):
        
        dati_acconto =["Acconco" , "" , acconto.title() , "" , ""]
        dati_buono_usato=["Buono Usato" , "" , buono_usato.title() , "" , ""]        
        #larghezze delle celle 
        widths = [25, 35, 73, 40, 14, 14, 14, 14, 14, 14, 14]
        #altezza della cella 
        row_height = 15
        
        #PDF
        #file pdf che creo 
        pdf_1 = to_Pdf()
        pdf = pdf_1.create_pdf() # creo il pdf
        #aggiungo i dati personali 
        pdf_1.add_row_with_empy_cels([f"{personal_data[0]}" , f"{personal_data[1].title()}" , f"{personal_data[2].title() + " " + personal_data[3].title()}" , "" , "" ] , widths , pdf , row_height)
        # aggiungo i dati della scuola 
        pdf_1.add_row_with_empy_cels(self.dati_scuola , widths , pdf , row_height)

        pdf_1.add_row_with_empy_cels(dati_acconto , widths , pdf , row_height)
        pdf_1.add_row_with_empy_cels(dati_buono_usato , widths , pdf , row_height)
        
        # aggiungo il nome delle colone
        pdf_1.add_column_names(pdf , self.columns_names , widths , row_height)
        # PARTE PIU IMPORTANTE AGGIUNGO I DATI DEI LIBRI
        
        
        for row in self.data_matrix:
            pdf_1.add_particular_row_books_data(row , widths, pdf , row_height)
            
        path = f"/Users/andreitarlev/Documents/Informatica/Progetti/AdvanceProjects/Scolastica/Src/Files/output_pdf/{file_name}.pdf"
        # salvo il pdf 
        pdf.output(path)
        
        return path
    
    
    def create_ods(self , file_name:str , personal_data:list , acconto , buono_usato):
        dati_acconto =["Acconco" , "" , acconto.title() , "" , ""]
        dati_buono_usato=["Buono Usato" , "" , buono_usato.title() , "" , ""]  
        
        # Lavoro sulle delle copie necessarie per il file ods
            
        arra_data_prox = self.data_matrix[:] # così creo una copia profonda dell'array 
        personal_data_copy = personal_data[:]
        dati_scuola_copy = self.dati_scuola[:] # crea una copia profonda anche qua perciò meglio usare questo metodo
        dati_accont_copy = dati_acconto[:]
        dati_buono_usato_copy = dati_buono_usato[:]
        
        for _ in range(6):
            dati_scuola_copy.append("")
            
        for _ in range(8):
            personal_data_copy.append("")
        
        for _ in range(6):
            dati_accont_copy.append("")
            dati_buono_usato_copy.append("")
        
        for array in arra_data_prox:
            for _ in range(6):
                array.append("")

        #creazione del file ods  e aggiunta dei dati nel file 
        ods_file = to_Ods(arra_data_prox)
        ods_file.create_spread_sheet()
        ods_file.style_the_spreadshet()
        ods_file.add_data(personal_data_copy)
        ods_file.add_data(dati_scuola_copy)
        ods_file.add_data(dati_accont_copy)
        ods_file.add_data(dati_buono_usato_copy)
        ods_file.add_data(self.columns_names)
        ods_file.add_books_data()
        ods_file.add_table_to_spreadsheet()
        path = f"/Users/andreitarlev/Documents/Informatica/Progetti/AdvanceProjects/Scolastica/Src/Files/output_ods/"
        ods_file.save_ods(path , file_name)
        return path + file_name + ".ods"
    
if __name__ == "__main__":
    
    Main().main(file_path="Src/Files/input_pdf_test/LISTA_LIBRI_GOBETTI_2024-25_1.pdf" , file_name="2CL" ,personal_data=[ "28/02/2034" , "3807991129" ,"Andrei Tarlev"])
    
    