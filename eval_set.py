import requests

eval_questions = [
    {"question": "What is context engineering?", "expected_source": "2507.13334v2.pdf"},
    {"question": "What does ACE stand for?", "expected_source": "2510.04618v3.pdf"},
    {"question": "Does providing context files improve coding agent performance?", "expected_source": "2602.11988v2.pdf"},
    {"question": "What is SWE Context Bench designed to evaluate?", "expected_source": "2602.08316v3.pdf"},
    {"question": "What happens to model performance as context length increases?", "expected_source": "2307.03172v3.pdf"},
    {"question": "What percentage performance gain does ACE report?", "expected_source": "2510.04618v3.pdf"},
    {"question": "What is 'context rot'?", "expected_source": "2507.13334v2.pdf"},
    {"question": "How many tasks does SWE Context Bench evaluate?", "expected_source": "2602.08316v3.pdf"},
    {"question": "What is the capital of France?", "expected_source": None},
    {"question": "What stock should I invest in?", "expected_source": None},
]

correct = 0
total = len(eval_questions)

results_log = []

for item in eval_questions:
    response = requests.post("http://127.0.0.1:8000/ask", json={"query": item["question"]})
    data = response.json()
    citations = data.get("citations", [])
    top_source = citations[0]["source_file"] if citations else None

    if item["expected_source"] is None:
        is_correct = (data["answer"] == "Not covered in the provided documents." or not citations)
    else:
        is_correct = any(c["source_file"] == item["expected_source"] for c in citations)

    if is_correct:
        correct += 1

    results_log.append({
        "question": item["question"],
        "expected": item["expected_source"],
        "top_retrieved": top_source,
        "correct": is_correct
    })

print(f"\nRetrieval@top-k Accuracy: {correct}/{total} = {correct/total*100:.1f}%\n")
for r in results_log:
    status = "✅" if r["correct"] else "❌"
    print(f"{status} {r['question']} | expected: {r['expected']} | got: {r['top_retrieved']}")