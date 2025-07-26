# Adobe-India-Hackathon25

# Connecting the Dots

Welcome to our submission for Adobe's "Connecting the Dots" Hackathon Challenge. This repository contains our solution for:

- **Round 1A: Understand Your Document**
- **Round 1B: Persona-Driven Document Intelligence**

---

## 🚀 Overview

This project reimagines PDF reading by extracting structured outlines and delivering contextual insights based on user personas. The two-part challenge includes:

- **Challenge 1A**: Extracting document structure (title, H1–H3 headings) in a clean JSON format.
- **Challenge 1B**: Identifying and ranking the most relevant sections across PDFs based on persona-driven tasks.

---

## 📁 Folder Structure

├── input/ # Input PDFs for processing

├── output/ # Output JSONs for each input PDF

├── src/ # Source code for heading extraction and persona analysis

├── models/ # Lightweight models (if any used)

├── Dockerfile # Container setup

├── approach_explanation.md # (Round 1B) 300–500 word explanation of methodology

└── README.md # You're here!

---

## 🧠 Our Approach

### ✅ Challenge 1A - Document Outline Extraction

We parse the PDF file to identify and extract:
- The **Title**
- Headings at levels **H1**, **H2**, and **H3**
- Page numbers for each heading

Key techniques:
- **Font analysis and layout heuristics** (not just font size)
- Use of `pdfminer.six` and `PyMuPDF` for text and layout parsing
- Post-processing with regex and position-based hierarchy building
- Final JSON output in the following format:

```json
{
  "title": "Understanding AI",
  "outline": [
    { "level": "H1", "text": "Introduction", "page": 1 },
    { "level": "H2", "text": "What is AI?", "page": 2 },
    { "level": "H3", "text": "History of AI", "page": 3 }
  ]
}
```

# approach_explanation.md

### ✅ Challenge 1B – Persona-Driven Document Intelligence

### 🧩 Problem Understanding

In this round, we were tasked with building a system that extracts and prioritizes the most relevant sections across a collection of PDFs based on a specific **persona** and their **job-to-be-done**. This required our system to understand diverse personas, interpret the task, and analyze documents across multiple domains — all under strict constraints (CPU-only, <1GB model, no internet access).

---

### 🔍 Our Methodology

Our approach follows a modular, pipeline-based design:

#### 1. **Preprocessing**
- Each PDF is parsed using `pdfplumber` or `PyMuPDF` to extract page-level content.
- Text blocks are segmented and associated with page numbers.
- Basic cleanup and sentence splitting is applied using `nltk`.

#### 2. **Semantic Matching**
- We treat the *persona* and *job-to-be-done* as a **natural language query**.
- Each text block from the documents is converted into vector embeddings using **TF-IDF + cosine similarity**.
- We compute relevance scores between the job query and each block of text.
- To improve context, we also extract named entities using `spaCy` and assign bonus weights if domain-specific terms (e.g., "revenue", "methodology") match persona expectations.

#### 3. **Section Extraction and Ranking**
- High-scoring blocks are mapped back to their document, page, and section title (if identifiable).
- We assign an `importance_rank` based on similarity score and uniqueness (to avoid redundancy).
- The top-N sections (configurable) are returned with document name, page number, and heading.

#### 4. **Sub-section Refinement**
- For each top-ranked section, we extract a 2–4 paragraph snippet using contextual cues.
- These are cleaned, summarized (using a lightweight extractive method), and returned under `refined_text`.

---

### 📤 Output

The final output JSON includes:
- Metadata (documents used, persona, job, timestamp)
- Extracted sections with titles, page numbers, and ranking
- Sub-section analysis with relevant text snippets

---

### 🧠 Why This Works

This solution is:
- **Domain-agnostic**: It works for research, finance, education, etc.
- **Persona-aware**: Uses job goals to inform relevance scoring
- **Scalable**: Easily extendable with multilingual handling or larger corpora
- **Lightweight**: Runs within CPU and time constraints

---

This modular design allows for future improvements, such as integrating LLM-powered summarization (offline) or personalization based on reading history.




