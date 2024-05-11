from langchain.text_splitter import RecursiveCharacterTextSplitter

def split_text_into_chunks(document):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=100,
        length_function=len
    )
    chunks = text_splitter.split_documents(document)
    return chunks