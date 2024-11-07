import camelot
import pandas as pd
from PyPDF2 import PdfReader
import re , os
from Backend.scaned import get_text_percentage


class Pdf_Dataframe:
    def __init__(self , file_path:str)->None:
        self.file_path = file_path
        
    def __extract_text(self):
        reader = PdfReader(self.file_path)
        page = reader.pages[0]
        text = page.extract_text()    
        return text
    
    #QUESTA FUNZIONE FA TANTO SCHIFO DA PULIRE E MIGLIORARE 
    def get_school_data(self):
        text = self.__extract_text() #Testo estratto dal pdf
        text = text.splitlines()
        
        school_data = []
        
        for line in text:
            subline = line.split(" ")
            for index , word in enumerate(subline):
                if word.lower() == "classe:":
                    temp  = subline[index + 1:]
                    user_class = "".join(temp).strip()
                    school_data.append(user_class)
                if word.lower() == "corso:":
                    temp = subline[index + 1]
                    user_course = " ".join(temp).strip()
                    school_data.append(user_course)
        
                
        school_data =[school_data[0].upper() , school_data[-1].upper()]
        user_course = school_data[-1]
           
        patterns  = [
            'LICEO SCIENTIFICO', 
            'LICEO LINGUISTICO' ,
            'INFORMATICA E TELECOMUNICAZIONI',
            'LICEO ARTISTICO',
            'LICEO CLASSICO'
            
        ]
        
        main_pattern = r''
        for index ,pattern in enumerate(patterns):
            if index != len(patterns) - 1:
                main_pattern += pattern + '|'
            else:
                main_pattern += pattern
        
        user_course = re.search(main_pattern , user_course).group(1) if re.search(main_pattern , user_course) else user_course
        school_data[-1] = user_course

        # Bisogna lavorare su il nome del corso 
        #[classe , corso]
        return school_data
        
        
    def __get_pages_number(self , file_path)->int:
        try:
            with open(file_path , "rb") as file:
                length = len(PdfReader(file).pages)
            return length
        except:
            return -1   
    
    def __aux_clear_empty(self, dataframe , iterator_func , axis_name ):
        to_drop = [] # colonna barra riga
        
        for index , data in iterator_func():
            len_data = len(data) #numero righe/colonne
            empty_cells = sum([1 for value in data if value ==  "" ]) # totale celle vuote
            empty_ratio = empty_cells / len_data #percentuale 
            ratio = 0
            
            # bisogna lavorare su questo parametro in base al numero di righe/colonne
            # così da ottenere un prodotto dinamico che decide quando cancellare 
            # in base alla lunghezza della riga 
            # Ci penser0
            
            if empty_ratio > 0.5:
                to_drop.append(index)
            
        if axis_name == "rows":
            dataframe = dataframe.drop(index=to_drop)
        elif axis_name == "columns":
            dataframe = dataframe.drop(columns=to_drop)
        
        return dataframe
    
    def __aux_clean_by_pattern(self, dataframe:pd.DataFrame  , pattern):
        for index , data in dataframe.iterrows():
           row = data.tolist()
           if any(pattern.strip() in str(element).upper().strip() for element in row):
               # se almeno uno degli elementi di questo array di booleans è vero la funzione dara vero 
               return index , row
        return None , None
    
    #QUESTA FUNZIONE ELIMINA TUTTE LE RIGHE/COLONE VUOTE DEL FILE 
    def __clear_empty(self , dataframe):
        # fare il drop della prima e dell'ultima colonna
        df = self.__aux_clear_empty(dataframe , dataframe.items , "columns" )
        df = self.__aux_clear_empty(df , dataframe.iterrows , "rows" )
        df = self.__reset_indexes(df)
        pattern = "MATERIA"
        
        index_to_remove , row_to_remove = self.__aux_clean_by_pattern(df , pattern=pattern)
        
        if index_to_remove is not None:
           df = df.drop(index=index_to_remove)
        df = self.__reset_indexes(df)
        return df  , row_to_remove
    
    #QUESTA FUNZIONE DEVE CONTROLLARE I DATI E ORGANIZZARLI IN MANIERA CORRETTA
    def __clean_row(self, row  , column_index , reg_exp , empty_column_index ):
        
        # Situazione in cui una delle due righe è vuote ma il patern non è rispettato
        column_value = row[column_index]
        
        if column_value == "":
            return row
        
        match = re.search(reg_exp , column_value)
        if match:
            number_text = match.group(1)
            rest_text = match.group(2)
        else:
            return row
            
        if row[empty_column_index].strip() == "": # è uguale a scrivere if row[empty] == ""
            row[1] = number_text
            row[2] = rest_text
            
        return row
    
    def __reset_indexes(self , dataframe):
        dataframe.reset_index(drop=True , inplace=True)
        dataframe.columns = [x for x in range(dataframe.columns.size)]
        return dataframe
    
    def dataframe_to_matrix(self , dataframe):
        df = []
        for _ , row in dataframe.iterrows():
            df.append(row.tolist())
        return df
    
    def __organize_df(self , dataframe):
        print(dataframe)
        df = self.dataframe_to_matrix(dataframe)
        
        reg_exp = r"(\d+)\s(\D+)"
        
        df_1 = [self.__clean_row(row ,1 ,reg_exp , 2) for row in df]
        df_2 = [self.__clean_row(row , 2 ,reg_exp , 1) for row in df_1]
       
        df = pd.DataFrame(df_2)
        df.drop_duplicates(ignore_index=True , inplace=True)
        self.__reset_indexes(dataframe)
        
        return df
            
    def get_dataframe(self , columns=None):
        # Logica di base dietro molto semplificato 
        # Quando uso read_pdf questo restituiesce un oggetto Table che contiene una lista di tabelle 
        # facendo df[0] -> prendo la prima Table che sta nella table list
        # Table list non é possibile iterare , e ottenere i risultati
        # ogni oggetto table va prima convertito in un oggetto dataframe con .df attributo di Table
        TableList = camelot.read_pdf(self.file_path , pages=f"all") # oggetto TableList
        
        #QUESTO ALGORITMO HA A CHE FARE UN PARTICOLARE TIPO DI PDF:
        #OVVERO QUELLO DELLE TABELLE DEI LIBRI SCOLASTICI
        #PER ORA PENSO A QUELLO FINE POI PENSERO A OTTIMIZZARE 
        
        list_of_dfs = [] # creo una lista vuota
        for num_table in range(len(TableList)):# prendo ogni tabella nella TablesList
            
            # creare una funzione che pulista ogni dataframe singolarmente
            df = TableList[num_table].df
            df , new_columns = self.__clear_empty(df) # elimino tutte le rige/vuote che possano esserci e lo restituisco indietro 
           
            df = self.__organize_df(df)
            list_of_dfs.append(df) # la aggiungo alla lista sottoforma di dataframe
        #Questo è il mio dataframe
        #Ora bisogna pulirlo

        
        df = pd.concat(list_of_dfs , ignore_index=True) # creo il dataframe finale facendo il concat dei dataframe nella lista dei dataframe
        
        #if df_columns is not None:
            #df = pd.DataFrame(df) # leggere è capire perché il dataframe con il parametro columns non funziona capire 
            # capire veramente cosa succede
            #df.columns = df_columns
        

        if columns is not None: 
            df = pd.DataFrame(df , columns=columns)
        
            
        return df
# Ho un piccolo problema che secondo me si risolve molto facilmente 

if __name__ == "__main__":
    
    patterns  = [
            'LICEO SCIENTIFICO', 
            'LICEO LINGUISTICO' ,
            'INFORMATICA E TELECOMUNICAZIONI',
            'LICEO ARTISTICO',
            'LICEO CLASSICO'
            
        ]
    
    user_course = "LICEO LINGUISTICOHoellosdfKJNKJN"
    main_pattern = r''
    for index ,pattern in enumerate(patterns):
        if index != len(patterns) - 1:
            main_pattern += pattern + '|'
        else:
            main_pattern += pattern
            
    # GROUPS FUNZIONA QUANDO QUANDO CI SONO I GRUPPI OVVERO ()
    # QUINDI ANCHE GROUP(1) E RESTO PRENDE IL ELEMENTI DI GROUPS
    # INVECE GRUPO(0) PRENDE IL PATTERN TROVATO 
    
    #ESEMPIO 
    #target_string = "The price of PINEAPPLE ice cream is 20"

    # two groups enclosed in separate ( and ) bracket
    #result = re.search(r"(\b[A-Z]+\b).+(\b\d+)", target_string)
    
    #RESULT GROUP(0) ->  PINEAPPLE ice cream is 20 DA DOVE A DOVE SONO STATI TROVATI I PATTERN 
    # PERO NON MI DA I SINGOLI PATTERN 
    
    user_course = re.search(main_pattern , user_course).groups() if re.search(main_pattern , user_course) else user_course
    print(user_course)