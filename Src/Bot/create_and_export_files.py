from Backend.main import Main
from datetime import datetime


def create_and_export_pdf(bot , file_name , directory_of_file , personal_data, chat_id):
  pdf = Main(f"{directory_of_file}/{file_name}.pdf")

  
  path = pdf.create_pdf(file_name , personal_data , "NO" , "no")
  with open(path , "rb") as file:
    bot.send_document(chat_id, file)
    
    
  
def create_and_export_ods(bot ,file_name , directory_of_file , personal_data , chat_id):
  ods = Main(f"{directory_of_file}/{file_name}.pdf")
  path = ods.create_ods(file_name , personal_data , "NO" , "NO")
  
  with open(path , "rb")  as file:
    bot.send_document(chat_id , file)

def create_and_export_exel(file_name , directory_of_file , personal_data):
  print("Al momento la funzione la funzione non accessibile ")