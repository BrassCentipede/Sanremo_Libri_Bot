import requests , os
from natsort import natsorted
import re


def urls(file_name):
    # Preso un file di url da cui scaricare i file ritorno la lista dei degli url 
    urls = []
    with open(file_name, "r") as file:
        lines = file.readlines()
        for index ,line in enumerate(lines):
            if index != len(lines) - 1: 
                line = line[:-1]
            urls.append(line)
    return urls

# BISOGNA VEDERE QUAL È FILE CON IL NUMERO PIÙ ALTO 
# 1-test.pdf , bisogna vedere quale di dei file della cartella ha il numero più altro 
# non usero nat sorted perché mi piace fare le cose a mano perciò lo faro a mano(scrivo io la funzione di confronto ) il confronto 
def get_highest_num_file(dir):
    #.DS_Store è una cartella nascota che contiene alcuni metadati della cartella
    list_of_files = os.listdir(dir)
    list_of_files.remove(".DS_Store")
    pattern = r'\d+|\D+'
    num_of_files = [re.findall(pattern , file_name) for file_name in list_of_files]
    nums = [int(row[0]) for row in num_of_files]
    max  = 0 
    for index in range(1, len(nums)):
        if nums[index] > nums[max]:
            max = index
    
    return nums[max]

def download_file(url , dest , file_name):
    response = requests.get(url)
    pdf_file = response.content
    with open(f"{dest}/{file_name}" , "wb") as pdf_to_save:
        pdf_to_save.write(pdf_file)


def delete_url(list_of_urls, sour_file , dest_file):
    poped_url = list_of_urls.pop(0) # funziona lui prende lo mette in una var e lo cancella 
    with open(dest_file , "a") as dest_urls_file:
        dest_urls_file.write(poped_url + "\n")
    with open(sour_file , "w") as source_urls_file:
        for url in list_of_urls:
            source_urls_file.write(url)

            
# ORA TOCCA LEGGEE GLI URL E VEDERE QUANTI SONO È CAPIRE DA CHE PUNTO IN POI DOVREI SALVARE 
#("./urls_of_files.txt" -> urls_file
#"./Src/FIiles/input_pdf_test" -> destination_folder
def download_files(source_urls_file , dest_folder , dest_urls_file):   
    list_of_urls = urls(source_urls_file) # lista di link da cui dovrei scaricare i file
    max_num_of_file = get_highest_num_file(dest_folder) # ex =  24 è il file con il numero più grande 24-test.pdf
   
    for url in list_of_urls:
        download_file(url, dest_folder ,f"{max_num_of_file + 1}-test.pdf")
        max_num_of_file += 1
        # I file letti vanno calcellati e messi in altro file readed_url così analizzo file sempre diversi
    for _ in range(len(list_of_urls)):
        delete_url(list_of_urls, source_urls_file , dest_urls_file)


if __name__ == "__main__":
    download_files(source_urls_file="./urls_of_files.txt" , dest_folder="./Src/Files/input_pdf_test" ,   dest_urls_file="./dest_urls_file.txt")
    