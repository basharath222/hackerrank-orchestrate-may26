
import pandas as pd
from dotenv import load_dotenv

import sys
import os

# Get the path to the 'src' directory relative to this script
# Since main.py is in 'code' and triage is in 'src', we go up one level then into 'src'
current_dir = os.path.dirname(os.path.realpath(__file__))
src_path = os.path.join(current_dir, '..', '..', 'hackerrank-orchestrate-may26/src')
sys.path.append(os.path.abspath(src_path))

# Now this should work
from triage import process_ticket

load_dotenv()

def main():
    # Adjusted paths based on your repo structure
    input_path = "../support_tickets/support_tickets.csv"
    output_path = "../support_tickets/output.csv"

    if not os.path.exists(input_path):
        print(f"❌ Could not find input file at {input_path}")
        return

    print(f"--- Starting Support Triage Agent ---")
    df = pd.read_csv(input_path)
    
    # DEBUG: Print columns to see exactly what they are named
    print(f"Detected columns: {df.columns.tolist()}")

    results = []

    for index, row in df.iterrows():
        # 1. Standardize column names to lowercase to handle 'Company' vs 'company'
        row_clean = {k.lower(): v for k, v in row.items()}
        
        comp = row_clean.get('company', 'Unknown') 
        subj = row_clean.get('subject', 'No Subject')
        iss  = row_clean.get('issue', 'No Issue Content')

        # 2. Combine for the AI
        full_issue = f"Company: {comp}\nSubject: {subj}\nIssue: {iss}"
        
        # Debug print to ensure data is actually being captured now
        print(f"[{index+1}/{len(df)}] Processing -> Co: {comp}, Sub: {str(subj)[:30]}...")

        try:
            # 3. Call the AI logic (Only once!)
            raw_output = process_ticket(full_issue)
            
            # 4. Parse the structured output
            lines = raw_output.strip().split('\n')
            parsed = {}
            for line in lines:
                if ":" in line:
                    key, val = line.split(":", 1)
                    parsed[key.strip().lower()] = val.strip()

            # 5. Append the structured data
            results.append({
                "status": parsed.get("status", "escalated"),
                "product_area": parsed.get("area", "General"),
                "response": parsed.get("response", "Internal Error"),
                "justification": parsed.get("justification", "Processed by AI."),
                "request_type": parsed.get("type", "product_issue")
            })
            
        except Exception as e:
            print(f"❌ Error on ticket {index}: {e}")
            results.append({
                "status": "escalated",
                "product_area": "Error",
                "response": "An error occurred during processing.",
                "justification": str(e),
                "request_type": "invalid"
            })

    # Save final results
    output_df = pd.DataFrame(results)
    output_df.to_csv(output_path, index=False)
    print(f"✅ Final predictions saved to {output_path}")

if __name__ == "__main__":
    main()