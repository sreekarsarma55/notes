# TDS — course overview

## Grading split

| Component | Weight |
|---|---|
| Graded assignments (best 7 of 9, GA0–GA8) | 20% |
| Project 1 | 20% |
| Project 2 | 20% |
| ROE (remote online exam) | 20% |
| Final end-term (in person) | 20% |

**GA0 counts.** The Sep 2026 FAQ states plainly that GA0 marks contribute to the
GAA average. Scoring below 40% does *not* remove you from the course — it is a
readiness signal, not a gate — but the marks are real, so treat it as an assignment
rather than a diagnostic.

Total GA0 weight: **35.5 marks**. 40% ≈ **14.2 marks**.

## Weekly topics (May/Sep 2026 edition)

| Week | Theme |
|---|---|
| 0 | Bridge course: install, Linux/shell, VS Code + `uv`, HTTP/DevTools/curl, Git |
| 1 | Dev environment: VS Code, `uv`, bash, git, SQLite, HTTP clients, data formats, GitHub Pages, LaTeX |
| 2 | Deployment & APIs: FastAPI, CORS, OAuth, Docker, observability, local LLMs |
| 3 | LLM engineering: prompt/context engineering, structured output, embeddings |
| 4 | RAG & hybrid RAG: vector DBs, chunking, reranking, RAGAS |
| 5 | Agentic AI: tool calling, memory, multi-agent, MCP, sandboxing |
| 6 | Web data acquisition & OSINT: hidden JSON APIs, Playwright, anti-bot, DuckDB/Parquet |
| 7 | CI/CD, security & cloud: GH Actions, LLM red-teaming, VMs, Terraform |
| 8 | MLOps & fine-tuning: MLflow, HuggingFace, LoRA, quantization |

## Strategy notes

- **The course is openly collaborative.** Internet, LLMs, friends, shared code are
  all explicitly allowed, including in projects. Understanding what you copy is
  the actual assessed skill.
- **Sequence GA0 by cost, not by order.** Several questions need a deployed public
  endpoint; one (Build a Binary Eval Rubric) spends ~90 AI Pipe calls *per attempt*
  against a $1–2/month budget. Do the free, deterministic ones first.
- **One deployment can answer several questions.** Q5, Q10, Q11 and Q25 all want a
  public HTTP endpoint — a single FastAPI app on Vercel serves all four paths.
- **Save, don't just Check.** Pressing *Check* only validates; only *Save* records a
  submission, and the last save before the deadline is the official score.
- **Budget.** AI Pipe gives `@ds.study.iitm.ac.in` emails ~$1–2 per calendar month.
  Prefer deterministic solutions over LLM calls wherever the grader allows it.

## Deadline

GA0 (Sep 2026 term): **Sun 11 Oct 2026, 11:59 pm IST**.
