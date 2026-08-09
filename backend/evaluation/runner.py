import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.retriever import hybrid_retrieve
import json

with open("evaluation/test_set.json", "r") as f:
    tests = json.load(f)

hits = 0
total = len(tests)

for test in tests:
    results = hybrid_retrieve(test["question"], top_k=3)
    retrieved_sources = [r["metadata"]["source"] for r in results]
    if test["ground_truth_doc"] in retrieved_sources:
        hits += 1

print(f"Hit@3 Rate: {hits / total * 100:.2f}%")