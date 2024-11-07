
from backend.create_pdf import to_Pdf
from backend.create_ods import to_Ods




def main():
    
    system_data = SystemData(["tabula-py" , "pandas" , "fpdf" , "pypdf" , "regex" , "jpype1"])
    # dati del file 
    file_name = "2B"
    file_path = f"input_pdf/{file_name}.pdf"
    # oggetto necessario per estrarre i dati dal file 
    data_from_pdf = Data_From_File(file_path)
    
    date = "27/08/2024"
    name =  "Andrei Tarlev"
    phone_number = "3807991129"
    
    personal_data = [date , name , phone_number]
    # i dati dei libri in due strutture diverse 
    #dizionario
    
    #dict_data = data_from_pdf.get_dict_data()
    #lista
    array_data = data_from_pdf.get_array_data2()
    print(array_data)
    
    
    #dati della scuola e della classe
    school_data = data_from_pdf.get_school_data()
    #lista con i dati della scuola 
    dati_scuola =["Scuola" , f"{school_data[0]}" , f"{school_data[1]}" , "" , ""]
    
    #larghezze delle celle 
    widths = [25, 35, 73, 40, 14, 14, 14, 14, 14, 14, 14]
    #altezza della cella 
    row_height = 15
    
    
    #PDF
    #file pdf che creo 
    pdf_1 = to_Pdf(file_path)
    pdf = pdf_1.create_pdf() # creo il pdf
    #aggiungo i dati personali 
    pdf_1.add_row_with_empy_cels([f"{personal_data[0]}" , f"{personal_data[1]}" , f"{personal_data[2]}" , "" , "" ] , widths , pdf , row_height)
    # aggiungo i dati della scuola 
    pdf_1.add_row_with_empy_cels(dati_scuola , widths , pdf , row_height)

    
    # Aggiungo i dati dell'accounto e del buono
    acconto = "NO".lower().capitalize()
    dati_accont=["Acconco" , "" , acconto , "" , ""]
    pdf_1.add_row_with_empy_cels(dati_accont , widths , pdf , row_height)
    buono_usato = "nO".lower().capitalize()
    dati_buono_usato=["Buono Usato" , "" , buono_usato , "" , ""]
    pdf_1.add_row_with_empy_cels(dati_buono_usato , widths , pdf , row_height)
    
    # raccolgo i dati personali 
    
    
    
    # aggiungo il nome delle colone
    columns_names = ["Codice Volume","Materia / Disciplina" , "Titolo / Sottotitolo",  "Editore", "Prezzo" , "Deve" , "Pagato" , "Magazzino" , "ORD" , "ARR" , "CONSE"]
    pdf_1.add_column_names(pdf , columns_names , widths , row_height)
    # PARTE PIU IMPORTANTE AGGIUNGO I DATI DEI LIBRI
    
    
    for row in array_data:
        pdf_1.add_particular_row_books_data(row , widths, pdf , row_height)
        

    # salvo il pdf 
    pdf.output("output_pdf/test.pdf")
    
    
    #ODS

    # Lavoro sulle delle copie necessarie per il file ods
    arra_data_prox = array_data[:] # così creo una copia profonda dell'array 
    personal_data_copy = personal_data[:]
    dati_scuola_copy = dati_scuola[:] # crea una copia profonda anche qua perciò meglio usare questo metodo
    dati_accont_copy = dati_accont[:]
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
    ods_file.add_data(columns_names)
    ods_file.add_books_data()
    ods_file.add_table_to_spreadsheet()
    ods_file.save_ods(f"output_ods/{name}")

if __name__ == "__main__":
    main()