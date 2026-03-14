import re

def detect_db_schema_leak(prompt):

    risk_score = 0

    findings = []

    matched_patterns = []

    # SQL operations
    SQL_OPERATIONS = r'\b(SELECT|INSERT|UPDATE|DELETE|JOIN|FROM|WHERE|GROUP BY|HAVING|ORDER BY)\b'

    # Schema definitions
    SCHEMA_WORDS = r'\b(CREATE TABLE|PRIMARY KEY|FOREIGN KEY|ALTER TABLE|INDEX|CONSTRAINT)\b'

    # Column listing patterns
    COLUMN_PATTERN = r'\b(id|customer_id|email|ssn|aadhaar|phone|risk_score|device_id|transaction_id|fraud_flag)\b'

    # Internal naming conventions
    INTERNAL_NAMES = r'\b(internal_|customer_|prod_|secure_|fraud_|risk_|payment_|transaction_|auth_|admin_)\w*'

    # ORM patterns (Django / SQLAlchemy)
    ORM_PATTERNS = r'\b(models\.Model|Column\(|ForeignKey|relationship\(|Integer\(|String\()\b'

    # NoSQL patterns
    NOSQL_PATTERNS = r'\b(collection|document|mongodb|mongo|firebase|dynamodb|cassandra)\b'

    # GraphQL schema patterns
    GRAPHQL_PATTERNS = r'\b(type Query|type Mutation|schema {|resolver|GraphQLObjectType)\b'

    # API contract patterns
    API_SCHEMA = r'\b(/api/|endpoint|POST|GET|PUT|PATCH|DELETE|request body|response schema)\b'

    # Table structure patterns
    TABLE_STRUCTURE = r'\b(Table:|Columns:|Fields:|Schema:)\b'

    if re.search(SQL_OPERATIONS,prompt,re.IGNORECASE):
        risk_score += 25
        findings.append("SQL query detected")
        matched_patterns.append("SQL")

    if re.search(SCHEMA_WORDS,prompt,re.IGNORECASE):
        risk_score += 40
        findings.append("Database schema definition detected")
        matched_patterns.append("Schema")

    if re.search(COLUMN_PATTERN,prompt,re.IGNORECASE):
        risk_score += 20
        findings.append("Sensitive column names detected")
        matched_patterns.append("Columns")

    if re.search(INTERNAL_NAMES,prompt,re.IGNORECASE):
        risk_score += 35
        findings.append("Internal table naming detected")
        matched_patterns.append("Internal names")

    if re.search(ORM_PATTERNS,prompt,re.IGNORECASE):
        risk_score += 30
        findings.append("ORM model structure detected")
        matched_patterns.append("ORM")

    if re.search(NOSQL_PATTERNS,prompt,re.IGNORECASE):
        risk_score += 25
        findings.append("NoSQL schema detected")
        matched_patterns.append("NoSQL")

    if re.search(GRAPHQL_PATTERNS,prompt,re.IGNORECASE):
        risk_score += 30
        findings.append("GraphQL schema detected")
        matched_patterns.append("GraphQL")

    if re.search(API_SCHEMA,prompt,re.IGNORECASE):
        risk_score += 20
        findings.append("API contract structure detected")
        matched_patterns.append("API")

    if re.search(TABLE_STRUCTURE,prompt,re.IGNORECASE):
        risk_score += 25
        findings.append("Structured schema description detected")
        matched_patterns.append("Structure")

    # Risk boost if multiple detected
    if len(matched_patterns) >= 3:
        risk_score += 20
        findings.append("Multiple architecture signals detected")

    # Cap risk
    risk_score = min(risk_score,100)

    return {

        "detector":"database_schema",

        "risk_score":risk_score,

        "findings":findings,

        "patterns_detected":matched_patterns

    }