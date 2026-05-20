import pandas as pd

# ─────────────────────────────────────────────
#  CREATING A DATAFRAME
#  A DataFrame is a table with rows and columns.
#  You pass a dict where keys = column names, values = lists of data.
# ─────────────────────────────────────────────
df = pd.DataFrame({
    "name":   ["Alice", "Bob", "Charlie", "Diana", "Eve"],
    "age":    [25, 30, 35, 28, 22],
    "city":   ["New York", "London", "Paris", "New York", "London"],
    "salary": [70000, 80000, 90000, 75000, 60000],
})


# ─────────────────────────────────────────────
#  VIEWING DATA
# ─────────────────────────────────────────────
print(df)               # print the whole table
print(df.head(3))       # first 3 rows (default head() = 5)
print(df.tail(2))       # last 2 rows
print(df.shape)         # (rows, columns) → (5, 4)
print(df.columns)       # Index of column names
print(df.dtypes)        # data type of each column
print(df.info())        # summary: types + non-null counts
print(df.describe())    # stats: mean, std, min, max, quartiles (numeric cols only)


# ─────────────────────────────────────────────
#  SELECTING COLUMNS
# ─────────────────────────────────────────────
print(df["name"])           # single column → returns a Series
print(df[["name", "age"]])  # multiple columns → returns a DataFrame


# ─────────────────────────────────────────────
#  SELECTING ROWS
#  .iloc = by integer position  (like a list index)
#  .loc  = by label / condition (more flexible)
# ─────────────────────────────────────────────
print(df.iloc[0])       # first row by position
print(df.iloc[1:3])     # rows at position 1 and 2 (slice, end is exclusive)
print(df.loc[0])        # row with index label 0
print(df.loc[0, "name"])         # single value: row 0, column "name"
print(df.loc[0:2, ["name","age"]]) # rows 0-2 (inclusive with loc!), two columns


# ─────────────────────────────────────────────
#  FILTERING ROWS  (boolean conditions)
# ─────────────────────────────────────────────
print(df[df["age"] > 27])                              # rows where age > 27
print(df[df["city"] == "London"])                      # rows from London
print(df[(df["age"] > 25) & (df["salary"] > 70000)])  # AND condition
print(df[(df["city"] == "Paris") | (df["age"] < 25)]) # OR condition


# ─────────────────────────────────────────────
#  ADDING & MODIFYING COLUMNS
# ─────────────────────────────────────────────
df["senior"] = df["age"] > 30           # new bool column
df["salary_k"] = df["salary"] / 1000    # new column derived from existing
df["name"] = df["name"].str.upper()     # overwrite column with modified values


# ─────────────────────────────────────────────
#  DROPPING COLUMNS & ROWS
#  axis=1 means columns, axis=0 (default) means rows
#  inplace=True modifies df directly instead of returning a new one
# ─────────────────────────────────────────────
df2 = df.drop(columns=["salary_k"])     # drop a column, returns new df
df3 = df.drop(index=[0, 1])             # drop rows by index label


# ─────────────────────────────────────────────
#  SORTING
# ─────────────────────────────────────────────
print(df.sort_values("age"))                          # ascending by age
print(df.sort_values("age", ascending=False))         # descending
print(df.sort_values(["city", "salary"]))             # sort by multiple columns


# ─────────────────────────────────────────────
#  GROUPBY  — split data into groups, then aggregate
#  Works like SQL GROUP BY
# ─────────────────────────────────────────────
grouped = df.groupby("city")["salary"].mean()   # avg salary per city
print(grouped)

print(df.groupby("city").agg(
    avg_salary=("salary", "mean"),
    count=("name", "count"),
    max_age=("age", "max"),
))


# ─────────────────────────────────────────────
#  AGGREGATION FUNCTIONS  (on a whole column)
# ─────────────────────────────────────────────
print(df["salary"].mean())   # average
print(df["salary"].sum())    # total
print(df["salary"].min())    # minimum
print(df["salary"].max())    # maximum
print(df["age"].median())    # median
print(df["city"].value_counts())  # count of each unique value (great for categories)
print(df["city"].nunique())       # number of unique values


# ─────────────────────────────────────────────
#  HANDLING MISSING VALUES  (NaN)
# ─────────────────────────────────────────────
import numpy as np
df_missing = df.copy()
df_missing.loc[0, "salary"] = np.nan     # introduce a missing value

print(df_missing.isnull())               # True where NaN
print(df_missing.isnull().sum())         # count NaNs per column
print(df_missing.dropna())              # drop rows with any NaN
print(df_missing.fillna(0))             # replace NaN with 0
print(df_missing["salary"].fillna(df_missing["salary"].mean()))  # fill with mean


# ─────────────────────────────────────────────
#  RENAMING COLUMNS
# ─────────────────────────────────────────────
df4 = df.rename(columns={"name": "full_name", "salary": "annual_salary"})


# ─────────────────────────────────────────────
#  RESETTING THE INDEX
#  Useful after filtering/dropping rows — index has gaps otherwise
# ─────────────────────────────────────────────
df5 = df[df["age"] > 25].reset_index(drop=True)  # drop=True discards old index


# ─────────────────────────────────────────────
#  APPLYING A CUSTOM FUNCTION
#  .apply() lets you run any function row-by-row or on a whole column
# ─────────────────────────────────────────────
df["age_group"] = df["age"].apply(lambda x: "young" if x < 30 else "senior")


# ─────────────────────────────────────────────
#  STRING OPERATIONS  (on text columns)
#  Access via .str — mirrors normal Python string methods
# ─────────────────────────────────────────────
print(df["name"].str.lower())           # lowercase
print(df["name"].str.contains("A"))     # True/False if contains letter
print(df["city"].str.replace(" ", "_")) # replace spaces


# ─────────────────────────────────────────────
#  MERGING / JOINING  (like SQL JOIN)
#  how = "inner" | "left" | "right" | "outer"
# ─────────────────────────────────────────────
extra = pd.DataFrame({
    "name":       ["ALICE", "BOB", "CHARLIE"],
    "department": ["Engineering", "Marketing", "Design"],
})
merged = pd.merge(df, extra, on="name", how="left")  # left join on "name"


# ─────────────────────────────────────────────
#  CONCATENATING DATAFRAMES  (stack rows or columns)
# ─────────────────────────────────────────────
df_a = df.iloc[:2]
df_b = df.iloc[2:]
combined = pd.concat([df_a, df_b], ignore_index=True)  # stack rows


# ─────────────────────────────────────────────
#  READING & WRITING FILES
# ─────────────────────────────────────────────
# df.to_csv("output.csv", index=False)   # save to CSV (index=False skips row numbers)
# df = pd.read_csv("data.csv")           # load from CSV

# df.to_excel("output.xlsx", index=False)
# df = pd.read_excel("data.xlsx")

# df.to_json("output.json")
# df = pd.read_json("data.json")
