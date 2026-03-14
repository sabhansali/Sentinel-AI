from risk_measuring_engine.scoring_config import SCORING,THRESHOLDS

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


    # Add detector scores
    total += pii_result["risk_score"]

    total += db_result["risk_score"]

    total += secret_result["risk_score"]


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