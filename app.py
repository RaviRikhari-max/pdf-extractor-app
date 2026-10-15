import pdfplumber
import pytesseract
from pdf2image import convert_from_bytes
import streamlit as st

st.set_page_config(
    page_title="Scanned PDF OCR Extractor", page_icon="👁️", layout="wide"
)

st.title("👁️ Scanned PDF OCR & Layout Extractor")
st.write(
    "Upload a scanned PDF. This app will automatically run OCR to read text"
    " from the image pages!"
)

uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file is not None:
  with st.spinner(
      "Processing PDF and running OCR engine (this may take a few seconds)..."
  ):
    # Read the file bytes
    pdf_bytes = uploaded_file.read()

    full_text = ""

    # Step 1: Try regular text extraction first (for normal PDFs)
    try:
      with pdfplumber.open(uploaded_file) as pdf:
        for page in pdf.pages:
          txt = page.extract_text(layout=True)
          if txt:
            full_text += txt + "\n"
    except Exception:
      pass

    # Step 2: If no text was found, it's a scanned image. Use OCR!
    if not full_text.strip():
      st.info(
          "No embedded text layer found. Running Tesseract OCR on image pages..."
      )

      # Convert PDF bytes to a list of images using poppler
      images = convert_from_bytes(pdf_bytes)

      ocr_text = ""
      for i, image in enumerate(images):
        page_text = pytesseract.image_to_string(image)
        ocr_text += (
            f"\n--- Page {i + 1} (OCR Extracted) ---\n" + page_text + "\n"
        )

      full_text = ocr_text
    else:
      st.success("Extracted text from native text layer successfully!")

  # Display the extracted text result
  st.subheader("📄 Extracted Text Results")
  with st.expander("View Full Extracted Text", expanded=True):
    st.text(full_text)
