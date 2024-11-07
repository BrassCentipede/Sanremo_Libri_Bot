import os
folder ="./Src/Files/input_pdf_test/"
files = os.listdir(folder)

files.sort()
print(files)

lenght_of_files = len(files)

for index  , file in enumerate(files):
    if file.endswith(".pdf"):
        file = os.path.join(folder , file)
        print(file)
        
        new_folder = "./Src/Files/input_pdf_test/"
        new_file_name = os.path.join( new_folder, f"{index + 1}-test.pdf")
        print(new_file_name)
        os.rename(src=file , dst=new_file_name)
        
        
    