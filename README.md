# 🧠 CodeSage: AI Code Explainer 

**CodeSage** is a powerful tool that allows developers to paste any code snippet and receive a structured, step-by-step explanation in plain English. Utilizing Groq's ultra-fast LLM API and a sleek Streamlit interface, CodeSage offers:

* **Multiple explanation styles**: ELI5, Professional, Interviewer
* **Depth control**: Short, Medium, Deep
* **Chain-of-Thought (CoT)** reasoning
* **Structured JSON output**: Summary, Steps, Complexity
* **Local complexity analysis**: Lines of Code (LOC), Cyclomatic Complexity
* **Token usage logging**: via `tiktoken`
* **Customizable generation parameters**: Temperature, Top-P, Stop Sequence

---

## 🚀 Features

* **Instant code explanation**: Paste any code and get an immediate, structured explanation.
* **Multiple explanation styles**: Choose between ELI5, Professional, or Interviewer styles.
* **Depth control**: Adjust the depth of the explanation to suit your needs.
* **Chain-of-Thought reasoning**: Enable step-by-step reasoning for complex code.
* **Structured JSON output**: Receive a JSON object with summary, steps, and complexity metrics.
* **Local complexity analysis**: Get insights into the code's complexity, including LOC and cyclomatic complexity.
* **Token usage logging**: Monitor token usage for each request.
* **Customizable generation parameters**: Fine-tune the model's responses with temperature, Top-P, and stop sequence settings.

---

## 📂 Project Structure

```
CodeSage/
│-- streamlit_app.py      # Main Streamlit app
│-- requirements.txt      # Python dependencies
│-- evaluation.py         # Simple evaluation script
│-- README.md             # Project documentation
```

---

## ⚙️ Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/your-username/CodeSage.git
   cd CodeSage
   ```

2. **Create and activate a virtual environment**:

   ```bash
   python -m venv venv
   source venv/bin/activate   # Mac/Linux
   venv\Scripts\activate      # Windows
   ```

3. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

---

## ▶️ Usage

Run the app:

```bash
streamlit run streamlit_app.py
```

Open in browser → `http://localhost:8501`

1. Paste your code snippet.
2. Choose **style** (ELI5 / Professional / Interviewer).
3. Set **depth**, temperature, top\_p, stop sequence.
4. Click **Explain** → get structured JSON + rendered explanation.

---

## 🧠 Prompting Setup (RTFC)

We use **RTFC** (Role, Task, Format, Constraints):

* **Role**: Senior software engineer + teacher.
* **Task**: Explain code and compute complexity.
* **Format**: Strict JSON schema `{summary, steps, complexity}`.
* **Constraints**: Short summary, concise steps, JSON-only output, optional step-by-step.

Supports:

* **Zero-shot** (no examples)
* **One-shot** (1 example included)
* **Multi-shot** (multiple examples)
* **Dynamic prompting** (user style/depth injected into prompt)
* **Chain-of-Thought (CoT)** (token-by-token reasoning via steps array)

---

## 🔬 Evaluation 

Basic evaluation with 5 code snippets.

```bash
python evaluation.py
```

The script:

* Runs model on test cases.
* Compares explanation vectors (embeddings) vs. reference answers.
* Scores outputs with cosine similarity.

---

## 📦 Requirements

* Python 3.9+
* [Streamlit](https://streamlit.io/)
* [Groq Python SDK](https://github.com/groq/groq-python)
* [tiktoken](https://github.com/openai/tiktoken)
* NumPy

---

    
## 🏷 License

MIT License. Free for personal & commercial use.
