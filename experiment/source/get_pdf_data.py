import tabula as tb # type: ignore
import pandas as pd 
from pypdf import PdfReader


class Data_From_File:
    #funzione init per i parametri iniziali 
    def __init__(self , file_path):
        self.file_path = file_path
        
#TODO:ALGORITMO PIU IMPORTANTE DEL PROGRAMMA 
    def cleanig_data(self, data_frame):
        combined_data = []  # Lista per memorizzare i dati combinati
        temp_row = None  # Riga temporanea per costruire la riga combinata
        # Itera attraverso ogni riga del DataFrame
        for _, row in data_frame.iterrows():
            # Se 'Materia / Disciplina' non è NaN, iniziamo una nuova riga
            if pd.notna(row['Materia / Disciplina'] and row['Codice Volume']):
                # Aggiungi la riga temporanea combinata alla lista se è già popolata
                    if temp_row is not None:
                        combined_data.append(temp_row)
                # Imposta la riga temporanea corrente come nuova riga di partenza
                    temp_row = row.tolist()
            else:
                # Se la riga è una continuazione (Materia / Disciplina è NaN), combinala con temp_row
                for col_index, value in enumerate(row):
                    if pd.notna(value):  # Combina solo i valori non NaN
                        
                        if pd.isna(temp_row[col_index]) or temp_row[col_index] == '':
                            temp_row[col_index] = value  # Inserisci il valore direttamente se temp_row è NaN o vuoto
                        else:
                            temp_row[col_index] = f"{temp_row[col_index]} {value}".strip()  # Combina con lo spazio

        # Aggiungi l'ultima riga combinata alla lista
        if temp_row is not None:
            combined_data.append(temp_row)
        # Crea un DataFrame dal risultato combinato
        combined_df = pd.DataFrame(combined_data, columns=data_frame.columns)
        # Converti 'Codice Volume' in stringa per evitare la notazione scientifica
        combined_df['Codice Volume'] = combined_df['Codice Volume'].apply(lambda x:  f"{x:.0f}" if isinstance(x , (int , float)) else x  )
        #combined_df['Codice Volume'] = combined_df['Codice Volume'].apply(lambda x:  print(type(x)))
        return combined_data


    def get_data(self): #funzione principale che raccoglie i dati dal file
        dfs = tb.read_pdf(self.file_path , pages="all" , pandas_options={"header":None}) # legge il file_path , tutte le pagine 
        df = pd.concat(dfs , ignore_index=True) # crea un dataset unico
        num_columns = df.columns.size
        pd.set_option("display.max_columns" , None)
        with open("data_frame.txt" , "w+") as file:
            df_string = df.to_string()
            file.write(df_string)
        
        print(num_columns)
        if num_columns > 9:
            targhet = num_columns - 9
            for i in range(1 , targhet + 1):
                df = df.drop(df.columns[[num_columns - i]] , axis=1)
            
        #elimino le colonne con indice 4 e 7 
        df = df.drop(df.columns[[4, 7]] , axis=1)
        # rigenero l'ordine
        df.columns = [
            "Materia / Disciplina " ,
            "Codice Volume ",
            "Autore/Curatore / Traduttore" ,
            "Titolo / Sottotitolo" ,
            "Editore",
            "Prezzo",
            "Da acq"
        ]
        
        
        print(df)
        #df = self.cleanig_data(df) # applico la funzione 

        return df
    #Organizzo i dati all'interno di un array di array 
    def get_array_data2(self):
        df = self.get_data()
        for array in df:
            number = str(array[1])
            numbers = [x for x in number]
            numbers.pop()
            numbers.pop()
            array[1] = "".join(numbers)
        l = []
        for array in df:
            m = []
            m.append(array[1]) # codice
            
            m.append(array[0]) # materia
            m.append(array[4]) #titolo
            m.append(array[6]) #editore
            m.append(array[7]) # prezzo
            print(array[7])
            l.append(m)
        return l
        
    def get_array_data(self):
        df = self.get_data()

        l = []
        for _ , data in df.iterrows():
            m = []
            m.append(data["Codice Volume"])
            m.append(data["Materia / Disciplina"])
            m.append(data["Titolo / Sottotitolo"])
            m.append(data["Editore"])
            m.append(data["Prezzo"])
            l.append(m)
        return l 
    
    #Organizzo i dati all'interno di un dizionario 
    def get_dict_data(self): 
        data_dict = dict() # creo un dizionario 
        df = self.get_data()#ottengo il data set
        
        
        #itero attraverso il dataset per otterene i dati necessari e inserirli all'interno del dizionario 
        for _ , data in df.iterrows():
            #aggiunda dell'elemento nel dizionario 
            data_dict.__setitem__(f"{data["Codice Volume"]}" , [data["Materia / Disciplina"] , data["Titolo / Sottotitolo"] , data["Editore"] , data["Prezzo"]])
            
        return data_dict
    # ottendo i dati della scuola leggendo il file , cioe il testo del file 
    def get_school_data(self):
        reader = PdfReader(self.file_path)
        page = reader.pages[0]
        text = page.extract_text()
        
        #Algoritmo per estrarre la scuola e la classe 
        #Fa schifo ma poi lo migliorero
        school = ""
        classes = ""
        #variabili provisorie 
        prov_st = ""
        prov_list = []

        for t in range(11 , 100): # inizio dal punto in cui inizia il nome della scuola , fino al punto dove c'è la classe
            if text[t] == "\n": # quando trovo un a capo vuol dire che ho un parametro diverso nella descrizione della scuola 
                prov_list.append(prov_st) # appendo alla lista solo delle parole che sono tagliate da un a capo 
                prov_st = "" # svuoto la stringa provvisoria 
            prov_st += text[t] # aggiungo alla stringa provvisoria fin quando non trovero un a capo 
            
        school = prov_list[0] #imposto dei valori della var scuola 
        classes = prov_list[len(prov_list)- 1]
        
        return [school, classes] # restituisco una lista con i miei dati 