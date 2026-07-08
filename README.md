# potens-intern-aiml-janvi-adam

## AIML - Document Q&A with Citations
### Context-RAG: Research Paper Q&A with Citations

"Ask questions about Context Engineering research papers and get answers with exact citations.
Or get an honest “not covered” instead of a guess"

## Demo
(Screenshot/GIF to be added once the Streamlit UI is complete — see Setup Instructions to run locally in the meantime.)

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

## Chunking Strategy

I used fixed-size chunking (500 characters, 50 character overlap) via LangChain's RecursiveCharacterTextSplitter. I chose this over semantic/header-based chunking because:
- My papers have inconsistent PDF formatting (arXiv-generated, no clean uniform headers).
- Fixed-size chunking is predictable and easier to debug under time pressure.
- 500 characters with overlap balances citation precision against enough context for the LLM to understand it.

Note: I first used pypdf to extract text. But 3 of my 5 PDFs used Object Streams encoding. pypdf could not parse them correctly. As a result, it extracted no text. No errors were reported. Switched to PyMuPDF (`fitz`), which handled all 5 files correctly. This is documented here as an example of a real debugging decision made during the build. It is not a copied tutorial choice.

## Multilingual RAG Citation System

A retrieval-augmented QA system with citation tracking and multilingual support (Hindi and English).

