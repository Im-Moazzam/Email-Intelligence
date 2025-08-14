from langchain_ollama import OllamaLLM
from langchain.prompts import PromptTemplate
from fetch_emails import fetch_latest_emails
import json

template = """
You are an assistant that classifies emails for the CEO.

Analyze the following email and return a JSON with the fields:
- concern: "Y" or "N" (Is this email concerning for the CEO?)
- category: one of ["urgency", "financial", "legal", "Executive Decisions Required"]
- urgency_level: 1 (lowest urgency) to 5 (highest urgency)
- requires_attention: "Y" or "N" (Should the CEO personally act on this?)

Email content:
{email}

Respond ONLY with valid JSON and nothing else.
"""

prompt = PromptTemplate(template=template, input_variables=["email"])
llm = OllamaLLM(model="llama3:latest")
chain = prompt | llm

def classify_emails(n=5):
    latest_emails = fetch_latest_emails(n=n)
    results = []
    
    for em in latest_emails:
        email_text = f"From: {em['from']}\nSubject: {em['subject']}\n\n{em['body']}"
        response = chain.invoke({"email": email_text})
        
        try:
            classification = json.loads(response)
            results.append({
                "from": em["from"],
                "subject": em["subject"],
                "urgency_level": classification.get("urgency_level", ""),
                "category": classification.get("category", ""),
                "concern": classification.get("concern", "N")
            })
        except json.JSONDecodeError:
            pass  # Skip invalid responses
    
    return results
