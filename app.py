import os
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

# Load API key
load_dotenv()
api_key = os.getenv("OPENROUTER_API_KEY")
if not api_key:
    st.error("⚠️ API key not set. Please add 'OPENROUTER_API_KEY' to your .env")
    st.stop()

# Initialize client
client = OpenAI(api_key=api_key, base_url="https://openrouter.ai/api/v1")

# Page config
st.set_page_config(page_title="Histopathology Report Bot", page_icon="🔬")
st.title("🔬 Histopathology Report Generator")
st.markdown("*Developed by Shehroz Khan Rind*")
st.markdown("---")

# Inputs
st.subheader("Patient & Specimen Details")
patient_info = st.text_input("Patient Information (Name, Age, Sex)")
specimen = st.text_input("Specimen Details (e.g., Biopsy type)")

st.subheader("Clinical & Pathology Findings")
clinical_history = st.text_area("Clinical History", height=100)
gross_description = st.text_area("Gross Description", height=100)
microscopic_findings = st.text_area("Microscopic Findings", height=100)

# Generate
if st.button("Generate Report"):
    if not all([patient_info, specimen, clinical_history, gross_description, microscopic_findings]):
        st.warning("Please fill in all fields before generating the report.")
    else:
        with st.spinner("Generating histopathology report..."):
            prompt = (
                f"You are an expert histopathologist. Generate a comprehensive histopathology report with these sections:\n"
                f"Patient Information: {patient_info}\n"
                f"Specimen Details: {specimen}\n"
                f"Clinical History: {clinical_history}\n"
                f"Gross Description: {gross_description}\n"
                f"Microscopic Findings: {microscopic_findings}\n\n"
                f"Report:\n- Diagnosis:\n- Commentary and Recommendations:\n"
            )
            try:
                response = client.chat.completions.create(
                    model="mistralai/mistral-7b-instruct:free",
                    messages=[
                        {"role": "system", "content": "You are a histopathology report writing assistant. Use professional medical language."},
                        {"role": "user", "content": prompt}
                    ]
                )
                report = response.choices[0].message.content.strip()
                st.subheader("📄 Generated Histopathology Report")
                st.text_area("", report, height=300)
            except Exception as e:
                st.error(f"❌ API Error: {e}")
