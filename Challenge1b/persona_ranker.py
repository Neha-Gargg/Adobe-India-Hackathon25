import fitz
import os
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def extract_sections(pdf_path):
    doc = fitz.open(pdf_path)
    sections = []

    for page_num, page in enumerate(doc):
        text = page.get_text()
        sections.append({
            "document": os.path.basename(pdf_path),
            "page": page_num + 1,
            "text": text
        })
    return sections

def rank_sections(sections, job_description):
    texts = [sec["text"] for sec in sections]
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf = vectorizer.fit_transform([job_description] + texts)
    sims = cosine_similarity(tfidf[0:1], tfidf[1:]).flatten()

    for i, score in enumerate(sims):
        sections[i]["score"] = float(score)

    ranked = sorted(sections, key=lambda x: x["score"], reverse=True)
    return ranked

def process_documents(input_dir, persona, job):
    all_sections = []
    for filename in os.listdir(input_dir):
        if filename.endswith(".pdf"):
            sections = extract_sections(os.path.join(input_dir, filename))
            ranked = rank_sections(sections, job)
            all_sections.extend(ranked)

    top_sections = all_sections[:5]

    output = {
        "metadata": {
            "persona": persona,
            "job_to_be_done": job
        },
        "sections": [{
            "document": s["document"],
            "page_number": s["page"],
            "importance_rank": i+1,
            "section_text": s["text"][:300]
        } for i, s in enumerate(top_sections)]
    }
    return output

if __name__ == "__main__":
    persona = "Investment Analyst"
    job = "Analyze revenue trends, R&D investments, and market positioning strategies"

    result = process_documents("input", persona, job)
    os.makedirs("output", exist_ok=True)

    with open("output/output.json", "w") as f:
        json.dump(result, f, indent=2)
