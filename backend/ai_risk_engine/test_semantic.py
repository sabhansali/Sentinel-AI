from ai_risk_engine.detection.semantic_detector import check_semantic_risk
from ai_risk_engine.detection.db_schema_detector import detect_db_schema_leak
from ai_risk_engine.detection.pii_detector import detect_pii

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