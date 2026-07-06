import pytesseract
import json
import re
import google.generativeai as genai
from config import (TESSERACT_PATH, USE_GEMINI_AI, GEMINI_API_KEY,
                    EXTRACTION_FIELDS)

pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH


# ---------- METHOD 1: TESSERACT OCR (offline, free) ----------
def extract_text_ocr(image):
    """Extract raw text from image using Tesseract."""
    text = pytesseract.image_to_string(image, lang='eng+hin')
    return text.strip()


def extract_structured_regex(text):
    """Use regex to find common Indian data patterns."""
    data = {}

    # Email
    emails = re.findall(r'[\w\.-]+@[\w\.-]+\.\w+', text)
    data['Email'] = emails[0] if emails else ''

    # Phone (Indian: +91 or 10 digit)
    phones = re.findall(r'(?:\+91[\-\s]?)?[6-9]\d{9}', text)
    data['Phone'] = phones[0] if phones else ''

    # Price (₹ or Rs.)
    prices = re.findall(r'(?:₹|Rs\.?)\s*([\d,]+(?:\.\d+)?)', text)
    data['Price'] = prices[0] if prices else ''

    # Date (multiple formats)
    dates = re.findall(r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b', text)
    data['Date'] = dates[0] if dates else ''

    # Invoice number
    inv = re.findall(r'(?:Invoice|Inv|Bill)\s*(?:No\.?|#)?\s*([A-Z0-9-]+)',
                     text, re.IGNORECASE)
    data['Invoice Number'] = inv[0] if inv else ''

    # Pincode (India)
    pin = re.findall(r'\b\d{6}\b', text)
    data['Pincode'] = pin[0] if pin else ''

    return data


# ---------- METHOD 2: GEMINI AI (smart, structured) ----------
def extract_with_gemini(image, fields):
    """Use Gemini Vision to extract structured data."""
    if not USE_GEMINI_AI or not GEMINI_API_KEY:
        return None

    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')

    fields_str = ", ".join(fields)
    prompt = f"""Look at this image and extract these fields: {fields_str}.

Return ONLY a valid JSON object. Use these exact keys: {fields_str}.
If a field is not found, use empty string "". No markdown, no comments."""

    try:
        response = model.generate_content([prompt, image])
        raw = response.text.strip()
        # Clean markdown wrappers if present
        raw = raw.replace('```json', '').replace('```', '').strip()
        return json.loads(raw)
    except Exception as e:
        print(f"⚠️ Gemini error: {e}")
        return None


# ---------- MAIN EXTRACTION FUNCTION ----------
def extract_data(image):
    """Try Gemini first, fallback to Tesseract + regex."""
    result = {'source_image_time': str(image.info.get('time', ''))}

    if USE_GEMINI_AI:
        print("🧠 Extracting with Gemini AI...")
        ai_data = extract_with_gemini(image, EXTRACTION_FIELDS)
        if ai_data:
            result.update(ai_data)
            result['_method'] = 'gemini'
            return result

    print("📄 Extracting with OCR (offline)...")
    text = extract_text_ocr(image)
    result['raw_text'] = text
    regex_data = extract_structured_regex(text)
    result.update(regex_data)
    result['_method'] = 'ocr'
    return result
