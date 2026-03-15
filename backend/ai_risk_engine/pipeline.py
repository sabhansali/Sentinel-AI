from ai_risk_engine.detection.semantic_detector import check_semantic_risk
from ai_risk_engine.detection.db_schema_detector import detect_db_schema_leak
from ai_risk_engine.detection.pii_detector import detect_pii
from ai_risk_engine.detection.secret_detector import detect_secrets
from ai_risk_engine.detection.ast_engine.engine import sanitize_code, restore_names

from ai_risk_engine.risk_measuring_engine.risk_aggregator import calculate_final_risk


def analyze_prompt(prompt):

    code_detected = False
    sanitized_prompt = prompt
    mapping = {}

    if "def " in prompt or "class " in prompt:

        result = sanitize_code(prompt)

        if result["status"] == "success":
            code_detected = True
            sanitized_prompt = result["sanitized_code"]
            mapping = result["mapping"]

    semantic_similarity,semantic_results = check_semantic_risk(sanitized_prompt)
    pii_result = detect_pii(sanitized_prompt)
    db_result = detect_db_schema_leak(sanitized_prompt)
    secret_result = detect_secrets(sanitized_prompt)
    final = calculate_final_risk(

        semantic_similarity,
        pii_result,
        db_result,
        secret_result
    )

    return {
        "original":prompt,
        "sanitized":sanitized_prompt,
        "mapping":mapping,
        "code_detected":code_detected,
        "semantic_similarity":semantic_similarity,
        "pii":pii_result,
        "db":db_result,
        "secrets":secret_result,
        "final":final

    }