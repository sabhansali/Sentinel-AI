from ai_risk_engine.detection.semantic_detector import check_semantic_risk
from ai_risk_engine.detection.db_schema_detector import detect_db_schema_leak
from ai_risk_engine.detection.pii_detector import detect_pii
from ai_risk_engine.detection.secret_detector import detect_secrets
# from ai_risk_engine.risk_measuring_engine.risk_aggregator import calculate_final_risk

prompt = input("Enter prompt: ")

similarity,results = check_semantic_risk(prompt)

print("\nSemantic Matches:")

for r in results:
    print("Source:",r["source"])
    print("Similarity:",round(r["similarity"],2))
    print()
print("Max similarity:",round(similarity,2))

db_result = detect_db_schema_leak(prompt)
print("\nDB Schema Detection:")
print("Risk score:",db_result["risk_score"])
for f in db_result["findings"]:
    print("-",f)


result = detect_pii(prompt)
print("\nPII Detection:")
print("Risk score:",result["risk_score"])
print("Entities detected:")
for e in result["entities_detected"]:
    print("-",e)

secret_result = detect_secrets(prompt)
print("\nSecret Detection:")
print("Risk score:",secret_result["risk_score"])
for f in secret_result["findings"]:
    print("-",f)

# final = calculate_final_risk(
#     similarity,
#     result,
#     db_result,
#     secret_result

# )
# print("\nFINAL DECISION:")
# print("Total risk:",final["total_risk"])
# print("Decision:",final["decision"])