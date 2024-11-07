import camelot

file_name = "2B"
file_path = f"input_pdf/{file_name}.pdf"

# extract all the tables in the PDF file
abc = camelot.read_pdf("test.pdf")   #address of file location
 
# print the first table as Pandas DataFrame
