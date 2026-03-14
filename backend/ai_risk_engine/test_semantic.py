from ai_risk_engine.detection.semantic_detector import check_semantic_risk

prompt = input("Enter prompt: ")

similarity,results = check_semantic_risk(prompt)

print("\nSemantic Matches:")

for r in results:

    print("Source:",r["source"])

    print("Similarity:",round(r["similarity"],2))

    print()

print("Max similarity:",round(similarity,2))