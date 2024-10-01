import os
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from langchain_groq import ChatGroq
from PyPDF2 import PdfReader
from langchain.docstore.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableParallel
from langgraph.prebuilt import create_react_agent
from retrieval import create_retriever
from templates import advisor_template, predictor_template, generator_template
from langchain.tools.retriever import create_retriever_tool
from tools import tavily_tool
from dotenv import load_dotenv
from typing import List

# Load environment variables
load_dotenv()

# Set up API key and Langchain model
groq_api_key = os.getenv("GROQ_API_KEY")
chat = ChatGroq(model="llama3-groq-8b-8192-tool-use-preview", api_key=groq_api_key)

app = FastAPI()
# Adding CORS middleware to allow all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)
@app.get("/")
async def read_root():
    return {"message": "Welcome to the Legal Research API! Please use the /legal-assistance/ endpoint for requests."}


@app.post("/legal-assistance/")
async def legal_assistance(
    query: str = Form(...), 
    option: str = Form(...), 
    files: List[UploadFile] = File(...)
):
    # Validate file upload and query
    if not files:
        raise HTTPException(status_code=400, detail="Please upload at least one PDF file.")
    
    if not query:
        raise HTTPException(status_code=400, detail="Please enter a query.")

    # Create a list to hold the loaded PDF content
    docs = []
    for uploaded_file in files:
        # Read the PDF file directly from the uploaded file
        reader = PdfReader(uploaded_file.file)  # Using the in-memory file
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        
        # Create a Document object from the extracted text
        docs.append(Document(page_content=text, metadata={"source": uploaded_file.filename}))

    # Set up the text splitter to chunk documents
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)

    # Split the loaded documents into chunks
    pdf_content = text_splitter.split_documents(docs)

    # Create a retriever from the PDF content
    retriever = create_retriever(pdf_content)
    retrieval_tool = create_retriever_tool(
        retriever,
        "Pdf_content_retriever",
        "Searches and returns excerpts from the set of PDF docs.",
    )

    #Defining the checkpointer
    memory = MemorySaver()

    # Tools setup for different options
    tools = [tavily_tool, retrieval_tool]

    # Create Langchain agents based on the task
    advisor_graph = create_react_agent(chat, tools=tools, interrupt_before=["tools"], checkpointer=memory, state_modifier=advisor_template)
    predictor_graph = create_react_agent(chat, tools=tools,interrupt_before=["tools"], checkpointer=memory, state_modifier=predictor_template)
    

    inputs = {"messages": [("human", query)]}

    # Process the request based on the selected option
    if option == "Legal Advisory":
        async for chunk in advisor_graph.astream(inputs, stream_mode="values"):
            final_result = chunk

        result = final_result["messages"][-1].content
        return {"result": result}

    elif option == "Legal Report Generation":
         set_ret = RunnableParallel(
    {"context": retriever, "query": RunnablePassthrough()} 
)
         rag_chain = set_ret |  generator_template | chat | StrOutputParser()
         report = rag_chain.invoke(query)
         return {"report": report}

    elif option == "Case Outcome Prediction":
        async for chunk in predictor_graph.astream(inputs, stream_mode="values"):
            final_prediction = chunk

        prediction = final_prediction["messages"][-1].content
        return {"prediction": prediction}

    else:
        raise HTTPException(status_code=400, detail="Invalid option selected.")


# Ensure that the server starts properly
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=10000)




