import telebot 
# IN QUESTO FILE SALVERO LE TASTIERE CREATE PER IL PROGRAMMA 
def main_keyboard(file_id , chat_id):
  #creazione della tastiera di bottoni
  key_board = telebot.types.InlineKeyboardMarkup(row_width=3)
  #bottoni per l'esportazione
  pdf_button =  telebot.types.InlineKeyboardButton(text="PDF" , callback_data=f"export_pdf {file_id} {chat_id}")
  ods_button = telebot.types.InlineKeyboardButton(text="ODS" , callback_data=f"export_ods {file_id} {chat_id}")
  exel_button = telebot.types.InlineKeyboardButton(text="EXEL" , callback_data="export_exel")
  
  #bottoni per la modica 
  #modicca nome / cognome
  change_first_name = telebot.types.InlineKeyboardButton(text="Modifica il nome" , callback_data=f"change_first_name {file_id} {chat_id}")
  change_last_name = telebot.types.InlineKeyboardButton(text="Modifica il Cognome" , callback_data=f"change_last_name {file_id} {chat_id}")
  #modifica numero di telefono 
  change_phone_number = telebot.types.InlineKeyboardButton(text="Modifica  il cellulare " , callback_data=f"change_phone_number {file_id} {chat_id}")
  #modifica data 
  change_date_of_creation = telebot.types.InlineKeyboardButton(text="Modifica data creazione" , callback_data=f"change_date_of_creation {file_id} {chat_id}")
  #aggiunta dei tasti alla tastiera 
  key_board.add(pdf_button , ods_button , exel_button , change_first_name , change_last_name , change_phone_number , change_date_of_creation)
  
  return key_board


def ask_to_change_phone_number( file_id , phone_number , chat_id):
  key_board = telebot.types.InlineKeyboardMarkup(row_width=2)
  yes_button = telebot.types.InlineKeyboardButton(text = "Yes" , callback_data=f"chage_phone_number {file_id} {phone_number} {chat_id}")
  no_button = telebot.types.InlineKeyboardButton(text="No" , callback_data=f"dont_change_number {file_id} {phone_number} {chat_id}")
  key_board.add(yes_button , no_button)
  
  return key_board