from setuptools import setup , find_packages # prima di usare questa libreria controllare se ho scaricato corretamnete la libreria 
# se è presente nel nella lista dei pacchetti installati , pipE

setup(name="scolastica", version=1.0, packages=find_packages(
))

# in questo file risolvo il problema con l'importazione dei moduli in python da una cartella ad un'altra 
# Questo metodo funziona 

#pip install -e . nella cartella dove sta setup.py