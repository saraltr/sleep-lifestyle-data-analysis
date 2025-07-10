import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

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
# print("\n=== Sleep Disorders by Occupation ===")
# print(formatted_percent)


#  clustered bar chart for better vizualisation 
plt.figure(figsize=(10, 6))
occupation_names = filtered_df.groupby("Occupation").size().index.tolist()
# print(occupation_names)

# define the x-axis group labels
labels = occupation_names

# get the percentage values for each type
insomnia = disorder_percent["Insomnia"].tolist()
sleep_apnea = disorder_percent["Sleep Apnea"].tolist()
no_disorder = disorder_percent["No Disorder"].tolist()

# set up positions for the bars
x = np.arange(len(labels))
width = 0.25  # width of each bar

# plot each category with an offset
plt.bar(x - width, insomnia, width, label="Insomnia")
plt.bar(x, sleep_apnea, width, label="Sleep Apnea")
plt.bar(x + width, no_disorder, width, label="No Disorder")

# customize chart
plt.title("Sleep Disorders by Occupation (%)")
plt.ylabel("Percentage")
plt.xticks(x, labels, rotation=45)  # add labels
plt.ylim(0, 100)  # percent scale
plt.legend()

# Optional: add value labels on top of bars (rounded percentages)
offset = 0.5  # small relative offset above each bar

for i in range(len(labels)):
    plt.text(x[i] - width, insomnia[i] + offset, f"{insomnia[i]:.1f}%", ha="center", va="bottom", fontsize=8)
    plt.text(x[i], sleep_apnea[i] + offset, f"{sleep_apnea[i]:.1f}%", ha="center", va="bottom", fontsize=8)
    plt.text(x[i] + width, no_disorder[i] + offset, f"{no_disorder[i]:.1f}%", ha="center", va="bottom", fontsize=8)


#  prevent labels to be cutoff
plt.tight_layout()
# display the chart
plt.show()
plt.close()

# Conclusion:
# Sales workers are the most affected by sleep disorders, with 85.3% reporting insomnia, 8.8% reporting sleep apnea, and only 5.9% reporting no disorder.
# Nurses report the highest levels of sleep apnea (83.6%) which is significantly higher than in any other profession surveyed where sleep apnea rates range from 0% to just 10%. 
# Teachers also show high insomnia levels (67.5%) and only 22.5% with no disorder.
# In contrast, Doctors, Engineers, Accountans, and Lawyers have the lowest disorder rates. Over 80% of individuals in each of those professions report no sleep disorder.

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

# display results
# print("\n=== Average Stress Levels ===")
# print(occupation_stress_levels)

# print("\n=== Average Sleep Duration ===")
# print(occupation_sleep_hours)

# print("\n=== Average Sleep Quality ===")
# print(occupation_sleep_quality)

# print("\n=== Average Physical Activity Level ===")
# print(occupation_physical_activity)


# clustered bar chart with two Y-axes
# get the values for each bar
stress_levels_list = (
    filtered_df.groupby("Occupation")["Stress Level"].mean().round(1).tolist()
)

sleep_hours_list = (
    filtered_df.groupby("Occupation")["Sleep Duration"].mean().round(1).to_list()
)

sleep_quality_list = (
    filtered_df.groupby("Occupation")["Quality of Sleep"].mean().round(1).tolist()
)

phy_activity_list = (
    filtered_df.groupby("Occupation")["Physical Activity Level"].mean().round(1).tolist()
)


# creates a new figure
fig, ax1 = plt.subplots(figsize=(9, 6))

# set up positions and width based on the same occupation data we gathered before
x = np.arange(len(labels))
width = 0.25

# plot on primary y axis
ax1.bar(x - width, stress_levels_list, width, label="Stress Level")
ax1.bar(x, sleep_hours_list, width, label="Sleep Duration")
ax1.bar(x + width, sleep_quality_list, width, label="Sleep Quality")

# customize primary y axis
ax1.set_ylabel("Scale (0–10)")
ax1.set_ylim(0, 10)
ax1.set_xticks(x)
ax1.set_xticklabels(labels, rotation=45)
ax1.set_title("Stress, Sleep, and Physical Activity by Occupation")

# secondary y axis for physical activity
ax2 = ax1.twinx()
ax2.set_ylabel("Physical Activity Level (0-100)")
ax2.plot(x, phy_activity_list, label="Physical Activity", color="tab:red", marker="o", linewidth=2)
ax2.set_ylim(0, 100)

# combine legends from both axes
lines_1, labels_1 = ax1.get_legend_handles_labels()
lines_2, labels_2 = ax2.get_legend_handles_labels()
ax1.legend(lines_1 + lines_2, labels_1 + labels_2,)

# displaye the chart
plt.tight_layout()
plt.show()
plt.close()

# Conclusion:
# There’s a clear correlation between higher stress and poorer sleep health.
# Sales workers report the highest stress level (7.1), lowest sleep duration (6.4 hours), and worst sleep quality (5.9).
# Doctors also show high stress (6.7) and poor sleep quality (6.6), although their sleep duration is slightly better (7 hours).
# Engineers, on the other hand, report the lowest stress (4.0), highest sleep duration (7.9 hours), and best sleep quality (8.3).
# Interestingly, physical activity levels appear to vary independently as nurses (78.6) and lawyers (70.4) report the highest activity, while engineers (51.6) and sales workers (44.1) are less active. Despite lower activity, engineers report excellent sleep, which may mean stress has a stronger influence on sleep health than physical activity alone.

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

# avg age by occupation
age_by_occupation = filtered_df.groupby("Occupation")["Age"].mean().round(1).sort_values(ascending=True)


# gender percent per occupation
gender_counts = filtered_df.groupby(["Occupation", "Gender"]).size().unstack(fill_value=0)
gender_counts["Total"] = gender_counts.sum(axis=1)
gender_percent = gender_counts.div(gender_counts["Total"], axis=0 ) *100
gender_formatted = gender_percent[["Male", "Female"]].round(1).astype(str) + "%"


# display results
# print("\n=== BMI Categories by Occupation ===")
# print(formatted_percent_bmi)
# print("\n=== Average Age by Occupation ===")
# print(age_by_occupation)
# print("\n=== Gender by Occupation ===")
# print(gender_formatted)


# BMI bar chart
fig, ax1 = plt.subplots(figsize=(9, 6))

# set primary y axis for BMI data
ax1.set_xlabel("Occupation")
ax1.set_ylabel("% Overweight + Obese")

# calculate combined BMI percentage
bmi_combined = bmi_percent["Overweight"] + bmi_percent["Obese"]

# plot BMI as a blue bar chart
bars = bmi_combined.plot(kind="bar", ax=ax1)
ax1.tick_params(axis="y")

# Rotate x-axis labels 45 degrees
ax1.set_xticklabels(bmi_combined.index, rotation=45, ha='right') 

# adds the dominant gender for that occupation
for i, occupation in enumerate(bmi_combined.index):
    percent_male = gender_percent.loc[occupation, "Male"]
    percent_female = gender_percent.loc[occupation, "Female"]

    # create label showing dominant gender and its percentage
    if percent_male > percent_female:
        label = f"{percent_male:.0f}% M"
    else:
        label = f"{percent_female:.0f}% F"

    # place the label above each bar
    ax1.text(i, bmi_combined[occupation] + 1, label, ha="center", va="bottom")

# create a secondary y axis for average age
ax2 = ax1.twinx()

# plot average age as a red line
color = "tab:red"
age_by_occupation[bmi_combined.index].plot(
    ax=ax2, color=color, marker="o", linewidth=2
)

# set properties for the secondary y-axis
ax2.set_ylabel("Average Age", color=color)
ax2.tick_params(axis="y", labelcolor=color)

plt.title("BMI Rate vs. Age by Occupation (with Dominant Gender %)")
plt.tight_layout()
plt.show()


# Conclusion:
# There are noticeable and significant differences in BMI category distribution across occupations, such as:
# Sales, nurses, and teachers are much more likely to be overweight or obese (85%–100% of participants)
# Doctors, engineers, and lawyers maintain predominantly healthy weights

# Is age or physical activity enough to explain this?
# No, because while physical activity is generally associated with better weight management, and age can influence metabolism, they don't fully explain the differences because:
# Nurses have the highest physical activity level, yet also have poor BMI results.
# Similarly, engineers are older on average and have only moderate physical activity (51.6), yet maintain healthy BMI levels.
# This suggested that other factorssuch as sleep quality & hours, stress, or working conditions might play a more important role in shaping BMI results.

# What about gender?
# Occupations with the highest overweight/obesity rates tend to be female-dominated (e.g. nurses, teachers).
# However, sales, a male-dominated field, also has extremely poor BMI results, which suggest that gender is also not enough to explain that alone the differences in BMI across occupations.

# ----

# Extended conclusion: revisiting BMI with sleep as a key factor 
#  Additional question: What if sleep quality and sleep duration were stronger predictors of BMI than age or physical activity?

# While the initial analysis showed clear differences in BMI across occupations the explanation wasn’t fully satisfying. Age, gender, and physical activity provided some clues, but they couldn’t explain everything.

# combine overweight + obese percentages to represent the total proportion of participants in each occupation with above-normal BMI
bmi_overweight_obese = bmi_percent["Overweight"] + bmi_percent["Obese"]

# get average sleep quality and duration by occupation
sleep_quality = filtered_df.groupby("Occupation")["Quality of Sleep"].mean()
sleep_duration = filtered_df.groupby("Occupation")["Sleep Duration"].mean()

# scatter plot BMI vs sleep quality to visualize correlation
fig, ax = plt.subplots(1, 2, figsize=(10,4))


ax[0].scatter(sleep_quality, bmi_overweight_obese)
for i, occ in enumerate(bmi_overweight_obese.index):
    ax[0].annotate(occ, (sleep_quality.iloc[i], bmi_overweight_obese.iloc[i]))
ax[0].set_xlabel("Average Sleep Quality")
ax[0].set_ylabel("% Overweight + Obese")
ax[0].set_title("BMI vs Sleep Quality by Occupation")

# Scatter plot BMI vs Sleep Duration
ax[1].scatter(sleep_duration, bmi_overweight_obese)
for i, occ in enumerate(bmi_overweight_obese.index):
    ax[1].annotate(occ, (sleep_duration.iloc[i], bmi_overweight_obese.iloc[i]))
ax[1].set_xlabel("Average Sleep Duration (hours)")
ax[1].set_ylabel("% Overweight + Obese")
ax[1].set_title("BMI vs Sleep Duration by Occupation")

plt.tight_layout()
plt.show()

# Conclusion

# By comparing the percentage of overweight + obese individuals in each occupation with their average sleep quality and average sleep duration, I discorved the following patterns:

# Salespeople:
# Worst sleep quality (5.9) and shortest sleep (6.4 hours)
# Highest BMI problem rate (~100% overweight/obese)

# Teachers & Nurses:
# Poor sleep (6.3–6.4 quality, 6.6 hours)
# Very high BMI issues (~85%–90%)

# Engineers & Lawyers:
# Best sleep (7.8–8.3 quality, 7.6–7.9 hours)
# Healthiest BMI profiles

# Doctors are the exception:
# Poorer sleep than expected (6.6 quality, 7.0 hours)
# But better BMI than engineers — suggesting **protective factors** like medical knowledge, healthier habits, or better dietary choices.

# Final Insights:

# Sleep quality and duration strongly correlate with BMI outcomes across occupations.
# Occupations with poor sleep (sales, teachers, nurses) consistently show worse BMI, even if physical activity is high.
# Engineers and lawyers maintain healthy weights possibly due to better sleep routines, even with sedentary work and older age.
# Doctors are a special case, they sleep habits are poor but they are able stay healthy, likely due to other unmeasured lifestyle factors.