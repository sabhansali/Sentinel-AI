def match_ai_domain(domain, ai_domains):

    for key in ai_domains:

        if key in domain:
            return ai_domains[key]

    return None