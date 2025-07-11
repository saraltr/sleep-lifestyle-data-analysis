import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


st.set_page_config(page_title="Sleep Dashboard", layout="centered")
st.title("Sleep Health and Lifestyle")

# caches the result to avoid reloading on every rerun
@st.cache_data
def load_data():
    df = pd.read_csv("Sleep_health_and_lifestyle_dataset.csv")

    # fill missing values in and remove extra whitespace
    df["Sleep Disorder"] = df["Sleep Disorder"].fillna("No Disorder").str.strip()

    # grouping similar roles
    df["Occupation"] = df["Occupation"].replace({
        "Sales Representative": "Sales",
        "Salesperson": "Sales",
        "Software Engineer": "Engineer"
    })

    # combine normal and normal weight BMI categories
    df["BMI Category"] = df["BMI Category"].replace({"Normal": "Normal Weight"})

    return df

data_load_state = st.text("Loading data...")
df = load_data()
data_load_state.text("Loading data...done! (using st.cache_data)")

# filter
if st.checkbox("Show raw data"):
    st.subheader("Raw Data")
    st.dataframe(df)

# occupation Filter
valid_jobs = df["Occupation"].value_counts()[lambda x: x >= 5].index

selected_jobs = st.multiselect(
    "Select Occupations to display:", 
    valid_jobs, 
    default=valid_jobs, 
    help="Please select at least one job to view data."
)

# defaulting to all jobs if user clears all
if not selected_jobs:
    st.info("At least one occupation must be selected.")
    selected_jobs = valid_jobs

# filter the dataset to include only the selected occupations
filtered_df = df[df["Occupation"].isin(selected_jobs)]

# get the unique occupation labels for the x-axis
labels = filtered_df["Occupation"].unique().tolist()
x = np.arange(len(labels))
width = 0.25 # width of each bar

# 1. Sleep disorder distribution by occupation bar chart
st.subheader("Question 1: Which occupations report the highest percentage of sleep disorders?")
st.write("Hello! This is a general-purpose way to write text.")

# count the number of occurrences for each occupation/ sleep disorder pair
disorder_counts = filtered_df.groupby(["Occupation", "Sleep Disorder"]).size().unstack(fill_value=0)

# convert counts to percentages
disorder_pct = disorder_counts.div(disorder_counts.sum(axis=1), axis=0) * 100

# extract percentages for main disorder types
insomnia = disorder_pct.get("Insomnia", pd.Series([0]*len(labels), index=labels)).reindex(labels).fillna(0).tolist()

sleep_apnea = disorder_pct.get("Sleep Apnea", pd.Series([0]*len(labels), index=labels)).reindex(labels).fillna(0).tolist()

no_disorder = disorder_pct.get("No Disorder", pd.Series([0]*len(labels), index=labels)).reindex(labels).fillna(0).tolist()

# create the bar chart
fig, ax = plt.subplots(figsize=(10, 6))

# plot each category of sleep disorder
ax.bar(x - width, insomnia, width, label="Insomnia")
ax.bar(x, sleep_apnea, width, label="Sleep Apnea")
ax.bar(x + width, no_disorder, width, label="No Disorder")

# chart title, labels & legend
ax.set_title("Sleep Disorders by Occupation (%)")
ax.set_ylabel("Percentage")
ax.set_xticks(x)
ax.set_xticklabels(labels, rotation=45)
ax.set_ylim(0, 100)
ax.legend()

# add percentage labels above each bar
for i in range(len(labels)):
    ax.text(x[i] - width, insomnia[i] + 0.5, f"{insomnia[i]:.1f}%", ha="center", va="bottom", fontsize=8)
    ax.text(x[i], sleep_apnea[i] + 0.5, f"{sleep_apnea[i]:.1f}%", ha="center", va="bottom", fontsize=8)
    ax.text(x[i] + width, no_disorder[i] + 0.5, f"{no_disorder[i]:.1f}%", ha="center", va="bottom", fontsize=8)

# display the chart
st.pyplot(fig)

st.write("Sales workers are the most affected by sleep disorders, with 85.3% reporting insomnia, 8.8% reporting sleep apnea, and only 5.9% reporting no disorder.")
st.write("Nurses report the highest levels of sleep apnea (83.6%) which is significantly higher than in any other profession surveyed where sleep apnea rates range from 0% to just 10%.")
st.write("Teachers also show high insomnia levels (67.5%) and only 22.5% with no disorder.")
st.write("In contrast, Doctors, Engineers, Accountans, and Lawyers have the lowest disorder rates. Over 80% of individuals in each of those professions report no sleep disorder.")

st.markdown("---")
# 2. Sleep duration by stress level bar chart with stress, sleep quality, physical activity)
st.subheader("Question 2: Do occupations with higher stress levels also report lower sleep quality or fewer sleep hours?")

# calculate means by Occupation
stress_levels = filtered_df.groupby("Occupation")["Stress Level"].mean().reindex(labels)
sleep_duration = filtered_df.groupby("Occupation")["Sleep Duration"].mean().reindex(labels)
sleep_quality = filtered_df.groupby("Occupation")["Quality of Sleep"].mean().reindex(labels)
physical_activity = filtered_df.groupby("Occupation")["Physical Activity Level"].mean().reindex(labels)

# let the user filter metrics
metric_options = ["Stress Level", "Sleep Duration", "Quality of Sleep"]
selected_metrics = st.multiselect(
    "Select metrics to display:",
    metric_options,
    default=metric_options,
    help="Choose which metrics to show as bars. Line chart always shows Physical Activity."
)

# create the figure
fig, ax1 = plt.subplots(figsize=(10, 6))

# offsets for bar positioning
offsets = {
    "Stress Level": -width,
    "Sleep Duration": 0,
    "Quality of Sleep": width
}

# plot only selected bars
if "Stress Level" in selected_metrics:
    ax1.bar(x + offsets["Stress Level"], stress_levels, width, label="Stress Level")
if "Sleep Duration" in selected_metrics:
    ax1.bar(x + offsets["Sleep Duration"], sleep_duration, width, label="Sleep Duration")
if "Quality of Sleep" in selected_metrics:
    ax1.bar(x + offsets["Quality of Sleep"], sleep_quality, width, label="Quality of Sleep")

# bar axis settings
ax1.set_ylabel("Scale (0–10)")
ax1.set_ylim(0, 10)
ax1.set_xticks(x)
ax1.set_xticklabels(labels, rotation=45)
ax1.set_title("Stress, Sleep, and Physical Activity by Occupation")

# line chart on twin axis
ax2 = ax1.twinx()
ax2.plot(x, physical_activity, label="Physical Activity", color="tab:red", marker="o", linewidth=2)
ax2.set_ylim(0, 100)
ax2.set_ylabel("Physical Activity Level (0–100)")

# combine legends
lines_1, labels_1 = ax1.get_legend_handles_labels()
lines_2, labels_2 = ax2.get_legend_handles_labels()
ax1.legend(lines_1 + lines_2, labels_1 + labels_2, loc='upper left')

# display chart
st.pyplot(fig)

st.write("There’s a clear correlation between higher stress and poorer sleep health.")
st.write("Sales workers report the highest stress level (7.1), lowest sleep duration (6.4 hours), and worst sleep quality (5.9).")
st.write("Doctors also show high stress (6.7) and poor sleep quality (6.6), although their sleep duration is slightly better (7 hours).")
st.write("Engineers, on the other hand, report the lowest stress (4.0), highest sleep duration (7.9 hours), and best sleep quality (8.3).")
st.write("Interestingly, physical activity levels appear to vary independently as nurses (78.6) and lawyers (70.4) report the highest activity, while engineers (51.6) and sales workers (44.1) are less active. Despite lower activity, engineers report excellent sleep, which may mean stress has a stronger influence on sleep health than physical activity alone.")

st.markdown("---")
# 3. BMI Category distribution by occupation bar chart with secondary axis for average age
st.subheader("Question 3: Are there noticeable differences in BMI category distribution across occupations?")

st.write("This analysis shows whether specific jobs are linked with higher rates of overweight or obesity.")

# filter for BMI categories
bmi_options = ["Overweight", "Obese"]
selected_bmi = st.multiselect(
    "Select metrics to display:",
    bmi_options,
    default=bmi_options,
    help="Choose which BMI categories to combine for each occupation."
)

# Compute BMI counts and percentages
bmi_counts = filtered_df.groupby(["Occupation", "BMI Category"]).size().unstack(fill_value=0).reindex(labels).fillna(0)
bmi_pct = bmi_counts.div(bmi_counts.sum(axis=1), axis=0) * 100

# Add together selected categories (default: Overweight + Obese)
bmi_combined = pd.Series([0]*len(labels), index=labels)
for category in selected_bmi:
    if category in bmi_pct.columns:
        bmi_combined += bmi_pct[category]

# Compute average age
age_by_occupation = filtered_df.groupby("Occupation")["Age"].mean().reindex(labels)

# Create plot
fig, ax1 = plt.subplots(figsize=(10, 6))
bars = ax1.bar(x, bmi_combined, color='steelblue')
ax1.set_ylabel("% " + " + ".join(selected_bmi) if selected_bmi else "BMI %")
ax1.set_xticks(x)
ax1.set_xticklabels(labels, rotation=45)
y_max = bmi_combined.max() if selected_bmi else 1
ax1.set_ylim(0, y_max + 10)
ax1.set_title("BMI Rate vs Age by Occupation")

# Gender label annotations
gender_counts = filtered_df.groupby(["Occupation", "Gender"]).size().unstack(fill_value=0).reindex(labels).fillna(0)
gender_pct = gender_counts.div(gender_counts.sum(axis=1), axis=0) * 100

for i, occupation in enumerate(labels):
    male_pct = gender_pct.loc[occupation, "Male"] if "Male" in gender_pct.columns else 0
    female_pct = gender_pct.loc[occupation, "Female"] if "Female" in gender_pct.columns else 0
    label = f"{male_pct:.0f}% M" if male_pct > female_pct else f"{female_pct:.0f}% F"
    ax1.text(i, bmi_combined.iloc[i] + 2, label, ha='center', va='bottom', fontsize=9)

# Secondary axis: average age
ax2 = ax1.twinx()
ax2.plot(x, age_by_occupation, color="tab:red", marker='o', linewidth=2, label="Average Age")
ax2.set_ylabel("Average Age")
ax2.set_ylim(age_by_occupation.min() * 0.95, age_by_occupation.max() * 1.05)

# Combine legends
lines_1, labels_1 = ax1.get_legend_handles_labels()
lines_2, labels_2 = ax2.get_legend_handles_labels()
ax1.legend(lines_1 + lines_2, labels_1 + labels_2, loc='upper right')

# Show chart
st.pyplot(fig)

st.write("There are noticeable and significant differences in BMI category distribution across occupations, such as:")
st.write("Sales workers, nurses, and teachers are much more likely to be overweight or obese (85%–100% of participants)")
st.write("Doctors, engineers, and lawyers maintain predominantly healthy weights")
st.write("Is age or physical activity enough to explain this?")
st.write("No, because while physical activity is generally associated with better weight management, and age can influence metabolism, they don't fully explain the differences because:")
st.write("Nurses have the highest physical activity level, yet also have poor BMI results.")
st.write("Similarly, engineers are older on average and have only moderate physical activity (51.6), yet maintain healthy BMI levels.")
st.write("This suggested that other factorssuch as sleep quality & hours, stress, or working conditions might play a more important role in shaping BMI results.")
st.write("What about gender?")
st.write("Occupations with the highest overweight/obesity rates tend to be female-dominated (e.g. nurses, teachers).")
st.write("However, sales, a male-dominated field, also has extremely poor BMI results, which suggest that gender is also not enough to explain that alone the differences in BMI across occupations.")


st.markdown("---")
# 4. Correlation: BMI vs Sleep Quality and Sleep Duration
st.subheader("Extended Conclusion: Revisiting BMI with Sleep as a Key Factor")

st.markdown("**Additional question:** *What if sleep quality and sleep duration were stronger predictors of BMI than gender or age?*")

st.markdown("""
While the initial analysis of question n°3 showed clear differences in BMI across occupations,  
factors like **age**, **gender**, and **physical activity** offered only **partial explanations**.
""")




# Combine BMI categories
bmi_percent = filtered_df.groupby(["Occupation", "BMI Category"]).size().unstack(fill_value=0)
bmi_percent = bmi_percent.div(bmi_percent.sum(axis=1), axis=0) * 100

# Combine Overweight + Obese for above-normal BMI %
bmi_overweight_obese = (
    bmi_percent.get("Overweight", pd.Series(0, index=bmi_percent.index)) +
    bmi_percent.get("Obese", pd.Series(0, index=bmi_percent.index))
).reindex(labels).fillna(0)

# Get average sleep quality and duration
sleep_quality = filtered_df.groupby("Occupation")["Quality of Sleep"].mean().reindex(labels)
sleep_duration = filtered_df.groupby("Occupation")["Sleep Duration"].mean().reindex(labels)

# plot
fig, ax = plt.subplots(1, 2, figsize=(12, 5))

# BMI vs Sleep Quality
ax[0].scatter(sleep_quality, bmi_overweight_obese)
for i, occ in enumerate(labels):
    ax[0].annotate(occ, (sleep_quality[i], bmi_overweight_obese[i]), fontsize=8)
ax[0].set_xlabel("Average Sleep Quality")
ax[0].set_ylabel("% Overweight + Obese")
ax[0].set_title("BMI vs Sleep Quality")

# BMI vs Sleep Duration
ax[1].scatter(sleep_duration, bmi_overweight_obese)
for i, occ in enumerate(labels):
    ax[1].annotate(occ, (sleep_duration[i], bmi_overweight_obese[i]), fontsize=8)
ax[1].set_xlabel("Average Sleep Duration (hrs)")
ax[1].set_ylabel("% Overweight + Obese")
ax[1].set_title("BMI vs Sleep Duration")

plt.tight_layout()
st.pyplot(fig)

st.markdown("#### Conclusion")

st.markdown("""
By comparing the percentage of overweight and obese individuals in each occupation with their average sleep quality and duration, I discovered the following patterns:

#### Sales Workers:
- **Worst sleep quality**: 5.9  
- **Shortest sleep duration**: 6.4 hours  
- **Highest BMI issues**: ~100% overweight/obese

#### Teachers & Nurses:
- **Poor sleep health**: 6.3–6.4 quality, 6.6 hours  
- **Very high BMI issues**: ~85%–90%

#### Engineers & Lawyers
- **Best sleep health**: 7.8–8.3 quality, 7.6–7.9 hours  
- **Healthiest BMI profiles**

#### Doctors are the exception:
- **Poorer sleep than expected**: 6.6 quality, 7.0 hours  
- **Better BMI than engineers**, suggesting external **protective factors** like:
  - Medical knowledge  
  - Healthier habits  
  - Better dietary choices

#### What it demonstrates:          
Sleep metrics (quality and hours) appear to better align with BMI patterns than other factors. Occupations with poor sleep = poor BMI results, and those with better sleep = healthier BMI result. Additionally, the results also suggest that possible protective factors can also play a strong role in BMI results.
""")



# Insights or Analysis Section
st.markdown("---")
st.header("📊 Analysis and Key Insights")

with st.expander("Show analysis and observations"):
    st.markdown("""
    ### 1. Sleep Disorders by Occupation
    - **Sales and Healthcare** occupations show the **highest rates of insomnia**.
    - Occupations like **Doctor** and **Nurse** tend to have a higher incidence of **Sleep Apnea**, likely due to irregular work hours and stress.

    ### 2. Stress, Sleep & Physical Activity
    - **Engineers** and **Accountants** report **lower stress levels** and **higher sleep quality**.
    - A clear inverse relationship can be observed between **stress level** and **sleep duration** in several occupations.
    - **Physical Activity** is lowest among sedentary roles like **Accountants** and highest among **Doctors** and **Nurses**.

    ### 3. BMI and Age by Occupation
    - Overweight and obesity are **most common in sales-related jobs**, which also tend to have **lower physical activity**.
    - **Average age** is higher in roles like **Lawyer** and **Teacher**, and this correlates slightly with BMI increase.
    - **Gender skew** is noticeable: roles like **Nurse** skew female, while **Engineer** and **Doctor** skew male.

    ### 4. BMI vs Sleep Duration & Quality
    - **Higher BMI (Overweight + Obese)** is generally associated with **lower sleep quality**.
    - Occupations with **longer sleep durations**, such as **Teachers** and **Scientists**, tend to have **lower BMI rates**.

    ---
    _These observations can help inform workplace wellness programs or further medical studies related to occupation and lifestyle._
    """)

