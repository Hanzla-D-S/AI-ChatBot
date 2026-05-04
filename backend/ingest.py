import os
from dotenv import load_dotenv
from langchain_community.document_loaders import TextLoader, PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

load_dotenv()

DOCS_PATH = "./data/docs"
VECTOR_STORE_PATH = "./vector_store"


def load_documents():
    documents = []
    for filename in os.listdir(DOCS_PATH):
        filepath = os.path.join(DOCS_PATH, filename)
        if filename.endswith(".txt"):
            loader = TextLoader(filepath, encoding="utf-8")
            documents.extend(loader.load())
        elif filename.endswith(".pdf"):
            loader = PyPDFLoader(filepath)
            documents.extend(loader.load())
    print(f"Loaded {len(documents)} document(s)")
    return documents


def split_documents(documents):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )
    chunks = splitter.split_documents(documents)
    print(f"Split into {len(chunks)} chunks")
    return chunks


def build_vector_store(chunks):
    embeddings = OpenAIEmbeddings()
    vector_store = FAISS.from_documents(chunks, embeddings)
    vector_store.save_local(VECTOR_STORE_PATH)
    print(f"Vector store saved to '{VECTOR_STORE_PATH}'")


if __name__ == "__main__":
    print("Document ingestion.")
    docs = load_documents()
    chunks = split_documents(docs)
    build_vector_store(chunks)
    print("Ingestion complete.")
    
    
# Load Documents, split into chunks, create embeddings and stored in the faiss vector store.