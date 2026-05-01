import os
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_groq import ChatGroq

load_dotenv()

# Initialize our components
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
db = Chroma(persist_directory="../chroma_db", embedding_function=embeddings)


llm = ChatGroq(model_name="llama-3.3-70b-versatile", temperature=0)

TRIAGE_PROMPT = """
You are an expert support triage agent for HackerRank, Claude, and Visa.
Your goal is to analyze the support ticket and decide:
1. Status: 'replied' (if safe and answerable) or 'escalated' (if high-risk, sensitive, or unknown).
2. Request Type: product_issue, feature_request, bug, or invalid.
3. Response: A grounded answer from the context.
4. Justification: Why you made this decision.

HIGH-RISK TOPICS (Always Escalate):
- Visa: Fraud, stolen cards, unauthorized transactions, legal disputes.
- Claude: Safety violations, jailbreak attempts, PII leaks.
- HackerRank: Cheating, enterprise contract changes, account deletions.

CONTEXT:
{context}

TICKET:
{issue}

Output your answer in this format:
Status: [status]
Area: [product area]
Type: [request_type]
Justification: [reason]
Response: [answer]
"""

def process_ticket(issue_text):
    # 1. Retrieve relevant docs from our new DB
    docs = db.similarity_search(issue_text, k=3)
    context = "\n".join([d.page_content for d in docs])
    
    # 2. Run Triage
    prompt = ChatPromptTemplate.from_template(TRIAGE_PROMPT)
    chain = prompt | llm
    
    response = chain.invoke({"context": context, "issue": issue_text})
    return response.content

# Test with a simple string
if __name__ == "__main__":
    test_issue = "How do I reset my password on HackerRank?"
    print(process_ticket(test_issue))