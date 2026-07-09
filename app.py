import streamlit as st
import json
import requests
import sqlite3
from groq import Groq

# Initialize SQLite database for local data governance
def init_db():
    conn = sqlite3.connect("gtm_analytics.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS leads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company_name TEXT,
            company_url TEXT,
            fintech_use_case TEXT,
            lead_score TEXT,
            personalized_outbound_hook TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def save_to_database(payload):
    conn = sqlite3.connect("gtm_analytics.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO leads (company_name, company_url, fintech_use_case, lead_score, personalized_outbound_hook)
        VALUES (?, ?, ?, ?, ?)
    """, (payload["company_name"], payload["company_url"], payload["fintech_use_case"], payload["lead_score"], payload["personalized_outbound_hook"]))
    conn.commit()
    conn.close()

# App Configurations
st.set_page_config(page_title="HyperScale GTM Infrastructure", page_icon="⚡", layout="wide")
init_db()

# Sidebar for Authentication
st.sidebar.title("Authentication")
groq_api_key = st.sidebar.text_input("Enter Groq API Key (starts with gsk_)", type="password")

st.title("⚡ HyperScale GTM: Production AI Lead Enrichment Pipeline")
st.markdown("Automating the transition between raw market web presence and structured CRM intelligence.")
st.write("---")

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📥 Inbound Lead Target")
    company_name = st.text_input("Company Name", value="Swiggy")
    company_url = st.text_input("Company URL (with https://)", value="https://www.swiggy.com")
    
    st.markdown("**Alternative: Paste Raw Copied Text Instead of Live Scrape**")
    fallback_text = st.text_area("Manual context fallback (Optional)", placeholder="Paste company description if website is protected...")
    
    execute = st.button("Run End-to-End Pipeline", type="primary")

with col2:
    st.subheader("📤 CRM Data Engine Pipeline Output")
    
    if execute:
        if not groq_api_key:
            st.error("Please provide a Groq API Key in the sidebar to run the cloud intelligence loop.")
        else:
            with st.spinner("Step 1: Scraping target website context via Jina Reader..."):
                scrape_url = f"https://r.jina.ai/{company_url}"
                headers = {"X-Return-Format": "markdown"}
                
                context_data = ""
                if fallback_text:
                    context_data = fallback_text
                else:
                    try:
                        res = requests.get(scrape_url, headers=headers, timeout=10)
                        if res.status_code == 200:
                            context_data = res.text[:4000]
                            st.success("Live web scraping complete!")
                        else:
                            context_data = fallback_text
                    except Exception:
                        context_data = fallback_text
            
            if not context_data:
                st.error("Failed to extract context. Please provide manual text context.")
            else:
                with st.spinner("Step 2: Orchestrating Groq LLM Extraction Loop (Llama-3.1)..."):
                    try:
                        # Instantiate Groq Client
                        client = Groq(api_key=groq_api_key)
                        
                        system_prompt = (
                            "You are an elite AI GTM Data Engineer at Razorpay. Analyze the scraped text raw data "
                            "and return a strict, valid JSON object matching this schema exactly. "
                            "Do not include markdown wraps like ```json. Your response must be parseable via json.loads().\n"
                            "{\n"
                            "  \"company_name\": \"Extract official name\",\n"
                            "  \"company_url\": \"Provide verified URL\",\n"
                            "  \"fintech_use_case\": \"Highly specific detailed way they can leverage Razorpay services (payouts, escrow, links, checkout optimization)\",\n"
                            "  \"lead_score\": \"High/Medium/Low based on transactional scale indicators found in text\",\n"
                            "  \"personalized_outbound_hook\": \"A hyper-personalized 2-sentence value proposition pitch opening targeting their exact business model.\"\n"
                            "}"
                        )
                        
                        completion = client.chat.completions.create(
                            model="llama-3.1-8b-instant",
                            messages=[
                                {"role": "system", "content": system_prompt},
                                {"role": "user", "content": f"Scraped Website Context:\n{context_data}"}
                            ],
                            temperature=0.1,
                            response_format={"type": "json_object"}
                        )
                        
                        raw_content = completion.choices[0].message.content.strip()
                        structured_json = json.loads(raw_content)
                        
                        st.metric("Automated Lead Score Priority", value=structured_json["lead_score"])
                        st.markdown("**Personalized Outbound Sales Hook:**")
                        st.info(structured_json["personalized_outbound_hook"])
                        
                        st.markdown("**Validated System JSON Payload:**")
                        st.json(structured_json)
                        
                        save_to_database(structured_json)
                        st.success("Step 3: Payload structurally validated and written to local database successfully!")
                        
                    except Exception as e:
                        st.error(f"Pipeline Execution Failed: {e}")

st.write("---")
st.subheader("📊 Core GTM Database Viewer (Stored Local Records)")
try:
    conn = sqlite3.connect("gtm_analytics.db")
    import pandas as pd
    df = pd.read_sql_query("SELECT * FROM leads ORDER BY timestamp DESC", conn)
    st.dataframe(df, use_container_width=True)
    conn.close()
except Exception:
    st.info("No records written to database yet.")