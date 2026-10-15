import pdfplumber
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="PDF Table & Layout Extractor", page_icon="📊", layout="wide"
)

st.title("📊 PDF Table & Layout Extractor")
st.write(
    "Upload a PDF with tables or column-aligned data to view it in its original format."
)

uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file is not None:
  with st.spinner("Analyzing tables and layout..."):
    with pdfplumber.open(uploaded_file) as pdf:
      all_tables = []
      layout_text = ""

      for page_num, page in enumerate(pdf.pages):
        # 1. Extract text while preserving visual layout and column spacing
        text = page.extract_text(layout=True)
        if text:
          layout_text += (
              f"\n--- Page {page_num + 1} (Layout Preserved) ---\n" + text + "\n"
          )

        # 2. Extract structured tables from the page
        tables = page.extract_tables()
        for table in tables:
          if table:
            all_tables.append((page_num + 1, table))

  st.success("PDF processed successfully!")

  # Display Extracted Tables using Streamlit dataframes
  if all_tables:
    st.subheader("📋 Extracted Tables")
    for idx, (page_num, table) in enumerate(all_tables):
      st.markdown(f"**Table {idx + 1} (Found on Page {page_num}):**")

      # Convert the table (list of lists) into a pandas DataFrame
      # Assumes the first row contains headers
      if len(table) > 1:
        # Clean up any None values in headers or rows
        header = [str(col) if col is not None else "" for col in table[0]]
        data = [
            [str(cell) if cell is not None else "" for cell in row]
            for row in table[1:]
        ]
        df = pd.DataFrame(data, columns=header)
      else:
        df = pd.DataFrame(table)

      # Display interactive table with download option
      st.dataframe(df, use_container_width=True)

      # Optional: Add a download button for each table as CSV
      csv = df.to_csv(index=False).encode("utf-8")
      st.download_button(
          label=f"Download Table {idx + 1} as CSV",
          data=csv,
          file_name=f"extracted_table_{idx + 1}.csv",
          mime="text/csv",
      )
  else:
    st.info(
        "No structured grid tables were automatically detected. Check the"
        " layout text below."
    )

  # Display layout-preserved text block
  with st.expander("View Full Page Layout (Columns & Spacing Preserved)"):
    st.text(layout_text)
