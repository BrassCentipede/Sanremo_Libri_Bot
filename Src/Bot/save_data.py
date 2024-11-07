def get_export_data(bot_data):
   with open("/Users/andreitarlev/Documents/Informatica/Progetti/AdvanceProjects/Scolastica/Src/Data/Export_data.txt" , "w") as f:
      for key , value in bot_data.items():
        f.write(f"file_id : {key}\n")
        f.write(f"classe: {value[0]}\n")
        f.write(f"directory: {value[1]}\n")
        f.write(f"personal_data: {value[2]}\n")
        f.write(f"import_time: {value[3]}\n")
        f.write(f"export_times: {value[4]}\n")
        f.write("\n")

def get_import_data(file_id , file_name , file_directory , moment_of_uploading):
  with open("/Users/andreitarlev/Documents/Informatica/Progetti/AdvanceProjects/Scolastica/Src/Data/Import_data.txt" , "a") as file:
    file.write(f"file_id: {file_id}\n")
    file.write(f"file_name: {file_name}\n")
    file.write(f"direcrory_path: {file_directory}\n")
    file.write(f"moment_of_uploading: {moment_of_uploading}\n")
    file.write("\n")
