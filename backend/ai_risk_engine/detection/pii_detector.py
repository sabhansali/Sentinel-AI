from presidio_analyzer import AnalyzerEngine
from presidio_analyzer import PatternRecognizer
from presidio_analyzer import Pattern
import re

analyzer = AnalyzerEngine()

# Custom Aadhaar recognizer
aadhaar_pattern = Pattern(
    name="aadhaar",
    regex=r'\b\d{4}-\d{4}-\d{4}\b',
    score=0.85
)

aadhaar_recognizer = PatternRecognizer(
    supported_entity="AADHAAR",
    patterns=[aadhaar_pattern]
)

analyzer.registry.add_recognizer(aadhaar_recognizer)


# PAN recognizer
pan_pattern = Pattern(
    name="pan",
    regex=r'\b[A-Z]{5}[0-9]{4}[A-Z]\b',
    score=0.85
)

pan_recognizer = PatternRecognizer(
    supported_entity="PAN",
    patterns=[pan_pattern]
)

analyzer.registry.add_recognizer(pan_recognizer)


def detect_pii(prompt):

    results = analyzer.analyze(
        text=prompt,
        language='en'
    )

    findings = []

    risk_score = 0

    for r in results:

        findings.append({

            "entity":r.entity_type,

            "score":round(r.score,2),

            "start":r.start,

            "end":r.end

        })

        risk_score += 10

    # Boost risk if multiple PII types
    entity_types = set([r.entity_type for r in results])

    if len(entity_types) >= 3:

        risk_score += 30

    if len(results) >= 5:

        risk_score += 40

    risk_score = min(risk_score,100)

    return {

        "detector":"pii",

        "risk_score":risk_score,

        "findings":findings,

        "entities_detected":list(entity_types)

    }