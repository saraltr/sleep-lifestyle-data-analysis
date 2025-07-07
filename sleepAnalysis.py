import pandas as pd

# load the dataset
df = pd.read_csv("Sleep_health_and_lifestyle_dataset.csv")

# Step 1
# clean and prepare the data

# check for missing values in each column
# print(df.isnull().sum())

# group similar roles into broader categories
occupation_mapping = {
    "Sales Representative": "Sales",
    "Salesperson": "Sales",
    "Software Engineer": "Engineer"
}
df["Occupation"] = df["Occupation"].replace(occupation_mapping)

# check new distribution of occupations
# print(df["Occupation"].value_counts())

# Step 2
# filter and analyze sleep disorder data

# only analyze occupations with a reasonable sample size (5 or more people)
counts = df["Occupation"].value_counts()
valid_jobs = counts[counts >= 5].index
filtered_df = df[df["Occupation"].isin(valid_jobs)]

# fill missing values in Sleep Disorder with No Disorder and remove any whitespace
filtered_df.loc[:, "Sleep Disorder"] = filtered_df["Sleep Disorder"].fillna("No Disorder").str.strip()


# Group by Occupation and Sleep Disorder to count how many people per disorder type
disorder_counts = filtered_df.groupby(["Occupation", "Sleep Disorder"]).size().unstack(fill_value=0)


# counts of each sleep disorder type per occupation
# print(disorder_counts)

# Step 3
# calculate proportions

# Add a new column with total number of people per occupation
disorder_counts["Total"] = disorder_counts.sum(axis=1)

# Calculate the percentage of each disorder type per occupation
disorder_percent = disorder_counts.div(disorder_counts["Total"], axis=0) * 100

# Format percentage values and add the raw count
formatted_percent = disorder_percent[["Insomnia", "Sleep Apnea", "No Disorder"]].round(1).astype(str) + "%"
formatted_percent["Total"] = disorder_counts["Total"]

# rint result
print(formatted_percent)