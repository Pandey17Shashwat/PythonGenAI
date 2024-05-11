from langchain.document_loaders import CSVLoader
from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader, UnstructuredExcelLoader

def parse_file(file,file_format):
    print("The File Format is this :" + file_format)
    if file_format == "pdf":
        loader = PyPDFLoader(file)
    elif file_format == "docx":
        loader = Docx2txtLoader(file)
    elif file_format == "xls":
        loader = UnstructuredExcelLoader(file)
    elif file_format == "csv":
        loader = CSVLoader(file)
    else:
        raise ValueError("Unsupported file format")
    return loader.load()