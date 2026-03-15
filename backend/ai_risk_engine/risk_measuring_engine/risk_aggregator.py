from ai_risk_engine.risk_measuring_engine.scoring_config import SCORING, THRESHOLDS
from .scoring_config import SCORING, THRESHOLDS

def calculate_final_risk(

    semantic_similarity,
    pii_result,
    db_result,
    secret_result

):

    total = 0

    # Semantic scoring

    if semantic_similarity > 0.65:

        total += SCORING["semantic_high"]

    elif semantic_similarity > 0.45:

        total += SCORING["semantic_medium"]


    # PII scoring

    if pii_result["risk_score"] > 20:

        total += SCORING["pii_high"]

    elif pii_result["risk_score"] > 5:

        total += SCORING["pii_medium"]


    # DB schema scoring

    if db_result["risk_score"] > 10:

        total += SCORING["db_schema_high"]


    # Secrets scoring

    if secret_result["risk_score"] > 20:

        total += SCORING["secrets_high"]


    total = min(total,100)


    if total >= THRESHOLDS["block"]:

        decision = "BLOCK"

    elif total >= THRESHOLDS["review"]:

        decision = "REVIEW"

    else:

        decision = "ALLOW"


    return {

        "total_risk":total,

        "decision":decision

    }