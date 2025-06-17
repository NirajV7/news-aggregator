from transformers import pipeline

print("Testing  Ai environment")
classifier = pipeline("zero-shot-classification")
result = classifier("Relience Industries merged with Tata Group", 
                    candidate_labels = ["Technology", "Business", "Politics" ])
print(f"Classification: {result['labels'][0]} ({result['scores'][0]:.0%} confidence)")