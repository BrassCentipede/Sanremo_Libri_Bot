from odf.opendocument import OpenDocumentSpreadsheet
from odf.style import Style , TableColumnProperties , TableCellProperties , TableRowProperties, TextProperties , PageLayout , PageLayoutProperties , MasterPage
from odf.table import Table , TableCell , TableColumn , TableRow
from odf.text import P


class to_Ods():
    def __init__(self , data):
        self.data = data 
    
    #creazione del documento 
    def create_spread_sheet(self):
        self.doc = OpenDocumentSpreadsheet()
        
        self.page_layout = PageLayout(name="LandscapeLayout")
        self.page_layout.addElement(PageLayoutProperties(
            margin="1cm", 
            pagewidth="29.7cm",  # A4 landscape width
            pageheight="21cm",   # A4 landscape height
            printorientation="landscape"
        ))
        self.doc.automaticstyles.addElement(self.page_layout)
        
        # Creazione di una pagina principale (master page) che usa il layout definito
        master_page = MasterPage(name="LandscapeMasterPage", pagelayoutname=self.page_layout)
        self.doc.masterstyles.addElement(master_page)
        
    def style_the_spreadshet(self):
        #creazione della tabella 
        self.table = Table(name="Dati-Libri")
        #larghezza della colonna 
        list_of_widths = ["3cm", "3.6cm" , "7cm", "3.5cm" , "1cm" , "1.4cm" , "1.4cm", "1.4cm", "1.4cm", "1.4cm" , "1.4cm"]
        #stile di una colonna
        for larghezza in list_of_widths:
            self.column_style =  Style(name=f"ColWidth_{larghezza}" , family="table-column")
            self.column_style.addElement(TableColumnProperties(columnwidth = larghezza))
            self.doc.automaticstyles.addElement(self.column_style)
            
            self.table.addElement(TableColumn(stylename = self.column_style))

        #stile riga 
        self.row_style = Style(name="RowHeight" , family="table-row")
        self.row_style.addElement(TableRowProperties(rowheight= "1.5cm"))
        self.doc.automaticstyles.addElement(self.row_style)
        
        # stile di una cella
        self.cell_style = Style(name="CellBorders", family="table-cell")  # Crea uno stile chiamato 'CellBorders' per le celle
        self.cell_style.addElement(TableCellProperties(border="0.6pt solid #000000"))  # Imposta il bordo a 0.06pt, solido e nero
        self.cell_style.addElement(TextProperties(fontsize = "7pt" , fontfamily="Arial"))
        self.doc.automaticstyles.addElement(self.cell_style) 
        
        # Definisci un layout di pagina con orientamento "landscape"
        page_layout = PageLayout(name="LandscapeLayout")
        page_layout.addElement(PageLayoutProperties(
            margin="1cm", 
            pagewidth="29.7cm",  # A4 landscape width
            pageheight="21cm",   # A4 landscape height
            printorientation="landscape"
        ))
        self.doc.automaticstyles.addElement(page_layout)

        # Creazione di una pagina principale (master page) che usa il layout definito

        

        # Creazione di una pagina principale (master page) che usa il layout definito
        master_page = MasterPage(name="Default", pagelayoutname=page_layout)
        self.doc.masterstyles.addElement(master_page)
               
    #aggiunta dei dati senza anadre a una nuova riga      
    def add_data(self , data):
        row = TableRow(stylename=self.row_style) # va a una nuova riga non crea righe ma ava a una nuova riga 
        for data in data:
            cell = TableCell(stylename = self.cell_style)
            cell.addElement(P(text=str(data))) # aggiunge qualcosa tipo testo a quella cella 
            row.addElement(cell)# agiiunge quella cella cioe quel testo alla riga 
            self.table.addElement(row) # aggiunge la riga , cioe cella alla tabella 
            
    #aggiunta dei dati dei libri al file 
    def add_books_data(self):
        for row_data in self.data:
            row = TableRow(stylename=self.row_style)
            for cell in row_data:
                cella = TableCell(stylename=self.cell_style)
                # cell e proprio la stringa in se
                
                data = str(cell).split()
                final_data = ""
                
                for word in data:
                    if word == "E" or word == "EDIZIONE" or word == "+"  or word == "/" or word == "-" or word == ".":
                        break
                    final_data += word + " "
                cella.addElement(P(text=str(final_data)))
                row.addElement(cella)
            self.table.addElement(row)
    
    #aggiunta della tabella al file spreadsheet
    def add_table_to_spreadsheet(self):
        self.doc.spreadsheet.addElement(self.table)
    
    #salvataggio  
    def save_ods(self , file_path , file_name):
        self.doc.save(f"{file_path}/{file_name}.ods")