from config import AI_DOMAINS

def detect_ai_tool(domain):

    for ai_domain in AI_DOMAINS:

        if ai_domain in domain:

            return {
                "tool": AI_DOMAINS[ai_domain],
                "domain": domain
            }

    return None