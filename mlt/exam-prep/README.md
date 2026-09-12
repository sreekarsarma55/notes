# 🎯 End-Term Exam Prep

Phone-friendly revision. Open these on GitHub — no laptop needed.

| File | Use it for |
|---|---|
| [`most-likely-questions.md`](most-likely-questions.md) | 🚨 **READ FIRST.** 5 patterns that appeared in BOTH 2026 papers |
| [`question-archetypes.md`](question-archetypes.md) | The 15 recurring question types + method + trap |
| [`solved-fn-2026.md`](solved-fn-2026.md) | FN T1 2026 worked out, answers verified |
| [`solved-an-2026.md`](solved-an-2026.md) | AN T1 2026 worked out, answers verified |
| [`practice-paper-patterns.md`](practice-paper-patterns.md) | 8 extra patterns from the solved practice papers |
| [`../cheat-sheet.md`](../cheat-sheet.md) | All formulas, Weeks 1–12 |
| [`../pyq-analysis.md`](../pyq-analysis.md) | Auto-extracted topic/marks stats |

## Paper shape (identical in all 7 past papers)

```text
15-18 questions   ·   50 marks
SA  (type a number)      39% of marks
MCQ (one correct)        36%
MSQ (select all)         25%
```

## Topic ranking by marks

```text
SVM              11.5%   <- biggest, by 3x
Ensembles         5.9%
PCA               4.6%
Decision trees    4.3%
Logistic reg.     3.9%
Kernels           3.9%
KNN               3.1%
Ridge / Lasso     2.9%
MLE / Bayesian    2.6%
Linear reg.       2.4%
Perceptron        2.3%
Neural nets       2.3%
Losses            2.0%
Naive Bayes       1.7%
K-means           1.3%
```

Note: ~45% of questions could not be auto-tagged (their
content is images), so these are lower bounds. The
ranking is reliable; SVM leading is unambiguous.

## Study order if time is short

```text
1. SVM        - dual, the 3 alpha cases, margin 2/||w||
2. Ensembles  - bagging vs boosting, (1-1/n)^n
3. Trees      - information gain, region area
4. Logistic   - sigmoid threshold -> count
5. PCA        - variance = eigenvalue
6. Perceptron / NN / losses
```

## 5 exam-day rules

1. **SA = 39% of marks, no partial credit.** Do the
   arithmetic twice.
2. **MSQ is all-or-nothing.** The false option usually
   contains *always / never / guaranteed*.
3. **Check the label convention.** Logistic uses
   `y ∈ {0,1}`; perceptron and SVM use `y ∈ {−1,+1}`.
4. **"Ignore the biases"** appeared twice in 2026 for
   the neural-net parameter count. Read the fine print.
5. Convert probability thresholds to score cut-offs
   before comparing (see archetype 5).
