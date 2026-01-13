# 📄 Round 1A – Understand Your Document  
### Connecting the Dots Through Docs

##  Overview

This project is developed for the **Round 1A Hackathon Challenge – "Understand Your Document"**.  
The main objective is to extract a **structured outline** from PDF documents including:


- **Title**
- **Headings (H1, H2, H3)**
- **Page Numbers**

The extracted structure is returned in a **clean JSON format** so that machines can understand the document hierarchy.

---


##  Problem Statement

PDFs are widely used, but machines do not naturally understand their structure.  
This solution bridges that gap by extracting the logical structure of documents, enabling:

- Semantic Search  
- Document Understanding  
- Insight Generation  
- Recommendation Systems  


---

##  What This Project Does


- Accepts PDF files (up to **50 pages**)
- Extracts:
  - Title
  - H1, H2, H3 headings
  - Page number for each heading
- Outputs a JSON file in the following format:
{
  "title": "Understanding AI",
  "outline": [
    { "level": "H1", "text": "Introduction", "page": 1 },
    { "level": "H2", "text": "What is AI?", "page": 2 },
    { "level": "H3", "text": "History of AI", "page": 3 }
  ]
}


##  Docker Requirements

Platform: linux/amd64 (x86_64)
CPU only (No GPU dependency)
Model size ≤ 200MB (if used)
Works fully offline
No internet access allowed


##  Expected Behavior

The container will:
Automatically read all PDFs from /app/input
Process each PDF
Generate a corresponding .json file in /app/output


## Example:


bash
Copy code
input/sample.pdf  →  output/sample.json
⏱ Constraints
Constraint	Requirement
Execution Time	≤ 10 seconds for 50-page PDF
Network	No internet access
Runtime	CPU only (amd64)
Model Size	≤ 200MB (if used)
System	8 CPUs, 16GB RAM


##  Approach

Load PDF files from /app/input
Parse text and layout information
Identify Title and heading levels (H1, H2, H3)
Build hierarchical outline structure
Export structured JSON to /app/output

