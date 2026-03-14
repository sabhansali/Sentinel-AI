import re
import math

def shannon_entropy(data):

    if not data:
        return 0

    entropy = 0

    for x in set(data):

        p_x = float(data.count(x))/len(data)

        entropy += - p_x*math.log2(p_x)

    return entropy


def detect_secrets(prompt):

    findings = []

    risk_score = 0

    # More flexible API patterns
    api_patterns = [

        r'sk-[A-Za-z0-9]{20,}',
        r'ghp_[A-Za-z0-9]{20,}',
        r'AIza[0-9A-Za-z\-_]{20,}',
        r'AKIA[0-9A-Z]{12,}',
        r'-----BEGIN PRIVATE KEY-----'

    ]

    for pattern in api_patterns:

        if re.search(pattern,prompt):

            findings.append("API key detected")

            risk_score += 50


    # Credential keywords
    credential_words = [

        "api key",
        "apikey",
        "secret",
        "password",
        "token",
        "private key",
        "auth key"

    ]

    for word in credential_words:
        if word in prompt.lower():
            findings.append("Credential keyword detected")
            risk_score += 20
            break


    # Better entropy detection
    candidates = re.findall(r'[A-Za-z0-9_\-]{16,}',prompt)

    for word in candidates:
        ent = shannon_entropy(word)
        if ent > 3.5:
            findings.append("High entropy token")
            risk_score += 30
            break

    if len(findings) >= 2:
        risk_score += 20

    risk_score = min(risk_score,100)

    return {
        "detector":"secrets",
        "risk_score":risk_score,
        "findings":findings

    }