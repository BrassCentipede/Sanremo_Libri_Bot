from fpdf import FPDF

class to_Pdf:    
    def __personal_data(self , name , phone_number , date) -> list:
        personal_data = [name , phone_number , date]
        return personal_data
    
    def add_row(self , data , widths , pdf , row_height):
        for i , datum in enumerate(data):
            pdf.cell(widths[i] , row_height , datum , border=1 )
        return True
            
    def add_row_with_empy_cels(self , data , widths , pdf , row_height):
        self.add_row(data , widths, pdf, row_height)
        for  _ in range(6):
            pdf.cell(widths[len(widths)- 1] , row_height , "", border=1)
        pdf.ln()
        return True
    
    #QUESTA FUNZIONE VA MODIFICA PER FORZA
    def add_particular_row_books_data(self , data , widths , pdf , row_height):
        for i , datum in enumerate(data): # enumerate permette di tenere traccia sia del dato che di un possibile indice    
            data = str(datum).split() # crea un array con le parole di una frase
            final_data = ""
            for word in data:
                if word == "E" or word == "EDIZIONE" or word == "+"  or word == "/" or word == "-" or word == ".":
                    break
                final_data += word + " "
                
            pdf.cell(widths[i], row_height, final_data,   border=1)
        
        for _ in range(6):
            pdf.cell(widths[len(widths)- 1], row_height, "",   border=1)
        pdf.ln() # c'e un valore ,di default che mi sposta la riga in giu
        
    def add_column_names(self , pdf , columns_names , widths , row_height ):
        for i , data in enumerate(columns_names):
            pdf.cell(widths[i] ,row_height , data , border=1)
        pdf.ln()
        
    def create_pdf(self)->FPDF:
        pdf =  FPDF()
        pdf.add_page("L")
        pdf.set_font("Times" , size=7)
        return pdf
        
        
