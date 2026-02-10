import pandas as pd
import os

# Load CSV
df = pd.read_csv("C:/Users/vippa/Downloads/archive/UpdatedResumeDataSet.csv")

# Number of rows per candidate
rows_per_candidate = 5

data = []
for i in range(0, len(df), rows_per_candidate):
    block = df.iloc[i:i+rows_per_candidate]
    
    skills = ", ".join(block[block['Category'].str.contains('Skills', na=False)]['Resume'].dropna())
    education = ", ".join(block[block['Category'].str.contains('Education', na=False)]['Resume'].dropna())
    experience = ", ".join(block[block['Category'].str.contains('Experience', na=False)]['Resume'].dropna())
    
    name = f"Candidate{i//rows_per_candidate + 1}"
    email = f"candidate{i//rows_per_candidate + 1}@example.com"
    
    data.append({
        "Name": name,
        "Email": email,
        "Skills": skills,
        "Experience": experience,
        "Education": education
    })

# Create clean dataframe
clean_df = pd.DataFrame(data)

# Make sure 'data' folder exists
os.makedirs("data", exist_ok=True)

# Save to CSV
clean_df.to_csv("data/resumes.csv", index=False)
print("resumes.csv created successfully!")
