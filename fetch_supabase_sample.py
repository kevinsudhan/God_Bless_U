import requests
import json

def fetch_supabase_vitals():
    supabase_url = "https://wghhrmgntnzudopyvshe.supabase.co/rest/v1/vitals"
    headers = {
        "apikey": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6IndnaGhybWdudG56dWRvcHl2c2hlIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDc0Nzc0ODAsImV4cCI6MjA2MzA1MzQ4MH0.n2k0oaI4xD1bIRs4Yu9zkTIQ9uMdeyrizkVodjJlxk8",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6IndnaGhybWdudG56dWRvcHl2c2hlIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDc0Nzc0ODAsImV4cCI6MjA2MzA1MzQ4MH0.n2k0oaI4xD1bIRs4Yu9zkTIQ9uMdeyrizkVodjJlxk8"
    }
    
    try:
        response = requests.get(supabase_url, headers=headers)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error fetching data from Supabase: {e}")
        return []

# Fetch the data
vitals_data = fetch_supabase_vitals()

# Save to a file with pretty formatting
with open('supabase_data_sample.json', 'w') as f:
    json.dump(vitals_data, f, indent=4)

# Display the data
print("Supabase Data Sample:")
print(json.dumps(vitals_data, indent=4))
print(f"\nSaved to 'supabase_data_sample.json'")
