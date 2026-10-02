import pandas as pd
want = {"\u2020", "\u017e", "\u201a"}   # † ž ‚
a = pd.read_csv("q22/data1.csv", encoding="cp1252")
b = pd.read_csv("q22/data2.csv", encoding="utf-8")
c = pd.read_csv("q22/data3.txt", encoding="utf-16", sep="\t")
df = pd.concat([a, b, c])
print("Q22", int(df[df.symbol.isin(want)].value.sum()), "first3:", list(a.symbol[:3]))
