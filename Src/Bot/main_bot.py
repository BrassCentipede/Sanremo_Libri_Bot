import telebot , os 
from file import File
from keyboards import * 
from create_and_export_files import *
from datetime import datetime
from Backend.scaned import get_text_percentage
from save_data import *

#30/10/2024 -> CREARE UNA PICCOLA DOCUMENTAZIONE E COMMENTARE IL CODICE 


bot = telebot.TeleBot("7640007202:AAG4vPZDL5QLmFuVPG40F04K5KiCOahq7QE") # creazione del bot in se 

#Creazio e del mini database per la gestione dei file e dei dati dei file
bot_data = {}

#COMMANDO START CHE DA INIZIO A TUTTO QUANTO
@bot.message_handler(commands=['start'])
def start_command(message):
  print(message.from_user.id == message.chat.id)
  print(message.from_user)
  bot.send_message(message.chat.id , welcome_message(message)) 

@bot.message_handler(content_types=["text"])
def history_manage(message):
  if message.text == "/history":
    history(message)
  elif message.text == "/help":
    bot.send_message(message.chat.id , "Prova a usare il comando /hello")
  elif message.text == "/commands":
    pass
  elif message.text == "/view":
    bot.send_message(message.chat.id , "Hai chiamato il comando view")
  else:
    bot.send_message(message.chat.id , "Testo non consentito inserire un file ") 
    
    

def history(message):
  chat_id = message.chat.id
  if len(bot_data) == 0:
    bot.send_message(chat_id , "La sua cronologia è vuota carica un file")
  for file_id , value in bot_data.items():
    bot.send_message(chat_id , f"Data di importazione : {bot_data[file_id][3][0]}")
    bot.send_message(chat_id , f"nome file: {value[0]} personal data ({value[2][0]} , {value[2][1]} , {value[2][2]}, {value[2][3]})" , reply_markup=main_keyboard(file_id , chat_id) )
 
#GESTIONE DEI DOCUMENTI 
@bot.message_handler(content_types=["document"] , func=lambda message : message.document.mime_type == "application/pdf")
def get_file(message):
  chat_id = message.chat.id 
  # recupero i dati necessari per lavorare con i file caricati dall'utente 
  file_id , file_name , directory_of_file  = download_file(message)
  
  file = File(f"{directory_of_file}/{file_name}.pdf")
  scan_persentage = get_text_percentage(f"{directory_of_file}/{file_name}.pdf")
  
  print("il file è un file pdf, ora possiamo iniziare l'analisi")
  moment_of_uploading = datetime.now().strftime("%d/%m/%Y , %H:%M:%S")
  bot_data[file_id] = [file_name , directory_of_file , [] , [] , []]
  
  bot_data[file_id][3].append(moment_of_uploading)
  
  get_import_data(file_id ,file_name , directory_of_file , moment_of_uploading)

  if scan_persentage < 0.1:
    bot.send_message(chat_id , "Il file inserito è uno file scannerizzato non è ancora gestito dal programma la invito a provare con un altro file" )
    bot_data[file_id][3][0] += "  file file attuale è uno scanner"
  else:
    print(f"Il file {file_name}.pdf è stato caricato il {moment_of_uploading}")
    if file.is_pdf() and file.is_redable() :
      # creo un campo con chiave fail_id , valore = dati necessari per recuperare il file 
      #inizio con il chiedere il nome e cognome del cliente 
      asks_name = bot.send_message(chat_id , "Inserisci il Nome e Cognome del cliente: ")
      # gestisco la risposta dell'utente tramite la funzione get_name
      bot.register_next_step_handler(asks_name , get_name , file_id , chat_id )
    else:
      bot.send_message(chat_id , "Il file inserito non è un file pdf \n Le chiedo gentilmente di inserire un file pdf")

# FUNZIONE PER LA GESTIONE E SALVAGGIO DEL NOME E COGNOME
def get_name(message , file_id , chat_id):
  try:
    bot_data[file_id][2].clear()
    name = message.text
    name_and_surname_list = name.strip().split()
    bot_data[file_id][2].append(name_and_surname_list[0])
    bot_data[file_id][2].append(name_and_surname_list[1])
    ask_phone_number = bot.send_message(chat_id , "Insersci il numero di telefono del cliente: ")
    bot.register_next_step_handler(ask_phone_number , get_phone_number , file_id , chat_id)
  except  Exception as e:
    bot.send_message(chat_id , "Si è verificato un errore , non ha inserito i dati corretamente la prego di riprovare")
    asks_name = bot.send_message(chat_id , "Inserisci il Nome e Cognome del cliente: ")
    bot.register_next_step_handler(asks_name , get_name , file_id , chat_id )
    
#FUNZIONE PER LA GESTIONE E SALVATAGGIO DEL NUMERO DI TELEFONO 
def get_phone_number(message , file_id , chat_id):
  phone_number = message.text 
  if len(phone_number) > 10:
    bot.send_message(message.chat.id , f"La lunghezza del numero di telefono di telefono supera il limite di cifre per un numero italiano , è sicuro di questo numero {phone_number} ")
    bot.send_message(message.chat.id , "Vorrebbe modificare il numero ? " , reply_markup=ask_to_change_phone_number(file_id , phone_number , chat_id))
  else:  
    confirm_and_save_phone_number(file_id , phone_number , chat_id)

@bot.callback_query_handler(func=lambda message : message.data.startswith("chage_phone_number") or  message.data.startswith("dont_change_number") )
def change_phone_call_back(message):
  command  , file_id  , phone_number , chat_id= message.data.split()
  
  if command == "chage_phone_number":
    # chiedo di inserire il nuov numero di di telefono 
    new_phone = bot.send_message(chat_id , "Inseresci il nuovo numero: ")
    # chiamo la funzione di cambio del numero
    bot.register_next_step_handler(new_phone , insert_changed_phone_number , file_id , chat_id , 0 )
    print(bot_data[file_id][2])
    
  if command == "dont_change_number":
    bot.send_message(chat_id , "Hai scelto di non cambiare il numero il numero verra inserito nei dati ")
    confirm_and_save_phone_number(file_id , phone_number , chat_id)
    print(bot_data[file_id][2])

def confirm_and_save_phone_number(file_id , phone_number , chat_id):
  bot_data[file_id][2].insert(0 , phone_number)
  ask_data_of_creation = bot.send_message(chat_id , "Inserisca la data di creazione della tabella : ")
  bot.register_next_step_handler(ask_data_of_creation , get_date_of_creation , file_id , chat_id)
  
def insert_changed_phone_number(messagge , file_id , chat_id , index):
  new_data = messagge.text
  bot_data[file_id][2].insert(index ,new_data)
  print(f"I dati sono stati cambiati con successo , i nuovi dati sono {bot_data[file_id][2]} ")
  ask_data_of_creation = bot.send_message(chat_id , "Inserisca la data di creazione della tabella : ")
  bot.register_next_step_handler(ask_data_of_creation , get_date_of_creation , file_id , chat_id)

# GESTIONE E SALVATAGGIO DELLA DATA DI CREAZIONE
def get_date_of_creation(message , file_id, chat_id):
  date_of_creation = message.text
  bot_data[file_id][2].insert(0 , date_of_creation)
  bot.send_message(chat_id , "Scelga il formato di esportazione oppure se vuoi effettuare delle modifiche" , reply_markup=main_keyboard(file_id , chat_id))
  
@bot.callback_query_handler(func=lambda message : message.data.startswith("export_"))
def export_pdf(message):
  command , file_id, chat_id = message.data.strip().split()
  file_info = bot_data.get(file_id)
  
  moment_of_export = datetime.now().strftime("%d/%m/%Y , %H:%M:%S")
  
  if file_info:
    file_name , directory_of_file , personal_data  , date_of_creation , date_of_exportation= file_info
    if command == "export_pdf":
      create_and_export_pdf(bot , file_name , directory_of_file , personal_data, chat_id)
      bot_data[file_id][4].append(f"pdf : {moment_of_export}")
      print(f"Il file {file_name} pdf elaborato è stato esportato in formato pdf il {moment_of_export}")
      get_export_data(bot_data)
    if command == "export_ods":
      create_and_export_ods(bot , file_name , directory_of_file , personal_data , chat_id)
      bot_data[file_id][4].append(f"ods : {moment_of_export}")
      print(f"Il file {file_name} pdf elaborato è stato esportato in formato os il {moment_of_export}")
      get_export_data(bot_data)
    if command == "export_exel":
      create_and_export_exel(bot , file_name , directory_of_file , personal_data)
      #print(f"Il file {file_name} pdf elaborato è stato esportato in formato exel il {moment_of_export}")
      #bot_data[file_id][4].append(f"pdf : {moment_of_export}")
  else:
      bot.send_message(chat_id, "Errore: Il file specificato non è stato trovato.")
@bot.callback_query_handler(func= lambda message : message.data.startswith("change_first_name") or message.data.startswith("change_last_name")  or message.data.startswith("change_phone_number")  or message.data.startswith("change_date_of_creation"))

def change(message):
  print(message.data)
  command , file_id, chat_id = message.data.strip().split()
  file_info = bot_data.get(file_id)
  
  if file_info:
    if command == "change_first_name":
      new_name = bot.send_message(chat_id , "Inserisca il nuovo nome:")
      bot.register_next_step_handler(new_name ,change_personal_data , file_id , 2)
      print("Hello World")
    if command == "change_last_name":
      print("change_last_name")
      new_surname = bot.send_message(chat_id, "Inserisca il nuovo cognome")
      bot.register_next_step_handler(new_surname , change_personal_data , file_id , 3)
    if command == "change_phone_number":
      new_phone = bot.send_message(chat_id , "Inserisca il nuovo numero di celluare:")
      bot.register_next_step_handler(new_phone ,change_personal_data , file_id , 1)
    if command == "change_date_of_creation":
      new_date_of_creation =  bot.send_message(chat_id , "Inserisci la nuova data di creazione ")
      bot.register_next_step_handler(new_date_of_creation , change_personal_data , file_id , 0)
      
def change_personal_data(message , file_id , index):
  data = message.text
  bot_data[file_id][2][index] = data
  bot.send_message(message.chat.id , f"Hai cambiato i dati con succeso ora i tuoi dati sono{bot_data[file_id][2]}")  

def welcome_message(message):
    welcome_message_text = f"""
Benvenuto a bordo {message.from_user.first_name} il nostro bot che vi aiuterà ad interfacciarti 
con il software di analisi e creazione di file che faciliterà la sua organizzarzione della scolastica 
Questo bot è soltanto un modo più facile per farvi interfacciare con gli algoritmi , perché per il momento 
non esiste una piattaforma online completa che possa aiuravi a usare i nostri algoritmi

LA ESORTIAMO A LEGGERE LE SEGUENTI RIGHE
REGOLE D'USO:
  - La preghiamo di inseriere un file pdf , un file pdf che non risulti scannerizzato , al momento il programma riesce a gestire 
    soltanto file pdf non scannerizzati 
  - Una volta inserito un file pdf valido , il programma vi guiderà attraverso il il suo processo2

    """
    return welcome_message_text
  
def download_file(message):
  #ottenfdo l'id del file
    file_id = message.document.file_id
    file_info =  bot.get_file(file_id)
    #print(file_info.file_unique_id)
    file_unique_id = file_info.file_unique_id
    file = bot.download_file(file_info.file_path)
    # cambio posizione nella cartella padre dei files
    #ottendo il perconso della cartella padre
    #os.chdir() -> questa funzione da cambiare 
    curent_dir = os.getcwd()
    #identifico la sotto_cartella cartella che voglio creare nella cartella padre
    DOWNLOAD_DIR = "input_pdf"
    #Documents/Informatica/Progetti/AdvanceProjects/Scolastica/Src/Files/input_pdf
    #percorso della cartella dove stanno i file inseriti dall'uente
    dir_to_save_file = f"{curent_dir}/Documents/Informatica/Progetti/AdvanceProjects/Scolastica/Src/Files/{DOWNLOAD_DIR}"
    if not os.path.exists(DOWNLOAD_DIR):
      os.makedirs(DOWNLOAD_DIR)
    # ottengo il nome del file 
    file_name = message.document.file_name
    where_to_save = f"{dir_to_save_file}/{file_name}"
    with open(where_to_save , "wb") as f:
      f.write(file)
    # tolgo dal nome il sufisso .pdf
    file_name = file_name.replace(".pdf" , "")
    
    return file_unique_id , file_name , dir_to_save_file
  
if __name__ == "__main__":
 
  bot.polling()
   


  