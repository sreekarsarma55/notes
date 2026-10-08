import json, numpy as np
d = json.load(open("q11-task.json"))
ids = [x["doc_id"] for x in d["documents"]]
D = np.array([x["embedding"] for x in d["documents"]])
D = D / np.linalg.norm(D, axis=1, keepdims=True)          # don't trust "already normalised"
out = {}
for q in d["queries"]:
    v = np.array(q["embedding"]); v = v / np.linalg.norm(v)
    sims = D @ v
    order = sorted(range(len(ids)), key=lambda i: (-round(float(sims[i]), 12), ids[i]))  # desc sim, then smaller id
    out[q["query_id"]] = [ids[i] for i in order[:5]]
print(json.dumps(out))
