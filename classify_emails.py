from langchain_ollama import OllamaLLM
from langchain.prompts import PromptTemplate
from fetch_emails import fetch_latest_emails
import json
import re

template = """
You are an assistant that classifies emails for the CEO.

Analyze the following email and return a JSON with the fields:
- concern: "Y" or "N" 
  (Mark as "Y" if the email contains urgent matters, financial/legal issues, executive decisions required, 
   OR if it expresses dissatisfaction, complaints, or any negative sentiment such as 'not happy', 'not good', 'not satisfied', 'unacceptable', etc.)
- category: one of ["urgency", "financial", "legal", "Executive Decisions Required", "negative feedback"]
- urgency_level: 1 (lowest urgency) to 5 (highest urgency)
- requires_attention: "Y" or "N" (Mark "Y" if the CEO should personally act on this or if it’s a serious negative sentiment from a key stakeholder)
ONLY USE GIVEN CATEGORIES, DONT MAKE ANY NEW ON YOUR OWN.
Email content:
{email}

Respond ONLY with valid JSON and nothing else.
"""


prompt = PromptTemplate(template=template, input_variables=["email"])
llm = OllamaLLM(model="llama3:latest")
chain = prompt | llm

def parse_model_output(raw: str):
    """Extracts the first JSON object from the model output and parses it."""
    match = re.search(r"\{.*\}", raw, re.DOTALL)
    if not match:
        raise ValueError(f"No JSON object found in output: {raw}")
    try:
        return json.loads(match.group(0))
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON: {e}\nRaw JSON: {match.group(0)}")



def classify_emails(n: int = 5):
    """Fetches latest emails and classifies them according to the schema."""
    latest_emails = fetch_latest_emails(n=n)
    results = []

    for em in latest_emails:
        email_text = f"From: {em['from']}\nSubject: {em['subject']}\n\n{em['body']}"
        response = chain.invoke({"email": email_text})

        try:
            classification = parse_model_output(response)
            results.append({
                "from": em["from"],
                "subject": em["subject"],
                "urgency_level": classification["urgency_level"],
                "category": classification["category"],
                "concern": classification["concern"]
            })
            print(classification)
        except ValueError as e:
            print(f"Parse error: {e}\nRaw output:\n{response}")
            continue

    return results
