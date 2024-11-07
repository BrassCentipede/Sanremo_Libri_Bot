DATI DELLA SCUOLA DEL PDF CARICATO

    #Algoritmo per estrarre la scuola e la classe  -> FA SCHIFO DA MIGLIORARE 
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
    print(school , classes)
    
    return [school, classes] # restituisco una lista con i miei dati 