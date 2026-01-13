import os
import re
import json
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer, LTChar
from langdetect import detect, DetectorFactory
DetectorFactory.seed = 0  


WEBSITE_PATTERN = re.compile(r'(https?://\S+|www\.\S+)', re.I)
ADDRESS_PATTERN = re.compile(r'\d{2,5}.*\b(?:Street|St|Avenue|Ave|Road|Rd|Lane|Ln|Drive|Dr|TN|ZIP|PIGEON|FORGE)\b', re.I)

def clean_text(text):
    """Remove only website URLs and normalize spacing."""
    text = WEBSITE_PATTERN.sub("", text).strip()
    text = re.sub(r'\s{2,}', ' ', text)  
    return text

def is_probably_heading(text):
    """Rules for deciding if a text block is a heading."""
    if not text.strip():
        return False
    if len(text.split()) > 25:
        return False
    if re.search(r'[:•|]', text):  
        return False
    if len(re.findall(r'\w+', text)) == 1 and text.isupper():
        return False
    return True

def detect_language_safe(text):
    try:
        return detect(text)
    except:
        return "unknown"

def extract_headings(pdf_path):
    headings = []
    title = ""
    candidate_titles = []  
    all_h1_sizes = []  
    title_lang = ""

    for page_layout in extract_pages(pdf_path):
        page_width = page_layout.bbox[2] - page_layout.bbox[0]
        page_height = page_layout.bbox[3] - page_layout.bbox[1]
        for element in page_layout:
            if isinstance(element, LTTextContainer):
                text = clean_text(element.get_text().strip())
                if not text:
                    continue

                font_sizes = [obj.size for line in element for obj in line if isinstance(obj, LTChar)]
                avg_size = sum(font_sizes) / len(font_sizes) if font_sizes else 0
                is_bold = any("Bold" in obj.fontname for line in element for obj in line if isinstance(obj, LTChar))

                x0, y0, x1, y1 = element.bbox
                block_center = (x0 + x1) / 2
                is_centered = abs(block_center - page_width / 2) < page_width * 0.1
                is_bottom = y1 < page_height * 0.3

                if is_centered and is_bold and not is_bottom:
                    candidate_titles.append((text, avg_size, is_bold))

                if avg_size > 12 and is_probably_heading(text):
                    match = re.match(r'^(\d+(\.\d+){0,3})\b', text)
                    if match:
                        depth = match.group(1).count('.') + 1
                        if depth == 1:
                            level = "H1"
                            all_h1_sizes.append(avg_size)
                        elif depth == 2:
                            level = "H2"
                        elif depth == 3:
                            level = "H3"
                        else:
                            level = "H4"
                    else:
                        if avg_size > 16:
                            level = "H1"
                            all_h1_sizes.append(avg_size)
                        elif avg_size > 14:
                            level = "H2"
                        elif avg_size > 12:
                            level = "H3"
                        else:
                            level = "H4"

                    lang = detect_language_safe(text)

                    headings.append({
                        "level": level,
                        "text": text,
                        "page": int(page_layout.pageid)
                    })

    if candidate_titles:
        candidate_titles.sort(key=lambda t: t[1], reverse=True)
        title_candidate, title_size, title_bold = candidate_titles[0]

        for t, size, bold in candidate_titles[1:]:
            if abs(size - title_size) < 0.5 and bold == title_bold:
                title_candidate = f"{title_candidate} {t}"

        if (all_h1_sizes and title_size < max(all_h1_sizes)) or ADDRESS_PATTERN.search(title_candidate):
            title = ""
        else:
            title = title_candidate.strip()
            title_lang = detect_language_safe(title)
            headings = [h for h in headings if h["text"].strip() not in title]

    return {
        "title": title,
        "outline": headings
    }

def process_pdfs(input_folder, output_folder):
    os.makedirs(output_folder, exist_ok=True)
    for filename in os.listdir(input_folder):
        if filename.lower().endswith(".pdf"):
            pdf_path = os.path.join(input_folder, filename)
            result = extract_headings(pdf_path)
            output_path = os.path.join(output_folder, filename.replace(".pdf", ".json"))

            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(result, f, indent=2, ensure_ascii=False)

            print(f"Processed: {filename} -> {output_path}")

if __name__ == "__main__":
    
    local_input = os.path.join("sample_dataset", "pdfs")
    local_output = os.path.join("sample_dataset", "outputs")

    
    docker_input = "/app/pdfs"
    docker_output = "/app/outputs"

    input_path = docker_input if os.path.exists(docker_input) else local_input
    output_path = docker_output if os.path.exists(docker_output) else local_output

    process_pdfs(input_path, output_path)


