# app.py
import streamlit as st
from src import groq_client, complexity, token_logger
import os
import json
import time

# ------------------------
# Page Config
# ------------------------
st.set_page_config(page_title="CodeSage: AI Code Explainer", layout="wide")

# ------------------------
# Sidebar: Project Info


# ------------------------
st.sidebar.title("About CodeSage 🚀")

with st.sidebar.expander("Project Overview"):
    st.markdown("""
    - Explain any code in plain English  
    - Customizable explanation styles & depths
    - Step-by-step reasoning and structured output  
    - Estimates code complexity (LOC, Cyclomatic & Execution Time)
    """)

with st.sidebar.expander("How to Use 🛠️"):
    st.markdown("""
    1. Paste code in the editor below.  
    2. Click **Explain**.  
    3. View AI explanation.
    4. Complexity metrics shown automatically.  
    """)


with st.sidebar.expander("Quick Tips 💡"):
    st.markdown("""
    - Use **CoT** for step-by-step reasoning.  
    - Adjust **Temperature** for creativity.  
    - **Top-P** controls randomness  
    - Clean code ensures better AI explanations.
    """)


st.sidebar.markdown("---")
if st.sidebar.button("Change Preferences ⚙️"):
    st.session_state.page = "Settings"

with st.sidebar.expander("Helpful Resources 🔗"):
    st.markdown("""
    - [Groq LLM Docs](https://docs.groq.com/)  
                
    - [Python Official Docs](https://docs.python.org/3/)  
                
    - [Cyclomatic Complexity Guide](https://en.wikipedia.org/wiki/Cyclomatic_complexity)
    """)

# ------------------------
# Session Defaults
# ------------------------
if "page" not in st.session_state:
    st.session_state.page = "Main"

if "style" not in st.session_state:
    st.session_state.style = "Professional"

if "depth" not in st.session_state:
    st.session_state.depth = "medium"

if "prompt_type" not in st.session_state:
    st.session_state.prompt_type = "Zero-Shot"

if "temperature" not in st.session_state:
    st.session_state.temperature = 0.2

if "top_p" not in st.session_state:
    st.session_state.top_p = 0.9

if "stop_seq" not in st.session_state:
    st.session_state.stop_seq = ""

if "model" not in st.session_state:
    st.session_state.model = "llama-3.1-8b-instant"

# ------------------------
# Settings Page
# ------------------------
if st.session_state.page == "Settings":
    st.title("Settings / Preferences")

    st.session_state.prompt_type = st.selectbox(
        "Prompt Type", ["Zero-Shot", "One-Shot",
                        "Multi-Shot", "Chain-of-Thought (CoT)"],
        index=["Zero-Shot", "One-Shot", "Multi-Shot",
               "Chain-of-Thought (CoT)"].index(st.session_state.prompt_type)
    )
    st.session_state.style = st.selectbox(
        "Explanation Style", ["ELI5", "Professional", "Interviewer"],
        index=["ELI5", "Professional", "Interviewer"].index(
            st.session_state.style)
    )
    st.session_state.depth = st.selectbox(
        "Depth", ["short", "medium", "deep"], index=["short", "medium", "deep"].index(st.session_state.depth)
    )
    st.session_state.temperature = st.slider(
        "Temperature", 0.0, 1.0, st.session_state.temperature)
    
    st.session_state.top_p = st.slider(
        "Top P", 0.0, 1.0, st.session_state.top_p)
    
    st.session_state.stop_seq = st.text_input(
        "Stop Sequence (optional)", st.session_state.stop_seq)
    
    st.session_state.model = st.selectbox(
        "Model", ["llama-3.1-8b-instant"], index=0)

    if st.button("Save & Go to Main"):
        st.session_state.page = "Main"

# ------------------------
# Main Page
# ------------------------
else:

    st.title("CodeSage: AI Code Explainer")

    # IDE-like text area for code input

    code_input = st.text_area(
        "Paste your code here:",
        height=400,
        placeholder="Write or paste your code here...",
        key="code_input"
    )

    if st.button("Explain"):
        if not code_input.strip():
            st.warning("Please enter some code to explain.")
        else:
            # Build prompt based on settings

            if st.session_state.prompt_type == "Zero-Shot":
                messages = groq_client.zero_shot_prompt(code_input,
                                                        style=st.session_state.style,

                                                        depth=st.session_state.depth)
            elif st.session_state.prompt_type == "Chain-of-Thought (CoT)":
                messages = groq_client.cot_prompt(code_input,
                                                  style=st.session_state.style,

                                                  depth=st.session_state.depth)
            else:
                messages = groq_client.zero_shot_prompt(code_input,
                                                        style=st.session_state.style,

                                                        depth=st.session_state.depth)

            # Count tokens

            tokens = token_logger.log_tokens(code_input)
            st.write(f"Tokens used for input: {tokens}")

            # Placeholder for streaming explanation

            explanation_placeholder = st.empty()

            full_text = ""
            start_time = time.time()

            try:
                # Stream AI output

                for chunk in groq_client.call_groq_llm_stream(
                        messages,
                        temperature=st.session_state.temperature,
                        top_p=st.session_state.top_p,
                        stop_sequence=st.session_state.stop_seq):
                    full_text += chunk
                    # Auto-expanding text area

                    explanation_placeholder.text_area("AI Explanation", value=full_text,
                                                      height=max(300, len(full_text)//2))

                # After streaming, calculate complexity
                end_time = time.time()
                comp = complexity.estimate_complexity(code_input)
                comp['execution_time_sec'] = round(end_time - start_time, 4)

                st.subheader("Code Complexity")
                st.json(comp)

                # Save output
                os.makedirs("output/explanations", exist_ok=True)
                with open("output/explanations/explanation.json", "w") as f:
                    json.dump({"ai_output": full_text,
                               "local_complexity": comp}, f, indent=2)

            except Exception as e:
                st.error(str(e))
