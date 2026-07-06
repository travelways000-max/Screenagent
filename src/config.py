# ============ CONFIGURATION ============

# Path to Tesseract OCR engine
TESSERACT_PATH = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Output Excel file
EXCEL_FILE = "extracted_data.xlsx"

# Screenshot folder
SCREENSHOT_FOLDER = "screenshots"

# ---------- AI EXTRACTION (optional) ----------
USE_GEMINI_AI = True  # Set False if you don't have API key
GEMINI_API_KEY = "PASTE_YOUR_GEMINI_API_KEY_HERE"

# What fields do you want to extract? Tell AI what to look for:
EXTRACTION_FIELDS = [
    "Name",
    "Email",
    "Phone",
    "Price",
    "Product",
    "Date",
    "Invoice Number",
    "Address",
    "Company"
]

# ---------- AUTO CAPTURE MODE ----------
AUTO_CAPTURE = False           # True = captures every X seconds
AUTO_CAPTURE_INTERVAL = 30     # seconds

# ---------- FORM FILLING ----------
FORM_FILL_ENABLED = False      # True = agent will type into forms
FORM_FIELDS_MAP = {
    # "field_label_in_target_form": "extracted_field_name"
    # Example:
    # "Full Name": "Name",
    # "Email Address": "Email",
    # "Mobile": "Phone"
}
