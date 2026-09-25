 # SentinelAI

SentinelAI is an enterprise AI security gateway for detecting and controlling sensitive information sent to generative AI tools. It combines prompt inspection, source-code anonymization, risk scoring, AI-service traffic monitoring, and administrator analytics.

The project is designed to help organizations identify shadow AI usage and prevent confidential information from leaving internal systems through AI prompts.

## What It Does

SentinelAI provides four connected capabilities:

- **Prompt risk analysis:** checks prompts for semantic similarity to confidential internal knowledge, personally identifiable information (PII), database/schema details, and secrets.
- **Source-code sanitization:** parses Python code with the AST module and replaces identifiers such as classes, functions, variables, and attributes with neutral names before a prompt is sent to an AI model. The original names can be restored in the response.
- **AI traffic monitoring:** observes DNS traffic for configured AI services, detects possible use of ChatGPT, Gemini, or GitHub Copilot, optionally checks whether an IDE is running, and reports events to the backend.
- **Security analytics:** records prompt-analysis outcomes by device and displays totals, risk distribution, prompt categories, and actions in a Streamlit administration dashboard.

## Main Workflow

```text
User prompt or Python code
	   |
	   v
   Streamlit Gateway UI
	   |
	   v
   analyze_prompt()
	   |
    +-----+----------------+----------------+----------------+
    |                      |                |                |
    v                      v                v                v
Code AST sanitizer   Semantic detector   PII detector   Schema/secret detectors
    |                      |                |                |
    +----------------------+----------------+----------------+
			      v
		      Risk aggregator
			      |
	      ALLOW / REVIEW / BLOCK decision
			      |
	      Log result and optionally call Gemini
```

The separate traffic-monitoring path watches DNS requests:

```text
DNS packet -> Known AI domain detector -> IDE process check -> FastAPI /ai-usage endpoint
```

## Features

### Prompt and code inspection

The analysis pipeline in `backend/ai_risk_engine/pipeline.py` performs these checks:

1. Detects likely Python code by looking for `def ` or `class `.
2. Parses and sanitizes detected code with Python `ast`.
3. Generates a semantic embedding for the sanitized prompt.
4. Searches the confidential knowledge base with FAISS.
5. Detects PII with Microsoft Presidio, including custom Aadhaar and PAN recognizers.
6. Detects database and API schema leakage using regular-expression patterns.
7. Detects API keys, credential keywords, private-key markers, and high-entropy tokens.
8. Combines detector results into a score from 0 to 100.
9. Returns an `ALLOW`, `REVIEW`, or `BLOCK` decision.

### Risk scoring

The scoring configuration is in `backend/ai_risk_engine/risk_measuring_engine/scoring_config.py`:

| Signal | Score contribution |
| --- | ---: |
| High semantic similarity | 50 |
| Medium semantic similarity | 30 |
| High PII risk | 25 |
| Medium PII risk | 15 |
| High database-schema risk | 25 |
| High secret risk | 40 |

Scores are capped at 100. Decisions use these thresholds:

- `0-49`: `ALLOW`
- `50-79`: `REVIEW`
- `80-100`: `BLOCK`

The current Streamlit gateway blocks prompts with a `BLOCK` decision. Allowed prompts can be sent to Gemini. For code prompts, the code is sanitized before being sent and the response is restored using the generated identifier mapping.

### Semantic knowledge base

Confidential reference files are stored in `backend/ai_risk_engine/confidential_data/`. The embedding build process:

1. Reads each file.
2. Normalizes whitespace.
3. Splits text into chunks of 200 words.
4. Encodes chunks using the `all-MiniLM-L6-v2` Sentence Transformers model.
5. Stores vectors in a FAISS `IndexFlatL2` index.
6. Stores source names and chunk text in `metadata.pkl`.

The generated files are stored in `backend/ai_risk_engine/vector_store/` and are loaded by the semantic detector at import time.

### AI traffic monitoring

The monitor in `backend/ai_traffic_monitor/` uses Scapy to inspect UDP DNS traffic on port 53. It currently recognizes configured domains for:

- ChatGPT/OpenAI
- GitHub Copilot
- Gemini

When a known domain is found, the monitor checks for `Code.exe` or `cursor.exe`, labels the activity as browser or IDE usage, and can send an event to the FastAPI backend. Domains are de-duplicated during the process lifetime.

### Browser extension

The Manifest V3 extension in `frontend/browser_extension/` supports ChatGPT/OpenAI pages. It:

- Watches editable fields for input.
- Extracts Python fenced code blocks when present.
- Debounces input for 600 ms.
- Sends code to the local `/sanitize` API.
- Stores the latest identifier mapping in Chrome local storage.
- Displays the original-to-anonymized mapping in its popup.

The extension currently performs sanitization and mapping display. It does not itself submit prompts to an AI service or enforce the full risk decision pipeline.

## Technology Stack

### Backend

- Python 3.13+
- FastAPI and Uvicorn for the local API
- Pydantic for request validation
- Streamlit for the prompt gateway and admin dashboard
- Sentence Transformers with `all-MiniLM-L6-v2` for embeddings
- FAISS for vector similarity search
- NumPy for embedding arrays
- Microsoft Presidio Analyzer for PII detection
- spaCy and `phonenumbers` as Presidio-related NLP dependencies
- Custom Python AST processing for code sanitization
- Google Generative AI SDK for Gemini 2.5 Flash
- Scapy for DNS packet sniffing
- psutil for IDE process detection
- Pandas and Plotly for dashboard analytics
- JSON and Pickle for local persistence of logs and vector metadata

### Frontend

- Chrome Manifest V3 browser extension
- HTML, CSS, and vanilla JavaScript
- Chrome `storage`, `scripting`, and `activeTab` APIs

The project does not directly use LangChain or TensorFlow. Hugging Face and PyTorch are used indirectly through the Sentence Transformers dependency rather than imported directly by the application code.

## Project Structure

```text
Sentinel-AI/
├── README.md
├── backend/
│   ├── requirements.txt              # Python runtime dependencies
│   ├── pyproject.toml                # Python project metadata and core dependencies
│   ├── main.py                       # Minimal backend entry point
│   ├── api_gateway/
│   │   └── main.py                   # FastAPI endpoints
│   ├── ai_risk_engine/
│   │   ├── pipeline.py               # End-to-end prompt analysis
│   │   ├── data_tracker.py            # JSON-backed analysis tracking
│   │   ├── analysis_log.json          # Stored analysis records
│   │   ├── confidential_data/         # Reference data used by semantic detection
│   │   ├── vector_store/              # Generated FAISS index and metadata
│   │   ├── detection/
│   │   │   ├── semantic_detector.py   # Similarity search against confidential data
│   │   │   ├── pii_detector.py        # Presidio PII analysis
│   │   │   ├── db_schema_detector.py  # Schema and API pattern detection
│   │   │   ├── secret_detector.py     # Secret and token detection
│   │   │   └── ast_engine/            # Python code parsing and anonymization
│   │   ├── embeddings/
│   │   │   ├── build_embeddings.py    # Builds the FAISS knowledge base
│   │   │   └── embedding_model.py     # Loads Sentence Transformers
│   │   ├── llm/
│   │   │   └── gemini_client.py       # Gemini API client
│   │   ├── risk_measuring_engine/
│   │   │   ├── risk_aggregator.py     # Combines detector scores
│   │   │   └── scoring_config.py       # Weights and decision thresholds
│   │   └── utils/
│   │       ├── chunker.py              # Word-based text chunking
│   │       └── text_cleaner.py         # Whitespace normalization
│   ├── ai_traffic_monitor/
│   │   ├── main.py                   # Starts the DNS monitor
│   │   ├── dns_sniffer.py             # Scapy packet capture and event handling
│   │   ├── detector.py                # Known AI-domain matching
│   │   ├── process_detector.py        # IDE process detection
│   │   ├── notifier.py                # Sends events to FastAPI
│   │   └── config.py                  # Domains, device ID, and endpoint settings
│   ├── gateway_ui.py                  # Streamlit prompt analysis interface
│   ├── admin_dashboard.py              # Streamlit security analytics dashboard
│   └── generate_test_data.py           # Generates local dashboard records
└── frontend/
    └── browser_extension/
	 ├── manifest.json              # Extension metadata and permissions
	 ├── content_script.js          # Detects editable page input
	 ├── background.js              # Calls the local sanitizer API
	 ├── popup.html                 # Mapping popup markup
	 ├── popup.js                   # Mapping rendering and storage access
	 └── styles.css                 # Popup styling
```

## Use Cases

- Prevent employees from sending customer PII, internal schemas, or proprietary logic to public AI tools.
- Sanitize source code before using an external AI assistant for debugging or explanation.
- Identify use of unmanaged AI services on employee devices.
- Give security or IT teams device-level visibility into prompt volume and enforcement actions.
- Build a local proof of concept for an enterprise AI data-loss-prevention gateway.
- Compare prompt risk categories and review blocked or sanitized activity.

## Prerequisites

- Windows, macOS, or Linux for the Python services. DNS sniffing may require additional packet-capture permissions and drivers.
- Python 3.13 or newer, as specified by `backend/pyproject.toml`.
- A virtual environment.
- Chrome or Chromium if you want to use the browser extension.
- A Gemini API key only if you want the gateway to forward allowed prompts to Gemini.

## Installation

From the repository root, create and activate a virtual environment:

### Windows PowerShell

```powershell
py -3.13 -m venv .venv
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r backend\requirements.txt
```

### macOS/Linux

```bash
python3.13 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r backend/requirements.txt
```

The first embedding-model use downloads `all-MiniLM-L6-v2`. If Presidio reports that a spaCy language model is missing, install the model required by the local Presidio/spaCy setup, for example:

```bash
python -m spacy download en_core_web_sm
```

## Build the Semantic Index

The semantic detector expects these files to exist:

- `backend/ai_risk_engine/vector_store/faiss_index.bin`
- `backend/ai_risk_engine/vector_store/metadata.pkl`

Rebuild them after changing files in `confidential_data`:

```powershell
cd backend
python -m ai_risk_engine.embeddings.build_embeddings
```

On macOS/Linux, use the same command after activating the virtual environment. The script uses paths relative to `backend`, so run it from that directory.

## Running the Project

Start each service from a separate terminal with the virtual environment activated.

### 1. FastAPI gateway

From `backend`:

```bash
uvicorn api_gateway.main:app --reload --host 127.0.0.1 --port 8000
```

Available endpoints:

| Method | Endpoint | Purpose |
| --- | --- | --- |
| `POST` | `/sanitize` | Sanitizes Python code and returns the mapping |
| `POST` | `/ai-usage` | Records an AI-service usage event |
| `GET` | `/events` | Returns usage events held in memory |

FastAPI documentation is available at `http://127.0.0.1:8000/docs` while the server is running.

Example sanitizer request:

```powershell
Invoke-RestMethod `
  -Uri http://127.0.0.1:8000/sanitize `
  -Method Post `
  -ContentType "application/json" `
  -Body '{"code":"def process_payment(customer_id): return customer_id"}'
```

### 2. Prompt gateway UI

From `backend`:

```bash
streamlit run gateway_ui.py
```

Open the URL printed by Streamlit. Enter a prompt or Python code, select a device ID, and choose **Analyze Prompt**. Allowed prompts can be sent to Gemini after configuring the API key.

### 3. Admin dashboard

From `backend`:

```bash
streamlit run admin_dashboard.py
```

The dashboard reads `backend/ai_risk_engine/analysis_log.json`. If there are no records yet, it displays the built-in seed statistics so the dashboard has a useful initial view.

### 4. Gemini configuration

Create a `.env` file in the directory from which the Gemini client is loaded, or otherwise expose the variable in the process environment:

```env
GEMINI_API_KEY=your_gemini_api_key
```

Do not commit API keys or other credentials to the repository. Gemini is called only when an analyzed prompt is allowed and the user clicks **Send to AI** in the gateway UI.

### 5. AI traffic monitor

Start the FastAPI gateway first, then from `backend/ai_traffic_monitor` run:

```bash
python main.py
```

Update `ai_traffic_monitor/config.py` to change the device ID, backend URL, recognized AI domains, or notification behavior. Packet capture may require administrator/root privileges and a packet-capture driver such as Npcap on Windows.

### 6. Browser extension

1. Start the FastAPI gateway on `http://127.0.0.1:8000`.
2. Open `chrome://extensions` in Chrome or Chromium.
3. Enable **Developer mode**.
4. Choose **Load unpacked**.
5. Select `frontend/browser_extension`.
6. Open a supported ChatGPT/OpenAI page and enter Python code in an editable field.
7. Open the extension popup to view the latest sanitizer mapping.

## Local Data and Security Notes

- `analysis_log.json` contains prompt-analysis metadata, including device IDs and risk results. Treat it as sensitive operational data.
- The current API stores `/ai-usage` events in process memory; restarting the API clears them.
- The analysis tracker persists records to a local JSON file and uses a thread lock for writes, but it is not a production database.
- The API endpoints do not currently implement authentication, authorization, rate limiting, or HTTPS. Keep the service bound to localhost during development and add these controls before network deployment.
- Secret detection is pattern-based and can produce false positives or miss unfamiliar token formats.
- Database-schema detection uses regular expressions and is not a complete parser.
- Semantic similarity depends on the confidential documents used to build the FAISS index and should be recalibrated with representative data.
- Code sanitization changes identifiers and restores them with simple text replacement. Review restored output before relying on it in production.
- DNS monitoring observes DNS requests, not the full encrypted request content. It is therefore an indicator of likely AI-tool usage, not proof of prompt transmission.
- The repository includes example confidential-data files for local development. Replace them with authorized organizational data and protect the directory in real deployments.

## Testing and Utilities

The repository includes small module-level scripts for manual checks, including:

- `backend/ai_risk_engine/test_semantic.py`
- `backend/ai_risk_engine/detection/ast_engine/test_script.py`
- `backend/ai_traffic_monitor/test_iface.py`
- `backend/generate_test_data.py`

The project currently does not include a dedicated pytest suite or CI configuration. Validate changes by running the relevant service, exercising the API endpoints, and checking the Streamlit interfaces.

## Current Scope

SentinelAI is currently a local development and demonstration system. It establishes the main security workflow, but a production deployment would need centralized storage, authentication, policy management, stronger secret detection, audit controls, encrypted communication, robust browser coverage, and automated tests.
