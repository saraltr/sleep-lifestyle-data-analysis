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

# replace inconsistent BMI labels
bmi_mapping = {
    "Normal": "Normal Weight"
}
df["BMI Category"] = df["BMI Category"].replace(bmi_mapping)

# check new distribution of occupations
# print(df["Occupation"].value_counts())

# filter and analyze sleep disorder data

# only analyze occupations with a reasonable sample size (5 or more people)
counts = df["Occupation"].value_counts()
valid_jobs = counts[counts >= 5].index
filtered_df = df[df["Occupation"].isin(valid_jobs)].copy()

# fill missing values in Sleep Disorder with No Disorder and remove any whitespace
filtered_df.loc[:, "Sleep Disorder"] = filtered_df["Sleep Disorder"].fillna("No Disorder").str.strip()

# Step 2: Analysis
# QUESTION 1: Which occupations report the highest percentage of sleep disorders?

# Group by Occupation and Sleep Disorder to count how many people per disorder type
disorder_counts = filtered_df.groupby(["Occupation", "Sleep Disorder"]).size().unstack(fill_value=0) # turns the Series into a DataFrame

# add total individuals per occupation
disorder_counts["Total"] = disorder_counts.sum(axis=1)

# calculate percentages of each disorder type
disorder_percent = disorder_counts.div(disorder_counts["Total"], axis=0) * 100

# format output as percentage strings
formatted_percent = disorder_percent[["Insomnia", "Sleep Apnea", "No Disorder"]].round(1).astype(str) + "%"
formatted_percent["Total"] = disorder_counts["Total"]

# display sleep disorder distribution
print("\n=== Sleep Disorders by Occupation ===")
print(formatted_percent)

# Conclusion:
# Sales workers are by far the most affected by sleep disorders, with 85.3% reporting insomnia and only 5.9% reporting no disorder.
# Teachers also show high insomnia levels (67.5%) and only 22.5% with no disorder.
# In contrast, Doctors, Engineers, and Lawyers have the lowest disorder rates. Over 89% of individuals in each of those professions report no sleep disorder.

# -------
# QUESTION 2: Do occupations with higher stress levels also report lower sleep quality or fewer sleep hours?

# average stress level
occupation_stress_levels = (
    filtered_df.groupby("Occupation")["Stress Level"]
    .mean().sort_values(ascending=False)
    .round(1).astype(str) + " stress level"
)

# average sleep duration
occupation_sleep_hours = (
    filtered_df.groupby("Occupation")["Sleep Duration"]
    .mean().sort_values(ascending=True)
    .round(1).astype(str) + " hours of sleep"
)

# average sleep quality
occupation_sleep_quality = (
    filtered_df.groupby("Occupation")["Quality of Sleep"]
    .mean().sort_values(ascending=True)
    .round(1)
)

# average physical activity level
occupation_physical_activity = (
    filtered_df.groupby("Occupation")["Physical Activity Level"]
    .mean().sort_values(ascending=True)
    .round(1)
)

gender_dist = filtered_df.groupby(["Occupation", "Gender"]).size().unstack(fill_value=0)
gender_dist["Total"] = gender_dist.sum(axis=1)
gender_dist["% Female"] = (gender_dist["Female"] / gender_dist["Total"] * 100).round(1)
print("\n=== Gender Distribution by Occupation ===")
print(gender_dist[["Female", "Male", "% Female"]])




# display results
print("\n=== Average Stress Levels ===")
print(occupation_stress_levels)

print("\n=== Average Sleep Duration ===")
print(occupation_sleep_hours)

print("\n=== Average Sleep Quality ===")
print(occupation_sleep_quality)

print("\n=== Average Physical Activity Level ===")
print(occupation_physical_activity)

# Conclusion:
# There’s a clear correlation between higher stress and poorer sleep health.
# Sales professionals report the highest stress level (7.1), lowest sleep duration (6.4 hours), and worst sleep quality (5.9).
# Doctors also show high stress (6.7) and poor sleep quality (6.6), although their sleep duration is slightly better (7 hours).
# Engineers, on the other hand, report the lowest stress (4.0), highest sleep duration (7.9 hours), and best sleep quality (8.3).
# This suggests that job-related stress may be strongly tied to both the quantity and quality of sleep.

# -------
# QUESTION 3: Are there noticeable differences in BMI category distribution across occupations?
# This analysis shows whether specific jobs are linked with higher rates of overweight or obesity.

# count BMI categories by occupation
bmi_counts = filtered_df.groupby(["Occupation", "BMI Category"]).size().unstack(fill_value=0)
bmi_counts["Total"] = bmi_counts.sum(axis=1)

# calculate percentage of BMI categories per occupation
bmi_percent = bmi_counts.div(bmi_counts["Total"], axis=0) * 100

# format BMI percentages
formatted_percent_bmi = bmi_percent[["Overweight", "Obese", "Normal Weight"]].round(1).astype(str) + "%"
formatted_percent_bmi["Total"] = bmi_counts["Total"]

# display BMI distribution
print("\n=== BMI Categories by Occupation ===")
print(formatted_percent_bmi)

# avg age by occupation
age_by_occupation = filtered_df.groupby("Occupation")["Age"].mean().round(1).sort_values(ascending=True)
print("\n=== Average Age by Occupation ===")
print(age_by_occupation)

