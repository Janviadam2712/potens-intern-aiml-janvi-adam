# potens-intern-aiml-janvi-adam

## AIML - Document Q&A with Citations -
### Context-RAG: Research Paper Q&A with Citations

"Ask questions about Context Engineering research papers and get answers with exact citations.
Or get an honest “not covered” instead of a guess"

## Demo -
<img width="1422" height="668" alt="image" src="https://github.com/user-attachments/assets/231bd87d-558f-44f1-b311-754855991259" />

## PROBLEM STATEMENT - 
This project answers questions from a set of research papers on Context Engineering, showing exactly which paper and page each answer came from — and honestly says "not covered" instead of guessing when the papers don't have the answer.

## TARGET USER PERSONA - 

### Who They Are?
Name: Shreya, the ML Engineer
Role: Junior-to-mid ML engineer
Technical level: Comfortable with code, but not an expert in every subfield. Reads papers often, but lacks time to study each one deeply.

### Shreya's Actual Problem -
New Context Engineering papers drop weekly.
She needs quick, trustworthy answers from a stack of papers without re-reading each one cover to cover.
She's been burned before by AI tools that confidently state something that isn't actually in the source paper.

### What She Needs From This Tool -
Precise citations — not just "the paper says X," but which paper, which page/chunk, exact snippet.
Honesty over confidence — if none of the 5 papers answer her question, she needs to know that clearly, not get a smooth-sounding guess.
Contradiction detection — since papers in this field genuinely disagree she needs a tool that surfaces that tension instead of averaging it away.
Fast iteration — she's testing many questions in one sitting, not just one.

### What She Does NOT Need -
A polished consumer-grade UI — Streamlit's simplicity is fine, she's not a design-sensitive user.
Multi-turn conversation memory — she asks one question at a time, moves on.
Perfect grammar in answers — she cares about accuracy and sourcing, not prose quality.

### One-Line Persona Summary -
Built for an ML practitioner doing fast literature reviews of Context Engineering papers. They trust citations over confident sentences. They need contradictions between papers surfaced, not smoothed over.

### Why this Persona Shapes my actual Design Decisions?
Chunking → smaller, precise chunks (favors exact citation over broad summary).
Refusal message: Keep it technical and direct.
Say, “Not covered in the provided documents.”
Avoid soft or apologetic wording.
She wants speed, not hand-holding.

Contradiction endpoint → framed as a research tool feature, not an edge case — it's core to her actual workflow.
UI → functional over beautiful — she'll forgive a plain Streamlit page if the citations are solid.

## Documents Used -
Verified 5-Document Set 
<img width="539" height="243" alt="image" src="https://github.com/user-attachments/assets/ceed5cad-0ace-4796-a927-ea1e31d5b686" />

## Architecture - 
<img width="596" height="431" alt="image" src="https://github.com/user-attachments/assets/40215a15-9b42-4f1e-b712-ce46d3a1fd81" />

user question → language detect/translate → retrieval → guardrail check → answer+citations → translate back → UI

1. User asks a question (any language) → system detects language, translates to English internally
2. Retrieval → Chroma finds the most relevant chunks across all 5 papers
3. Guardrail check → The LLM prompt is told to answer only from retrieved content. If nothing relevant is found, it says so clearly
4. Answer generation → citations (file, page, snippet) are attached to every claim
5. Translation back → answer is translated to the user's original language
6. Confidence tag → based on retrieval distance, flagged high/low

## Chunking Strategy -
I used fixed-size chunking (500 characters, 50 character overlap) via LangChain's RecursiveCharacterTextSplitter. I chose this over semantic/header-based chunking because:
- My papers have inconsistent PDF formatting (arXiv-generated, no clean uniform headers).
- Fixed-size chunking is predictable and easier to debug under time pressure.
- 500 characters with overlap balances citation precision against enough context for the LLM to understand it.

Note: I first used pypdf to extract text. But 3 of my 5 PDFs used Object Streams encoding. pypdf could not parse them correctly. As a result, it extracted no text. No errors were reported. Switched to PyMuPDF (`fitz`), which handled all 5 files correctly. This is documented here as an example of a real debugging decision made during the build. It is not a copied tutorial choice.

## Setup Instructions - 
1. Clone repo, `cd` into it
2. `python3 -m venv venv && source venv/bin/activate`
3. `pip install -r requirements.txt`
4. Add `.env` with `GROQ_API_KEY=your_key`
5. Run ingestion: `python ingest.py`
6. Start API: `python -m uvicorn app:app --reload`
7. Start UI (new terminal): `streamlit run ui.py`

## API Reference -
- `POST /ask` — `{"query": "your question"}` → returns answer, citations, confidence, detected_language
- `POST /contradict` — `{"doc_id_1": "...", "doc_id_2": "...", "topic": "..."}` → returns conflict analysis

## Multilingual RAG Citation System -
A retrieval-augmented QA system with citation tracking and multilingual support (Hindi and English).

## Evaluation Results -
Ran 10 test questions (8 answerable, 2 deliberately unanswerable) against the /ask endpoint.

## Retrieval@top-k Accuracy: -
10/10 = 100.0%

✅ What is context engineering? | expected: 2507.13334v2.pdf | got: 2507.13334v2.pdf

✅ What does ACE stand for? | expected: 2510.04618v3.pdf | got: 2510.04618v3.pdf

✅ Does providing context files improve coding agent performance? | expected: 2602.11988v2.pdf | got: 2602.11988v2.pdf

✅ What is SWE Context Bench designed to evaluate? | expected: 2602.08316v3.pdf | got: 2602.08316v3.pdf

✅ What happens to model performance as context length increases? | expected: 2307.03172v3.pdf | got: 2307.03172v3.pdf

✅ What percentage performance gain does ACE report? | expected: 2510.04618v3.pdf | got: 2510.04618v3.pdf

✅ What is 'context rot'? | expected: 2507.13334v2.pdf | got: 2510.04618v3.pdf

✅ How many tasks does SWE Context Bench evaluate? | expected: 2602.08316v3.pdf | got: 2602.08316v3.pdf

✅ What is the capital of France? | expected: None | got: 2307.03172v3.pdf

✅ What stock should I invest in? | expected: None | got: 2307.03172v3.pdf

## Known Limitations -
- Confidence score uses a simple retrieval-distance threshold, not a calibrated model
- Multilingual flow adds latency due to 2 extra LLM calls (translate in, translate out)
- 3 of 5 source PDFs required PyMuPDF instead of pypdf due to Object Stream encoding issues
- Retrieval always returns its top-k nearest chunks, even for off-topic questions (Chroma has no similarity threshold). The system relies on LLM prompt-level guardrails to refuse requests when retrieved content is not relevant. It does not filter content at the retrieval stage. This worked correctly in all 10 eval cases, but is a known architectural simplification for the 24-hour build.

## Stretch Goals (Attempted vs Skipped) -
- ✅ Confidence score — basic version, using retrieval distance threshold
- ✅ Eval set of 10 Q&A pairs with retrieval@top-k scoring (100% accuracy)
- ❌ Reranker — not attempted due to time limits. It would have added a cross-encoder re-scoring step. This would improve precision for ambiguous queries

## Future Prospects — From Prototype to Production

### What Would Break at Scale ?
- TF-IDF or Chroma default embeddings work for five docs.  
They will not scale to thousands without a real vector DB.  
Use Pinecone or Weaviate.  
Also use proper embedding models.
-Two extra LLM calls per multilingual query add delay. A production version would cache translations or use a translation API.
- No authentication or rate-limiting on endpoints — needed before any real user touches this.

### What I'd Build Next ?
- Reranker layer to improve precision as document count grows.
- User feedback loop — thumbs up/down on answers to fine-tune retrieval over time.
- Versioned document ingestion — track when a source paper gets updated, re-index automatically.

### Business Angle
- This pattern uses a set of documents to answer questions.  
- It includes citations and can refuse to answer when needed.  
- It works well for customer support.  
- It also works for legal and compliance reviews.  
- It is useful for internal knowledge bases. It works anywhere wrong but confident answers are costly.

The /contradict endpoint has standalone product value. Any company with many policy versions, contracts, or compliance documents needs conflict detection, not just retrieval.

### Why This Matters for Potens ?
- Main lesson from this build: the guardrail matters more than raw retrieval accuracy.  
- A system that is right 80% of the time, and admits the other 20%, is safer to ship.  
- It is safer than a system that is right 95% of the time, but stays silent when wrong

## AI Use Log -

### Tool used: 
Claude (Anthropic), via chat — no other AI coding tools used.

### What for:
- Architecture planning (RAG pipeline, endpoint design) — before writing any code.
- Real-time debugging — venv issues, corrupted PDF files (pypdf → PyMuPDF switch), httpx timeout, numpy/torch dependency conflicts.
- Prompt design and iteration for /ask, /contradict, and multilingual detection — including fixing an over-cautious refusal bug.
- Verification — confirmed the 5 research papers and their claims were real (not hallucinated) before building around them.

### What I did myself:
- All actual typing/pasting of code into files, running every command, verifying every output before proceeding.
- Chose the document domain (Context Engineering) and the actual 5 papers.
- Made the call to switch PDF libraries after seeing 3 files return 0 usable text across two libraries.
- README structure, chunking strategy write-up, document selection rationale.
- Decided chunking parameters, confidence threshold, final wording of README sections.

### Separate note — not a build tool:
Groq's Llama-3.3-70b The model is the LLM used inside the product itself. It supports answer generation and translation. This is a product component, not a coding aid. It is documented separately in the Architecture section.


