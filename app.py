# ----------------- Imports -----------------
import streamlit as st
import pandas as pd
import openai
import os
from dotenv import load_dotenv

# ----------------- Page Setup -----------------
st.set_page_config(page_title="Bell Co-Pilot", layout="centered")
st.title("Bell Co-Pilot")
st.markdown("Upload today's offer sheet and get smart sales suggestions.")

# ----------------- Load OpenAI API Key -----------------
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# ----------------- Offer Sheet Upload -----------------
uploaded_file = st.file_uploader("Upload Today's Offer Sheet (Excel)", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    st.markdown("### Today's Offers")
    st.dataframe(df)
else:
    st.warning("No offer sheet uploaded yet.")
    df = None  # So we can reference it later safely

# ----------------- Customer Info Form -----------------
st.markdown("---")
st.header("👤 Customer Profile")

with st.form("customer_form"):
    internet = st.text_input("Internet Plan")
    tv = st.text_input("TV Plan")
    mobility = st.text_input("Mobility Plan")
    usage = st.text_area("Usage / Preferences")
    budget = st.text_input("Budget (optional)")
    submitted = st.form_submit_button("Get Pitch")

# ----------------- AI Suggestion Output -----------------
if submitted:
    if df is not None:
        offers_text = df.to_string()
    else:
        offers_text = "No offers uploaded."

    with st.spinner("🔍 Generating Co-Pilot Suggestion..."):

        system_prompt = """
        You are Bell Co-Pilot, an assistant for Bell sales reps.
        Return your answer in this exact format:

        Upgrade Suggestion: <...>
        Bundle Tip: <...>
        Pitch: <...>
        """

        user_prompt = f"""
        Customer Profile:
        - Internet: {internet}
        - TV: {tv}
        - Mobility: {mobility}
        - Usage: {usage}
        - Budget: {budget}

        Today's Offers:
        {offers_text}
        """

        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                max_tokens=400
            )
            reply = response['choices'][0]['message']['content']
            st.markdown("### Co-Pilot Suggestion")
            st.text(reply)

        except Exception as e:
            st.error(f"Error generating pitch: {e}")
