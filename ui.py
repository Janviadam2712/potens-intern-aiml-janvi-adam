import streamlit as st
import requests

st.set_page_config(page_title="Context Engineering RAG", layout="centered")

st.title("Context Engineering — Research Q&A")
st.caption("Ask questions across 5 Context Engineering papers. Answers include citations. If it's not in the papers, it says so.")

tab1, tab2 = st.tabs(["Ask a Question", "Check for Contradictions"])

with tab1:
    query = st.text_input("Your question:")
    if st.button("Ask", key="ask_btn"):
        if query.strip():
            with st.spinner("Searching papers..."):
                try:
                    response = requests.post(
                        "http://127.0.0.1:8000/ask",
                        json={"query": query}
                    )
                    data = response.json()
                    st.subheader("Answer")
                    st.write(data["answer"])

                    st.subheader("Citations")
                    for c in data["citations"]:
                        st.markdown(f"**{c['source_file']}**, page {c['page']}")
                        st.caption(c["snippet"])
                except Exception as e:
                    st.error(f"Error: {e}")
        else:
            st.warning("Please type a question first.")

with tab2:
    doc1 = st.text_input("Document ID 1 (exact filename):", value="2510.04618v3.pdf")
    doc2 = st.text_input("Document ID 2 (exact filename):", value="2602.11988v2.pdf")
    topic = st.text_input("Topic to compare:", value="whether extra context improves agent performance")

    if st.button("Check Contradiction", key="contradict_btn"):
        with st.spinner("Comparing documents..."):
            try:
                response = requests.post(
                    "http://127.0.0.1:8000/contradict",
                    json={"doc_id_1": doc1, "doc_id_2": doc2, "topic": topic}
                )
                data = response.json()
                st.subheader("Analysis")
                st.write(data.get("analysis", data.get("reasoning", "No result")))
            except Exception as e:
                st.error(f"Error: {e}")