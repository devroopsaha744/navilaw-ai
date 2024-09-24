#RAG method
from PyPDF2 import PdfReader
from langchain.document_loaders import PyPDFLoader
from langchain.docstore.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceInferenceAPIEmbeddings
from langchain_core.vectorstores import InMemoryVectorStore
from dotenv import load_dotenv
import os

#Configuring API keys
load_dotenv()
hf_token = os.getenv("HF_TOKEN")

# Function to load and chunk PDF documents
def load_and_chunk_pdfs(directory_path):
    docs = []
    
    # Iterate through all PDFs in the directory
    for filename in os.listdir(directory_path):
        if filename.endswith(".pdf"):
            file_path = os.path.join(directory_path, filename)
            
            # Load the PDF
            reader = PdfReader(file_path)
            text = ""
            for page in reader.pages:
                text += page.extract_text()
            
            # Create a Document object from the extracted text
            doc = Document(page_content=text, metadata={"source": filename})
            docs.append(doc)
    
    # Set up the text splitter to chunk documents
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    
    # Split the loaded documents into chunks
    chunked_docs = text_splitter.split_documents(docs)
    return chunked_docs


# Extract text from PDFs
#pdf_directory = "input"  # Replace with your actual directory path
#pdf_content = load_and_chunk_pdfs(pdf_directory)

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
    # Set up the Hugging Face embeddings
    embeddings = HuggingFaceInferenceAPIEmbeddings(api_key=hf_token, model_name="sentence-transformers/all-MiniLM-l6-v2")

    # Set up the vector store and add documents
    vectorstore = InMemoryVectorStore(embedding=embeddings)
    vectorstore.add_documents(documents)

    # Return the retriever object
    return vectorstore.as_retriever()



