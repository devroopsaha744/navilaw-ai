#RAG method
from PyPDF2 import PdfReader
from langchain.document_loaders import PyPDFLoader
from langchain.docstore.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceInferenceAPIEmbeddings
from langchain_core.vectorstores import InMemoryVectorStore
from dotenv import load_dotenv
import os

load_dotenv()
hf_token = os.getenv("HF_TOKEN")

def load_and_chunk_pdfs(directory_path):
    docs = []
    
    for filename in os.listdir(directory_path):
        if filename.endswith(".pdf"):
            file_path = os.path.join(directory_path, filename)
            
            reader = PdfReader(file_path)
            text = ""
            for page in reader.pages:
                text += page.extract_text()
            
            doc = Document(page_content=text, metadata={"source": filename})
            docs.append(doc)
    
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    
    chunked_docs = text_splitter.split_documents(docs)
    return chunked_docs


def create_retriever(documents: list):
    """
    Function to create and return a retriever using HuggingFace Embeddings and InMemory VectorStore.

    Args:
        api_key (str): Hugging Face API key.
        model_name (str): The model name for sentence transformer embeddings.
        documents (list): The list of documents to be embedded and added to the vectorstore.

    Returns:
        retriever: A retriever object to query the vector store.
    """
    embeddings = HuggingFaceInferenceAPIEmbeddings(api_key=hf_token, model_name="sentence-transformers/all-MiniLM-l6-v2")

    vectorstore = InMemoryVectorStore(embedding=embeddings)
    vectorstore.add_documents(documents)

    return vectorstore.as_retriever()


