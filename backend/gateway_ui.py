import streamlit as st

from ai_risk_engine.pipeline import analyze_prompt
from ai_risk_engine.detection.ast_engine.engine import restore_names
from ai_risk_engine.llm.gemini_client import ask_gemini


# ---------- SESSION STATE ----------
if "analysis" not in st.session_state:
    st.session_state.analysis = None

if "ai_response" not in st.session_state:
    st.session_state.ai_response = None

if "safe_prompt" not in st.session_state:
    st.session_state.safe_prompt = None


# ---------- UI ----------
st.title("SentinelAI Enterprise AI Security Gateway")

prompt = st.text_area("Enter Prompt or Code")


# ---------- ANALYZE ----------
if st.button("Analyze Prompt"):

    if prompt.strip() == "":
        st.warning("Enter a prompt first")
        st.stop()

    st.session_state.analysis = analyze_prompt(prompt)
    st.session_state.ai_response = None

result = st.session_state.analysis


# ---------- SHOW RESULTS ----------
if result:

    if result["code_detected"]:

        st.subheader("Code Protection Layer")

        st.write("Original Code")
        st.code(result["original"], language="python")

        st.write("Sanitized Code")
        st.code(result["sanitized"], language="python")


    st.subheader("Risk Report")

    st.write(
        "Semantic similarity:",
        round(result["semantic_similarity"],2)
    )

    st.write(
        "PII risk:",
        result["pii"]["risk_score"]
    )

    st.write(
        "DB risk:",
        result["db"]["risk_score"]
    )

    st.write(
        "Secret risk:",
        result["secrets"]["risk_score"]
    )


    st.subheader("Final Decision")

    st.write(
        "Total risk:",
        result["final"]["total_risk"]
    )

    st.write(
        "Decision:",
        result["final"]["decision"]
    )


# ---------- BLOCK CASE ----------
    if result["final"]["decision"] == "BLOCK":

        st.error(
            "PROMPT BLOCKED\n"
            "Policy Violation: Enterprise AI Data Protection Policy\n"
            "Action: Transmission prevented"
        )

        st.button("Send to AI", disabled=True)


# ---------- ALLOW CASE ----------
    else:

        if result["code_detected"]:
            st.session_state.safe_prompt = result["sanitized"]

        else:
            st.session_state.safe_prompt = prompt


        if st.button("Send to AI"):

            try:

                with st.spinner("Querying AI securely..."):

                    ai_response = ask_gemini(
                        st.session_state.safe_prompt
                    )

                if result["code_detected"]:

                    ai_response = restore_names(
                        ai_response,
                        result["mapping"]
                    )

                st.session_state.ai_response = ai_response

            except Exception as e:

                st.error(f"AI Error: {e}")


# ---------- AI RESPONSE ----------
if st.session_state.ai_response:

    st.subheader("AI Response")

    st.write(st.session_state.ai_response)