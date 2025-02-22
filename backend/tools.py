from dotenv import load_dotenv
from langchain_community.tools import TavilySearchResults
from langchain.tools.retriever import create_retriever_tool
import os
load_dotenv()

tavily_api_key = os.getenv("TAVILY_API_KEY")

from langchain_community.tools import TavilySearchResults

tavily_tool = TavilySearchResults(
    max_results=5,
    search_depth="advanced",
    include_answer=True,
    include_raw_content=True,
    include_images=False,
    include_domains=[
        "indiankanoon.org",        # Indian case law
        "barandbench.com",         # Legal news and updates
        "legallyindia.com",        # Legal developments in India
        "scconline.com",           # Supreme Court Cases Online
        "lawtimesjournal.in",      # Legal news and case analysis
        "lawyersclubindia.com",    # Legal community discussions
        "vlex.in",                 # Global legal information with Indian focus
        "taxmann.com"              # Taxation and corporate law in India
    ],
    exclude_domains=["globalsearch.com", "genericnews.com"]
)

