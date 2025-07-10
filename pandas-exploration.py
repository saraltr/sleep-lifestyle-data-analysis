import pandas as pd

# load and read dataset
df = pd.read_csv("Sleep_health_and_lifestyle_dataset.csv")
print(df.shape)

# explore the data
df.head()          # first 5 rows
df.tail()          # last 5 rows
df.shape           # rows & columns
df.columns         # list of column names
df.info()          # data types and non-null values
df.describe()      # summary stats for numerical columns

# select and filter
df["Sleep duration"]                     # select one column (returns a Series)
df[["Occupation", "Sleep duration"]]     # select multiple columns

# filter rows 
df[df["Occupation"] == "Engineer"]

# filter with multiple conditions
df[(df["Occupation"] == "Engineer") & (df["Sleep duration"] > 7)]

# clean data
df.isnull().sum()   # count missing values in each column
df.dropna() # remove rows with missing values
df.fillna(0)    # replace missing values with 0
df["Occupation"] = df["Occupation"].str.lower()  # normalize strings
df = df.drop_duplicates()   # remove duplicated rows


# Analyze and Aggregate
# average
df.groupby("Occupation")["Sleep duration"].mean()

# count values
df["Occupation"].value_counts()

# count by condition
df.groupby("Occupation")["Sleep disorder"].value_counts()

# sort
df.sort_values(by="Sleep duration", ascending=False)