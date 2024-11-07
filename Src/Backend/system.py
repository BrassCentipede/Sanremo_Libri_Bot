import os
import platform
import sys
import subprocess


#to_install = ["tabula-py" , "pandas" , "fpdf" , "pypdf" , "regex" , "jpype1"]
class SystemData:
    def __init__(self , library_to_install):
        self.library_to_install =  library_to_install
    
    
    def system_flag(self):
    #/Users/andreitarlev/Documents/Informatica/Progetti/Intermediate Projects/Scolastica/main2.py
    # meglio creare il file nella home directory dove nessuno protrebbe toccarlo perché la gente è stupida è potrebbe rovinare tutto 
        self.file_flag = os.path.expanduser("~/.libraries_os_data_file") # rappresenta una convenzione /Users/andreitarlev/.file.txt espando il percorso nella directory

    """
    Nella directory home , non creo file per creare questo file bisogna usare with open(file , "w") as file : per poter poi scrivere al suo interno 
    Il file senza estensione viene trattato allo stesso modo uno senza estensione 

    expand user non crea alcun file mi da solo un percorso per un possibile file , che non esiste ancora quindi se non verrra creato le librerie verrano cmq installate in continuazione 
    perció bisogna creare il file 
    """

    def install_libraries(self):
        """ Questa funzione usera subpress una libreria che eseguira comandi nel terminale """
        for library in self.library_to_install:
            subprocess.check_call([sys.executable , "-m" , "pip" , "install" , library])
            #sys.executable -> è l'iterpretarore python usato per installare tutte queste librerie 
            # libreria subprocess con la funzione check_call mi permette di eseguire comandi sul terminale

    # quando voglio scrivere una funzione che mi restituesce dei dati ottenuti in qualche modo 
    # come inzio del nome della funzione uso get
    def get_system_info(self):
        """Raccolgo dati sul sistema operativo"""
        system_info = {
            "os_name" : os.name,
            "platform_system":  platform.system(),
            "platform_release": platform.release(), # quando è stato rilasciato 
            "platform_version": platform.version(), # versione Darwin Kernel -> Mac os 
            "platform_machine": platform.machine(), # processore arm , x86 e cosi via 
            "paltform_platform": platform.platform(),  # sistema op tipo mac or windows
        }
        return system_info

    

    def create_windows_launcher(script_path):
        file  = "run_launcher.bat"
        bat_content = f"""@echo off
        python {script_path}
        pause
        """
        with open(file , "w") as launcher:
            launcher.write(bat_content)
        
    def create_mac_launcher(script_path):
        file = "run_launcher.sh"
        sh_content = f"""#!/bin/bash
    python3 "{script_path}"
        """
        with open(file , "w") as laucher:
            laucher.write(sh_content)
        subprocess.run(["chmod", "+x", "run_launcher.sh"])
"""
    def main():
        system_info = get_system_info()
        script_path = os.path.abspath("main2.py")
        os_name = system_info["platform_system"] 
        
        if os_name == "Darwin":
            create_mac_launcher(script_path)
        elif os_name == "Windows":
            create_windows_launcher(script_path)
        elif os_name == "Linux":
            create_mac_launcher(script_path) 
        
        Se il file non esiste installo le librerie e poi creo il file 
        if not os.path.exists(file_flag) :
            install_libraries(to_install)
            with open(file_flag , "w+") as flag_file : # al percorso file con il nome file crearea un file 
                for library in to_install:
                    flag_file.write(f"{library}")
                    
                flag_file.write("\n")
                # ora iteriamo attraverso un dizionario 
                for key , item in system_info.items():
                    flag_file.write(f"{key}  {item} \n") 
        
if __name__ == "__main__":
    main()            
    
"""