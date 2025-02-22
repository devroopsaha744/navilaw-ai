import os
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from langchain_groq import ChatGroq
from PyPDF2 import PdfReader
from langchain.docstore.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableParallel
from langgraph.prebuilt import create_react_agent
from retrieval import create_retriever
from templates import advisor_template, predictor_template, generator_template
from langchain.tools.retriever import create_retriever_tool
from tools import tavily_tool
from dotenv import load_dotenv
from typing import List

load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")
chat = ChatGroq(model = "llama-3.3-70b-versatile", api_key=groq_api_key)
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def read_root():
    return {"message": "Welcome to the Legal Research API! Please use one of the endpoints for requests."}

def process_files(files: List[UploadFile]):
    if not files:
        raise HTTPException(status_code=400, detail="Please upload at least one PDF file.")
    docs = []
    for uploaded_file in files:
        reader = PdfReader(uploaded_file.file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        docs.append(Document(page_content=text, metadata={"source": uploaded_file.filename}))
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    pdf_content = text_splitter.split_documents(docs)
    return pdf_content

def setup_retriever(pdf_content):
    retriever = create_retriever(pdf_content)
    retrieval_tool = create_retriever_tool(
        retriever,
        "Pdf_content_retriever",
        "Searches and returns excerpts from the set of PDF docs.",
    )
    return retriever, retrieval_tool

def setup_agents(tools):
    advisor_graph = create_react_agent(chat, tools=tools, state_modifier=advisor_template)
    predictor_graph = create_react_agent(chat, tools=tools, state_modifier=predictor_template)
    return advisor_graph, predictor_graph

@app.post("/legal-assistance/")
async def legal_assistance(
    query: str = Form(...),
    option: str = Form(...),
    files: List[UploadFile] = File(...)
):
    if not query:
        raise HTTPException(status_code=400, detail="Please enter a query.")
    pdf_content = process_files(files)
    retriever, retrieval_tool = setup_retriever(pdf_content)
    tools = [tavily_tool, retrieval_tool]
    advisor_graph, predictor_graph = setup_agents(tools)
    inputs = {"messages": [("human", query)]}
    if option == "Legal Advisory":
        async for chunk in advisor_graph.astream(inputs, stream_mode="values"):
            final_result = chunk
        result = final_result["messages"][-1].content
        return {"result": result}
    elif option == "Legal Report Generation":
        set_ret = RunnableParallel({"context": retriever, "query": RunnablePassthrough()})
        rag_chain = set_ret | generator_template | chat | StrOutputParser()
        report = rag_chain.invoke(query)
        return {"report": report}
    elif option == "Case Outcome Prediction":
        async for chunk in predictor_graph.astream(inputs, stream_mode="values"):
            final_prediction = chunk
        prediction = final_prediction["messages"][-1]
        return {"prediction": prediction}
    else:
        raise HTTPException(status_code=400, detail="Invalid option selected.")

@app.post("/legal-advisory/")
async def legal_advisory_endpoint(
    query: str = Form(...),
    files: List[UploadFile] = File(...)
):
    if not query:
        raise HTTPException(status_code=400, detail="Please enter a query.")
    pdf_content = process_files(files)
    retriever, retrieval_tool = setup_retriever(pdf_content)
    tools = [tavily_tool, retrieval_tool]
    advisor_graph, _ = setup_agents(tools)
    inputs = {"messages": [("human", query)]}
    async for chunk in advisor_graph.astream(inputs, stream_mode="values"):
        final_result = chunk
    result = final_result["messages"][-1].content
    return {"result": result}

@app.post("/case-outcome-prediction/")
async def case_outcome_prediction_endpoint(
    query: str = Form(...),
    files: List[UploadFile] = File(...)
):
    if not query:
        raise HTTPException(status_code=400, detail="Please enter a query.")
    pdf_content = process_files(files)
    retriever, retrieval_tool = setup_retriever(pdf_content)
    tools = [tavily_tool, retrieval_tool]
    _, predictor_graph = setup_agents(tools)
    inputs = {"messages": [("human", query)]}
    async for chunk in predictor_graph.astream(inputs, stream_mode="values"):
        final_prediction = chunk
    prediction = final_prediction["messages"][-1].content
    return {"prediction": prediction}

@app.post("/report-generator/")
async def report_generator_endpoint(
    query: str = Form(...),
    files: List[UploadFile] = File(...)
):
    if not query:
        raise HTTPException(status_code=400, detail="Please enter a query.")
    pdf_content = process_files(files)
    retriever, _ = setup_retriever(pdf_content)
    set_ret = RunnableParallel({"context": retriever, "query": RunnablePassthrough()})
    rag_chain = set_ret | generator_template | chat | StrOutputParser()
    report = rag_chain.invoke(query)
    return {"report": report}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=10000)
