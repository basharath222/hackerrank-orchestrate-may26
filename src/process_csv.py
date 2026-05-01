import pandas as pd
import os
from triage import process_ticket

def run_challenge():
    input_file = "hackerrank-orchestrate-may26/support_tickets/support_tickets.csv"
    output_file = "hackerrank-orchestrate-may26/support_tickets/output.csv"

    if not os.path.exists(input_file):
        print(f"❌ Input CSV not found at {input_file}")
        return

    print(f"--- Starting CSV Processing: {input_file} ---")
    df = pd.read_csv(input_file)

    results = []
    for index, row in df.iterrows():
        print(f"Processing ticket {index + 1}/{len(df)}...")
        
        # Combine subject and issue for better context
        full_issue = f"Subject: {row['subject']}\nIssue: {row['issue']}"
        
        # Call the triage logic we built in the previous step
        ai_output = process_ticket(full_issue)
        
        # Parse the AI's string response back into a dictionary (simplified for now)
        # In a real build, you'd use structured output or regex here
        results.append({
            "status": "replied", # Defaulting; your AI should determine this
            "product_area": "General",
            "response": ai_output,
            "justification": "Grounded in corpus.",
            "request_type": "product_issue"
        })

    # Save to CSV
    output_df = pd.DataFrame(results)
    output_df.to_csv(output_file, index=False)
    print(f"✅ Done! Results saved to {output_file}")

if __name__ == "__main__":
    run_challenge()