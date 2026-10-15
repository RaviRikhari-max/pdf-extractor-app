import re
import pdfplumber
import streamlit as st

st.set_page_config(
    page_title="PDF Value Extractor", page_icon="📄", layout="centered"
)

st.title("📄 PDF Value Extractor App")
st.write(
    "Upload any PDF document below to automatically read its text and extract key values using Python!"
)

# File uploader widget
uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file is not None:
  with st.spinner("Reading PDF..."):
    # Open the PDF using pdfplumber
    with pdfplumber.open(uploaded_file) as pdf:
      full_text = ""
      for page in pdf.pages:
        text = page.extract_text()
        if text:
          full_text += text + "\n"

  st.success("PDF successfully uploaded and read!")

  # Extract specific values using Regular Expressions
  invoice_match = re.search(
      r'(?:Invoice\s*(?:#|No\.?|:)?)\s*([A-Za-z0-9-]+)',
      full_text,
      re.IGNORECASE,
  )
  date_match = re.search(r'\b\d{2}[-/]\d{2}[-/]\d{4}\b', full_text)
  total_match = re.search(
      r'(?:Total|Amount Due|Balance)\s*[:\$]?\s*([0-9,]+\.[0-9]{2})',
      full_text,
      re.IGNORECASE,
  )

  # Display Extracted Values in a clean layout
  st.subheader("🔍 Extracted Data Results")
  col1, col2, col3 = st.columns(3)
  col1.metric(
      "Invoice Number",
      invoice_match.group(1) if invoice_match else "Not Found",
  )
  col2.metric("Date", date_match.group(0) if date_match else "Not Found")
  col3.metric(
      "Total Amount", total_match.group(1) if total_match else "Not Found"
  )

  # Expandable section to view the full raw text of the PDF
  with st.expander("View Full Extracted Text"):
    st.text(full_text)
