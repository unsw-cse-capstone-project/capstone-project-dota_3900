import pandas as pd

df = pd.read_csv("test.csv")

print(df.columns)
# print(df.ISBN13.value_counts())
# print(df.book_cover_url.value_counts())
print(df.categories.value_counts())
