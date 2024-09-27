import pandas as pd
from transformers import AutoModelForSequenceClassification, AutoTokenizer
import torch

# Load the Detoxify model
model_name = "unitary/toxic-bert"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)

# Load the Excel file and get the first column (assumed to contain text data)
file_path = 'files/Annotation_file_ML.xlsx'  # Replace with the path to your Excel file
df = pd.read_excel(file_path)

# List to store the results
results = []

# Iterate over each row in the first column (assuming it's named 'Text')
for text in df.iloc[:, 0]:
    # Preprocess text and predict toxicity
    inputs = tokenizer(text, return_tensors="pt", truncation=True)
    outputs = model(**inputs)

    # Get toxicity score (raw logits) and apply sigmoid to get probabilities
    logits = outputs.logits
    probs = torch.sigmoid(logits)

    # If you want to sum the probabilities or get the first toxicity score
    toxicity_score = probs[0][0].item()  # Extract the first toxicity score from the tensor

    # Save the result in a list (text and its toxicity score)
    results.append({'Text': text, 'Toxicity Score': toxicity_score})

# Convert the results to a DataFrame
output_df = pd.DataFrame(results)

# Save the result to a new Excel file
output_file = 'files/toxicity_scores.xlsx'
output_df.to_excel(output_file, index=False)

print(f"Results saved to {output_file}.")
