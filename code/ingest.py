import os
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings

# 1. Force load the .env file from the current directory
load_dotenv(override=True)

# 2. DEBUG: Check if the key is actually loaded
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    print("❌ ERROR: OPENAI_API_KEY is still empty!")
    print(f"Current working directory: {os.getcwd()}")
    print("Files in this directory:", os.listdir("."))
else:
    # Print only the first 5 chars for safety
    print(f"✅ Key found! (Starts with: {api_key[:5]}...)")



def ingest_support_data():
    # Attempt to find the correct data directory
    # If you are in D:\hackerank, and the files are in the subfolder:
    # Inside code/ingest.py
    possible_paths = [
        "../data",                       # Go up to find the data folder
        "../../data",                    # Go up twice just in case
        "data"                           # Check local if they moved it
    ]
    
    base_dir = None
    for p in possible_paths:
        if os.path.exists(p) and os.path.isdir(p):
            base_dir = p
            break
            
    if not base_dir:
        print("❌ Error: Could not find 'data' folder. Make sure you are running the script from the root of the repo.")
        return

    persist_dir = "chroma_db"
    all_docs = []
    companies = ["hackerrank", "claude", "visa"]

    for company in companies:
        path = os.path.join(base_dir, company)
        if os.path.exists(path):
            print(f"--- Loading {company} corpus from {path} ---")
            
            # Using silent_errors=True and forcing utf-8 encoding to prevent the crashes you saw
            loader = DirectoryLoader(
                path, 
                glob="**/*.md", 
                loader_cls=TextLoader, 
                loader_kwargs={'encoding': 'utf-8'},
                silent_errors=True
            )
            
            try:
                company_docs = loader.load()
                for doc in company_docs:
                    doc.metadata["company"] = company
                all_docs.extend(company_docs)
                print(f"✅ Loaded {len(company_docs)} files from {company}")
            except Exception as e:
                print(f"⚠️ Minor issue loading {company}: {e}")

    if not all_docs:
        # If no .md files, try .txt
        print("No .md files found, trying .txt...")
        loader = DirectoryLoader(base_dir, glob="**/*.txt", loader_cls=TextLoader, loader_kwargs={'encoding': 'utf-8'})
        all_docs = loader.load()

    if not all_docs:
        print("❌ Final Error: Still no documents found. Check if the files are actually in the folders.")
        return

    # Splitting logic
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    chunks = text_splitter.split_documents(all_docs)
    
    print(f"--- Creating Vector DB with {len(chunks)} chunks ---")
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    Chroma.from_documents(
        documents=chunks, 
        embedding=embeddings, 
        persist_directory=persist_dir
    )
    print(f"🚀 Success! Knowledge base saved to '{persist_dir}'")

if __name__ == "__main__":
    ingest_support_data()