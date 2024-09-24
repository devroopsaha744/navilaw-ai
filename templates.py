from pydantic import BaseModel, Field
from typing import Literal
from langchain.prompts import PromptTemplate
advisor_template = """You are a legal research assistant tasked with providing 
legal advice based on the given vectorstore context. If needed, conduct 
additional research using the Tavily Search tool. Analyze the query for 
specific legal issues, reference relevant sections of legal documents, and 
ensure jurisdictional relevance. Consider conflicting interpretations or 
unclear areas of law, and provide practical recommendations or next steps. 
Include a disclaimer regarding the limitations of AI-generated legal advice.."""


predictor_template = """
You are a legal research assistant tasked with predicting the outcome of a 
legal case using the provided vectorstore context. If needed, conduct 
additional research using the Tavily Search tool. Analyze relevant legal 
precedents, evidence, and arguments, and reference supporting sections from 
legal documents. Provide a prediction of the case outcome with confidence 
intervals (e.g., 70 percent hance of a favorable outcome), considering 
jurisdictional differences. Highlight any uncertainties that could impact the
 result, and include a disclaimer about the limitations of AI-generated 
 predictions in real-world legal decisions.
"""

example_generator_template = """
---
### Legal Report template
**Task Overview:**
Generate a concise legal report based on the provided vectorstore according to the 
context and query:
{context}

query: {query}
**Report Structure:**
1. **Title:**
   - Clear and descriptive.
2. **Introduction:**
   - State the legal issue addressed.
3. **Legal Precedents:**
   - Summarize relevant precedents that apply.
4. **Key Findings:**
   - Present significant evidence and findings.
5. **Analysis:**
   - Discuss implications and potential outcomes.
6. **Conclusion:**
   - Summarize main points and recommendations.
7. **Disclaimer:**
   - Acknowledge that the report is AI-generated and may not account for all legal factors.
---
This streamlined template ensures clarity and professionalism without being overly detailed. Let me know if you need any adjustments!
"""

generator_template = PromptTemplate.from_template(template=example_generator_template)


class LegalReportResponse(BaseModel):
    """Respond to the user with this"""
    return_direct: bool = False
    case_summary: str = Field(description="A concise summary of the legal case")
    relevant_precedents: str = Field(description="Key legal precedents or statutes relevant to the case")
    evidence_analysis: str = Field(description="Summary of evidence and arguments presented by both sides")
    key_findings: str = Field(description="Important findings or factors that influence the case")
    conclusion: str = Field(description="A brief conclusion based on the analysis")

class CaseOutcomePredictionResponse(BaseModel):
    """Respond to the user with this"""
    return_direct: bool = False
    outcome_prediction: str = Field(description="Predicted outcome of the case")
    confidence_interval: str = Field(description="Confidence interval for the prediction (e.g., 70% chance for the plaintiff)")
    jurisdiction: str = Field(description="The legal jurisdiction relevant to the prediction")
    uncertainty_factors: str = Field(description="Factors that might lead to different outcomes")
    disclaimer: str = Field(description="AI-generated prediction disclaimer for limitations")

class LegalAdviceResponse(BaseModel):
    """Respond to the user with this"""
    return_direct: bool = False
    legal_issue: str = Field(description="The specific legal issue or query addressed")
    advice: str = Field(description="The legal advice or recommendation provided based on the given context")
    relevant_sections: str = Field(description="Relevant sections from legal documents or case law supporting the advice")
    jurisdiction: str = Field(description="The jurisdiction applicable to the legal advice")
    conflicting_interpretations: str = Field(description="Any conflicting interpretations or unclear areas of law")
    next_steps: str = Field(description="Practical recommendations or next steps for the user to take")
    disclaimer: str = Field(description="AI-generated legal advice disclaimer for limitations")
