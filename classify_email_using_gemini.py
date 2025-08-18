import json
import re

from pydantic import BaseModel

from langchain.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_ollama import OllamaLLM

from fetch_emails import fetch_latest_emails

template = """
You are an assistant that classifies emails for the CEO.

Analyze the following email and return a JSON with the fields:
- concern: "Y" or "N" 
  (Mark as "Y" if the email contains urgent matters, financial/legal issues, executive decisions required, 
   OR if it expresses dissatisfaction, complaints, or any negative sentiment such as 'not happy', 'not good', 'not satisfied', 'unacceptable', etc.)
- category: one of ["urgency", "financial", "legal", "Executive Decisions Required", "negative feedback"]
- urgency_level: 1 (lowest urgency) to 5 (highest urgency)
- requires_attention: "Y" or "N" (Mark "Y" if the CEO should personally act on this or if it’s a serious negative sentiment from a key stakeholder)

Email content:
{email}

Respond ONLY with valid JSON and nothing else.
"""


prompt = PromptTemplate(template=template, input_variables=["email"])

llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0)
# llm = OllamaLLM(model="gemma2:2b")
chain = prompt | llm


class Classification(BaseModel):
    concern: str
    category: str
    urgency_level: int
    requires_attention: str


def parse_model_output(raw: str) -> Classification:
    # Remove ```json and ``` fences if present
    cleaned = re.sub(r"```json|```", "", raw).strip()
    try:
        return Classification.model_validate_json(cleaned)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON after cleaning: {e}")


def classify_emails(n=5):
    latest_emails = fetch_latest_emails(n=n)
    results = []

    for em in latest_emails:
        email_text = f"From: {em['from']}\nSubject: {em['subject']}\n\n{em['body']}"
        response = chain.invoke({"email": email_text})

        try:
            classification = parse_model_output(response.content)

            results.append(
                {
                    "from": em["from"],
                    "subject": em["subject"],
                    "urgency_level": classification.urgency_level,
                    "category": classification.category,
                    "concern": classification.concern,
                    "requires_attention": classification.requires_attention,
                }
            )

        except json.JSONDecodeError:
            print("Invalid JSON:", response)
            continue
    print(results)

    return results
