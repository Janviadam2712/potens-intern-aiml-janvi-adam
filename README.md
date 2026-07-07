# potens-intern-aiml-janvi-adam

PROBLEM STATEMENT - This project answers questions from a set of research papers on Context Engineering, showing exactly which paper and page each answer came from — and honestly says "not covered" instead of guessing when the papers don't have the answer.

TARGET USER PERSONA - Who They Are
Name: Shreya, the ML Engineer
Role: Junior-to-mid ML engineer
Technical level: Comfortable with code, NOT an expert in every subfield — reads papers regularly but doesn't have time to deep-read all of them.

Shreya's Actual Problem -
New Context Engineering papers drop weekly.
She needs quick, trustworthy answers from a stack of papers without re-reading each one cover to cover.
She's been burned before by AI tools that confidently state something that isn't actually in the source paper.

What She Needs From This Tool -
Precise citations — not just "the paper says X," but which paper, which page/chunk, exact snippet.
Honesty over confidence — if none of the 5 papers answer her question, she needs to know that clearly, not get a smooth-sounding guess.
Contradiction detection — since papers in this field genuinely disagree she needs a tool that surfaces that tension instead of averaging it away.
Fast iteration — she's testing many questions in one sitting, not just one.

What She Does NOT Need -
A polished consumer-grade UI — Streamlit's simplicity is fine, she's not a design-sensitive user.
Multi-turn conversation memory — she asks one question at a time, moves on.
Perfect grammar in answers — she cares about accuracy and sourcing, not prose quality.

One-Line Persona Summary -
Built for an ML practitioner doing rapid literature review across Context Engineering papers — someone who trusts a citation over a confident-sounding sentence, and needs contradictions between papers surfaced, not smoothed over.

Why this Persona Shapes my actual Design Decisions -
Chunking → smaller, precise chunks (favors exact citation over broad summary).
Refusal message → technical and direct ("Not covered in the provided documents") rather than soft/apologetic — she wants speed, not hand-holding.
Contradiction endpoint → framed as a research tool feature, not an edge case — it's core to her actual workflow.
UI → functional over beautiful — she'll forgive a plain Streamlit page if the citations are solid.
