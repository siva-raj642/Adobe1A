# Adobe Hackathon 2025 - Challenge 1a Solution

## Overview

This project is a solution for **Challenge 1a** of the Adobe India Hackathon 2025. It processes PDF files, extracts the **document title** and **hierarchical headings (H1–H4)**, and outputs structured JSON files matching the schema provided.

The solution is designed to run inside a container, without internet access, and under strict resource and time constraints.

## Features

- Extracts meaningful **title** and **headings** (H1–H4) based on font size, numbering, and layout  
- Filters out non-headings using heuristics  
- Detects **multilingual text** using `langdetect`  
- Handles formatting issues like **extra spacing**  
- Fully **offline**, **CPU-only**, and fast (sub-10s)  
- Outputs JSON per PDF, matching required schema

---

## Project Structure

Challenge_1a/
├── Dockerfile
├── requirements.txt
├── process_pdfs.py # Main script
├── README.md
└── sample_dataset/
├── pdfs/ # Input PDFs
├── outputs/ # Output JSONs
└── schema/
└── output_schema.json


### To run:

```bash
docker build -t adobe-outline-extractor .
docker run -v "${PWD}/sample_dataset:/app/sample_dataset" adobe-outline-extractor


