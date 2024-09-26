# NaviLaw

## Overview
The  **NaviLaw** system integrates the **ReAct** (Reasoning and Action Agentic Architecture) with **RAG** (Retrieval Augmented Generation), powered by the Llama3 70B language model, to manage tasks such as legal advisory, report generation, and case outcome prediction. This setup allows the system to act as an intelligent agent, conducting in-depth research on relevant legal databases and retrieving critical documents from user-uploaded files. Through sophisticated reasoning and document processing, it delivers actionable insights. Utilizing prebuilt tools and models, Law Navigator processes user queries, retrieves relevant legal excerpts, and dynamically generates responses, reports, or predictions, while ensuring real-time interactivity.

![img-1](https://github.com/LawNavigator/navilaw-ai/blob/main/Screenshot%202024-09-25%20193623.png)

## Features
- **Legal Query Processing:** Users can submit queries related to legal issues, and the system generates relevant insights based on the context of uploaded legal documents.
- **Document Upload:** Supports uploading multiple PDF documents for analysis and retrieval.
- **Legal Precedent Retrieval:** Automatically retrieves and summarizes relevant legal precedents based on the query.
- **Dynamic Report Generation:** Generates concise legal reports, including key findings, analysis, and recommendations.
- **AI-Powered Search:** Utilizes the Tavily Search tool for supplementary legal research when needed.

## Requirements
- Python 3.7 or higher
- FastAPI
- LangChain
- PyPDF2
- Tavily Search Tool
- Streamlit
- Other dependencies listed in `requirements.txt`

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/LawNavigator/navilaw-ai
   cd navilaw-ai
   ```
2. Set up a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```
3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   Create a `.env` file in the root directory and add your API keys:
   ```
   GROQ_API_KEY=your_api_key_here
   TAVILY_API_KEY=your_api_key_here
   HF_TOKEN = your_hf_token
   ```
## Usage
To start the FastAPI application, run:
```bash
uvicorn main:app --host 0.0.0.0 --port 10000
```
You can then access the API at `https://navilaw-ai.onrender.com/legal-assistance/`.

### API Endpoints
- **POST /legal-assistance/**: Submit a legal query along with PDF documents for analysis.
  - **Parameters:**
    - `query` (string): The legal question or issue.
    - `option` (string): The type of legal assistance requested (e.g., "Legal Advisory", "Legal Report Generation", "Case Outcome Prediction").
    - `files` (multiple PDF files): Legal documents relevant to the query.
  - **Response:**
    - Returns a JSON object with the results based on the chosen option.

## Example Request
```json
{
  "query": "Whatare the legal implications of XYZ Corp terminating the contract with ABC Ltd. due to non-payment? Can ABC Ltd. challenge the termination?",
  "option": "Legal Advisory",
  "files": ["contract.pdf", "case_law.pdf"]
}
```
## Demo Video
[Watch the video here](https://youtu.be/NzFPQV9l6pY?si=R9D_Zmb7tMv0fJ49)

## Disclaimer
This application is AI-generated and may not account for all real-world legal factors. It is not intended as a substitute for professional legal advice.

## License
This project is licensed under the MIT License. See the LICENSE file for details.

## Acknowledgments
- FastAPI for building the API
- LangChain for RAG capabilities
- PyPDF2 for PDF processing
- Tavily for supplementary legal research
- Streamlit for the User Interface


Feel free to customize any sections to better fit your project’s details or your preferred formatting style! Let me know if you need further adjustments or additional information.
