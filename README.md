
```markdown
# HyperScale GTM: Production AI Lead Enrichment Pipeline

### Live Production Application: [Launch Live Dashboard](https://gtm-flow-ai-jczuqn2kf2v69aiui9vxx2.streamlit.app/)

An automated data engineering pipeline designed to bridge the gap between unstructured corporate web footprints and structured CRM intelligence. This application ingests raw company URLs, dynamically scrapes their landing pages, extracts deep fintech alignment metrics using high-throughput open-source LLMs, and structures the output into an analytics database ledger.

---

## System Architecture & Data Flow

The application executes a three-stage asynchronous pipeline to convert messy web data into deterministic enterprise intelligence:


```

[Target URL] ---> [Jina Reader API] ---> [Raw Markdown Context]
|
[SQLite Database] <--- [Validated JSON] <--- [Groq Engine (Llama 3.1)]

```

### Core Component Engineering

* **Context Ingestion Pipeline (Jina AI Reader):** Standard web scraping workflows often break when encountering modern JavaScript-heavy frontend frameworks or bot-detection barriers. To bypass this, the ingestion engine passes target URLs through a proxy reader layer, cleanly parsing active web layouts into high-density, text-only Markdown. This strips away redundant HTML scripts, media elements, and boilerplate styling to maximize contextual relevance and conserve LLM token windows.
* **Deterministic Structured Extraction (Groq & Llama-3.1-8b-instant):** The processed Markdown payload is fed into Groq’s hardware-accelerated inference cluster. By utilizing a highly rigid system instruction set paired with the native `response_format={"type": "json_object"}` parameter, the pipeline enforces a strict schema extraction layer. This completely bypasses standard conversational prose, guaranteeing a reliable, JSON payload matching the exact business requirements (fintech_use_case, lead_score, personalized_outbound_hook).
* **Local Data Governance Hub (SQLite3 & Pandas):** Upon validation via a structural `json.loads()` interceptor, the structured payload is securely committed to an atomic relational database (gtm_analytics.db). The frontend visualization layer uses `pandas.read_sql_query` to automatically pull, index, and render the historical record ledger sorted by transaction timestamps, ensuring complete data persistence across server lifecycles.

---

## Tech Stack & Protocols

* **Frontend UI Framework:** Streamlit (Production-grade state handling & real-time UI components)
* **LLM Orchestration:** Groq Python SDK (Leveraging ultra-low latency Llama-3.1-8b-instant)
* **Context Extraction API:** Jina AI Reader Protocol (Markdown conversion engine)
* **Data Layer:** SQLite3 (Relational transactional storage) & Pandas (Dataframe parsing)

---

## Getting Started (Local Development)

### 1. Clone the Architecture
```bash
git clone [https://github.com/YOUR_USERNAME/GTM-Flow-AI.git](https://github.com/YOUR_USERNAME/GTM-Flow-AI.git)
cd GTM-Flow-AI

```

### 2. Provision Dependencies

Ensure your local Python environment has the necessary client libraries installed:

```bash
pip install streamlit groq pandas requests

```

### 3. Initialize the Pipeline

Boot up the Streamlit CLI server to run the full dashboard on your local network:

```bash
streamlit run app.py

```

### 4. Inject Runtime Environment Keys

Once the dashboard initializes in your browser, enter your generated Groq API Key (gsk_...) into the secure sidebar input field, configure your inbound lead domain targets, and trigger the end-to-end cloud execution loop.

```

```
